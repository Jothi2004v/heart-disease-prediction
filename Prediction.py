import streamlit as st
import pandas as pd
import joblib
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.platypus import Image
import datetime

def predict():
    def generate_pdf(data, model_name, result):

        file_path = "heart_report.pdf"
        doc = SimpleDocTemplate(file_path,pagesize=letter,topMargin=10)
        styles = getSampleStyleSheet()
        
        # 🎨 Custom Styles
        title_style = ParagraphStyle('title_style',parent=styles['Title'],textColor=colors.HexColor("#eb5b34"), alignment=TA_CENTER,spaceAfter=2)

        normal_style = ParagraphStyle('normal_style',parent=styles['Normal'],fontName='Times-Roman', fontSize=11,leading=18)

        right_style = ParagraphStyle('right_style',parent=styles['Normal'],alignment=TA_RIGHT,fontName='Times-Roman',fontSize=12,leading=18)

        center_style = ParagraphStyle('center_style',parent=styles['Normal'],alignment=TA_CENTER,fontName='Times-Roman')
        
        result_style = ParagraphStyle('result_style',parent=styles['Normal'],fontName='Times-Bold',fontSize=13)
        
        content= []

        #logo
        logo = Image("logo.png", width=60, height=60)
        #Clinic Title
        title = Paragraph("Udhayan Mathesh Lab & Research Centre", title_style)

        header_table = Table([[logo, title]],colWidths=[60, 440])
        header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'),]))
        content.append(header_table)
        

        line = Table([[""]], colWidths=[500])
        line.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 2, "#eb5b34")]))

        content.append(line)
        content.append(Spacer(1, 8))

       # 📅 Date
        content.append(Paragraph(f"Report Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}",styles['Heading3']))
        content.append(Spacer(1, 12))

        # 👤 Patient Info Table
        patient_table = [
                ["Patient Name", data.get("Name", "N/A")],
                ["Age", data.get("Age")],
                ["Sex", data.get("Sex")],
                ["Model Used", model_name]
            ]

        table = Table(patient_table, colWidths=[150, 200])
        table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1),"#ff9a7d"),
                ('TEXTCOLOR',(0,0),(-1,-1),colors.white),
                ('FONTNAME',(0,0),(-1,-1),'Times-Bold'),    
                ('FONTSIZE', (0,0), (-1,-1), 12), 
                # ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('GRID',(0,0),(-1,-1),1,colors.white)
            ]))
        
        content.append(table)
        content.append(Spacer(1, 15))

        # 🧾 Patient Details Section
        content.append(Paragraph("Patient Details:", styles['Heading2']))
        
        # Convert dictionary to list
        items = list(data.items())

        # Create rows with 2 columns
        rows = []
        for i in range(0, len(items), 2):
            row = []
            # First column
            key1, val1 = items[i]
            row.append(Paragraph(f"<b>{key1}:</b> {val1}", normal_style))
            # Second column (if exists)
            if i + 1 < len(items):
                key2, val2 = items[i + 1]
                row.append(Paragraph(f"<b>{key2}:</b> {val2}", normal_style))
            else:
                row.append("")  # empty if odd number
            rows.append(row)

        # Create table
        details_table = Table(rows, colWidths=[250, 250])
        # Style
        details_table.setStyle(TableStyle([
                ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
                ('FONTSIZE', (0,0), (-1,-1), 11),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LEFTPADDING', (0,0), (-1,-1), 50),
                ('TOPPADDING', (0,0), (-1,-1), 6),
            ]))
        content.append(details_table)
    
        content.append(Spacer(1,10))

        # 🧠 Prediction Result
        result_text = "No Heart Disease" if result == 0 else "Possibility of Heart Disease"  
        if result == 0:
            color = "#00A86B"
        else:
            color = "#FF2800"      

        final_result_para = f"""<b>Final Result: </b><font color="{color}">{result_text}</font>"""
        content.append(Paragraph(final_result_para, result_style))
        content.append(Spacer(1,30))

        content.append(Paragraph("----- End of Report -----", center_style))
        content.append(Spacer(1,40))

        tech_sign = Image("hari.png", width=120, height=40)
        doc_sign = Image("jp.png", width=120, height=40)
        # Table layout (left + right)
        sign_table = Table([[tech_sign,doc_sign],["Signature of Chief Technician", "Dr. V.  Jothi Prakash M.D."],["", "Consultant - Microbiologist"]], colWidths=[250, 250])
        sign_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (0,0), 'LEFT'),
                ('ALIGN', (1,0), (1,0), 'RIGHT'),
                ('ALIGN', (0,1), (0,1), 'LEFT'),
                ('ALIGN', (1,1), (1,1), 'RIGHT'),
                ('ALIGN', (1,2), (1,2), 'RIGHT'),
                ('FONTNAME', (0,1), (-1,1), 'Times-Roman'),
                ('FONTSIZE', (0,1), (-1,1), 11), 
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5)
            ]))
        content.append(sign_table)


        def draw_footer(canvas, doc):
            foot_color = "#eb5b34"
            canvas.saveState()

            # Set font
            canvas.setFont("Times-Roman",10)

            # Page width
            width, height = letter

            # Footer text (centered)
            footer1 = "Katpadi, Vellore - 632 007, Tamil Nadu, INDIA. | Ph: +91 79045 25565, +91 89460 54872"
            footer2 = "Email: udhayan_mathesh_labs@gmail.com | www.udhayan_mathen_lab.com"
            footer3 = "Connect with us: Udhayan Mathesh Lab (Facebook)"

            canvas.setFillColor(colors.HexColor(foot_color))
            # Draw lines (Y position controls bottom spacing)
            canvas.drawCentredString(width/2, 40, footer1)
            canvas.drawCentredString(width/2, 28, footer2)
            canvas.drawCentredString(width/2, 16, footer3)

            canvas.restoreState()

        doc.build(content, onFirstPage=draw_footer, onLaterPages=draw_footer)
        return file_path
    
    st.header("🎯 Heart Disease Prediction")

    if not os.path.exists("models.pkl"):
        st.warning("⚠️ Please train models first from About page")
        return
      # Load everything
    models = joblib.load("models.pkl")   # 🔥 all models
    scaler = joblib.load("scaler.pkl")
    columns = joblib.load("columns.pkl")

    cont_val = ['age','trestbps','chol','thalach','oldpeak']

    # Select model
    model_choice = st.selectbox("Select Model", list(models.keys()))
    st.info(f"Using Model: {model_choice}")

    # Session state for result
    if "predicted_result" not in st.session_state:
        st.session_state["predicted_result"] = None

# ✅ Reset button (separate clean block)
    if st.button("🔄 Reset Prediction"):
        st.session_state.clear()
        st.rerun()

    st.markdown("""<style>div[data-testid="stForm"] {
                        background: linear-gradient(135deg, #667eea, #764ba2);
                        padding: 20px;
                        border-radius: 15px;
                        color: white    ;
                    }
                label {color: white !important;
                font-weight: bold   ;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>
                div[data-testid="stForm"] button {
                    color: black;
                }</style>""", unsafe_allow_html=True)
    
    #form
    with st.form(key="prediction_form"):

        st.subheader("Enter Patient Details ✍")   
        name = st.text_input("Patient Name")
        age = st.number_input("Age", 1, 120, 50)
        sex = st.selectbox("Sex (1=Male, 0=Female)", [1,0])
        cp = st.selectbox("Chest Pain Type", [0,1,2,3])
        trestbps = st.number_input("Resting BP", value=120)
        chol = st.number_input("Cholesterol", value=200)
        fbs = st.selectbox("Fasting Blood Sugar >120", [1,0])
        restecg = st.selectbox("Rest ECG", [0,1,2])
        thalach = st.number_input("Max Heart Rate", value=150)
        exang = st.selectbox("Exercise Angina", [1,0])
        oldpeak = st.number_input("Oldpeak", value=1.0)
        slope = st.selectbox("Slope", [0,1,2])
        ca = st.selectbox("Major Vessels", [0,1,2,3])
        thal = st.selectbox("Thal", [1,2,3])

        # Submit button inside form
        submit_button = st.form_submit_button("🪄 Predict")

        if submit_button:

            # Create DataFrame
            input_data = pd.DataFrame({
                'age': [age],
                'sex': [sex],
                'cp': [cp],
                'trestbps': [trestbps],
                'chol': [chol],
                'fbs': [fbs],
                'restecg': [restecg],
                'thalach': [thalach],
                'exang': [exang],
                'oldpeak': [oldpeak],   
                'slope': [slope],
                'ca': [ca],
                'thal': [thal]
            })

            # Preprocessing
            input_data = pd.get_dummies(input_data)
            input_data = input_data.reindex(columns=columns, fill_value=0)
            input_data[cont_val] = scaler.transform(input_data[cont_val])

            # Model prediction
            model = models[model_choice]
            prediction = model.predict(input_data)

            st.session_state["predicted_result"] = prediction[0]

            st.session_state["input_data"] = {
               "Name": name if name else "N/A",
                "Age" : age,
                "Sex": "Male" if sex == 1 else "Female",
                "Chest Pain" : cp,
                "Rest BP" : trestbps,
                "Cholesterol": chol,
                "FBS": "High" if fbs == 1 else "Normal",
                "Rest ECG" : restecg,
                "Max HR" : thalach,
             "Exercise Angina": "Yes" if exang == 1 else "No",
                "Oldpeak" : oldpeak,
                "Slope" : slope,
                "CA" : ca,
                "Thal" : thal
            }
            st.session_state["model_used"] = model_choice

    # 🔥 RESULT OUTSIDE FORM (important)
    if st.session_state.get("predicted_result") is not None:
        result = st.session_state["predicted_result"]

        if st.session_state["predicted_result"] == 0:
            st.balloons()
            st.success("✅ No Heart Disease")
            st.info("🎉 You are healthy! Keep maintaining a good lifestyle.")

        else:
            st.error("⚠️ Possibility of Heart Disease")
            st.warning("🚨 Please consult a doctor immediately.")
            st.info("💡 Maintain proper diet and regular checkups.")    

        #generate pdf
        pdf_file = generate_pdf(st.session_state["input_data"],st.session_state["model_used"],result)
        with open(pdf_file, "rb") as f:
             pdf_bytes = f.read()
        st.download_button(label="⬇️ Download Report", data=pdf_bytes,file_name="Heart_Report.pdf",mime="application/pdf")
