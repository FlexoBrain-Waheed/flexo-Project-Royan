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
        l_price = st.number_input("Lam Price (SAR)",
