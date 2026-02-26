import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="NexFlexo Smart Plant", layout="wide")
st.title("🏭 NexFlexo Smart Plant Simulator")

tabs = st.tabs([
    "1. Raw Materials", "2. Production & Power", "3. Consumables", 
    "4. HR & OPEX", "5. Recipes", "6. P&L Dashboard", "7. Commercial"
])

# --- TAB 1 ---
with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    p_bopp = c1.number_input("BOPP Price", 6.0)
    d_bopp = c1.number_input("BOPP Den", 0.91)
    
    p_pet = c2.number_input("PET Price", 5.5)
    d_pet = c2.number_input("PET Den", 1.40)
    
    p_pe = c3.number_input("PE Price", 5.0)
    d_pe = c3.number_input("PE Den", 0.92)
    
    p_alu = c4.number_input("ALU Price", 18.0)
    d_alu = c4.number_input("ALU Den", 2.70)
    
    mat_db = {
        "BOPP": {"p": p_bopp, "d": d_bopp},
        "PET": {"p": p_pet, "d": d_pet},
        "PE": {"p": p_pe, "d": d_pe},
        "ALU": {"p": p_alu, "d": d_alu},
        "None": {"p": 0.0, "d": 0.0}
    }
    
    ci1, ci2, ci3 = st.columns(3)
    ink_p = ci1.number_input("Ink/Kg", 15.0)
    solv_p = ci2.number_input("Solvent/Kg", 6.0)
    adh_p = ci3.number_input("Adhesive/Kg", 12.0)

# --- TAB 2 ---
with tabs[1]:
    cw1, cw2 = st.columns(2)
    d_yr = cw1.number_input("Days/Yr", 300)
    s_day = cw1.number_input("Shifts/Day", 2)
    h_sh = cw1.number_input("Hrs/Shift", 12)
    
    j_mo = cw2.number_input("Jobs/Mo", 60)
    c_hrs = cw2.number_input("Changeover Hrs", 1.0)
    
    gross_hrs = d_yr * s_day * h_sh
    down_hrs = j_mo * 12 * c_hrs
    net_run_hrs = gross_hrs - down_hrs
    
    st.success(f"Net Running Hours: {net_run_hrs} Hrs")
    kw_price = st.number_input("SAR / kWh", 0.18)
    
    def m_inp(col, n, sp, kw, pr, eff=70):
        s = col.number_input(f"{n} Speed", sp)
        w = col.number_input(f"{n} Width", 1.0)
        e = col.slider(f"{n} Eff %", 40, 100, eff)
        k = col.number_input(f"{n} kW", kw)
        p = col.number_input(f"{n} CAPEX", pr)
        
        lm = net_run_hrs * 60 * s * (e/100)
        sqm = lm * w
        pc = net_run_hrs * k * kw_price
        
        col.info(f"📏 {lm:,.0f} m | 🔲 {sqm:,.0f} m² | ⚡ SAR {pc:,.0f}")
        return lm, sqm, pc, p

    m1, m2, m3 = st.columns(3)
    with m1: 
        f_lm, f_sqm, f_pc, f_pr = m_inp(st, "Flexo", 300, 150.0, 8000000)
    with m2: 
        l_lm, l_sqm, l_pc, l_pr = m_inp(st, "Lam", 250, 80.0, 1200000, 75)
    with m3: 
        s_lm, s_sqm, s_pc, s_pr = m_inp(st, "Slit", 400, 40.0, 800000, 80)
        
    total_capex = f_pr + l_pr + s_pr + 500000
    pwr_cost = f_pc + l_pc + s_pc

# --- TAB 3 ---
with tabs[2]:
    cc1, cc2, cc3 = st.columns(3)
    an_pr = cc1.number_input("Anilox SAR", 15000)
    an_lf = cc1.number_input("Anilox Life(M)", 200)
    bl_pr = cc2.number_input("Blade SAR/m", 12.0)
    bl_lf = cc2.number_input("Blade Life(k)", 500)
    es_pr = cc3.number_input("EndSeal SAR", 150.0)
    es_lf = cc3.number_input("EndSeal Hrs", 72)

# --- TAB 4 ---
with tabs[3]:
    ch1, ch2, ch3, ch4 = st.columns(4)
    eng = ch1.number_input("Eng Qty", 3)
    eng_s = ch1.number_input("Eng Sal", 8000)
    
    opr = ch2.number_input("Op Qty", 6)
    opr_s = ch2.number_input("Op Sal", 4500)
    
    wrk = ch3.number_input("Worker Qty", 8)
    wrk_s = ch3.number_input("Worker Sal", 2500)
    
    adm = ch4.number_input("Admin Qty", 5)
    adm_s = ch4.number_input("Admin Sal", 8000)
    
    st.markdown("---")
    c_p1, c_p2 = st.columns(2)
    admin_exp = c_p1.number_input("Monthly Admin Exp", 40000)
    c_p2.metric("Annual Power Cost", f"SAR {pwr_cost:,.0f}")
    
    payroll = (eng*eng_s) + (opr*opr_s) + (wrk*wrk_s) + (adm*adm_s)

# --- TAB 5 ---
with tabs[4]:
    c_c1, c_c2, c_c3 = st.columns(3)
    w_ink = c_c1.number_input("Wet Ink", 5.0)
    i_loss
