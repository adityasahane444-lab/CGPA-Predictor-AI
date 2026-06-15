import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "cgpa_model.pkl")

model = joblib.load(model_path)
model = joblib.load("cgpa_model.pkl")


def predict_gp(cie, see):
    data = pd.DataFrame([[cie, see]], columns=["cie_total", "see"])
    return model.predict(data)[0]


def calculate_cgpa(cie_list, see):

    total = 0

    for cie in cie_list:
        total += predict_gp(cie, see)

    return total / 4


def find_required_see(cie_list, target_cgpa):

    for see in range(0, 61):

        cgpa = calculate_cgpa(cie_list, see)

        if cgpa >= target_cgpa:
            return see

    return "Not possible"


print("\n================ SEE PREDICTOR ================\n")

print("INSTRUCTIONS:")
print(" Enter CIE marks for 4 subjects (0–60)")
print("Enter target CGPA (example: 8, 9, etc.)\n")

cie_list = []

for i in range(4):
    cie = float(input(f"Enter CIE marks for Subject {i+1}: "))
    cie_list.append(cie)

target_cgpa = float(input("\nEnter target CGPA: "))

result = find_required_see(cie_list, target_cgpa)

print("\n================ RESULT ================")
print("Required SEE Marks (approx):", result)