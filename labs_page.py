# pages/labs_page.py
import streamlit as st
import plotly.express as px
import pandas as pd

def labs_page(df):
    st.markdown("<div class='title-block'><h2>Vital Signs & Lab Results</h2></div>", unsafe_allow_html=True)
    st.write("")

    # KPIs with safe column access
    avg_sys = round(df['Systolic_BP'].mean(skipna=True), 1) if 'Systolic_BP' in df.columns else 0
    avg_dia = round(df['Diastolic_BP'].mean(skipna=True), 1) if 'Diastolic_BP' in df.columns else 0
    avg_hba1c = round(df['HbA1c'].mean(skipna=True), 2) if 'HbA1c' in df.columns else 0
    avg_egfr = round(df['eGFR'].mean(skipna=True), 1) if 'eGFR' in df.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{avg_sys}</h3><div style='opacity:0.8'>Avg Systolic BP</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{avg_dia}</h3><div style='opacity:0.8'>Avg Diastolic BP</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{avg_hba1c}</h3><div style='opacity:0.8'>Avg HbA1c</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{avg_egfr}</h3><div style='opacity:0.8'>Avg eGFR</div></div>", unsafe_allow_html=True)

    # Blood Pressure distribution
    if 'Systolic_BP' in df.columns and 'Diastolic_BP' in df.columns:
        st.markdown("### Blood Pressure distribution")
        fig_bp = px.box(
            df,
            y=['Systolic_BP', 'Diastolic_BP'],
            title='BP distribution',
            points='outliers',
            color_discrete_sequence=px.colors.qualitative.Plotly  # multi-color palette
        )
        st.plotly_chart(fig_bp, use_container_width=True)

    # Lipid profile scatter
    if all(col in df.columns for col in ['LDL', 'HDL', 'Triglycerides']):
        st.markdown("### Lipid profile scatter (LDL vs HDL) colored by Triglycerides")
        df_lip = df.dropna(subset=['LDL', 'HDL'])
        if not df_lip.empty:
            fig_lip = px.scatter(
                df_lip,
                x='LDL',
                y='HDL',
                size='Triglycerides',
                title='LDL vs HDL (size = Triglycerides)',
                color='Triglycerides',
                color_continuous_scale=px.colors.sequential.Plasma  # visually attractive multi-color
            )
            st.plotly_chart(fig_lip, use_container_width=True)
        else:
            st.info("Insufficient LDL/HDL data for scatter.")

    # Abnormal lab flags
    if 'Flag' in df.columns:
        st.markdown("### Abnormal lab flags (sample)")
        flag_counts = df['Flag'].value_counts().reset_index()
        flag_counts.columns = ['Flag', 'Count']  # safe renaming
        fig_flag = px.bar(
            flag_counts,
            x='Flag',
            y='Count',
            title='Lab Flags (abnormal/etc.)',
            color='Flag',
            color_discrete_sequence=px.colors.qualitative.Set3  # multi-color palette
        )
        st.plotly_chart(fig_flag, use_container_width=True)
    else:
        st.info("No lab 'Flag' field available.")

    # Summary
    st.markdown(
        "**Summary (Labs):** This page highlights averages for core vitals and labs — BP, HbA1c, and kidney function (eGFR). "
        "Use these markers to flag patients who need urgent review or medication adjustments."
    )
