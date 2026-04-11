import streamlit as st
import pandas as pd
import joblib
import os

def predict():
    
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
        st.session_state["predicted_result"] = None

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

    # 🔥 RESULT OUTSIDE FORM (important)
    if st.session_state.get("predicted_result") is not None:

        if st.session_state["predicted_result"] == 0:
            st.balloons()
            st.success("✅ No Heart Disease")
            st.info("🎉 You are healthy! Keep maintaining a good lifestyle.")

        else:
            st.error("⚠️ Possibility of Heart Disease")
            st.warning("🚨 Please consult a doctor immediately.")
            st.info("💡 Maintain proper diet and regular checkups.")    