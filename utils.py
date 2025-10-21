# utils.py
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

DATA_PATH = r"C:\Users\uyyur\OneDrive\Desktop\AI AND PYTHON\smart health care\dataset.csv"

@st.cache_data
def load_data(path=DATA_PATH):
    df = pd.read_csv(path, parse_dates=['Diagnosis_Date','Start_Date','End_Date','Test_Date'], dayfirst=False, low_memory=False)
    # Basic cleaning & typed columns
    # Make sure required columns exist - if missing, create safe defaults
    cols_needed = [
        'Patient_ID','Name','Gender','Age','City','State','Pincode','Blood_Group','Height_cm','Weight_kg','BMI',
        'Condition_Primary','Condition_Secondary','Diagnosis_Date','Systolic_BP','Diastolic_BP','Resting_Heart_Rate',
        'HbA1c','LDL','HDL','Triglycerides','Creatinine_mg_dl','eGFR','Smoker','Alcohol_Use','Insurance_Type',
        'Marital_Status','Occupation','Allergies','Primary_Care_Doctor','Prescription_ID','Visit_ID','Drug_Name',
        'Drug_Category','Form','Strength_mg','Dose_per_day','Route','Start_Date','End_Date','Duration_days','Quantity',
        'Refills','Prescribing_Doctor','Department','Cost_USD','Generic','Adverse_Event_Reported','Adherence_Percent',
        'Indication','Lab_ID','Test_Name','Panel','Result_Value','Unit','Reference_Low','Reference_High','Flag',
        'Fasting','Sample_Type','Lab_Name','Test_Date','Turnaround_Hours'
    ]
    for c in cols_needed:
        if c not in df.columns:
            df[c] = np.nan

    # numeric conversions
    numcols = ['Age','Height_cm','Weight_kg','BMI','Systolic_BP','Diastolic_BP','Resting_Heart_Rate',
               'HbA1c','LDL','HDL','Triglycerides','Creatinine_mg_dl','eGFR','Strength_mg','Dose_per_day',
               'Duration_days','Quantity','Refills','Cost_USD','Result_Value','Turnaround_Hours']
    for c in numcols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Normalize some categorical fields
    if 'Smoker' in df.columns:
        df['Smoker'] = df['Smoker'].fillna('Unknown').astype(str)
    if 'Alcohol_Use' in df.columns:
        df['Alcohol_Use'] = df['Alcohol_Use'].fillna('Unknown').astype(str)

    return df

def apply_global_style():
    """Inject CSS: Times New Roman font, dark title/KPI background, footer and presenter styling"""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Tinos&display=swap');
        html, body, [class*="css"]  {
            font-family: "Times New Roman", Tinos, serif;
        }
        .title-block {
            background: linear-gradient(90deg, #0f172a, #111827);
            color: white;
            padding: 18px;
            border-radius: 8px;
        }
        .kpi-card {
            background: linear-gradient(180deg,#0b1220, #0f1a2b);
            color: #f3f4f6;
            padding: 12px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(2,6,23,0.6);
        }
        .presenter {
            position: fixed;
            left: 20px;
            bottom: 8px;
            color: #e5e7eb;
            background: rgba(0,0,0,0.5);
            padding:6px 10px;
            border-radius:6px;
            font-size:13px;
        }
        .footer {
            position: fixed;
            right: 20px;
            bottom: 8px;
            color: #cbd5e1;
            background: rgba(0,0,0,0.5);
            padding:6px 10px;
            border-radius:6px;
            font-size:13px;
        }
        </style>
        """, unsafe_allow_html=True
    )

def kpi_col_formatter(val, subtitle=""):
    return f"<div class='kpi-card'><h3 style='margin:0'>{val}</h3><div style='opacity:0.8'>{subtitle}</div></div>"

# Standard color sequences - visually insightful and accessible
COLOR_SEQ = px.colors.sequential.Viridis + px.colors.sequential.Plasma + px.colors.diverging.RdBu
