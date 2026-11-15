import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


def data_visualization(total_rows,duplicate_rows,unique_rows):
    chart_data = pd.DataFrame({
        "Category": ['Total Rows', "Duplicate Rows", "Unique Rows"],
        "Count": [total_rows,duplicate_rows,unique_rows],
        "color": ["#0096FF","#FF2800","#00A86B"]
    })
    fig = px.bar(chart_data,x="Category",y="Count",color="Category",
                    color_discrete_map={"Total Rows": "#0096FF", "Duplicate Rows": "#FF2800","Unique Rows":"#00A86B"},
                    text="Count",width=700,height=500)
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig,use_container_width=False)
    
def correlation_matrix(df_cleaned):
    corr = df_cleaned.corr(numeric_only=True)
    fig = px.imshow(corr,text_auto=True,color_continuous_scale="RdBu_r",width=700,height=500)
    st.plotly_chart(fig,use_container_width=False)

def heart_disease_visualization(total_patients,have_hd,no_hd):
    chart_data = pd.DataFrame({
                "Category": ["Total Patients","Have Heart Disease","No Heart Disease"],
                "Count": [total_patients,have_hd,no_hd],
                "color": ["#0096FF","#FF2800","#00A86B"]
            })
    fig = px.bar(chart_data,x="Category",y="Count",color="Category",
                         color_discrete_map={"Total Patients":"#0096FF","Have Heart Disease": "#FF2800","No Heart Disease":"#00A86B"},
                         text="Count",width=700,height=500)
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig,use_container_width=False)

def  age_distribution(df):
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=df["age"],
            nbinsx=20,
            name="Age"
        )
    )
    fig.update_layout(
        title="Age Distribution",
        xaxis_title="Age",
        yaxis_title="Number of Patients",
        bargap=0.1
    )
    return fig
    # st.plotly_chart(fig,use_container_width=False)    

def chest_pain_type(df,cp_map):
    cp_counts = df['cp'].map(cp_map).value_counts()
    cp_df = cp_counts.reset_index()
    cp_df.columns = ["Chest Pain Type", "Count"]
    fig = px.pie(cp_df,names="Chest Pain Type",values="Count",color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(textinfo='percent+label',hole=0.4)
    st.plotly_chart(fig, use_container_width=False)

def cpt_heart(plot_df,cp_map,target_map):
    plot_df['cp'] = plot_df['cp'].map(cp_map)
    plot_df['target'] = plot_df['target'].map(target_map)
    grouped = plot_df.groupby(['cp','target']).size().reset_index(name='Count')
    fig = px.bar(grouped,x='cp',y='Count',color='target',barmode='group',text='Count',color_discrete_map={"Heart Disease":"#FF2800","No Heart Disease":"#00A86B"})
    fig.update_layout(xaxis_title="Chest Pain Type",yaxis_title="Count",height=500)
    st.plotly_chart(fig,use_container_width=True)

def fasting_blood(df_plot,fbs_map,target_map):
    df_plot['fbs'] = df_plot['fbs'].map(fbs_map)
    df_plot['target'] = df_plot['target'].map(target_map)
    grouped = df_plot.groupby(['fbs', 'target']).size().reset_index(name='Count')
    fig = px.bar(grouped,x='fbs',y='Count',color='target',barmode='group',text='Count',color_discrete_map={"Heart Disease":"#FF2800","No Heart Disease":"#00A86B"})
    st.plotly_chart(fig, use_container_width=True)

def resting_blood(df_plot,sex_map):
    df_plot['sex'] = df_plot['sex'].map(sex_map)
    fig = px.histogram(df_plot, x='trestbps',facet_col='sex',nbins=20)
    st.plotly_chart(fig, use_container_width=True)

def Continuous_distribution(df):
    continuous_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    df_melt = df[continuous_cols].melt(var_name="Feature", value_name="Value")
    fig = px.histogram(df_melt,x="Value",facet_col="Feature",facet_col_wrap=2,nbins=30)
    fig.update_layout(height=650)
    st.plotly_chart(fig, use_container_width=True)
