# main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import pandas as pd
import io, joblib, datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = FastAPI(title="Sahayata Report Backend")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Load model if available
try:
    model = joblib.load("eligibility_model.pkl")
except Exception as e:
    model = None
    print("Model not loaded:", e)

LAST_RESULTS = []

# Scheme-specific rule helpers (Telugu with English in parentheses)
def reasons_for_Raithu_Bandhu(row):
    reasons = []
    if int(row.get("land_document_present", 0)) != 1:
        reasons.append("భూమి పత్రాలు అందుబాటులో లేవు (Land documents not provided)")
    if float(row.get("income", 0)) >= 150000:
        reasons.append("ఆదాయం పథకం పరిమితిని మించి ఉంది (Income exceeds scheme threshold)")
    if float(row.get("marks", 0)) < 40:
        reasons.append("అర్హత మార్కులు తక్కువగా ఉన్నాయి (Marks below eligibility requirement)")
    return reasons

def reasons_for_Aasara_Pension(row):
    reasons = []
    if float(row.get("age", 0)) < 60:
        reasons.append("వయోజన పరిమితికి చేరలేదు (Applicant not reached minimum age requirement)")
    if float(row.get("income", 0)) >= 100000:
        reasons.append("పెన్షన్ అర్హత ఆదాయ పరిమితిని మించుతుంది (Income exceeds pension eligibility limit)")
    return reasons

def reasons_for_Arogya_Sri(row):
    reasons = []
    if int(row.get("medical_certificate_present", 0)) != 1:
        reasons.append("వైద్య ధృవపత్రం సమర్పించబడలేదు (Medical certificate not submitted)")
    return reasons

def default_reasons(row):
    reasons = []
    if float(row.get("income", 0)) >= 150000:
        reasons.append("ఆదాయం పరిమితిని మించినది (Income exceeds threshold)")
    if float(row.get("attendance", 0)) < 75:
        reasons.append("హాజరు శాతం తక్కువగా ఉంది (Attendance percentage is low)")
    return reasons

SCHEME_REASON_FN = {
    "Raithu_Bandhu": reasons_for_Raithu_Bandhu,
    "Aasara_Pension": reasons_for_Aasara_Pension,
    "Arogya_Sri": reasons_for_Arogya_Sri,
    # for other schemes use default_reasons
}

def format_reasons_tel_en(reasons_list):
    if not reasons_list:
        return "స్పష్టమైన కారణం లేదు (No clear reason given)"
    return "; ".join(reasons_list)

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...), scheme: str = Form(...)):
    global LAST_RESULTS, model
    if not file:
        raise HTTPException(status_code=400, detail="File required.")

    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {e}")

    reason_fn = SCHEME_REASON_FN.get(scheme, default_reasons)

    results = []
    for i, row in df.iterrows():
        # normalize row to dict
        row_dict = {}
        for col in df.columns:
            val = row[col]
            if pd.isna(val):
                row_dict[col] = 0
                continue
            # try parse numeric, else keep string
            try:
                if isinstance(val, str):
                    s = val.strip()
                    if s.lower() in ("1","yes","true","y"):
                        row_dict[col] = 1
                    else:
                        row_dict[col] = float(s.replace(",",""))
                else:
                    row_dict[col] = val
            except:
                row_dict[col] = val

        # rule-based reasons
        reasons = reason_fn(row_dict)

        # ML-based probability (optional, when model present)
        proba = None
        if model is not None:
            try:
                feature_vec = [[float(row_dict.get("income", 0)), float(row_dict.get("attendance", 0))]]
                proba = float(model.predict_proba(feature_vec)[0][1])
            except Exception:
                proba = None

        qualified = True if (len(reasons) == 0) else False

        if not qualified and not reasons:
            reasons = default_reasons(row_dict)

        result = {
            "applicant_name": row_dict.get("name", f"Applicant_{i+1}"),
            "qualified": bool(qualified),
            "probability": round(proba, 3) if proba is not None else None,
            "reason_tel_en": format_reasons_tel_en(reasons)
        }
        results.append(result)

    LAST_RESULTS = results
    return {"scheme": scheme, "results": results}

def create_pdf_bytes(record: dict) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 60, "Decision Receipt / నిర్ణయ రసీదు")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 78, f"Generated: {datetime.datetime.utcnow().isoformat()} UTC")

    y = height - 120
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, f"Applicant: {record.get('applicant_name','-')}")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(40, y, f"Qualified: {'Yes' if record.get('qualified') else 'No'}")
    y -= 18
    c.drawString(40, y, f"Probability: {record.get('probability', '-')}")
    y -= 22

    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Reasons:")
    y -= 16
    c.setFont("Helvetica", 11)
    for r in record.get("reason_tel_en", "").split(";"):
        c.drawString(60, y, f"• {r.strip()}")
        y -= 14
        if y < 60:
            c.showPage()
            y = height - 60

    c.showPage()
    c.save()
    buf.seek(0)
    return buf.read()

@app.get("/receipt/{idx}")
def receipt(idx: int):
    if not LAST_RESULTS:
        raise HTTPException(status_code=404, detail="No previous results available. Call /predict first.")
    if idx < 0 or idx >= len(LAST_RESULTS):
        raise HTTPException(status_code=400, detail="Index out of range.")
    record = LAST_RESULTS[idx]
    pdf_bytes = create_pdf_bytes(record)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf",
                             headers={"Content-Disposition": f"attachment; filename=receipt_{idx}.pdf"})
