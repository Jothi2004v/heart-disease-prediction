import streamlit as st
import pandas as pd
import plotly.express as px
import os

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from train_model import train_models

def show_about():

    # Title
    st.header(" Heart Disease Prediction Model Comparison ↔️")

    # Load dataset
    data = pd.read_csv('heart.csv')
    st.subheader("***Data set***📄")
    st.write(data.head(8))
    st.markdown("---")

    st.subheader("***Missing Values***❓")
    st.dataframe(data.isnull().sum(),use_container_width=False)
    st.markdown("---")

    # Remove duplicates
    data_dup = data.duplicated().any()
    st.subheader("Duplicate Rows searching...🔍 ")
    st.error(f"***Duplicates: {data_dup}❌***")
    data = data.drop_duplicates()
    st.subheader("***Removing the Duplicates***🧹")
    st.write(data.head(8))
    data_dup = data.duplicated().any()
    st.success(f"***Duplicates: {data_dup}✅***")
    st.markdown("---")

    # Data processing
    st.subheader("⚙️***Data Processing***")
    cate_val = []
    cont_val = []

    for column in data.columns:
        if data[column].nunique() <= 10:
            cate_val.append(column)
        else:
            cont_val.append(column)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown("<h4>Categorical Values</h4>",unsafe_allow_html=True)
        st.dataframe(cate_val,use_container_width=False)
    with col2:
        st.markdown("<h4>Continuous Values</h4>",unsafe_allow_html=True)
        st.dataframe(cont_val,use_container_width=False)
    with col3:
        # Encoding
        st.markdown("<h4>Encoding Categorical Data</h4>",unsafe_allow_html=True)
        st.write("**Removing the sex and target column**")
        cate_val.remove('sex')
        cate_val.remove('target')
        st.dataframe(cate_val,use_container_width=False)
        data = pd.get_dummies(data, columns=cate_val, drop_first=True)
    st.markdown("---")

    # Feature Scaling
    st.subheader("📏***Feature Scaling***")
    st_scaler = StandardScaler()
    data[cont_val] = st_scaler.fit_transform(data[cont_val])
    st.write(data.head())
    st.markdown("---")

    # Split data
    st.subheader("***Splitting the Dataset*** ✂")
    X = data.drop('target', axis=1)
    y = data['target']
    st.markdown("<h4>X</h4>",unsafe_allow_html=True)
    st.write(X)
    st.markdown("<h4>Y",unsafe_allow_html=True)
    st.dataframe(y,use_container_width=False)
    st.markdown("---")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Models
    models = {
        "Logistic Regression": LogisticRegression(),
        "SVM": svm.SVC(),
        "KNN": KNeighborsClassifier(),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "Gradient Boosting": GradientBoostingClassifier()
    }

    # Train and evaluate
    results = []

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        results.append((name, acc))

    # Convert to DataFrame
    final_data = pd.DataFrame(results, columns=['Models', 'Accuracy'])

    # Show table
    st.subheader("📊 Model Accuracy Comparison ⇄")
    st.dataframe(final_data,use_container_width=True)

    # Plot graph
    st.subheader("📈 Accuracy Visualization")
    fig = px.bar(final_data,x="Models",y="Accuracy",color="Models",text="Accuracy",width=600,height=500)
    fig.update_traces(texttemplate='%{text: .2f}',textposition='outside')
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("---")
    st.subheader("⚙️ Model Training")

    # Check if already trained
    if os.path.exists("models.pkl"):
        st.info("✅ Models already trained")

        if st.button("🔄 Retrain Models"):
            with st.spinner("Training models... ⏳"):
                train_models()
            st.success("✅ Models retrained successfully!")
            st.balloons()

    else:
        if st.button("🚀 Train & Save Models"):
            with st.spinner("Training models... ⏳"):
                train_models()
            st.success("✅ Models trained and saved successfully!")
            st.balloons()