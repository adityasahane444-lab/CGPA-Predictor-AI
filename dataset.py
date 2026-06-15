import pandas as pd
import random
import os

def get_gp(marks):
    if marks >= 90: return 10
    elif marks >= 80: return 9
    elif marks >= 70: return 8
    elif marks >= 60: return 7
    elif marks >= 55: return 6
    elif marks >= 50: return 5
    elif marks >= 40: return 4
    else: return 0


data = []

for i in range(200):

    cie = random.randint(20, 60)
    see = random.randint(15, 60)

    cie_scaled = (cie / 60) * 40

    noise = random.uniform(-3, 3)

    final_score = cie_scaled + see + noise
    final_score = max(0, min(100, final_score))

    gp = get_gp(final_score)

    data.append([cie, see, gp])


df = pd.DataFrame(data, columns=[
    "cie_total", "see", "grade_point"
])



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(BASE_DIR, "cgpa_data.csv")

df.to_csv(csv_path, index=False)

print("CSV saved in:", csv_path)

print("Dataset created successfully!")