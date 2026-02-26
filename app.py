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
    
    m1, m2, m3 = st.columns(3)
    with m1: 
        f_s = m1.number_input("Flexo Speed", 300)
        f_w = m1.number_input("Flexo Width", 1.0)
        f_e = m1.slider("Flexo Eff %", 40, 100, 70)
        f_k = m1.number_input("Flexo kW", 150.0)
        f_pr = m1.number_input("Flexo CAPEX", 8000000)
        
        f_lm = net_run_hrs * 60 * f_s * (f_e/100)
        f_sqm = f_lm * f_w
        f_pc = net_run_hrs * f_k * kw_price
        m1.info(f"📏 {f_lm:,.0f} m | 🔲 {f_sqm:,.0f} m² | ⚡ SAR {f_pc:,.0f}")

    with m2: 
        l_s = m2.number_input("Lam Speed", 250)
        l_w = m2.number_input("Lam Width", 1.0)
        l_e = m2.slider("Lam Eff %", 40, 100, 75)
        l_k = m2.number_input("Lam kW", 80.0)
        l_pr = m2.number_input("Lam CAPEX", 1200000)
        
        l_lm = net_run_hrs * 60 * l_s * (l_e/100)
        l_sqm = l_lm * l_w
        l_pc = net_run_hrs * l_k * kw_price
        m2.info(f"📏 {l_lm:,.0f} m | 🔲 {l_sqm:,.0f} m² | ⚡ SAR {l_pc:,.0f}")

    with m3: 
        s_s = m3.number_input("Slit Speed", 400)
        s_w = m3.number_input("Slit Width", 1.0)
        s_e = m3.slider("Slit Eff %", 40, 100, 80)
        s_k = m3.number_input("Slit kW", 40.0)
        s_pr = m3.number_input("Slit CAPEX", 800000)
        
        s_lm = net_run_hrs * 60 * s_s * (s_e/100)
        s_sqm = s_lm * s_w
        s_pc = net_run_hrs * s_k * kw_price
        m3.info(f"📏 {s_lm:,.0f} m | 🔲 {s_sqm:,.0f} m² | ⚡ SAR {s_pc:,.0f}")
        
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
    i_loss = c_c2.number_input("Ink Loss%", 40.0)
    a_gsm = c_c3.number_input("Adh GSM", 1.8)
    
    d_ink = w_ink * (1.0 - (i_loss / 100.0))
    tgt_tons = st.number_input("Target Tons", 3600.0)
    
    init_data = [
        {"Product":"1 Lyr", "L1":"BOPP", "M1":38, "L2":"None", "M2":0, "L3":"None", "M3":0, "Mix%":60, "Price":12.0},
        {"Product":"2 Lyr", "L1":"BOPP", "M1":20, "L2":"BOPP", "M2":20, "L3":"None", "M3":0, "Mix%":30, "Price":13.0},
        {"Product":"3 Lyr", "L1":"PET", "M1":12, "L2":"ALU", "M2":7, "L3":"PE", "M3":50, "Mix%":10, "Price":15.0}
    ]
    df_rec = st.data_editor(pd.DataFrame(init_data), num_rows="dynamic", use_container_width=True)
    
    w_gsm = 0.0
    w_rmc = 0.0
    w_sp = 0.0
    l_mix = 0.0
    t_ink = 0.0
    t_slv = 0.0
    t_adh = 0.0
    dets = []
    
    for _, r in df_rec.iterrows():
        g1 = r["M1"] * mat_db[r["L1"]]["d"]
        g2 = r["M2"] * mat_db[r["L2"]]["d"]
        g3 = r["M3"] * mat_db[r["L3"]]["d"]
        
        lp = 0
        if r["M2"] > 0: lp += 1
        if r["M3"] > 0: lp += 1
        
        ag = lp * a_gsm
        tg = g1 + g2 + g3 + d_ink + ag
        
        c1 = (g1/1000) * mat_db[r["L1"]]["p"]
        c2 = (g2/1000) * mat_db[r["L2"]]["p"]
        c3 = (g3/1000) * mat_db[r["L3"]]["p"]
        ca = (ag/1000) * adh_p
        ci = (w_ink/1000) * ink_p
        cs = (w_ink*0.5/1000) * solv_p
        
        cpk = 0.0
        if tg > 0:
            cpk = (c1 + c2 + c3 + ca + ci + cs) / (tg/1000)
            
        r_ton = tgt_tons * (r["Mix%"]/100)
        
        if tg > 0:
            sq = (r_ton * 1000000) / tg
            t_ink += (sq * w_ink) / 1000
            t_slv += (sq * w_ink * 0.5) / 1000
            t_adh += (sq * ag) / 1000
        
        mr = r["Mix%"] / 100.0
        w_gsm += tg * mr
        w_rmc += cpk * mr
        w_sp += r["Price"] * mr
        
        if lp > 0: 
            l_mix += mr
            
        dets.append({
            "Product": r["Product"],
            "Tons": r_ton,
            "Final GSM": round(tg, 1),
            "Cost/Kg": round(cpk, 2),
            "Margin": round(r["Price"] - cpk, 2)
        })
        
    st.dataframe(pd.DataFrame(dets), use_container_width=True)
    
    c_k1, c_k2, c_k3 = st.columns(3)
    c_k1.metric("Ink (Kg/Mo)", f"{t_ink/12:,.0f}")
    c_k2.metric("Solv (Kg/Mo)", f"{t_slv/12:,.0f}")
    c_k3.metric("Adh (Kg/Mo)", f"{t_adh/12:,.0f}")
    
    fx_max = (f_sqm * w_gsm) / 1000000
    sl_max = (s_sqm * w_gsm) / 1000000
    
    lm_max = 999999
    if l_mix > 0:
        lm_max = (l_sqm * w_gsm) / 1000000 / l_mix
    
    cb1, cb2, cb3 = st.columns(3)
    if tgt_tons <= fx_max:
        cb1.success(f"Flexo Max: {fx_max:,.0f} T")
    else:
        cb1.error(f"Flexo Max: {fx_max:,.0f} T")
        
    if tgt_tons <= lm_max:
        cb2.success(f"Lam Max: {lm_max:,.0f} T")
    else:
        cb2.error(f"Lam Max: {lm_max:,.0f} T")
        
    if tgt_tons <= sl_max:
        cb3.success(f"Slit Max: {sl_max:,.0f} T")
    else:
        cb3.error(f"Slit Max: {sl_max:,.0f} T")

# --- CALCS & TABS 6/7 ---
tot_rev = tgt_tons * 1000 * w_sp
a_rm = tgt_tons * 1000 * w_rmc

esm = 0
if w_gsm > 0:
    esm = tgt_tons * (1000/w_gsm) * 1000
    
a_cons = 0
if an_lf > 0: a_cons += (esm/(an_lf*1000000)) * an_pr * 8
if bl_lf > 0: a_cons += (esm/(bl_lf*1000)) * bl_pr * 8
if es_lf > 0: a_cons += (net_run_hrs/es_lf) * es_pr * 8

a_hr = (payroll + admin_exp) * 12
t_opex = a_rm + a_cons + a_hr + pwr_cost
n_prof = tot_rev - t_opex

pbk = 0
if n_prof > 0: pbk = total_capex / n_prof

atr = 0
roi = 0
if total_capex > 0:
    atr = tot_rev / total_capex
    roi = (n_prof / total_capex) * 100

with tabs[5]:
    cr1, cr2, cr3, cr4 = st.columns(4)
    cr1.metric("Rev", f"{tot_rev:,.0f}")
    cr2.metric("OPEX", f"{t_opex:,.0f}")
    cr3.metric("Profit", f"{n_prof:,.0f}")
    cr4.metric("Payback", f"{pbk:.1f}y")
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        df_ex = pd.DataFrame({
            "Metric":["CAPEX", "Tons", "Rev", "OPEX", "Profit", "ROI%", "Payback"],
            "Val":[total_capex, tgt_tons, tot_rev, t_opex, n_prof, f"{roi:.1f}%", pbk]
        })
        df_ex.to_excel(w, sheet_name='1.Exec', index=False)
        
        df_op = pd.DataFrame({
            "Metric":["Net Hrs", "Tons", "Flexo Max", "Lam Max", "Slit Max"],
            "Val":[net_run_hrs, tgt_tons, fx_max, lm_max, sl_max]
        })
        df_op.to_excel(w, sheet_name='2.Ops', index=False)
        
        pd.DataFrame(dets).to_excel(w, sheet_name='3.Mix', index=False)
        
        df_ox = pd.DataFrame({
            "Item":["Mats", "Consumables", "HR", "Admin", "Power"],
            "SAR":[a_rm, a_cons, payroll*12, admin_exp*12, pwr_cost]
        })
        df_ox.to_excel(w, sheet_name='4.OPEX', index=False)
        
        df_ch = pd.DataFrame({
            "Chem":["Ink", "Solvent", "Adhesive"],
            "Mo Kg":[t_ink/12, t_slv/12, t_adh/12],
            "Yr Kg":[t_ink, t_slv, t_adh]
        })
        df_ch.to_excel(w, sheet_name='5.Chem', index=False)
        
    st.download_button("📥 Excel Report", buf.getvalue(), "NexFlexo.xlsx", "application/vnd.ms-excel", use_container_width=True)

with tabs[6]:
    ct1, ct2, ct3 = st.columns(3)
    ct1.metric("Turnover", f"SAR {tot_rev:,.0f}")
    ct2.metric("Asset Turn", f"{atr:.2f}x")
    ct3.metric("ROI", f"{roi:.1f}%")
    
    st.markdown("---")
    cq1, cq2 = st.columns(2)
    cn = cq1.text_input("Customer", "Valued Client")
    sr = cq2.selectbox("Product", [i["Product"] for i in dets])
    
    sc = 0
    sg = 0
    for i in dets:
        if i["Product"] == sr:
            sc = i["Cost/Kg"]
            sg = i["Final GSM"]
            break
            
    mp = cq1.number_input("Margin %", 5, 100, 20)
    
    if st.button("Generate Offer"):
        final_price = sc * (1 + mp/100)
        st.info(f"**To:** {cn}\n\n**Product:** {sr} ({sg} g/m²)\n\n**Price/Kg:** SAR {final_price:.2f}\n\n*Waheed Waleed Malik, NexFlexo*")
