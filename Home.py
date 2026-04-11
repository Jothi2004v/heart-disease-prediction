import streamlit as st
import pandas as pd
import plotly.express as px
from Visualization import data_visualization,correlation_matrix,heart_disease_visualization,age_distribution,chest_pain_type,cpt_heart,fasting_blood,resting_blood,Continuous_distribution

#uploading a file
def show_home():

    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    with st.expander("Upload the DataSet"):
        file = st.file_uploader("📂 Upload your file (Excel)", type=["xlsx"])
        st.markdown("<style>div.block-container{padding-top:7em;}</style>", unsafe_allow_html=True)

    if file is not None:
        st.session_state.uploaded_file = file

    if st.session_state.uploaded_file is not None:
        df = pd.read_excel(st.session_state.uploaded_file)
        st.write("**Uploaded file name:**", st.session_state.uploaded_file.name)
        st.markdown("---")

        #displaying the dataset
        st.subheader("***Data set***📄")
        st.write(df.head(8))
        st.markdown("---")

        #data columns
        st.markdown("***<h1 style='text-align: center;'>Data Explanation📝</h1>***", unsafe_allow_html=True)
        st.markdown("<ul style='list-style-type: square;font-size:20px;'>"
        "<li><b><i>Age -</b></i> patient's age (in years)</li>"
        "<li><b><i>Sex -</b></i> gender (1 = Male; 0 = Female)</li>"

        "<li><b><i>cp(Chest Pain Type - 4 values):</b></i>"
        "<ul style='list-style-tupe: circle;'>" \
        "<li>Value 0 = typical agina</li>"
        "<li>Value 1 =  atypical agina</li>"
        "<li>Value 2 = non- aginal pain</li>"
        "<li>Value 3 = asymptomatic</li>"
        "</ul></li>"

        "<li><b><i>trestbps(Resting Blood Pressure) -</b></i> blood pressure at rest(in mm Hg)</li>"
        "<li><b><i>chol(Cholesterol) -</b> serum cholestoral in mg/dl</i></li>"
        "<li><b><i>fbs(Fasting Blood Sugar) -</b></i> blood sugar level after fasting(1 = >120mg/dl; 0 = normal)</li>"

        "<li><b><i>restecg(Resting ElectroCardioGraphic(ecg) results):</b></i>"
        "<ul style='list-style-tupe: circle;'>" \
        "<li>Value 0 = normal</li>"
        "<li>Value 1 = having ST-T wave abnormally (T wave inversions and/or ST elevation or depression of > 0.05 mV)</li>"
        "<li>Value 2 = showing probable or definite left ventricular hypertrophy by Estes' criteria</li>"
        "</ul></li>"

        "<li><b><i>thalch -</b> maximum heart rate during exercise</i></li>"
        "<li><b><i>exang -</b></i>chest pain during exercise (1 = yes; 0 = no)</li>"
        "<li><b><i>oldpeak -</b></i>ST depression induced by exercise relative to rest</li>"
        
        "<li><b><i>slope -</b> ST segment during exercise</i>"
        "<ul style='list-style-tupe: circle;'>" \
        "<li>Value 0 = upsloping</li>"
        "<li>Value 1 = flat</li>"
        "<li>Value 2 = downsloping</li>"
        "</ul></li>"

        "<li><b><i>ca -</b></i> number of major vessel (0-3) colored by flourscopy</li>"

        "<li><b><i>thal(Thalassemia) -</b> blood disorder test result</i>"
        "<ul style='list-style-tupe: circle;'>" \
        "<li>Value 1 = normal</li>"
        "<li>Value 2 = fixed defect</li>"
        "<li>Value 3 = reversable defect</li>"
        "</ul></li>"

        "<li><b><i>target(output):</b></i>" 
        "<ul style='list-style-tupe: circle;'>" \
        "<li>Value 0 = No Heart Disease</li>"
        "<li>Value 1 = Heart Disease Present</li>"
        "</ul></li>"
        "</ul>",unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("***<h1 style='text-align: center;'>Data Shape</h1>***", unsafe_allow_html=True)
        st.markdown(f"<h4 style='font-style: italic;'>Number of Rows: <span style = 'color: #808080';>{df.shape[0]}</span></h4>",unsafe_allow_html=True)
        st.markdown(f"<h4 style='font-style: italic;'>Number of Columns:  <span style = 'color: #808080';>{df.shape[1]}</span></h4>",unsafe_allow_html=True)
        st.markdown("---")

        #dataset information
        st.markdown("***<h1 style='text-align: center;'>Dataset Information📋</h1>***", unsafe_allow_html=True)
        info_df = pd.DataFrame({
            "Column": df.columns,
            "Non-null Count": df.count().values,
            "Data Type": df.dtypes.values
        })
        st.dataframe(info_df,use_container_width=False)
        st.markdown("---")

        #Data Cleaning
        st.markdown("***<h1 style='text-align: center;'>Data Cleaning🧼</h1>***", unsafe_allow_html=True)
        duplicates = df[df.duplicated()]
        st.subheader("Duplicate Rows searching...🔍 ")
        if duplicates.empty:
            st.success("No duplicate rows found ✅")
        else:
            st.error("***Duplicate Rows Found ❌*** ")

        total_rows = len(df)
        duplicate_rows = df.duplicated().sum()
        unique_rows = df.drop_duplicates().shape[0]
        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
        <div style="background-color:#0096FF;padding:10px;border-radius:10px;text-align:center">
            <h3 style="color:white;">Total Rows</h3>
            <h1 style="color:white;">{total_rows}</h1>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div style="background-color:#FF2800;padding:10px;border-radius:10px;text-align:center">
            <h3 style="color:white;">Duplicate Rows</h3>
            <h1 style="color:white;">{duplicate_rows}</h1>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div style="background-color:#00A86B;padding:10px;border-radius:10px;text-align:center">
            <h3 style="color:white;">Unique Rows</h3>
            <h1 style="color:white;">{unique_rows}</h1>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown(f"<h4 style='font-style: italic;'>Total Duplicate Rows:  <span style = 'color: #808080';>{duplicates.shape[0]}</span></h4>",unsafe_allow_html=True)
        st.dataframe(duplicates, use_container_width=True)
        st.markdown("---")

        #removed duplicates
        df_cleaned = df.drop_duplicates()
        st.subheader("🧹 After Removing Duplicates")
        st.markdown(f"<h4 style='font-style: italic;'>Original Rows:  <span style = 'color: #808080';>{df.shape[0]}</span></h4>",unsafe_allow_html=True)
        st.markdown(f"<h4 style='font-style: italic';>Cleaned Rows:  <span style = 'color: #808080';>{df_cleaned.shape[0]}</span></h4>",unsafe_allow_html=True)
        st.success("***No duplicate rows found ✅***")
        st.dataframe(df_cleaned, use_container_width=True)

        #download the data
        st.download_button(
        label="⬇️ Download Cleaned Data",
        data=df_cleaned.to_csv(index=False),
        file_name="Heart.csv",
        mime="text/csv"
        )
        st.markdown("---")
        
        #Graph
        st.subheader("📊***Data Visualization***")
        data_visualization(total_rows,duplicate_rows,unique_rows)
        st.markdown("---")

        #statistics
        st.markdown("***<h1 style='text-align: center;'>📈Statistics of Data</h1>***", unsafe_allow_html=True)
        st.write(df_cleaned.describe())
        st.markdown("---")

        #correlation Matrix
        st.markdown("***<h1 style='text-align: center;'>📉Correlation Matrix</h1>***", unsafe_allow_html=True)
        correlation_matrix(df_cleaned)
        st.markdown("---")

        #heart disease
        st.markdown("***<h1 style='text-align: center;'>Heart Disease DashBoard🫀</h1>***", unsafe_allow_html=True)
        counts = df_cleaned['target'].value_counts()
        total_patients = df_cleaned.shape[0]
        have_hd = counts.get(1,0)
        no_hd = counts.get(0,0)
        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
        <div style="background-color:#0096FF;padding:10px;border-radius:50px;text-align:center">
            <h3 style="color:white;">Total Patients</h3>
            <h3 style="color:white;">{total_patients}</h3>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div style="background-color:#FF2800;padding:10px;border-radius:50px;text-align:center">
            <h3 style="color:white;">Heart Disease  </h3>
            <h3 style="color:white;">{have_hd}</h3>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div style="background-color:#00A86B;padding:10px;border-radius:50px;text-align:center">
            <h3 style="color:white;">No Heart Disease</h3>
            <h3 style="color:white;">{no_hd}</h3>
        </div>
        """, unsafe_allow_html=True)

    
        #Visualization
        st.markdown("<br>",unsafe_allow_html=True)
        st.subheader("📊***Heart Disease Visualization***")
        heart_disease_visualization(total_patients,have_hd,no_hd)

        #Gender Distribution
        st.subheader("🚻***Gender Distribution***")
        df = df_cleaned.copy()
        
        df['Gender'] = df['sex'].map({1: "Male", 0: "Female"})
        df['Target'] = df['target'].map({1: "Heart Disease", 0: "No Heart Disease"})

        gender_filter = st.multiselect("Select Gender", options = df['Gender'].unique(),default = df['Gender'].unique())
        df_filtered = df[df['Gender'].isin(gender_filter)]

        gender_count = df_filtered['Gender'].value_counts().reset_index()
        gender_count.columns = ["Gender","Count"]

        gender_count["Percentage"] = (gender_count["Count"] / gender_count["Count"].sum())*100

        fig1 = px.bar(gender_count,x="Gender",y="Count",color="Gender",text=gender_count["Percentage"].round(1).astype(str) + "%",
                        color_discrete_map={"Male": "#82CAFF", "Female": "#E75480"},width=700,height=500)
        fig1.update_traces(textposition="outside")
        fig1.update_layout(showlegend=True)
        st.plotly_chart(fig1,use_container_width=False)

        #Heart disease by gender
        st.subheader("***Heart Disease by Gender***")

        grouped = df_filtered.groupby(['Gender','Target']).size().reset_index(name='Count')
        grouped["Percentage"] = grouped.groupby("Gender")["Count"].transform(lambda x: x/x.sum() * 100)

        fig2 = px.bar(grouped,x="Gender",y="Count",color="Target",text=grouped["Percentage"].round(1).astype(str) + "%",
                        barmode="stack", color_discrete_map={"Heart Disease": "#FF2800","No Heart Disease": "#00A86B"},width=700,height=500)
        fig2.update_traces(textposition="inside")
        st.plotly_chart(fig2,use_container_width=False)
        st.markdown("---")

        #age distribution
        st.markdown("***<h1 style='text-align: center;'>Age Distribution👤</h1>***", unsafe_allow_html=True)
        age_distribution(df)
        st.markdown("---")

        #pie chart
        st.markdown("***<h1 style='text-align: center;'>Chest Pain Type🫁</h1>***", unsafe_allow_html=True)
        cp_map = {0: "Typical Angina",1:"Atypical Angina",2:"Non-anginal Pain",3:"Asymptomatic Pain"}
        chest_pain_type(df,cp_map)

        #chest pain type by heart disease
        st.subheader("🫁🫀***Chest Pain Type by Heart Disease***")
        plot_df  = df
        target_map ={0: "No Heart Disease",1:"Heart Disease"}
        cpt_heart(plot_df,cp_map,target_map)
        st.markdown("---")
        
        #fast blood sugar
        st.markdown("***<h1 style='text-align: center;'>Fasting Blood Sugar by Heart Disease🩸</h1>***", unsafe_allow_html=True)
        fbs_map = {0: "Normal", 1: "High"}
        df_plot = df_cleaned.copy()
        fasting_blood(df_plot,fbs_map,target_map)
        st.markdown("---")

        #Resting Blood pressure
        st.markdown("***<h1 style='text-align: center;'>Resting Blood Pressure Distribution🩸</h1>***", unsafe_allow_html=True)
        fig = px.histogram(df,x='trestbps',nbins=20)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

        #resting blood pressure as per sex
        st.markdown("***<h1 style='text-align: center;'>Resting Blood Pressure Distribution as per Gender🩸</h1>***", unsafe_allow_html=True)
        sex_map = {0: "Female", 1: "Male"}
        resting_blood(df_plot,sex_map)
        st.markdown("---")

        #cholesterol Distribution
        st.markdown("***<h1 style='text-align: center;'>Serum Cholesterol Distribution as per Gender🧪</h1>***", unsafe_allow_html=True)
        fig = px.histogram(df,x='chol',nbins=30)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

        st.markdown("***<h1 style='text-align: center;'>Continuous Variables Distribution as per Gender🔢</h1>***", unsafe_allow_html=True)
        Continuous_distribution(df)
    
    
        



