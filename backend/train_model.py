# train_model.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

df = pd.read_csv("training_data.csv")
X = df[['income','attendance']]
y = df['eligible']

model = LogisticRegression(max_iter=500)
model.fit(X, y)

joblib.dump(model, "eligibility_model.pkl")
print("Saved eligibility_model.pkl")
