# pages/providers_page.py
import streamlit as st
import plotly.express as px
import pandas as pd

def providers_page(df):
    st.markdown("<div class='title-block'><h2>Healthcare Providers & Utilization</h2></div>", unsafe_allow_html=True)
    st.write("")

    # KPIs with safe checks
    num_doctors = df['Prescribing_Doctor'].nunique() if 'Prescribing_Doctor' in df.columns else 0
    top_doctor = df['Prescribing_Doctor'].value_counts().idxmax() if 'Prescribing_Doctor' in df.columns and not df['Prescribing_Doctor'].value_counts().empty else "N/A"
    avg_cost_per_visit = round(
        (df['Cost_USD'].sum(skipna=True) / (df['Visit_ID'].nunique() if 'Visit_ID' in df.columns else 1)),
        2
    )

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{num_doctors}</h3><div style='opacity:0.8'>Unique Prescribing Doctors</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{top_doctor}</h3><div style='opacity:0.8'>Top prescribing doctor</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card'><h3 style='margin:0'>${avg_cost_per_visit}</h3><div style='opacity:0.8'>Avg Cost per Visit</div></div>", unsafe_allow_html=True)

    # Department visit frequency
    st.markdown("### Department visit frequency")
    if 'Department' in df.columns and not df['Department'].dropna().empty:
        dept_counts = df['Department'].value_counts().reset_index()
        dept_counts.columns = ['Department', 'Count']
        fig = px.bar(
            dept_counts,
            x='Department',
            y='Count',
            title='Visits by Department',
            color='Department',
            color_discrete_sequence=px.colors.qualitative.Plotly  # multi-color palette
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Department data available.")

    # Insurance utilization
    st.markdown("### Insurance utilization")
    if 'Insurance_Type' in df.columns and not df['Insurance_Type'].dropna().empty:
        ins_counts = df['Insurance_Type'].fillna('None').value_counts().reset_index()
        ins_counts.columns = ['Insurance', 'Count']
        fig2 = px.pie(
            ins_counts,
            names='Insurance',
            values='Count',
            title='Insurance Type Utilization',
            color='Insurance',
            color_discrete_sequence=px.colors.qualitative.Pastel  # colorful slices
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Insurance_Type field not available.")

    # Summary
    st.markdown(
        "**Summary (Providers):** This page shows provider load and resource utilization by department and doctor. "
        "It can reveal high-prescribing clinicians and distribution of insurance usage, useful for operational decisions."
    )
