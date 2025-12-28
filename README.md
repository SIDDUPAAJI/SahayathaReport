# Sahayata Report: AI-Powered Welfare Transparency System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange)](https://scikit-learn.org/)
[![XAI](https://img.shields.io/badge/Explainable%20AI-SHAP-green)](https://shap.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

Sahayata Report is an AI-assisted middleware system designed to bridge the trust deficit in government welfare distribution. By leveraging Explainable AI (XAI), specifically SHAP (SHapley Additive exPlanations), the system transforms opaque "black-box" eligibility predictions into transparent, human-readable Decision Receipts.The primary objective of this project is to empower citizens with actionable feedback, reduce administrative overhead for government officers, and eliminate systemic dependency on intermediaries through algorithmic accountability.The ProblemTraditional welfare processing systems suffer from a significant transparency gap:Opaque Logic: Applicants are frequently issued binary outcomes (Approved/Rejected) without a formal Statement of Reasons.The Re-submission Loop: Without an understanding of specific rejection criteria, citizens often submit identical, invalid applications, resulting in redundant processing loads for administrative servers.Public Trust Deficit: A lack of transparency fosters suspicion and creates opportunities for fraudulent intermediaries to exploit vulnerable populations.The SolutionSahayata Report serves as an interpretability layer between the welfare database and the end-user:High-Throughput Ingestion: The system processes bulk applicant data via standardized CSV interfaces.Predictive Analytics: It employs a pretrained gradient-boosted ensemble (such as XGBoost or Random Forest) to determine eligibility based on historical parameters.Algorithmic Transparency: The system utilizes the SHAP engine to calculate exact feature contributions for every individual decision.Actionable Synthesis: It generates a "Decision Receipt" PDF that translates mathematical feature weights into plain-language guidance and requisite next steps.System ArchitectureThe platform is developed on a decoupled, modular architecture to ensure scalability and seamless integration with existing government digital infrastructure.Core ComponentsInference Engine: Facilitates data normalization and executes high-speed eligibility classification.Explanation Engine (SHAP): Decomposes the model's output into specific contribution scores (Shapley Values) for each input feature.Natural Language Generation (NLG) Layer: Maps feature importance to predefined linguistic templates—for example, mapping a negative SHAP value for income to the phrase: "Annual income exceeds the established eligibility threshold."Receipt Generator: A high-performance PDF engine that compiles outcomes into a secure, standardized document suitable for distribution.

#Technology Stack
Layer                    Technology
Language                 Python 3.8+
Predictive Modeling      Scikit-learn 
XGBoostExplainability    (XAI)SHAP (SHapley Additive exPlanations)
Backend API              FastAPI
User Interface           Streamlit
Document                 EngineReportLab / FPDFProject 

StructurePlaintextsahayata-report/
│
├── models/             # Pretrained .pkl models and weights
├── src/
│   ├── app.py          # Main application / Administrative Dashboard
│   ├── explainability.py # SHAP logic and weight calculation
│   ├── generator.py    # PDF rendering and Receipt formatting
│   └── processing.py   # Data sanitization and ML inference
├── templates/          # PDF layout and linguistic mapping templates
└── requirements.txt    # Library dependencies

#Installation and Setup

Clone the Repository
Bashgit clone https://github.com/yourusername/sahayata-report.git
cd sahayata-report

Initialize Virtual Environment
Bashpython -m venv venv
source venv/bin/activate  # MacOS/Linux
OR
venv\Scripts\activate     # Windows

Install Dependencies
Bashpip install -r requirements.txt

Launch the ApplicationBash
streamlit run src/app.py


#Usage Workflow
Data Upload: Administrative officers upload bulk application CSV files to the secure dashboard.
Model Inference: The system executes eligibility checks across the dataset in parallel.
Interpretability Pass: SHAP values are computed to identify the primary drivers behind each individual outcome.
Receipt Distribution: The system generates a comprehensive ZIP archive containing individual PDF "Decision Receipts" for digital or physical distribution.

Academic and Regulatory SignificanceThis project implements the principle of the "Right to Explanation" as advocated in contemporary data protection frameworks. By applying Shapley Value concepts from cooperative game theory to public welfare, Sahayata Report demonstrates that computational efficiency in governance can be achieved without compromising institutional accountability or citizen rights.
