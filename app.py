import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="NexFlexo Smart Plant", layout="wide")
st.title("🏭 NexFlexo Smart Plant Simulator")
st.markdown("---")

tabs = st.tabs([
    "1. Raw Materials", "2. Production (OEE)", "3. Consumables", 
    "4. HR & OPEX", "5. Recipes", "6. P&L Dashboard", "7. Commercial"
])

# --- TAB 1 ---
with tabs[0]:
    st.header("Raw Materials (Price & Density)")
    c1, c2, c3, c4 = st.columns(4)
    p_bopp = c1.number_input("BOPP Price/Kg", 6.0)
    d_bopp = c1.number_input("BOPP Density", 0.91)
    p_pet = c2.number_input("PET Price/Kg", 5.5)
    d_pet = c2.number_input("PET Density", 1.40)
    p_pe = c3.number_input("PE Price/Kg", 5.0)
    d_pe = c3.number_input("PE Density", 0.92)
    p_alu = c4.number_input("ALU Price/Kg", 18.0)
    d_alu = c4.number_input("ALU Density", 2.70)

    mat_db = {
        "BOPP": {"p": p_bopp, "d": d_bopp},
        "PET": {"p": p_pet, "d": d_pet},
        "PE": {"p": p_pe, "d": d_pe},
        "ALU": {"p": p_alu, "d": d_alu},
        "None": {"p": 0.0, "d": 0.0}
    }
    
    st.markdown("---")
    ci1, ci2, ci3 = st.columns(3)
    ink_price = ci1.number_input("Ink Price/Kg", 15.0)
    solvent_price = ci2.number_input("Solvent Price/Kg", 6.0)
    adhesive_price = ci3.number_input("Adhesive Price/Kg", 12.0)

# --- TAB 2 ---
with tabs[1]:
    st.header("Production Capacity & OEE")
    col_w1, col_w2 = st.columns(2)
    work_days = col_w1.number_input("Working Days/Year", 300)
    shifts_day = col_w1.number_input("Shifts/Day", 2)
    hrs_shift = col_w1.number_input("Hours/Shift", 12)
    total_avail_hrs = work_days * shifts_day * hrs_shift
    
    jobs_month = col_w2.number_input("Jobs/Month", 60)
    hrs_per_changeover = col_w2.number_input("Hours/Changeover", 1.0)
    total_downtime = (jobs_month * 12) * hrs_per_changeover
    net_running_hrs = total_avail_hrs - total_downtime

    st.success(f"Available: {total_avail_hrs} Hrs | Net Running: {net_running_hrs} Hrs")
    st.markdown("---")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.subheader("1. Flexo CI")
        f_speed = st.number_input("Flexo Speed (m/min)", 300)
        f_width = st.number_input("Flexo Web Width (m)", 1.0)
        f_eff = st.slider("Flexo Efficiency %", 40, 100, 70)
        f_price = st.number_input("Flexo Price (SAR)", 8000000)
        f_lin_m = net_running_hrs * 60 * f_speed * (f_eff / 100)
        f_sq_m = f_lin_m * f_width
        st.info(f"📏 Linear: {f_lin_m:,.0f} m\n🔲 Area: {f_sq_m:,.0f} Sq.m")

    with m2:
        st.subheader("2. Lamination")
        l_speed = st.number_input("Lam Speed (m/min)", 250)
        l_width = st.number_input("Lam Web Width (m)", 1.0)
        l_eff = st.slider("Lam Efficiency %", 40, 100, 75)
        l_price = st.number_input("Lam Price (SAR)", 1200000)
        l_lin_m = net_running_hrs * 60 * l_speed * (l_eff / 100)
        l_sq_m = l_lin_m * l_width
        st.info(f"📏 Linear: {l_lin_m:,.0f} m\n🔲 Area: {l_sq_m:,.0f} Sq.m")

    with m3:
        st.subheader("3. Slitter")
        s_speed = st.number_input("Slitter Speed (m/min)", 400)
        s_width = st.number_input("Slitter Web Width (m)", 1.0)
        s_eff = st.slider("Slitter Efficiency %", 40, 100, 80)
        s_price = st.number_input("Slitter Price (SAR)", 800000)
        s_lin_m = net_running_hrs * 60 * s_speed * (s_eff / 100)
        s_sq_m = s_lin_m * s_width
        st.info(f"📏 Linear: {s_lin_m:,.0f} m\n🔲 Area: {s_sq_m:,.0f} Sq.m")

    total_capex = f_price + l_price + s_price + 500000 

# --- TAB 3 ---
with tabs[2]:
    st.header("Consumables")
    cc1, cc2, cc3 = st.columns(3)
    anilox_price = cc1.number_input("Anilox Roller Price", 15000)
    anilox_life = cc1.number_input("Anilox Life (Million m)", 200)
    blade_price = cc2.number_input("Doctor Blade Price/m", 12.0)
    blade_life = cc2.number_input("Blade Life (1000 m)", 500)
    endseal_price = cc3.number_input("End Seals Price", 150.0)
    endseal_life = cc3.number_input("End Seals Life (Hrs)", 72)

# --- TAB 4 ---
with tabs[3]:
    st.header("HR & Admin (OPEX)")
    
    # تم التعديل هنا لتشمل 4 أعمدة وإضافة العمال (Workers)
    ch1, ch2, ch3, ch4 = st.columns(4)
    engineers = ch1.number_input("Engineers Qty", 3)
    eng_salary = ch1.number_input("Engineer Salary", 8000)
    
    operators = ch2.number_input("Operators Qty", 6)
    op_salary = ch2.number_input("Operator Salary", 4500)
    
    workers = ch3.number_input("Workers / Helpers Qty", 8)
    worker_salary = ch3.number_input("Worker Salary", 2500)
    
    admin_sales = ch4.number_input("Admin & Sales Qty", 5)
    as_salary = ch4.number_input("Admin/Sales Salary", 8000)
    
    st.markdown("---")
    admin_expenses = st.number_input("Monthly Admin Expenses", 40000)
    power_cost_annual = st.number_input("Annual Power Cost", 400000)
    
    # تم تحديث معادلة الرواتب لتشمل العمال
    monthly_payroll = (engineers*eng_salary) + (operators*op_salary) + (workers*worker_salary) + (admin_sales*as_salary)

# --- TAB 5 ---
with tabs[4]:
    st.header("Recipes & Production Mix")
    col_c1, col_c2, col_c3 = st.columns(3)
    wet_ink_gsm = col_c1.number_input("Wet Ink Applied (g/m²)", value=5.0)
    ink_loss_percent = col_c2.number_input("Ink Evaporation Loss %", value=40)
    adh_gsm_per_pass = col_c3.number_input("Adhesive per Lam Pass", value=1.8)
    
    dry_ink_gsm = wet_ink_gsm * (1 - (ink_loss_percent / 100))
    solvent_ratio = 0.5
