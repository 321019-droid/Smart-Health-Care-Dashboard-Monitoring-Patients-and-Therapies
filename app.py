# app.py
import streamlit as st
from utils import load_data, apply_global_style
from pages.home_page import home_page
from pages.demographics_page import demographics_page
from pages.conditions_page import conditions_page
from pages.labs_page import labs_page
from pages.prescriptions_page import prescriptions_page
from pages.providers_page import providers_page
from pages.patient_journey_page import patient_journey_page

st.set_page_config(page_title="Smart Health Care Dashboard :Monitoring Patients And Therapies", layout="wide", initial_sidebar_state="expanded")
apply_global_style()

df = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home","Demographics","Conditions","Labs","Prescriptions","Providers","Patient Journey"])

if page == "Home":
    home_page(df)
elif page == "Demographics":
    demographics_page(df)
elif page == "Conditions":
    conditions_page(df)
elif page == "Labs":
    labs_page(df)
elif page == "Prescriptions":
    prescriptions_page(df)
elif page == "Providers":
    providers_page(df)
elif page == "Patient Journey":
    patient_journey_page(df)

# presenter details & footer (fixed position via CSS from utils)
st.markdown("<div class='presenter'>Name: u.kusuma &nbsp;&nbsp; Roll No: 321019 &nbsp;&nbsp; Course: V Pharm. D</div>", unsafe_allow_html=True)
st.markdown("<div class='footer'>@All Rights Reserved To UYYURI KUSUMA</div>", unsafe_allow_html=True)
