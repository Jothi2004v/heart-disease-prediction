
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def data_visualization(total_rows, duplicate_rows, unique_rows):
    chart_data = pd.DataFrame({
        "Category": ["Total Rows", "Duplicate Rows", "Unique Rows"],
        "Count": [total_rows, duplicate_rows, unique_rows]
    })

    fig = px.bar(
        chart_data,
        x="Category",
        y="Count",
        color="Category",
        color_discrete_map={
            "Total Rows": "#0096FF",
            "Duplicate Rows": "#FF2800",
            "Unique Rows": "#00A86B"
        },
        text="Count",
        title="Dataset Overview",
        height=450
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        showlegend=False,
        template="plotly_white",
        yaxis_title="Number of Rows",
        xaxis_title=""
    )

    st.plotly_chart(fig, use_container_width=True)


def correlation_matrix(df_cleaned):
    corr = df_cleaned.corr(numeric_only=True)

    if corr.empty:
        st.warning("No numeric columns available for correlation.")
        return

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="Correlation Matrix",
        aspect="auto"
    )

    st.plotly_chart(fig, use_container_width=True)


def heart_disease_visualization(total_patients, have_hd, no_hd):
    chart_data = pd.DataFrame({
        "Category": [
            "Total Patients",
            "Have Heart Disease",
            "No Heart Disease"
        ],
        "Count": [total_patients, have_hd, no_hd]
    })

    fig = px.bar(
        chart_data,
        x="Category",
        y="Count",
        color="Category",
        color_discrete_map={
            "Total Patients": "#0096FF",
            "Have Heart Disease": "#FF2800",
            "No Heart Disease": "#00A86B"
        },
        text="Count",
        title="Heart Disease Overview",
        height=450
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        showlegend=False,
        template="plotly_white",
        yaxis_title="Number of Patients",
        xaxis_title=""
    )

    st.plotly_chart(fig, use_container_width=True)


def age_distribution(df):
    if "age" not in df.columns:
        st.warning("Age column not found.")
        return

    fig = px.histogram(
        df,
        x="age",
        nbins=20,
        title="Age Distribution",
        labels={"age": "Age"},
        height=450
    )

    fig.update_layout(
        xaxis_title="Age",
        yaxis_title="Number of Patients",
        bargap=0.1
    )

    st.plotly_chart(fig, use_container_width=True)


def chest_pain_type(df, cp_map):
    if "cp" not in df.columns:
        st.warning("Chest pain column not found.")
        return

    cp_counts = df["cp"].map(cp_map).fillna("Unknown").value_counts()

    cp_df = cp_counts.reset_index()
    cp_df.columns = ["Chest Pain Type", "Count"]

    fig = px.pie(
        cp_df,
        names="Chest Pain Type",
        values="Count",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Chest Pain Type Distribution"
    )

    fig.update_traces(
        textinfo="percent+label",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)


def cpt_heart(plot_df, cp_map, target_map):
    if not {"cp", "target"}.issubset(plot_df.columns):
        st.warning("Required columns (cp, target) not found.")
        return

    df = plot_df.copy()

    df["cp"] = df["cp"].map(cp_map).fillna("Unknown")
    df["target"] = df["target"].map(target_map).fillna("Unknown")

    grouped = (
        df.groupby(["cp", "target"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        grouped,
        x="cp",
        y="Count",
        color="target",
        barmode="group",
        text="Count",
        title="Chest Pain Type vs Heart Disease",
        color_discrete_map={
            "Heart Disease": "#FF2800",
            "No Heart Disease": "#00A86B"
        }
    )

    fig.update_layout(
        xaxis_title="Chest Pain Type",
        yaxis_title="Number of Patients",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)


def fasting_blood(df_plot, fbs_map, target_map):
    if not {"fbs", "target"}.issubset(df_plot.columns):
        st.warning("Required columns (fbs, target) not found.")
        return

    df = df_plot.copy()

    df["fbs"] = df["fbs"].map(fbs_map).fillna("Unknown")
    df["target"] = df["target"].map(target_map).fillna("Unknown")

    grouped = (
        df.groupby(["fbs", "target"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        grouped,
        x="fbs",
        y="Count",
        color="target",
        barmode="group",
        text="Count",
        title="Fasting Blood Sugar vs Heart Disease",
        color_discrete_map={
            "Heart Disease": "#FF2800",
            "No Heart Disease": "#00A86B"
        }
    )

    fig.update_layout(
        xaxis_title="Fasting Blood Sugar",
        yaxis_title="Number of Patients",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)


def resting_blood(df_plot, sex_map):
    if not {"trestbps", "sex"}.issubset(df_plot.columns):
        st.warning("Required columns (trestbps, sex) not found.")
        return

    df = df_plot.copy()
    df["sex"] = df["sex"].map(sex_map).fillna("Unknown")

    fig = px.histogram(
        df,
        x="trestbps",
        facet_col="sex",
        nbins=20,
        title="Resting Blood Pressure Distribution",
        labels={
            "trestbps": "Resting Blood Pressure",
            "sex": "Gender"
        }
    )

    st.plotly_chart(fig, use_container_width=True)


def Continuous_distribution(df):
    continuous_cols = [
        "age",
        "trestbps",
        "chol",
        "thalach",
        "oldpeak"
    ]

    available_cols = [
        col for col in continuous_cols
        if col in df.columns
    ]

    if not available_cols:
        st.warning("No continuous numerical columns found.")
        return

    df_melt = df[available_cols].melt(
        var_name="Feature",
        value_name="Value"
    )

    fig = px.histogram(
        df_melt,
        x="Value",
        facet_col="Feature",
        facet_col_wrap=2,
        nbins=30,
        title="Continuous Feature Distribution"
    )

    fig.update_layout(height=650)

    st.plotly_chart(fig, use_container_width=True)
