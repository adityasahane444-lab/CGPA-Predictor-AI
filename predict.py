import joblib
import pandas as pd

model = joblib.load("cgpa_model.pkl")


def predict_gp(cie, see):
    data = pd.DataFrame([[cie, see]], columns=["cie_total", "see"])
    return model.predict(data)[0]


print("\n================ CGPA PREDICTOR ================\n")

print("INSTRUCTIONS:")
print(" Enter CIE and SEE marks ex.{CIE,SEE} for 4 subjects")
print(" CIE range: 0 to 60")
print(" SEE range: 0 to 60\n")

cie_list = []
see_list = []

for i in range(4):
    print(f"\nSubject {i+1}")

    cie = float(input("Enter CIE marks: "))
    see = float(input("Enter SEE marks: "))

    cie_list.append(cie)
    see_list.append(see)

total_gp = 0

for cie, see in zip(cie_list, see_list):
    total_gp += predict_gp(cie, see)

cgpa = total_gp / 4

print("\n================ RESULT ================")
print("CGPA:", round(cgpa, 2))