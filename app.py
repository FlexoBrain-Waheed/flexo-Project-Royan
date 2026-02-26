import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="NexFlexo Plant", layout="wide")
st.title("🏭 NexFlexo Smart Plant Simulator")

tabs = st.tabs([
    "1. Materials", "2. Production & Chart", "3. Consumables", 
    "4. HR & OPEX", "5. Recipes", "6. P&L", "7. Commercial"
])

# --- TAB 1 ---
with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    p_b = c1.number_input("BOPP SAR", 6.0)
    d_b = c1.number_input("BOPP Den", 0.91)
    p_pt = c2.number_input("PET SAR", 6.3)
    d_pt = c2.number_input("PET Den", 1.40)
    p_pe = c3.number_input("PE SAR", 5.0)
    d_pe = c3.number_input("PE Den", 0.92)
    p_al = c4.number_input("ALU SAR", 18.0)
    d_al = c4.number_input("ALU Den", 2.70)
    
    mat_db = {
        "BOPP": {"p": p_b, "d": d_b},
        "PET": {"p": p_pt, "d": d_pt},
        "PE": {"p": p_pe, "d": d_pe},
        "ALU": {"p": p_al, "d": d_al},
        "None": {"p": 0.0, "d": 0.0}
    }
    st.markdown("---")
    ci1, ci2, ci3 = st.columns(3)
    ink_p = ci1.number_input("Ink/Kg", 15.0)
    solv_p = ci2.number_input("Solvent/Kg", 6.0)
    adh_p = ci3.number_input("Adhesive/Kg", 12.0)

# --- TAB 2 ---
with tabs[1]:
    cw1, cw2, cw3 = st.columns(3)
    d_yr = cw1.number_input("Days/Yr", 300)
    s_day = cw1.number_input("Shifts/Day", 2)
    h_sh = cw1.number_input("Hrs/Shift", 12)
    
    j_mo = cw2.number_input("Jobs/Mo", 100)
    c_hrs = cw2.number_input("C.O. Hrs", 2.0)
    kw_p = cw3.number_input("SAR/kWh", 0.18)
    
    net_hrs = (d_yr * s_day * h_sh) - (j_mo * 12 * c_hrs)
    st.success(f"✅ Net Running Hours / Year: {net_hrs}")
    
    st.markdown("### 1. Extrusion & Printing")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.subheader("Extruder")
        e_kg = st.number_input("Extruder Kg/h", 300.0)
        e_kw = st.number_input("Extruder kW", 300.0)
        e_pr = st.number_input("Extruder CAPEX", 5000000.0)
        e_tons = (e_kg * net_hrs) / 1000.0
        e_pc = net_hrs * e_kw * kw_p
        st.info(f"⚖️ {e_tons:,.0f} Tons/Yr | ⚡ SAR {e_pc:,.0f}")
        
    with m2:
        st.subheader("Flexo CI")
        f_s = st.number_input("Flexo Speed", 300.0)
        f_w = st.number_input("Flexo Width", 1.0)
        f_e = st.slider("Flexo Eff%", 40, 100, 70)
        f_k = st.number_input("Flexo kW", 150.0)
        f_pr = st.number_input("Flexo CAPEX", 8000000.0)
        f_lm = net_hrs * 60.0 * f_s * (f_e/100.0)
        f_sq = f_lm * f_w
        f_pc = net_hrs * f_k * kw_p
        st.info(f"📏 {f_lm:,.0f} m | ⚡ SAR {f_pc:,.0f}")
        
    with m3:
        st.subheader("Lamination")
        l_s = st.number_input("Lam Speed", 250.0)
        l_w = st.number_input("Lam Width", 1.0)
        l_e = st.slider("Lam Eff%", 40, 100, 75)
        l_k = st.number_input("Lam kW", 80.0)
        l_pr = st.number_input("Lam CAPEX", 1200000.0)
        l_lm = net_hrs * 60.0 * l_s * (l_e/100.0)
        l_sq = l_lm * l_w
        l_pc = net_hrs * l_k * kw_p
        st.info(f"📏 {l_lm:,.0f} m | ⚡ SAR {l_pc:,.0f}")
        
    st.markdown("### 2. Finishing")
    m4, m5 = st.columns(2)
    
    with m4:
        st.subheader("Slitter")
        s_s = st.number_input("Slit Speed", 400.0)
        s_w = st.number_input("Slit Width", 1.0)
        s_e = st.slider("Slit Eff%", 40, 100, 80)
        s_k = st.number_input("Slit kW", 40.0)
        s_pr = st.number_input("Slit CAPEX", 800000.0)
        s_lm = net_hrs * 60.0 * s_s * (s_e/100.0)
        s_sq = s_lm * s_w
        s_pc = net_hrs * s_k * kw_p
        st.info(f"📏 {s_lm:,.0f} m | ⚡ SAR {s_pc:,.0f}")
        
    with m5:
        st.subheader("Bag Making (5 Machines)")
        b_q = st.number_input("Mach Qty", 5)
        b_s = st.number_input("Bag Speed m/m", 75.0)
        b_e = st.slider("Bag Eff%", 40, 100, 85)
        b_k = st.number_input("Total kW (for all)", 75.0)
        b_pr = st.number_input("Total Bag CAPEX", 500000.0)
        b_lm = net_hrs * 60.0 * b_s * b_q * (b_e/100.0)
        b_sq = b_lm * 1.0
        b_pc = net_hrs * b_k * kw_p
        st.info(f"📏 {b_lm:,.0f} m | ⚡ SAR {b_pc:,.0f}")
        
    st.markdown("---")
    # CHART GENERATION
    st.subheader("📊 Machines Capacity Check (Tons/Year)")
    est_gsm = st.number_input("Estimated Avg GSM for Chart", 80.0)
    
    f_tons_chart = (f_sq * est_gsm) / 1000000.0
    l_tons_chart = (l_sq * est_gsm) / 1000000.0
    s_tons_chart = (s_sq * est_gsm) / 1000000.0
    b_tons_chart = (b_sq * est_gsm) / 1000000.0
    
    df_chart = pd.DataFrame({
        "Machine": ["1. Extruder", "2. Flexo", "3. Lamination", "4. Slitter", "5. Bag Making"],
        "Max Tons / Year": [e_tons, f_tons_chart, l_tons_chart, s_tons_chart, b_tons_chart]
    })
    
    fig = px.bar(df_chart, x="Machine", y="Max Tons / Year", color="Machine", text_auto='.0f', title="Production Bottleneck Graph")
    st.plotly_chart(fig, use_container_width=True)
    
    c_cap1, c_cap2 = st.columns(2)
    t_capex = e_pr + f_pr + l_pr + s_pr + b_pr + 500000.0
    c_cap1.metric("Total CAPEX (Investment)", f"SAR {t_capex:,.0f}")
    
    dep_y = c_cap2.number_input("Depreciation Yrs", 15.0)
    ann_dep = 0.0
    if dep_y > 0:
        ann_dep = t_capex / dep_y
        
    t_pwr = e_pc + f_pc + l_pc + s_pc + b_pc

# --- TAB 3 ---
with tabs[2]:
    cc1, cc2, cc3 = st.columns(3)
    an_pr = cc1.number_input("Anilox SAR", 15000.0)
    an_lf = cc1.number_input("Anilox Life(M)", 200.0)
    
    bl_pr = cc2.number_input("Blade SAR/m", 12.0)
    bl_qt = cc2.number_input("Blade m/Job", 21.0)
    es_pr = cc2.number_input("EndSeal SAR", 150.0)
    bl_lf = cc2.number_input("Blade/Seal Life(m)", 33000.0)
    
    tp_pr = cc3.number_input("Tape SAR/m²", 85.0)
    tp_qt = cc3.number_input("Tape m²/Job", 6.0)

# --- TAB 4 ---
with tabs[3]:
    st.header("HR & Admin (OPEX)")
    ch1, ch2, ch3, ch4 = st.columns(4)
    eng_q = ch1.number_input("Eng Qty", 3)
    eng_s = ch1.number_input("Eng Sal", 8000)
    opr_q = ch2.number_input("Op Qty", 6)
    opr_s = ch2.number_input("Op Sal", 4500)
    wrk_q = ch3.number_input("Wrk Qty", 10)
    wrk_s = ch3.number_input("Wrk Sal", 2500)
    adm_q = ch4.number_input("Adm Qty", 5)
    adm_s = ch4.number_input("Adm Sal", 8000)
    
    st.markdown("#### Saudization")
    cs1, cs2 = st.columns(2)
    sau_q = cs1.number_input("Saudi Qty", 5)
    sau_s = cs2.number_input("Saudi Sal", 4000)
    
    payroll = (eng_q*eng_s) + (opr_q*opr_s) + (wrk_q*wrk_s) + (adm_q*adm_s) + (sau_q*sau_s)
    
    st.markdown("---")
    cp1, cp2, cp3 = st.columns(3)
    adm_exp = cp1.number_input("Monthly Admin Exp", 40000)
    cp2.metric("Total Monthly Payroll", f"SAR {payroll:,.0f}")
    cp3.metric("Annual Power Cost", f"SAR {t_pwr:,.0f}")

# --- TAB 5 ---
with tabs[4]:
    c_c1, c_c2, c_c3 = st.columns(3)
    w_ink = c_c1.number_input("Wet Ink", 5.0)
    i_loss = c_c2.number_input("Ink Loss%", 40.0)
    a_gsm = c_c3.number_input("Adh GSM", 1.8)
    d_ink = w_ink * (1.0 - (i_loss / 100.0))
    
    st.markdown("---")
    ct1, ct2 = st.columns(2)
    t_tons = ct1.number_input("Target Tons", 3600.0)
    std_w = ct2.number_input("Web Width (m)", 1.0)
    
    init_data = [
        {"Product": "1 Lyr", "L1": "BOPP", "M1": 38, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 50, "Price": 12.0},
        {"Product": "2 Lyr", "L1": "BOPP", "M1": 20, "L2": "BOPP", "M2": 20, "L3": "None", "M3": 0, "Mix%": 30, "Price": 13.0},
        {"Product": "3 Lyr", "L1": "PET", "M1": 12, "L2": "ALU", "M2": 7, "L3": "PE", "M3": 50, "Mix%": 20, "Price": 15.0}
    ]
    df_rec = st.data_editor(pd.DataFrame(init_data), num_rows="dynamic", use_container_width=True)
    
    w_gsm = 0.0
    w_rmc = 0.0
    w_sp = 0.0
    l_mix = 0.0
    t_ink_k = 0.0
    t_slv_k = 0.0
    t_adh_k = 0.0
    
    dets = []
    m_nd = {}
    
    for _, r in df_rec.iterrows():
        g1 = r["M1"] * mat_db[r["L1"]]["d"]
        g2 = r["M2"] * mat_db[r["L2"]]["d"]
        g3 = r["M3"] * mat_db[r["L3"]]["d"]
        
        lp = 0
        if r["M2"] > 0: lp += 1
        if r["M3"] > 0: lp += 1
        
        ag = lp * a_gsm
        tg = g1 + g2 + g3 + d_ink + ag
        
        c1 = (g1/1000.0) * mat_db[r["L1"]]["p"]
        c2 = (g2/1000.0) * mat_db[r["L2"]]["p"]
        c3 = (g3/1000.0) * mat_db[r["L3"]]["p"]
        ca = (ag/1000.0) * adh_p
        ci = (w_ink/1000.0) * ink_p
        cs = (w_ink*0.5/1000.0) * solv_p
        
        cpk = 0.0
        if tg > 0:
            cpk = (c1+c2+c3+ca+ci+cs)/(tg/1000.0)
            
        r_ton = t_tons * (r["Mix%"]/100.0)
        l_len = 0.0
        
        if tg > 0:
            sq = (r_ton * 1000000.0) / tg
            if std_w > 0: 
                l_len = sq / std_w
            t_ink_k += (sq * w_ink) / 1000.0
            t_slv_k += (sq * w_ink * 0.5) / 1000.0
            t_adh_k += (sq * ag) / 1000.0
            
            for lyr, mic in [("L1","M1"), ("L2","M2"), ("L3","M3")]:
                if r[lyr] != "None" and r[mic] > 0:
                    mk = f"{r[lyr]} {r[mic]}µ"
                    m_nd[mk] = m_nd.get(mk, 0.0) + l_len
                    
        mr = r["Mix%"] / 100.0
        w_gsm += tg * mr
        w_rmc += cpk * mr
        w_sp += r["Price"] * mr
        if lp > 0: 
            l_mix += mr
            
        dets.append({
            "Product": r["Product"], 
            "Tons": r_ton, 
            "Length(m)": round(l_len,0), 
            "GSM": round(tg,1), 
            "Cost/Kg": round(cpk,2), 
            "Margin": round(r["Price"]-cpk,2)
        })
        
    st.dataframe(pd.DataFrame(dets), use_container_width=True)
    
    if m_nd: 
        st.dataframe(pd.DataFrame([{"Material": k, "Meters": f"{v:,.0f}"} for k, v in m_nd.items()]), use_container_width=True)
    
    ck1, ck2, ck3 = st.columns(3)
    ck1.metric("Ink Kg/Mo", f"{t_ink_k/12:,.0f}")
    ck2.metric("Solv Kg/Mo", f"{t_slv_k/12:,.0f}")
    ck3.metric("Adh Kg/Mo", f"{t_adh_k/12:,.0f}")
    
    # حساب القدرات بناءً على الوزن الحقيقي (GSM) الممزوج
    fx_max = (f_sq * w_gsm) / 1000000.0
    sl_max = (s_sq * w_gsm) / 1000000.0
    bg_max = (b_sq * w_gsm) / 1000000.0
    
    lm_max = 999999.0
    if l_mix > 0:
        lm_max = (l_sq * w_gsm) / 1000000.0 / l_mix
        
    st.markdown("### 🚦 Exact Line Balancing")
    cb1, cb2, cb3, cb4, cb5 = st.columns(5)
    
    if t_tons <= e_tons: cb1.success(f"Ext: {e_tons:,.0f} T")
    else: cb1.error(f"Ext: {e_tons:,.0f} T")
        
    if t_tons <= fx_max: cb2.success(f"Flx: {fx_max:,.0f} T")
    else: cb2.error(f"Flx: {fx_max:,.0f} T")
        
    if t_tons <= lm_max: cb3.success(f"Lam: {lm_max:,.0f} T")
    else: cb3.error(f"Lam: {lm_max:,.0f} T")
        
    if t_tons <= sl_max: cb4.success(f"Slt: {sl_max:,.0f} T")
    else: cb4.error(f"Slt: {sl_max:,.0f} T")
        
    if t_tons <= bg_max: cb5.success(f"Bag: {bg_max:,.0f} T")
    else: cb5.error(f"Bag: {bg_max:,.0f} T")

# --- TAB 6 & 7 ---
tot_rev = t_tons * 1000.0 * w_sp
a_rm = t_tons * 1000.0 * w_rmc
esm = 0.0
if w_gsm > 0:
    esm = t_tons * (1000.0/w_gsm) * 1000.0
ln_m = esm
if std_w > 0:
    ln_m = esm / std_w

a_an = 0.0
if an_lf > 0:
    a_an = (ln_m / (an_lf*1000000.0)) * an_pr * 8.0
    
a_bl_es = 0.0
if bl_lf > 0:
    a_bl_es = (ln_m / bl_lf) * (bl_qt*bl_pr + es_pr*8.0)
    
a_tp = (j_mo * 12.0) * tp_qt * tp_pr
a_cons = a_an + a_bl_es + a_tp

a_hr = (payroll + adm_exp) * 12.0
t_opex = a_rm + a_cons + a_hr + t_pwr + ann_dep
n_prof = tot_rev - t_opex

pbk = 0.0
if n_prof > 0:
    pbk = t_capex / n_prof
    
atr = 0.0
roi = 0.0
if t_capex > 0:
    atr = tot_rev / t_capex
    roi = (n_prof / t_capex) * 100.0

with tabs[5]:
    cr1, cr2, cr3, cr4 = st.columns(4)
    cr1.metric("Rev", f"{tot_rev:,.0f}")
    cr2.metric("Total Cost", f"{t_opex:,.0f}")
    cr3.metric("Profit", f"{n_prof:,.0f}")
    cr4.metric("Payback", f"{pbk:.1f}y")
    st.info(f"Includes Annual Depr. SAR {ann_dep:,.0f}")
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        pd.DataFrame({
            "Metric":["CAPEX","Tons","Rev","Cost","Profit","ROI%","Payback"], 
            "Val":[t_capex,t_tons,tot_rev,t_opex,n_prof,f"{roi:.1f}%",pbk]
        }).to_excel(w, index=False, sheet_name='Exec')
        
        pd.DataFrame({
            "Metric":["Hrs","Tons","Ext Max","Fx Max","Lm Max","Sl Max","Bg Max"], 
            "Val":[net_hrs,t_tons,e_tons,fx_max,lm_max,sl_max,bg_max]
        }).to_excel(w, index=False, sheet_name='Ops')
        
        pd.DataFrame(dets).to_excel(w, index=False, sheet_name='Mix')
        
        pd.DataFrame({
            "Item":["Mats","Cons","HR","Admin","Pwr","Depr"], 
            "SAR":[a_rm,a_cons,payroll*12.0,adm_exp*12.0,t_pwr,ann_dep]
        }).to_excel(w, index=False, sheet_name='Costs')
        
        pd.DataFrame({
            "Chem":["Ink","Solv","Adh"], 
            "Mo Kg":[t_ink_k/12.0,t_slv_k/12.0,t_adh_k/12.0]
        }).to_excel(w, index=False, sheet_name='Chem')
        
    st.download_button("📥 Excel Report", buf.getvalue(), "NexFlexo.xlsx", "application/vnd.ms-excel", use_container_width=True)

with tabs[6]:
    ct1, ct2, ct3 = st.columns(3)
    ct1.metric("Turnover", f"SAR {tot_rev:,.0f}")
    ct2.metric("Asset Turn", f"{atr:.2f}x")
    ct3.metric("ROI", f"{roi:.1f}%")
    st.markdown("---")
    cq1, cq2 = st.columns(2)
    cn = cq1.text_input("Customer", "Valued Client")
    
    pl = [i["Product"] for i in dets]
    sr = cq2.selectbox("Product", pl)
    
    sc = 0
    sg = 0
    for i in dets:
        if i["Product"] == sr:
            sc = i["Cost/Kg"]
            sg = i["GSM"]
            
    mp = cq1.number_input("Margin %", 5, 100, 20)
    if st.button("Generate Offer"):
        fp = sc * (1.0 + (mp/100.0))
        st.info(f"**To:** {cn}\n\n**Product:** {sr} ({sg} g/m²)\n\n**Price/Kg:** SAR {fp:.2f}\n\n*Waheed Waleed Malik, NexFlexo*")
