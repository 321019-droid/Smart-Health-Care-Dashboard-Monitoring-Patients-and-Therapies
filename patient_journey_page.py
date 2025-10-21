# pages/patient_journey_page.py
import streamlit as st
import pandas as pd
import plotly.express as px

def patient_journey_page(df):
    st.markdown("<div class='title-block'><h2>Patient Journey & Outcomes</h2></div>", unsafe_allow_html=True)
    st.write("")
    st.markdown("Select a patient to view an illustrative timeline (diagnosis → prescription → lab results):")
    unique_patients = df['Patient_ID'].dropna().unique().tolist()
    sel = st.selectbox("Select Patient ID", options=unique_patients)

    patient_df = df[df['Patient_ID'] == sel].sort_values(by='Diagnosis_Date', na_position='last')
    if patient_df.empty:
        st.info("No records for this patient.")
        return

    # Timeline: create combined events with date and label
    events = []
    for _, r in patient_df.iterrows():
        if pd.notna(r['Diagnosis_Date']):
            events.append({'date': pd.to_datetime(r['Diagnosis_Date'], errors="coerce"),
                           'event': f"Diagnosis: {r.get('Condition_Primary', '')}"})
        if pd.notna(r['Start_Date']):
            events.append({'date': pd.to_datetime(r['Start_Date'], errors="coerce"),
                           'event': f"Rx Start: {r.get('Drug_Name','')}"})
        if pd.notna(r['End_Date']):
            events.append({'date': pd.to_datetime(r['End_Date'], errors="coerce"),
                           'event': f"Rx End: {r.get('Drug_Name','')}"})
        if pd.notna(r['Test_Date']) and pd.notna(r['Test_Name']):
            events.append({'date': pd.to_datetime(r['Test_Date'], errors="coerce"),
                           'event': f"Lab: {r.get('Test_Name')} = {r.get('Result_Value')}"})

    if not events:
        st.info("No timeline events (diagnosis, start/end dates, or labs) available for this patient.")
        return

    # Ensure valid dates only
    timeline_df = pd.DataFrame(events).dropna(subset=['date']).sort_values('date')

    # Use scatter plot for chronological flow (avoids fake 1970 timestamps)
    fig = px.scatter(
        timeline_df,
        x='date',
        y='event',
        color='event',
        title=f"Timeline for Patient {sel}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(marker=dict(size=12, symbol="circle"))
    fig.update_layout(yaxis_title="Event", xaxis_title="Date")

    st.plotly_chart(fig, use_container_width=True)

    # Funnel: Diagnosed -> Treated -> Adherent -> Controlled (approx)
    diagnosed = patient_df['Patient_ID'].nunique()
    treated = patient_df[patient_df['Prescription_ID'].notna()]['Patient_ID'].nunique()
    adherent = patient_df[patient_df['Adherence_Percent'] >= 80]['Patient_ID'].nunique()
    cond_ctrl = 0
    if 'HbA1c' in patient_df.columns and patient_df['HbA1c'].notna().any():
        cond_ctrl = patient_df[patient_df['HbA1c'] < 7]['Patient_ID'].nunique()

    funnel = pd.DataFrame({
        'stage': ['Diagnosed', 'Treated', 'Adherent (>=80%)', 'Controlled (HbA1c<7)'],
        'count': [diagnosed, treated, adherent, cond_ctrl]
    })

    st.markdown("### Patient Funnel")
    fig2 = px.bar(
        funnel,
        x='stage',
        y='count',
        title='Patient conversion funnel',
        color='stage',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        "**Summary (Patient Journey):** Timeline and funnel let you follow individual patient pathways and spot drop-offs "
        "(e.g., diagnosed but not treated or low adherence). Use to prioritize outreach."
    )
