import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import streamlit as st

def train_models():

# Load data
    data = pd.read_csv('heart.csv')
    data = data.drop_duplicates()

    # Processing
    cate_val = []
    cont_val = []

    for col in data.columns:
        if data[col].nunique() <= 10:
            cate_val.append(col)
        else:
            cont_val.append(col)

    cate_val.remove('sex')
    cate_val.remove('target')

    data = pd.get_dummies(data, columns=cate_val, drop_first=True)

    # Scaling
    scaler = StandardScaler()
    data[cont_val] = scaler.fit_transform(data[cont_val])

    # Split
    X = data.drop('target', axis=1)
    y = data['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Models
    models = {
        "Logistic Regression": LogisticRegression(),
        "SVM": svm.SVC(),
        "KNN": KNeighborsClassifier(),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "Gradient Boosting": GradientBoostingClassifier()
    }

    trained_models = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        trained_models[name] = model

    # Save
    joblib.dump(trained_models, "models.pkl")
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(X.columns, "columns.pkl")
