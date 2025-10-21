# pages/prescriptions_page.py
import streamlit as st
import pandas as pd
import plotly.express as px

def prescriptions_page(df):
    st.markdown("<div class='title-block'><h2>Prescription & Medication Insights</h2></div>", unsafe_allow_html=True)
    st.write("")

    # KPIs with safe access
    total_rx = df['Prescription_ID'].nunique() if 'Prescription_ID' in df.columns else 0
    avg_adherence = round(df['Adherence_Percent'].mean(skipna=True), 1) if 'Adherence_Percent' in df.columns else 0
    avg_duration = round(df['Duration_days'].mean(skipna=True), 1) if 'Duration_days' in df.columns else 0
    total_cost = round(df['Cost_USD'].sum(skipna=True), 2) if 'Cost_USD' in df.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{total_rx}</h3><div style='opacity:0.8'>Total Prescriptions</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{avg_adherence}%</h3><div style='opacity:0.8'>Avg Adherence</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{avg_duration} days</h3><div style='opacity:0.8'>Avg Duration</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card'><h3 style='margin:0'>${total_cost}</h3><div style='opacity:0.8'>Total Cost (sum)</div></div>", unsafe_allow_html=True)

    # Most prescribed drugs
    st.markdown("### Most prescribed drugs")
    if 'Drug_Name' in df.columns and not df['Drug_Name'].dropna().empty:
        top_drugs = df['Drug_Name'].value_counts().reset_index()
        top_drugs.columns = ['Drug', 'Count']
        top_drugs = top_drugs.head(15)
        fig = px.bar(
            top_drugs,
            x='Drug',
            y='Count',
            title='Top prescribed drugs',
            color='Drug',
            color_discrete_sequence=px.colors.qualitative.Set3  # multi-color palette
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No drug prescription data available.")

    # Adherence distribution
    if 'Adherence_Percent' in df.columns and not df['Adherence_Percent'].dropna().empty:
        st.markdown("### Adherence distribution")
        fig2 = px.histogram(
            df,
            x='Adherence_Percent',
            nbins=20,
            title='Adherence % distribution',
            color='Adherence_Percent',
            color_discrete_sequence=px.colors.qualitative.Plotly  # multi-color bars
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Adherence data not available.")

    # Generic vs Brand breakdown
    st.markdown("### Generic vs Brand breakdown")
    if 'Generic' in df.columns and not df['Generic'].dropna().empty:
        gen_counts = df['Generic'].fillna('Unknown').value_counts().reset_index()
        gen_counts.columns = ['Generic', 'Count']
        fig3 = px.pie(
            gen_counts,
            names='Generic',
            values='Count',
            title='Generic vs Brand',
            color='Generic',
            color_discrete_sequence=px.colors.qualitative.Pastel  # colorful slices
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Generic/Brand field not available.")

    st.markdown(
        "**Summary (Prescriptions):** Tracks prescribing volume, adherence and cost. "
        "Look for drugs with low adherence or high cost for interventions (counselling, generics substitution)."
    )
