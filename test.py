import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Student Admissions Dashboard", layout="wide")
st.title("📊 Student Admissions, Retention & Satisfaction Dashboard")

# Cargar datos (Reemplazar con carga real de datos)
data = pd.read_csv("university_student_dashboard_data.csv")

# Métricas generales
total_applications = data['Applications'].sum()
total_admitted = data['Admitted'].sum()
total_enrolled = data['Enrolled'].sum()
avg_retention = data['Retention Rate (%)'].mean()
avg_satisfaction = data['Student Satisfaction (%)'].mean()
stats = {"Total Applications": total_applications, "Total Admitted": total_admitted, "Total Enrolled": total_enrolled, "Avg. Retention Rate (%)": avg_retention, "Avg. Student Satisfaction (%)": avg_satisfaction}

# Mostrar métricas
t1, t2, t3, t4, t5 = st.columns(5)
t1.metric("Total Applications", f"{total_applications:,}")
t2.metric("Total Admitted", f"{total_admitted:,}")
t3.metric("Total Enrolled", f"{total_enrolled:,}")
t4.metric("Avg. Retention Rate (%)", f"{avg_retention:.2f}%")
t5.metric("Avg. Student Satisfaction (%)", f"{avg_satisfaction:.2f}%")

st.write("Observamos que el 59% de las personas que han aplicado a la universidad han sido admitidas y de ese porcentaje, solo el 39.8% decidió tomar los cursos. Además, en promedio, tomando todos los semestres y todos los años, la tasa de retención es de un 87.10% y la satisfacción un 82.6%")

# Gráficos en dos columnas
col1, col2, col3 = st.columns(3)

# Bar Chart: Total applications and enrollments per year
year_counts = data.groupby("Year")[["Applications", "Enrolled"]].sum().reset_index()
fig_bar = px.bar(year_counts, x="Year", y=["Applications", "Enrolled"], title="Total Applications and Enrollments per Year", barmode='group', color_discrete_sequence=["#4682B4", "#87CEFA"])
col2.plotly_chart(fig_bar)

# Pie Chart: Total students enrolled per term
term_counts = data.groupby("Term")["Enrolled"].sum().reset_index()
fig_pie = px.pie(term_counts, values="Enrolled", names="Term", title="Total Enrolled Students per Term", color_discrete_sequence=["#87CEFA", "#4682B4"])
col1.plotly_chart(fig_pie)

# Funnel Chart: Year selection
year_selected = col3.selectbox("Select Year", data["Year"].unique())
funnel_data = data[data["Year"] == year_selected]
fig_funnel = go.Figure(go.Funnel(y=["Applications", "Admitted", "Enrolled"], x=[funnel_data["Applications"].sum(), funnel_data["Admitted"].sum(), funnel_data["Enrolled"].sum()], marker=dict(color=['#4682B4', '#5F9EA0', '#87CEFA'])))
fig_funnel.update_layout(title=f"Admissions Funnel ({year_selected})")
col3.plotly_chart(fig_funnel)

st.write("De los 35.100 estudiantes que se han matriculado en la universidad, obtenemos que ha habido igual porcentaje de estudiantes ingresando tanto en otoño como primavera. Lo que sugiere a grosso modo que puede no existir una relación entre campañas realizadas en alguno de los periodos o que el inicio de distintos calendarios de clase pueden no afectar el interés por tomar los cursos")

st.title("📊 Terms behavior overview")

# Gráficos en dos columnas
col1, col2 = st.columns(2)

# Select term for time series analysis
selected_term = col1.selectbox("Select Term", data["Term"].unique())
term_data = data[data["Term"] == selected_term]

# Time series
fig_time = go.Figure()
fig_time.add_trace(go.Scatter(x=term_data["Year"], y=term_data["Applications"], mode='lines+markers', name='Applications', line=dict(color='#4682B4')))
fig_time.add_trace(go.Scatter(x=term_data["Year"], y=term_data["Admitted"], mode='lines+markers', name='Admitted', line=dict(color='#5F9EA0')))
fig_time.add_trace(go.Scatter(x=term_data["Year"], y=term_data["Enrolled"], mode='lines+markers', name='Enrolled', line=dict(color='#87CEFA')))
fig_time.update_layout(title=f"Applications, Admitted, and Enrolled Trends ({selected_term})")
col1.plotly_chart(fig_time)

# Ratio of Enrolled/Applications per Term
data["Enrollment Ratio"] = data["Enrolled"] / data["Applications"]
year_slider = col2.slider("Select Year", min_value=int(data["Year"].min()), max_value=int(data["Year"].max()), value=int(data["Year"].min()))
ratio_data = data[(data["Year"] == year_slider)]
fig_ratio = px.bar(ratio_data, x="Term", y="Enrollment Ratio", title=f"Enrollment Ratio per Term ({year_slider})", color_discrete_sequence=["#87CEFA"])
fig_ratio.update_yaxes(range=[0, 1])  # Ajusta los valores según necesidad
fig_ratio.update_traces(texttemplate='%{y:.2f}', textposition='outside')
col2.plotly_chart(fig_ratio)

st.write("Tanto en spring como fall, la cantidad de estudiantes que han intentado aplicar a la universidad tiene tendencia a la alta, solo en 2020 se observó menos estudiantes. Aunque si bien se observa que la cantidad de estudiantes matriculados pareció también aumentar, cuando lo comparamos con el total de estudiantes que aplicaron podemos observar que el porcentaje ha venido disminuyendo, donde se encontraba en 24.1% en 2018 y 2024 un 22.8%. Esto puede sugerir baja preparación en los aplicantes o criterios más rigurosos de selección, es importante revisar esta tendencia dado que reduce el ingreso que recibe la universidad y el menor acceso a programas de educación superior.")



st.title("📊 Students retention and satisfaction")

col1, col2 = st.columns(2)

# 1. Time Series: Retention Rate vs. Student Satisfaction
time_series_fig = go.Figure()
time_series_fig.add_trace(go.Scatter(x=data["Year"], y=data["Retention Rate (%)"], mode='lines+markers', name='Retention Rate (%)', line=dict(color='#4682B4')))
time_series_fig.add_trace(go.Scatter(x=data["Year"], y=data["Student Satisfaction (%)"], mode='lines+markers', name='Student Satisfaction (%)', line=dict(color='#5F9EA0')))
time_series_fig.update_layout(title="Retention Rate and Student Satisfaction Over Time")
col1.plotly_chart(time_series_fig)

# 4. Additional Analysis: Correlation Heatmap
cols = ["Enrolled","Student Satisfaction (%)","Retention Rate (%)"]
correlation_fig = px.imshow(data[cols].corr(), text_auto=True, title="Correlation Heatmap of Student Data", color_continuous_scale="blues")
col2.plotly_chart(correlation_fig)

col1, col2 = st.columns(2)

# 2. Bar Chart: Retention Rate by Term Over Time
retention_bar = px.bar(data, x="Year", y="Retention Rate (%)", color="Term", barmode='group', title="Retention Rate Over Time (Spring vs. Fall)", color_discrete_sequence=["#4682B4", "#5F9EA0"])
col1.plotly_chart(retention_bar)

# 3. Bar Chart: Student Satisfaction by Term Over Time
satisfaction_bar = px.bar(data, x="Year", y="Student Satisfaction (%)", color="Term", barmode='group', title="Student Satisfaction Over Time (Spring vs. Fall)", color_discrete_sequence=["#4682B4", "#5F9EA0"])
col2.plotly_chart(satisfaction_bar)
