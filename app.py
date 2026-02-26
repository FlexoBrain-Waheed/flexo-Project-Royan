import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Flexo Smart Plant", layout="wide")

st.title("🏭 Flexo Smart Plant Simulator")
st.markdown("---")

tabs = st.tabs([
    "1. Raw Materials", 
    "2. Production (OEE)", 
    "3. Consumables", 
    "4. HR & OPEX", 
    "5. Recipes & Line Balance", 
    "6. P&L Dashboard"
])

# ==========================================
# 1. Raw Materials Master Data
# ==========================================
with tabs[0]:
    st.header("Raw Materials (Price & Density)")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        p_bopp = st.number_input("BOPP Price/Kg", 6.0)
        d_bopp = st.number_input("BOPP Density (g/cm3)", 0.91)
    with c2: 
        p_pet = st.number_input("PET Price/Kg", 5.5)
        d_pet = st.number_input("PET Density (g/cm3)", 1.40)
    with c3: 
        p_pe = st.number_input("PE Price/Kg", 5.0)
        d_pe = st.number_input("PE Density (g/cm3)", 0.92)
    with c4: 
        p_alu = st.number_input("ALU Price/Kg", 18.0)
        d_alu = st.number_input("ALU Density (g/cm3)", 2.70)

    mat_db = {
        "BOPP": {"p": p_bopp, "d": d_bopp},
        "PET": {"p": p_pet, "d": d_pet},
        "PE": {"p": p_pe, "d": d_pe},
        "ALU": {"p": p_alu, "d": d_alu},
        "None": {"p": 0.0, "d": 0.0}
    }
    
    st.markdown("---")
    st.subheader("Inks, Adhesives & Solvents")
    ci1, ci2, ci3 = st.columns(3)
    ink_price = ci1.number_input("Ink Price/Kg", 15.0)
    solvent_price = ci2.number_input("Solvent Price/Kg", 6.0)
    adhesive_price = ci3.number_input("Adhesive Price/Kg", 12.0)

# ==========================================
# 2. Production & OEE
# ==========================================
with tabs[1]:
    st.header("Production Capacity & OEE")
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.subheader("Working Schedule")
        work_days = st.number_input("Working Days/Year", 300)
        shifts_day = st.number_input("Shifts/Day", 2)
        hrs_shift = st.number_input("Hours/Shift", 12)
        total_avail_hrs = work_days * shifts_day * hrs_shift
    with col_w2:
        st.subheader("Changeovers (Downtime)")
        jobs_month = st.number_input("Jobs/Month", 60)
        hrs_per_changeover = st.number_input("Hours/Changeover", 1.0)
        total_downtime = (jobs_month * 12) * hrs_per_changeover
        net_running_hrs = total_avail_hrs - total_downtime

    st.success(f"Available: {total_avail_hrs} Hrs | Downtime: {total_downtime} Hrs | Net Running: {net_running_hrs} Hrs")
    st.markdown("---")
    
    st.header("Machines Speeds & Output (Area)")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.subheader("1. Flexo CI")
        f_speed = st.number_input("Flexo Speed (m/min)", 300)
        f_width = st.number_input("Flexo Web Width (m)", 1.0)
        f_eff = st.slider("Flexo Efficiency %", 40, 100, 70)
        f_price = st.number_input("Flexo Price (SAR)", 8000000)
        
        f_lin_m = net_running_hrs * 60 * f_speed * (f_eff / 100)
        f_sq_m = f_lin_m * f_width
        st.info(f"📏 Annual Linear: {f_lin_m:,.0f} m\n📉 Monthly Avg: {(f_lin_m/12):,.0f} m\n\n🔲 Annual Area: {f_sq_m:,.0f} Sq.m")

    with m2:
        st.subheader("2. Lamination")
        l_speed = st.number_input("Lam Speed (m/min)", 250)
        l_width = st.number_input("Lam Web Width (m)", 1.0)
        l_eff = st.slider("Lam Efficiency %", 40, 100, 75)
        l_price = st.number_input("Lam Price (SAR)", 1200000)
        
        l_lin_m = net_running_hrs * 60 * l_speed * (l_eff / 100)
        l_sq_m = l_lin_m * l_width
        st.info(f"📏 Annual Linear: {l_lin_m:,.0f} m\n📉 Monthly Avg: {(l_lin_m/12):,.0f} m\n\n🔲 Annual Area: {l_sq_m:,.0f} Sq.m")

    with m3:
        st.subheader("3. Slitter")
        s_speed = st.number_input("Slitter Speed (m/min)", 400)
        s_width = st.number_input("Slitter Web Width (m)", 1.0)
        s_eff = st.slider("Slitter Efficiency %", 40, 100, 80)
        s_price = st.number_input("Slitter Price (SAR)", 800000)
        
        s_lin_m = net_running_hrs * 60 * s_speed * (s_eff / 100)
        s_sq_m = s_lin_m * s_width
        st.info(f"📏 Annual Linear: {s_lin_m:,.0f} m\n📉 Monthly Avg: {(s_lin_m/12):,.0f} m\n\n🔲 Annual Area: {s_sq_m:,.0f} Sq.m")

    total_capex = f_price + l_price + s_price + 500000 

# ==========================================
# 3. Consumables
# ==========================================
with tabs[2]:
    st.header("Consumables")
    cc1, cc2, cc3 = st.columns(3)
    
    with cc1:
        anilox_price = st.number_input("Anilox Roller Price", 15000)
        anilox_life = st.number_input("Anilox Life (Million m)", 200)
    with cc2:
        blade_price = st.number_input("Doctor Blade Price/m", 12.0)
        blade_life = st.number_input("Blade Life (1000 m)", 500)
    with cc3:
        endseal_price = st.number_input("End Seals Price", 150.0)
        endseal_life = st.number_input("End Seals Life (Hrs)", 72)

# ==========================================
# 4. HR & OPEX
# ==========================================
with tabs[3]:
    st.header("HR & Admin (OPEX)")
    ch1, ch2, ch3 = st.columns(3)
    
    with ch1:
        engineers = st.number_input("Engineers Qty", 3)
        eng_salary = st.number_input("Engineer Salary", 8000)
    with ch2:
        operators = st.number_input("Operators Qty", 6)
        op_salary = st.number_input("Operator Salary", 4500)
    with ch3:
        admin_sales = st.number_input("Admin & Sales Qty", 5)
        as_salary = st.number_input("Admin/Sales Salary", 8000)
        
    st.markdown("---")
    admin_expenses = st.number_input("Monthly Admin Expenses (Rent, etc.)", 40000)
    power_cost_annual = st.number_input("Annual Power Cost", 400000)
    monthly_payroll = (engineers*eng_salary) + (operators*op_salary) + (admin_sales*as_salary)

# ==========================================
# 5. Recipes & Line Balance
# ==========================================
with tabs[4]:
    st.header("Recipes & Production Mix")
    
    # New Added Feature: Chemicals & Weights Settings
    st.markdown("### 🧪 Chemicals & Weights Settings")
    st.info("These settings apply instantly to all recipes. Ink evaporates 40%, and Solvent evaporates 100%.")
    col_c1, col_c2, col_c3 = st.columns(3)
    
    wet_ink_gsm = col_c1.number_input("Wet Ink Applied (g/m²)", value=5.0)
    ink_loss_percent = col_c2.number_input("Ink Evaporation Loss %", value=40)
    adh_gsm_per_pass = col_c3.number_input("Adhesive per Lam Pass (g/m²)", value=1.8)
    
    # Calculate dry ink that actually stays on the product
    dry_ink_gsm = wet_ink_gsm * (1 - (ink_loss_percent / 100))
    # Solvent is always half of ink (added to cost, but 100% evaporates so it's 0g in final product)
    solvent_ratio = 0.5 
    
    st.markdown("---")
    target_sales_tons = st.number_input("Target Annual Sales (Tons)", 1200)
    
    recipe_data = [
        {"Structure": "1 Layer (Label)", "L1": "BOPP", "Mic_1": 38, "L2": "None", "Mic_2": 0, "L3": "None", "Mic_3": 0, "Mix_%": 60, "
