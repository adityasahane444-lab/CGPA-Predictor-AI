import streamlit as st
import pandas as pd
import joblib
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import plotly.express as px

# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="CGPA Predictor AI",
    page_icon="🎓",
    layout="wide"
)

# ---------------- STYLE ----------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#312e81,#2563eb);
}

.card{
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    border-radius:25px;
    padding:25px;
    height:180px;
    text-align:center;
    transition:0.3s;
    border:1px solid rgba(255,255,255,0.2);
}

.card:hover{
    transform: translateY(-8px);
    box-shadow:0 15px 35px rgba(0,0,0,0.4);
}

.title{
    color:white;
    font-size:24px;
    font-weight:700;
}

.text{
    color:#dbeafe;
}

.big{
    color:white;
    font-size:45px;
    font-weight:bold;
}

button{
    border-radius:15px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(
    os.path.join(BASE_DIR, "cgpa_model.pkl")
)

def predict_gp(cie, see):
    df = pd.DataFrame(
        [[cie, see]],
        columns=["cie_total", "see"]
    )
    return float(model.predict(df)[0])

def grade(x):
    if x >= 9:
        return "O Outstanding"
    if x >= 8:
        return "A+ Excellent"
    if x >= 7:
        return "A Very Good"
    if x >= 6:
        return "B Good"
    if x >= 5:
        return "C Average"
    return "F"

def home():
    st.session_state.page = "home"

# ---------------- SESSION ----------------

if "page" not in st.session_state:
    st.session_state.page = "home"

# ✅ REPORT SESSION (ADDED)
if "report" not in st.session_state:
    st.session_state.report = None

# ---------------- SIDEBAR ----------------

st.sidebar.title("👤 Student Profile")

name = st.sidebar.text_input("Name", "Aditya Sahane")

branch = st.sidebar.text_input("Branch", "AI & DS")

sem = st.sidebar.number_input("Semester", 1, 8, 3)

def generate_pdf(report):
    file_name = f"{report['name'].replace(' ', '_')}_marksheet.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=A4)

    styles = getSampleStyleSheet()
    content = []

    # ================= HEADER =================
    content.append(Paragraph(
        "<b>UNIVERSITY OF ACADEMIC EXCELLENCE</b>",
        styles["Title"]
    ))

    content.append(Paragraph(
        "Official Grade Sheet / Provisional Marksheet",
        styles["Heading2"]
    ))

    content.append(Spacer(1, 12))

    # ================= STUDENT INFO BOX =================
    student_info = [
        ["Name", report["name"]],
        ["Branch", report["branch"]],
        ["Semester", report["semester"]],
        ["Date", str(datetime.today().date())]
    ]

    info_table = Table(student_info)

    info_table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 2, colors.black),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),
        ("PADDING", (0,0), (-1,-1), 6),
    ]))

    content.append(info_table)
    content.append(Spacer(1, 15))

    # ================= CGPA HIGHLIGHT BOX =================
    cgpa = float(report["cgpa"])

    if cgpa >= 8:
        grade = "A (Excellent)"
    elif cgpa >= 6:
        grade = "B (Good)"
    else:
        grade = "C (Needs Improvement)"

    content.append(Paragraph(
        f"<b>FINAL CGPA:</b> {cgpa} &nbsp;&nbsp;&nbsp; <b>GRADE:</b> {grade}",
        styles["Heading2"]
    ))

    content.append(Spacer(1, 15))

    # ================= SUBJECT TABLE =================
    table_data = [["Subject", "CIE", "SEE", "Grade Point"]]

    for row in report["data"]:
        table_data.append([
            row["Subject"],
            row["CIE"],
            row["SEE"],
            round(row["GP"], 2)
        ])

    table = Table(table_data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 11),
        ("GRID", (0,0), (-1,-1), 1.2, colors.black),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.lightgrey]),
    ]))

    content.append(table)
    content.append(Spacer(1, 20))

    # ================= PERFORMANCE ANALYSIS =================
    best = max(report["data"], key=lambda x: x["GP"])
    weak = min(report["data"], key=lambda x: x["GP"])

    content.append(Paragraph(
        f"<b>Strong Subject:</b> {best['Subject']} (GP {best['GP']})",
        styles["Normal"]
    ))

    content.append(Paragraph(
        f"<b>Improvement Needed:</b> {weak['Subject']} (GP {weak['GP']})",
        styles["Normal"]
    ))

    content.append(Spacer(1, 30))

    # ================= SIGNATURE SECTION =================
    sign_data = [
        ["__________________", "__________________"],
        ["Class Advisor", "Head of Department"]
    ]

    sign_table = Table(sign_data)

    sign_table.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 20),
    ]))

    content.append(sign_table)

    content.append(Spacer(1, 20))

    # ================= FOOTER =================
    content.append(Paragraph(
        "This is a system generated marksheet and does not require physical signature verification.",
        styles["Normal"]
    ))

    doc.build(content)

    return file_name
st.subheader("📄 Report Section")

# Make sure report exists
if report:

    st.write("### Student Report Preview")
    st.json(report)  # optional preview (you can remove later)

    if st.button("🎓 Generate Report Card PDF"):
        file_name = generate_pdf(report)

        with open(file_name, "rb") as f:
            st.download_button(
                label="⬇️ Download Report Card",
                data=f,
                file_name=file_name,
                mime="application/pdf"
            )

# =================================================
# HOME
# =================================================

if st.session_state.page == "home":

    st.markdown(f"""
    <div class="card">

    <div class="big">🎓</div>

    <div class="title">
    CGPA Predictor AI
    </div>

    <div class="text">
    Welcome {name} 👋
    <br>
    {branch} • Semester {sem}
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("✨ Features")

    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    cards = [
        ("📊", "Predict CGPA", "predict"),
        ("🎯", "Target Planner", "planner"),
        ("🎮", "Simulator", "simulator"),
        ("📈", "Report", "report")
    ]

    cols = [c1, c2, c3, c4]

    for col, item in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div class="card">

            <div class="big">
            {item[0]}
            </div>

            <div class="title">
            {item[1]}
            </div>

            <div class="text">
            Explore feature
            </div>

            </div>
            """, unsafe_allow_html=True)

            if st.button(item[1], key=item[1]):
                st.session_state.page = item[2]
                st.rerun()

# =================================================
# PREDICT
# =================================================

elif st.session_state.page == "predict":

    st.button("🏠 Home", on_click=home)

    st.title("📊 CGPA Prediction")

    subjects = st.number_input("Number of subjects", 1, 12, 4)

    total = 0
    chart = []

    for i in range(subjects):

        st.markdown(f"### Subject {i+1}")

        cie = st.slider("CIE", 0, 60, 30, key=f"c{i}")
        see = st.slider("SEE", 0, 60, 30, key=f"s{i}")

        gp = predict_gp(cie, see)

        total += gp

        chart.append({
            "Subject": f"S{i+1}",
            "CIE": cie,
            "SEE": see,
            "GP": gp
        })

    if st.button("Predict"):

        cgpa = total / subjects

        st.metric("Predicted CGPA", round(cgpa, 2))
        st.success(grade(cgpa))

        fig = px.bar(chart, x="Subject", y="GP")
        st.plotly_chart(fig, use_container_width=True)

        # ---------------- SAVE REPORT ----------------
        st.session_state.report = {
            "name": name,
            "branch": branch,
            "semester": sem,
            "cgpa": round(cgpa, 2),
            "data": chart
        }

# =================================================
# PLANNER
# =================================================

elif st.session_state.page == "planner":

    st.button("🏠 Home", on_click=home)

    st.title("🎯 Target CGPA Planner")

    cie = st.slider("Current CIE", 0, 60, 30)
    target = st.slider("Target CGPA", 5.0, 10.0, 8.5)

    if st.button("Find Required SEE"):

        ans = "Not possible"

        for see in range(61):
            if predict_gp(cie, see) >= target:
                ans = see
                break

        st.metric("Required SEE", ans)

# =================================================
# SIMULATOR
# =================================================

elif st.session_state.page == "simulator":

    st.button("🏠 Home", on_click=home)

    st.title("🎮 CGPA Simulator")

    cie = st.slider("CIE Marks", 0, 60, 30)
    see = st.slider("SEE Marks", 0, 60, 30)

    gp = predict_gp(cie, see)

    st.markdown(f"""
    <div class="card">

    <div class="title">
    Predicted GP
    </div>

    <div class="big">
    {round(gp, 2)}
    </div>

    </div>
    """, unsafe_allow_html=True)

# =================================================
# REPORT
# =================================================

else:

    st.button("🏠 Home", on_click=home)

    st.title("📈 Student Report")

    if st.session_state.report is None:
        st.warning("⚠ First predict CGPA to generate report")

    else:

        r = st.session_state.report

        st.markdown(f"""
        <div class="card">

        <div class="title">
        🎓 {r['name']}
        </div>

        <div class="text">
        {r['branch']}<br>
        Semester {r['semester']}
        </div>

        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Final CGPA", r["cgpa"])

        with col2:
            if r["cgpa"] >= 8:
                st.success("Excellent Performance 🚀")
            elif r["cgpa"] >= 7:
                st.info("Good Performance 👍")
            else:
                st.warning("Needs Improvement")

        df = pd.DataFrame(r["data"])

        st.subheader("📋 Performance Table")
        st.dataframe(df, use_container_width=True)

        # ---------------- ANALYSIS ----------------

        st.subheader("🧠 AI Analysis")

        best = df.loc[df["GP"].idxmax()]
        weak = df.loc[df["GP"].idxmin()]

        st.success(f"""
💪 Strength:
{best['Subject']} is your strongest subject
""")

        st.warning(f"""
⚠ Weak Area:
{weak['Subject']} needs improvement
""")

        # ---------------- CHARTS ----------------

        st.subheader("📊 Performance Charts")

        fig1 = px.bar(
            df,
            x="Subject",
            y="GP",
            title="Subject Grade Points"
        )
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.line(
            df,
            x="Subject",
            y=["CIE", "SEE"],
            markers=True,
            title="CIE vs SEE Comparison"
        )
        st.plotly_chart(fig2, use_container_width=True)

