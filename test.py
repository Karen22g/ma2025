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

# Pie Chart: Total students per term
term_counts = data.groupby("Term")["Enrolled"].sum().reset_index()
fig_pie = px.pie(term_counts, values="Enrolled", names="Term", title="Total Enrolled Students per Term", color_discrete_sequence=["#87CEFA", "#4682B4"])
st.plotly_chart(fig_pie)

# Bar Chart: Total students per year
year_counts = data.groupby("Year")["Enrolled"].sum().reset_index()
fig_bar = px.bar(year_counts, x="Year", y="Enrolled", title="Total Enrolled Students per Year", color_discrete_sequence=["#4682B4"])
st.plotly_chart(fig_bar)

# Select term for time series analysis
selected_term = st.selectbox("Select Term", data["Term"].unique())
term_data = data[data["Term"] == selected_term]

# Time series
fig_time = go.Figure()
fig_time.add_trace(go.Scatter(x=term_data["Year"], y=term_data["Applications"], mode='lines+markers', name='Applications', line=dict(color='#4682B4')))
fig_time.add_trace(go.Scatter(x=term_data["Year"], y=term_data["Admitted"], mode='lines+markers', name='Admitted', line=dict(color='#5F9EA0')))
fig_time.add_trace(go.Scatter(x=term_data["Year"], y=term_data["Enrolled"], mode='lines+markers', name='Enrolled', line=dict(color='#87CEFA')))
fig_time.update_layout(title=f"Applications, Admitted, and Enrolled Trends ({selected_term})")
st.plotly_chart(fig_time)

# Funnel Chart: Year selection
year_selected = st.selectbox("Select Year", data["Year"].unique())
funnel_data = data[data["Year"] == year_selected]
fig_funnel = go.Figure(go.Funnel(y=["Applications", "Admitted", "Enrolled"], x=[funnel_data["Applications"].sum(), funnel_data["Admitted"].sum(), funnel_data["Enrolled"].sum()], marker=dict(color=['#4682B4', '#5F9EA0', '#87CEFA'])))
fig_funnel.update_layout(title=f"Admissions Funnel ({year_selected})")
st.plotly_chart(fig_funnel)

# Ratio of Enrolled/Applications per Term
data["Enrollment Ratio"] = data["Enrolled"] / data["Applications"]
year_slider = st.slider("Select Year", min_value=int(data["Year"].min()), max_value=int(data["Year"].max()), value=int(data["Year"].min()))
ratio_data = data[data["Year"] == year_slider]
fig_ratio = px.bar(ratio_data, x="Term", y="Enrollment Ratio", title=f"Enrollment Ratio per Term ({year_slider})", color_discrete_sequence=["#87CEFA"])
st.plotly_chart(fig_ratio)

# Ratio of Enrolled in Each Department
department_ratios = ratio_data.melt(
    id_vars=["Term"], 
    value_vars=["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"], 
    var_name="Department", 
    value_name="Enrolled"
)
department_ratios["Department Enrollment Ratio"] = department_ratios["Enrolled"] / ratio_data.loc[ratio_data["Term"] == term_slider, "Enrolled"].sum()
fig_dept_ratio = px.bar(department_ratios, x="Department", y="Department Enrollment Ratio", color="Term", barmode="group", title=f"Department Enrollment Ratios ({year_slider}, {term_slider})", color_discrete_sequence=["#4682B4", "#5F9EA0"])
st.plotly_chart(fig_dept_ratio)
