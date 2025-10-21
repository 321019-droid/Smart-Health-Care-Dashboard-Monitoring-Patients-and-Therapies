# pages/conditions_page.py
import streamlit as st
import plotly.express as px
import pandas as pd

def conditions_page(df):
    st.markdown("<div class='title-block'><h2>Clinical Conditions & Diagnosis Trends</h2></div>", unsafe_allow_html=True)
    st.write("")

    # --- Safety checks ---
    if "Condition_Primary" not in df.columns:
        st.error("⚠️ The dataset does not contain 'Condition_Primary' column.")
        return
    if "Patient_ID" not in df.columns:
        st.error("⚠️ The dataset does not contain 'Patient_ID' column.")
        return

    # --- KPIs ---
    top_primary = df['Condition_Primary'].value_counts().head(1)
    top_primary_label = top_primary.index[0] if not top_primary.empty else "N/A"

    if "Condition_Secondary" in df.columns:
        comorbidity_pct = round(
            100 * (
                df[df['Condition_Secondary'].notna()]['Patient_ID'].nunique()
                / (df['Patient_ID'].nunique() or 1)
            ),
            1
        )
    else:
        comorbidity_pct = 0

    avg_diags = df['Diagnosis_Date'].dropna().nunique() if "Diagnosis_Date" in df.columns else 0

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{top_primary_label}</h3><div style='opacity:0.8'>Most common primary condition</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{comorbidity_pct}%</h3><div style='opacity:0.8'>Patients with secondary conditions</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card'><h3 style='margin:0'>{avg_diags}</h3><div style='opacity:0.8'>Distinct diagnosis dates</div></div>", unsafe_allow_html=True)

    # --- Primary condition prevalence ---
    st.markdown("### Primary condition prevalence")
    primary_counts = df['Condition_Primary'].value_counts().reset_index()
    primary_counts.columns = ['Condition', 'Count']
    fig = px.bar(
        primary_counts.head(12),
        x='Condition',
        y='Count',
        title='Top Primary Conditions',
        color='Condition',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Diagnosis trend over time ---
    if "Diagnosis_Date" in df.columns:
        df_dt = df.dropna(subset=['Diagnosis_Date']).copy()
        df_dt['Diagnosis_Date'] = pd.to_datetime(df_dt['Diagnosis_Date'], errors='coerce')
        diag_timeseries = (
            df_dt.groupby(pd.Grouper(key='Diagnosis_Date', freq='ME'))['Patient_ID']  # fixed deprecated 'M'
            .nunique()
            .reset_index()
        )
        if not diag_timeseries.empty:
            fig2 = px.line(
                diag_timeseries,
                x='Diagnosis_Date',
                y='Patient_ID',
                title='New Diagnoses per Month',
                markers=True,
                line_shape='linear',
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No valid diagnosis dates available for time trend.")
    else:
        st.info("No 'Diagnosis_Date' column in dataset.")

    # --- Summary ---
    st.markdown(
        "**Summary (Conditions):** Top conditions and monthly diagnosis trends are displayed to detect rising conditions. "
        "Comorbidity percentage indicates the burden of multimorbidity and can prioritize multi-therapy management."
    )
