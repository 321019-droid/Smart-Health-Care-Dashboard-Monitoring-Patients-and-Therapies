# pages/home_page.py
import streamlit as st
import plotly.express as px
from utils import kpi_col_formatter, COLOR_SEQ
import pandas as pd

def home_page(df):
    st.markdown("<div class='title-block'><h1>Smart Health Care Dashboard :Monitoring Patients And Therapies</h1></div>", unsafe_allow_html=True)
    st.write("")  # spacing

    # KPIs
    total_patients = df['Patient_ID'].nunique() if 'Patient_ID' in df.columns else 0
    total_visits = df['Visit_ID'].nunique() if 'Visit_ID' in df.columns else 0
    avg_age = round(df['Age'].mean(skipna=True),1) if 'Age' in df.columns else 0
    avg_bmi = round(df['BMI'].mean(skipna=True),1) if 'BMI' in df.columns else 0
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(kpi_col_formatter(total_patients, "Total unique patients"), unsafe_allow_html=True)
    col2.markdown(kpi_col_formatter(total_visits, "Total clinic visits recorded"), unsafe_allow_html=True)
    col3.markdown(kpi_col_formatter(avg_age, "Average patient age (years)"), unsafe_allow_html=True)
    col4.markdown(kpi_col_formatter(avg_bmi, "Average BMI"), unsafe_allow_html=True)

    # Snapshot charts
    st.markdown("### Snapshot charts")
    c1, c2 = st.columns([2,1])
    with c1:
        if 'Age' in df.columns and not df['Age'].dropna().empty:
            fig = px.histogram(
                df,
                x='Age',
                nbins=20,
                title="Age Distribution",
                color='Age',
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Age data not available.")

    with c2:
        if 'Gender' in df.columns and not df['Gender'].dropna().empty:
            gender_counts = df.groupby('Gender')['Patient_ID'].nunique().reset_index()
            fig2 = px.pie(
                gender_counts,
                names='Gender',
                values='Patient_ID',
                title='Gender Ratio',
                color='Gender',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Gender data not available.")

    # Quick insights
    st.markdown("### Top quick insights")
    insights = [
        f"• Total unique patients: **{total_patients}**",
        f"• Total visits recorded: **{total_visits}**",
        f"• Average age: **{avg_age} years** — check Demographics for age-band risks.",
        f"• Average BMI: **{avg_bmi}** — used for condition risk assessment.",
    ]
    for line in insights:
        st.write(line)

    st.markdown("---")
    st.markdown("**Summary (Home):** This landing page gives a quick overview of patient counts, key averages and demographic snapshots. Use the left navigation to dive into condition prevalence, labs, prescriptions and patient journeys.")

    # Dataset Overview
    st.markdown("### 📊 Dataset Overview")

    # Shape
    st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")

    # Preview data
    st.markdown("**Sample (first 10 rows):**")
    st.dataframe(df.head(10), use_container_width=True)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download full dataset as CSV",
        data=csv,
        file_name="dataset_overview.csv",
        mime="text/csv"
    )
