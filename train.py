import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib



df = pd.read_csv("cgpa_data.csv")

X = df[["cie_total", "see"]]
y = df["grade_point"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

print("Model Accuracy:", model.score(X_test, y_test))

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "cgpa_model.pkl")

joblib.dump(model, model_path)

print("Model saved in:", model_path)
print("Model saved successfully!")
