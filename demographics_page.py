# pages/demographics_page.py
import streamlit as st
import pandas as pd
import plotly.express as px

def demographics_page(df):
    st.markdown("<div class='title-block'><h2>Demographics & Lifestyle</h2></div>", unsafe_allow_html=True)
    st.write("")

    # KPIs
    total_patients = df['Patient_ID'].nunique() if 'Patient_ID' in df.columns else 0
    male_pct = round(100 * (df[df['Gender'].str.lower()=='male']['Patient_ID'].nunique() / (total_patients or 1)),1) if 'Gender' in df.columns else 0
    female_pct = round(100 * (df[df['Gender'].str.lower()=='female']['Patient_ID'].nunique() / (total_patients or 1)),1) if 'Gender' in df.columns else 0
    smoker_pct = round(100 * (df[df['Smoker'].str.lower()=='yes']['Patient_ID'].nunique() / (total_patients or 1)),1) if 'Smoker' in df.columns else 0
    alcohol_pct = round(100 * (df[df['Alcohol_Use'].str.lower()=='yes']['Patient_ID'].nunique() / (total_patients or 1)),1) if 'Alcohol_Use' in df.columns else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{total_patients}</h3><div style='opacity:0.8'>Total Patients</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{male_pct}%</h3><div style='opacity:0.8'>Male (%)</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{female_pct}%</h3><div style='opacity:0.8'>Female (%)</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{smoker_pct}%</h3><div style='opacity:0.8'>Smokers (%)</div></div>", unsafe_allow_html=True)

    # Geographic distribution
    st.markdown("### Geographic distribution")
    if 'State' in df.columns and not df['State'].dropna().empty:
        fig_map = px.histogram(df, x='State', title="Patients by State (count)", color='State', color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("State data not available.")

    # BMI categories
    st.markdown("### BMI categories")
    if 'BMI' in df.columns:
        df['BMI_cat'] = pd.cut(df['BMI'], bins=[0,18.5,24.9,29.9,200], labels=['Underweight','Normal','Overweight','Obese'])
        bmi_counts = df.groupby('BMI_cat', observed=False)['Patient_ID'].nunique().reset_index()  # fixed warning
        fig_bmi = px.pie(bmi_counts, names='BMI_cat', values='Patient_ID', title='BMI Category Distribution', color='BMI_cat', color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart(fig_bmi, use_container_width=True)
    else:
        st.info("BMI data not available.")

    # Age distribution
    st.markdown("### Age by category")
    if 'Age' in df.columns:
        fig_age = px.histogram(df, x='Age', nbins=12, title="Age distribution", color='Age', color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart(fig_age, use_container_width=True)
    else:
        st.info("Age data not available.")

    # Summary
    st.markdown(
        "**Summary (Demographics):** The population overview highlights which states have highest patient load, age and BMI structure, "
        "and the percentage of smokers. These metrics guide targeted prevention and screening programs."
    )
