import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Flexo Smart Plant", layout="wide")
st.title("🏭 Flexo Smart Plant Simulator")
st.markdown("---")

tabs = st.tabs(["1. Raw Materials", "2. Production & OEE", "3. Consumables", "4. HR & OPEX", "5. Sales Mix", "6. P&L Dashboard"])

with tabs[0]:
    st.header("Raw Materials (Price & Density)")
    mat_data = [
        {"Material": "BOPP", "Density (g/cm3)": 0.91, "Price/Kg": 6.0},
        {"Material": "PET", "Density (g/cm3)": 1.40, "Price/Kg": 5.5},
        {"Material": "PE", "Density (g/cm3)": 0.92, "Price/Kg": 5.0}
    ]
    df_mat = st.data_editor(pd.DataFrame(mat_data), use_container_width=True)
    avg_price_kg = df_mat["Price/Kg"].mean()
    avg_raw_mat_cost_ton = avg_price_kg * 1000 
    
    st.markdown("---")
    c_ink1, c_ink2 = st.columns(2)
    ink_price = c_ink1.number_input("Ink Price/Kg", value=15.0)
    adhesive_price = c_ink2.number_input("Solventless Adhesive Price/Kg", value=12.0)

with tabs[1]:
    st.header("Production Capacity & OEE")
    col1, col2, col3 = st.columns(3)
    with col1:
        work_days = st.number_input("Working Days/Year", value=300)
        shifts_day = st.number_input("Shifts/Day", value=2)
        hrs_shift = st.number_input("Hours/Shift", value=12)
        total_avail_hrs = work_days * shifts_day * hrs_shift
    with col2:
        jobs_month = st.number_input("Jobs/Month", value=60)
        hrs_per_changeover = st.number_input("Hours/Changeover", value=1.0)
        total_downtime = (jobs_month * 12) * hrs_per_changeover
        net_running_hrs = total_avail_hrs - total_downtime
    with col3:
        flexo_speed = st.number_input("Avg Speed (m/min)", value=300)
        web_width = st.number_input("Avg Web Width (meter)", value=1.0)
        avg_gsm = st.number_input("Avg Structure Weight (GSM)", value=60)
        
    annual_linear_meters = net_running_hrs * 60 * flexo_speed
    annual_sqm = annual_linear_meters * web_width
    annual_tons_capacity = (annual_sqm * avg_gsm) / 1000000

    st.success(f"Available: {total_avail_hrs} Hrs | Downtime: {total_downtime} Hrs | Net Running: {net_running_hrs} Hrs")
    st.info(f"Max Capacity: {annual_tons_capacity:,.0f} Tons/Year")
    
    st.markdown("---")
    cm1, cm2, cm3 = st.columns(3)
    flexo_price = cm1.number_input("Flexo CI Price", value=8000000)
    lam_price = cm2.number_input("Lamination Price", value=1200000)
    slit_price = cm3.number_input("Slitter Price", value=800000)
    total_capex = flexo_price + lam_price + slit_price + 500000
    with tabs[2]:
    st.header("Consumables")
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        anilox_price = st.number_input("Anilox Roller Price", value=15000)
        anilox_life = st.number_input("Anilox Life (Million m)", value=200)
    with cc2:
        blade_price = st.number_input("Doctor Blade Price/m", value=12.0)
        blade_life = st.number_input("Blade Life (1000 m)", value=500)
    with cc3:
        endseal_price = st.number_input("End Seals Price", value=150.0)
        endseal_life = st.number_input("End Seals Life (Hrs)", value=72)

with tabs[3]:
    st.header("HR & Admin (OPEX)")
    ch1, ch2, ch3 = st.columns(3)
    with ch1:
        engineers = st.number_input("Engineers Qty", value=3)
        eng_salary = st.number_input("Engineer Salary", value=8000)
    with ch2:
        operators = st.number_input("Operators Qty", value=6)
        op_salary = st.number_input("Operator Salary", value=4500)
    with ch3:
        admin_sales = st.number_input("Admin & Sales Qty", value=5)
        as_salary = st.number_input("Admin/Sales Salary", value=8000)
        
    admin_expenses = st.number_input("Monthly Admin Expenses (Rent, etc.)", value=40000)
    power_cost_annual = st.number_input("Annual Power Cost", value=400000)
    monthly_payroll = (engineers*eng_salary) + (operators*op_salary) + (admin_sales*as_salary)

with tabs[4]:
    st.header("Sales Mix & Revenue")
    client_data = [
        {"Structure": "1 Layer", "Mix %": 60, "Price/Kg": 12.0},
        {"Structure": "2 Layers", "Mix %": 30, "Price/Kg": 13.0},
        {"Structure": "3 Layers", "Mix %": 10, "Price/Kg": 15.0},
    ]
    df_mix = st.data_editor(pd.DataFrame(client_data), use_container_width=True)
    target_sales_tons = st.number_input("Target Annual Sales (Tons)", value=1200)
    weighted_avg_price = sum((row["Mix %"] / 100) * row["Price/Kg"] for index, row in df_mix.iterrows()) * 1000
    total_revenue = target_sales_tons * weighted_avg_price
