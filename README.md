# Sahayata Report: AI-Powered Welfare Transparency System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange)](https://scikit-learn.org/)
[![XAI](https://img.shields.io/badge/Explainable%20AI-SHAP-green)](https://shap.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

**Sahayata Report** is an AI-assisted middleware system designed to bring transparency to government welfare schemes. It processes applicant data, predicts eligibility using a pretrained model, and uses **SHAP (SHapley Additive exPlanations)** to generate a transparent "Decision Receipt" for every applicant. This receipt explains exactly *why* an application was approved or rejected in simple, readable language.

---

## 📖 Table of Contents
- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Installation & Setup](#-installation--setup)
- [Usage Workflow](#-usage-workflow)
- [Project Structure](#-project-structure)
- [Future Roadmap](#-future-roadmap)

---

## 🚩 The Problem
Government welfare schemes receive thousands of applications, but the decision process is often opaque.
* **Lack of Feedback:** Applicants receive binary "Approved/Rejected" outcomes without explanation.
* **Administrative Burden:** Officers waste time answering repetitive inquiries ("Why was I rejected?").
* **Cycle of Failure:** Without knowing the specific error, citizens "blindly resubmit" invalid applications, clogging the system.
* **Trust Deficit:** Lack of transparency breeds suspicion and reliance on exploitative middlemen.

## 💡 The Solution
**Sahayata Report** acts as an interpretability layer between the welfare database and the citizen.
1.  **Ingests Data:** Officers upload bulk application data (CSV).
2.  **Predicts:** A machine learning model determines eligibility.
3.  **Explains:** The system uses SHAP to calculate the specific factors (e.g., *Income > Threshold*) driving the decision.
4.  **Generates Receipt:** A PDF is created containing the status, top 3 reasons, and actionable next steps.

---

## ✨ Key Features
* **Glass-Box Decision Making:** Converts complex "Black Box" AI predictions into human-readable reasons.
* **Automated Decision Receipts:** Generates a downloadable PDF for every applicant automatically.
* **Actionable Feedback:** Tells rejected applicants exactly what document or criteria needs correction.
* **Bulk Processing:** Handles thousands of rows via CSV upload in minutes.
* **Lightweight & Secure:** Runs on standard hardware; processes data in-memory without permanent storage.

---

## 🏗 System Architecture
The system is modularized into 7 core components:

1.  **Data Input Module:** Validates CSV structure and sanitizes applicant data.
2.  **Eligibility Prediction Module:** Runs data through a pretrained ML classifier (XGBoost/Random Forest).
3.  **Explanation Engine:** Uses SHAP to identify top influencing factors for each specific row.
4.  **NLG Layer:** Translates mathematical weights into vernacular text (e.g., `income_val < 0` -> *"Income below poverty line"*).
5.  **Receipt Generator:** Compiles status and reasons into a standardized PDF using `ReportLab`/`FPDF`.
6.  **API Backend:** FastAPI/Flask routes to handle inference and file generation requests.
7.  **Frontend UI:** A Streamlit or HTML dashboard for officers to interact with the system.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.8+ |
| **Machine Learning** | Scikit-learn, XGBoost, Pandas, NumPy |
| **Explainability (XAI)** | SHAP (SHapley Additive exPlanations) |
| **Web Framework** | FastAPI (Backend), Streamlit (Frontend) |
| **PDF Generation** | ReportLab / FPDF |
| **Deployment** | Docker, Render/Heroku |

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.8 or higher installed.
* git installed.

### Steps
1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/sahayata-report.git](https://github.com/yourusername/sahayata-report.git)
    cd sahayata-report
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    ```bash
    # If using Streamlit
    streamlit run app.py
    
    # If using FastAPI
    uvicorn main:app --reload
    ```

---

## 📝 Usage Workflow

1.  **Login:** Officer accesses the web dashboard.
2.  **Upload:** Drag and drop the `applications.csv` file.
3.  **Process:** Click "Generate Reports." The system runs the ML model and SHAP analysis in the background.
4.  **Review:** View the summary dashboard showing Approval Rates and Common Rejection Reasons.
5.  **Export:** Download the "Decision Receipts" (Individual PDFs or Bulk ZIP).

---

## 📂 Project Structure

```text
sahayata-report/
│
├── data/                   # Sample datasets for testing
├── models/                 # Pretrained ML models (.pkl)
├── src/
│   ├── app.py              # Main application entry point
│   ├── explainability.py   # SHAP logic implementation
│   ├── generator.py        # PDF generation logic
│   └── processing.py       # Data cleaning and inference
│
├── templates/              # PDF layout templates
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── LICENSE                 # License file
