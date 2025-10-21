# Smart-Health-Care-Dashboard-Monitoring-Patients-and-Therapies
An interactive Streamlit dashboard designed to visualize and monitor patient demographics, conditions, labs, treatments, and overall healthcare journey.   Built for healthcare data analysis, this dashboard provides clinical and operational insights using rich visual analytics.
📁 Project Structure
Smart_Healthcare_Dashboard/
│
├── app.py # Main entry point (runs Streamlit)
│
├── pages/ # Sub-pages of the dashboard
│ ├── home_page.py
│ ├── demographics_page.py
│ ├── conditions_page.py
│ ├── labs_page.py
│ ├── providers_page.py
│ └── patient_journey_page.py
│
├── utils.py # Helper functions (data preprocessing, KPIs, plotting)
│
├── dataset.csv # Patient dataset used across the dashboard
│
└── assets/
└── styles.css # Optional custom styling
🚀 Features
✅ Home Page Overview
- Displays total patients, total visits, and key statistics (average age, BMI, etc.)
- Visualizes age and gender distributions
- Summarizes key dataset insights
✅ Demographics & Lifestyle
- Geographic distribution by state
- BMI category breakdown
- Age group segmentation and smoking status
✅ Conditions Page
- Prevalence of major health conditions
- Comorbidity and risk factor visualization
✅ Labs Page
- Lab test results and abnormality tracking
- Clinical KPIs (e.g., HbA1c control rate, lipid profiles)
✅ Providers Page
- Breakdown of patient visits by provider type, department, or specialty
✅ Patient Journey
- Tracks patient visits, medications, outcomes, and time-based treatment flow
 ⚙️ Installation & Setup
1. Clone the repository
```bash
git clone https://github.com/your-username/Smart_Healthcare_Dashboard.git
cd Smart_Healthcare_Dashboard
2. Install dependencies
Make sure you have Python 3.9+ and install required libraries:
bash
Copy code
pip install -r requirements.txt
Typical libraries used:

text
Copy code
streamlit
pandas
plotly
matplotlib
numpy
3. Run the dashboard
bash
Copy code
streamlit run app.py
4. Open in browser
Visit 👉 http://localhost:8501

📊 Dataset Description
File: dataset.csv
Contains anonymized patient information including:
Demographics (Age, Gender, State)
Clinical data (Diagnosis, Labs, BMI)
Provider & Visit details
Prescription and treatment data
🎨 Styling
Custom CSS (assets/styles.css) is used to enhance UI consistency and aesthetics.
The dark-themed header and cards ensure clear visual hierarchy for KPIs and charts.
📈 Example Pages
🏠 Home Page
Overview KPIs
Age and gender charts
Dataset preview and quick insights
👥 Demographics Page
Gender, BMI, and lifestyle distribution visualizations
💡 Summary
This interactive dashboard empowers healthcare teams to:
Monitor patients’ therapy progress.
Identify trends in demographics, conditions, and treatments.
Support data-driven clinical decisions with visual analytics.

