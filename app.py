import streamlit as st, pandas as pd, io, plotly.express as px

st.set_page_config(page_title="Royan Plant", layout="wide")
st.title("🏭 Royan Smart Plant Simulator")

tabs = st.tabs(["1. Materials", "2. Production & Chart", "3. Consumables", "4. HR & OPEX", "5. Recipes", "6. P&L", "7. Commercial"])

# --- TAB 1 ---
with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    p_b, d_b = c1.number_input("BOPP SAR", 6.0), c1.number_input("BOPP Den", 0.91)
    p_pt, d_pt = c2.number_input("PET SAR", 6.3), c2.number_input("PET Den", 1.40)
    p_pe, d_pe = c3.number_input("PE SAR", 3.7), c3.number_input("PE Den", 0.92)
    p_al, d_al = c4.number_input("ALU SAR", 18.0), c4.number_input("ALU Den", 2.70)
    mat_db = {"BOPP":{"p":p_b,"d":d_b}, "PET":{"p":p_pt,"d":d_pt}, "PE":{"p":p_pe,"d":d_pe}, "ALU":{"p":p_al,"d":d_al}, "None":{"p":0.0,"d":0.0}}
    st.markdown("---")
    ci1, ci2, ci3 = st.columns(3)
    ink_p = ci1.number_input("Ink/Kg", 14.0)
    solv_p = ci2.number_input("Solvent/Kg", 6.0)
    adh_p = ci3.number_input("Adhesive/Kg", 12.0)

# --- TAB 2 ---
with tabs[1]:
    cw1, cw2, cw3 = st.columns(3)
    d_yr = cw1.number_input("Days/Yr", 300)
    s_day = cw1.number_input("Shifts/Day", 2)
    h_sh = cw1.number_input("Hrs/Shift", 12)
    j_mo = cw2.number_input("Jobs/Mo", 75)
    c_hrs = cw2.number_input("C.O. Hrs", 2.0)
    kw_p = cw3.number_input("SAR/kWh", 0.18)
    net_hrs = (d_yr * s_day * h_sh) - (j_mo * 12 * c_hrs)
    st.success(f"✅ Net Running Hours / Year: {net_hrs:,.0f}")
    
    st.markdown("### 1. Extrusion & Printing")
    m1, m2, m3 = st.columns(3)
    with m1:
        e_kg = st.number_input("Extruder Kg/h", 500.0)
        e_kw = st.number_input("Extruder kW", 300.0)
        e_pr = st.number_input("Extruder CAPEX", 5000000.0)
        e_tons = (e_kg * net_hrs) / 1000.0
        e_pc = net_hrs * e_kw * kw_p
        st.info(f"⚖️ {e_tons:,.0f} Tons/Yr | ⚡ SAR {e_pc:,.0f}")
    with m2:
        f_s = st.number_input("Flexo Speed", 350.0)
        f_w = st.number_input("Flexo Width", 1.0)
        f_e = st.slider("Flexo Eff%", 40, 100, 80)
        f_k = st.number_input("Flexo kW", 150.0)
        f_pr = st.number_input("Flexo CAPEX", 8000000.0)
        f_lm = net_hrs * 60.0 * f_s * (f_e/100.0)
        f_sq = f_lm * f_w
        f_pc = net_hrs * f_k * kw_p
        st.info(f"📏 {f_lm:,.0f} m | ⚡ SAR {f_pc:,.0f}")
    with m3:
        l_s = st.number_input("Lam Speed", 450.0)
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
        b_q = st.number_input("Mach Qty", 5)
        b_s = st.number_input("Bag Speed m/m", 75.0)
        b_e = st.slider("Bag Eff%", 40, 100, 85)
        b_k = st.number_input("Total kW (all)", 75.0)
        b_pr = st.number_input("Bag CAPEX", 500000.0)
        b_lm = net_hrs * 60.0 * b_s * b_q * (b_e/100.0)
        b_sq = b_lm * 1.0
        b_pc = net_hrs * b_k * kw_p
        st.info(f"📏 {b_lm:,.0f} m | ⚡ SAR {b_pc:,.0f}")
        
    st.markdown("### 3. Utilities & Facilities")
    u1, u2, u3 = st.columns(3)
    with u1:
        st.subheader("Building (Hangar)")
        hng_pr = st.number_input("Hangar CAPEX", 4000000.0)
        hng_dep_y = st.number_input("Hangar Depr Yrs", 25.0)
    with u2:
        st.subheader("Chiller (10 Units)")
        chl_k = st.number_input("Chiller kW", 50.0)
        chl_pr = st.number_input("Chiller CAPEX", 500000.0)
        chl_dep_y = st.number_input("Chiller Depr Yrs", 10.0)
        chl_pc = net_hrs * chl_k * kw_p
        st.info(f"⚡ SAR {chl_pc:,.0f}")
    with u3:
        st.subheader("Air Compressor")
        cmp_k = st.number_input("Compressor kW", 30.0)
        cmp_pr = st.number_input("Compressor CAPEX", 250000.0)
        cmp_dep_y = st.number_input("Comp. Depr Yrs", 10.0)
        cmp_pc = net_hrs * cmp_k * kw_p
        st.info(f"⚡ SAR {cmp_pc:,.0f}")

    st.markdown("---")
    st.subheader("📊 Machines Capacity Check (Tons/Year)")
    est_gsm = st.number_input("Estimated Total Avg GSM for Chart", 40.0)
    est_flexo_gsm = est_gsm * 0.45 
    df_chart = pd.DataFrame({
        "Machine": ["1. Extruder", "2. Flexo", "3. Lamination", "4. Slitter", "5. Bag Making"],
        "Max Tons / Year": [e_tons, (f_sq*est_flexo_gsm)/1000000, (l_sq*est_gsm)/1000000, (s_sq*est_gsm)/1000000, (b_sq*est_gsm)/1000000]
    })
    st.plotly_chart(px.bar(df_chart, x="Machine", y="Max Tons / Year", color="Machine", text_auto='.0f'), use_container_width=True)
    
    c_cap1, c_cap2 = st.columns(2)
    mac_capex = e_pr + f_pr + l_pr + s_pr + b_pr
    t_capex = mac_capex + hng_pr + chl_pr + cmp_pr
    c_cap1.metric("Total CAPEX (Machines + Utilities)", f"SAR {t_capex:,.0f}")
    
    mac_dep_y = c_cap2.number_input("Machines Depreciation Yrs", 10.0)
    mac_dep = mac_capex / mac_dep_y if mac_dep_y > 0 else 0.0
    hng_dep = hng_pr / hng_dep_y if hng_dep_y > 0 else 0.0
    chl_dep = chl_pr / chl_dep_y if chl_dep_y > 0 else 0.0
    cmp_dep = cmp_pr / cmp_dep_y if cmp_dep_y > 0 else 0.0
    ann_dep = mac_dep + hng_dep + chl_dep + cmp_dep
    
    t_pwr = e_pc + f_pc + l_pc + s_pc + b_pc + chl_pc + cmp_pc

# --- TAB 3 ---
with tabs[2]:
    st.subheader("🛠️ Production Consumables")
    cc1, cc2, cc3 = st.columns(3)
    pl_pr = cc1.number_input("Plate SAR (Cliché)", 2500.0)
    pl_lf = cc1.number_input("Plate Life (m)", 400000.0)
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
    st.markdown("### ⚙️ 1. Global Production Settings")
    c_set1, c_set2, c_set3, c_set4, c_set5 = st.columns(5)
    t_tons = c_set1.number_input("🎯 Target Tons", 4500.0)
    std_w = c_set2.number_input("📏 Web Width (m)", 1.0)
    w_ink = c_set3.number_input("🎨 Wet Ink", 5.0)
    i_loss = c_set4.number_input("💧 Ink Loss%", 40.0)
    a_gsm = c_set5.number_input("🍯 Adh GSM", 1.8)
    d_ink = w_ink * (1.0 - (i_loss / 100.0))
    
    st.markdown("### 📋 2. Product Portfolio (Recipes)")
    
    init_data = [
        {"Product": "1 Lyr", "Print": True, "L1": "BOPP", "M1": 40, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 20, "Price": 13.0},
        {"Product": "2 Lyr", "Print": True, "L1": "BOPP", "M1": 20, "L2": "BOPP", "M2": 20, "L3": "None", "M3": 0, "Mix%": 25, "Price": 13.0},
        {"Product": "3 Lyr", "Print": True, "L1": "PET", "M1": 12, "L2": "ALU", "M2": 7, "L3": "PE", "M3": 50, "Mix%": 5, "Price": 15.0},
        {"Product": "Shrink Plain", "Print": False, "L1": "PE", "M1": 40, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 30, "Price": 5.0},
        {"Product": "Printed Shop. Bag", "Print": True, "L1": "PE", "M1": 40, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 20, "Price": 10.0}
    ]
    df_rec = st.data_editor(pd.DataFrame(init_data), num_rows="dynamic", use_container_width=True)
    
    w_gsm = 0.0; w_flexo_gsm = 0.0; w_rmc = 0.0; w_sp = 0.0; l_mix = 0.0
    t_ink_k = 0.0; t_slv_k = 0.0; t_adh_k = 0.0
    t_pe_req_tons = 0.0  
    
    t_flexo_lm_req = 0.0
    t_lam_sqm_req = 0.0
    t_total_sqm_req = 0.0
    
    temp_dets = []; m_nd = {}
    
    for _, r in df_rec.iterrows():
        is_printed = r.get("Print", True)
        
        g1 = r["M1"] * mat_db[r["L1"]]["d"]
        g2 = r["M2"] * mat_db[r["L2"]]["d"]
        g3 = r["M3"] * mat_db[r["L3"]]["d"]
        
        flexo_g = (g1 + d_ink) if is_printed else 0.0 
        pe_layer_gsm = 0.0
        if r["L1"] == "PE": pe_layer_gsm += g1
        if r["L2"] == "PE": pe_layer_gsm += g2
        if r["L3"] == "PE": pe_layer_gsm += g3

        lp = 0
        if r["M2"] > 0: lp += 1
        if r["M3"] > 0: lp += 1
        
        ag = lp * a_gsm
        tg = g1 + g2 + g3 + ag + (d_ink if is_printed else 0.0)
        
        c1 = (g1/1000.0) * mat_db[r["L1"]]["p"]
        c2 = (g2/1000.0) * mat_db[r["L2"]]["p"]
        c3 = (g3/1000.0) * mat_db[r["L3"]]["p"]
        ca = (ag/1000.0) * adh_p
        ci = ((w_ink/1000.0) * ink_p) if is_printed else 0.0
        cs = ((w_ink*0.5/1000.0) * solv_p) if is_printed else 0.0
        
        c_mat_kg = (c1+c2+c3+ca+ci+cs)/(tg/1000.0) if tg > 0 else 0.0
        
        r_ton = t_tons * (r["Mix%"]/100.0)
        l_len = 0.0
        
        if tg > 0:
            sq = (r_ton * 1000000.0) / tg
            t_total_sqm_req += sq  
            
            if std_w > 0: l_len = sq / std_w
            
            if is_printed:
                t_flexo_lm_req += l_len  
                t_ink_k += (sq * w_ink) / 1000.0
                t_slv_k += (sq * w_ink * 0.5) / 1000.0
                
            if lp > 0:
                t_lam_sqm_req += sq  
                
            t_adh_k += (sq * ag) / 1000.0
            t_pe_req_tons += r_ton * (pe_layer_gsm / tg)
            
            for lyr, mic in [("L1","M1"), ("L2","M2"), ("L3","M3")]:
                if r[lyr] != "None" and r[mic] > 0:
                    mk = f"{r[lyr]} {r[mic]}µ"
                    m_nd[mk] = m_nd.get(mk, 0.0) + l_len
                    
        mr = r["Mix%"] / 100.0
        w_gsm += tg * mr
        w_flexo_gsm += flexo_g * mr
        w_rmc += c_mat_kg * mr
        w_sp += r["Price"] * mr
            
        temp_dets.append({
            "Product": r["Product"], "Printed": is_printed, "Tons": r_ton, 
            "Length(m)": l_len, "GSM": tg, "Flexo GSM": flexo_g,
            "Mat Cost/Kg": c_mat_kg, "Price": r["Price"]
        })
        
    esm = t_tons * (1000.0/w_gsm) * 1000.0 if w_gsm > 0 else 0.0
    ln_m = esm / std_w if std_w > 0 else esm

    a_an = (ln_m / (an_lf*1000000.0)) * an_pr * 8.0 if an_lf > 0 else 0.0
    a_bl_es = (ln_m / bl_lf) * (bl_qt*bl_pr + es_pr*8.0) if bl_lf > 0 else 0.0
    a_pl = (t_flexo_lm_req / pl_lf) * pl_pr if pl_lf > 0 else 0.0
    a_tp = (j_mo * 12.0) * tp_qt * tp_pr
    a_cons = a_an + a_bl_es + a_pl + a_tp
    a_hr = (payroll + adm_exp) * 12.0
    
    total_conv_cost = a_cons + a_hr + t_pwr + ann_dep
    conv_cost_per_kg = total_conv_cost / (t_tons * 1000.0) if t_tons > 0 else 0.0
    
    dets = []
    for d in temp_dets:
        total_true_cost = d["Mat Cost/Kg"] + conv_cost_per_kg
        net_profit_kg = d["Price"] - total_true_cost
        margin_pct = (net_profit_kg / d["Price"]) if d["Price"] > 0 else 0.0
        
        dets.append({
            "Product": d["Product"],
            "Printed": "✅" if d["Printed"] else "❌",
            "Tons": d["Tons"],
            "Length(m)": d["Length(m)"],
            "GSM": d["GSM"],                   # 🌟 تم إصلاح الخطأ وإضافة GSM هنا
            "Flexo GSM": d["Flexo GSM"],       # 🌟 تمت إضافته للرجوع إليه عند الحاجة
            "Mat. Cost/Kg": d["Mat Cost/Kg"],
            "Mfg Cost/Kg": conv_cost_per_kg,
            "Total Cost/Kg": total_true_cost,
            "Sell Price": d["Price"],
            "Profit/Kg": net_profit_kg,
            "Margin %": margin_pct
        })
        
    st.markdown("### 📊 3. Full Absorbed Costing & True Profit Margins")
    df_dets = pd.DataFrame(dets)
    col_t1, col_t2 = st.columns([7, 3])
    with col_t1:
        st.dataframe(df_dets[["Product", "Printed", "Tons", "Length(m)", "Mat. Cost/Kg", "Mfg Cost/Kg", "Total Cost/Kg", "Sell Price", "Profit/Kg", "Margin %"]].style.format({
            "Tons": "{:,.1f}", "Length(m)": "{:,.0f}", 
            "Mat. Cost/Kg": "{:,.2f}", "Mfg Cost/Kg": "{:,.2f}", "Total Cost/Kg": "{:,.2f}", 
            "Sell Price": "{:,.2f}", "Profit/Kg": "{:,.2f}", "Margin %": "{:,.1%}"
        }), use_container_width=True)
    with col_t2:
        if m_nd:
            df_m_nd = pd.DataFrame([{"Material Roll": k, "Linear Meters": v} for k, v in m_nd.items()])
            st.dataframe(df_m_nd.style.format({"Linear Meters": "{:,.0f}"}), use_container_width=True)
            
    fig_margin = px.bar(df_dets, x="Product", y="Profit/Kg", color="Product", title="💰 True Net Profit per Product (SAR/Kg)", text_auto=".2f")
    st.plotly_chart(fig_margin, use_container_width=True)
    
    st.markdown("### 🧪 4. Monthly Chemicals")
    ck1, ck2, ck3 = st.columns(3)
    ck1.metric("🎨 Ink Kg/Mo", f"{t_ink_k/12:,.0f}")
    ck2.metric("🧪 Solv Kg/Mo", f"{t_slv_k/12:,.0f}")
    ck3.metric("🍯 Adh Kg/Mo", f"{t_adh_k/12:,.0f}")
    
    lm_max = t_tons * (l_sq / t_lam_sqm_req) if t_lam_sqm_req > 0 else 999999.0
    sl_max = t_tons * (s_sq / t_total_sqm_req) if t_total_sqm_req > 0 else 999999.0
    bg_max = t_tons * (b_sq / t_total_sqm_req) if t_total_sqm_req > 0 else 999999.0
        
    st.markdown("### 🚦 5. Exact Line Balancing (Tons & Meters)")
    cb1, cb2, cb3, cb4, cb5 = st.columns(5)
    
    if t_pe_req_tons <= e_tons: cb1.success(f"Ext: {e_tons:,.0f} T | Need PE: {t_pe_req_tons:,.0f} T")
    else: cb1.error(f"Ext: {e_tons:,.0f} T | Need PE: {t_pe_req_tons:,.0f} T")
        
    if t_flexo_lm_req <= f_lm: 
        cb2.success(f"Flx Cap: {f_lm/1000000:,.2f}M m | Need: {t_flexo_lm_req/1000000:,.2f}M m")
    else: 
        cb2.error(f"Flx Cap: {f_lm/1000000:,.2f}M m | Need: {t_flexo_lm_req/1000000:,.2f}M m")
    
    if t_tons <= lm_max: cb3.success(f"Lam: {lm_max:,.0f} T | {l_lm/1000000:,.1f}M m")
    else: cb3.error(f"Lam: {lm_max:,.0f} T | {l_lm/1000000:,.1f}M m")
    
    if t_tons <= sl_max: cb4.success(f"Slt: {sl_max:,.0f} T | {s_lm/1000000:,.1f}M m")
    else: cb4.error(f"Slt: {sl_max:,.0f} T | {s_lm/1000000:,.1f}M m")
    
    if t_tons <= bg_max: cb5.success(f"Bag: {bg_max:,.0f} T | {b_lm/1000000:,.1f}M m")
    else: cb5.error(f"Bag: {bg_max:,.0f} T | {b_lm/1000000:,.1f}M m")

# --- TAB 6 & 7 (EXCEL FORMULAS INTEGRATION) ---
tot_rev = t_tons * 1000.0 * w_sp
a_rm = t_tons * 1000.0 * w_rmc

t_opex = a_rm + total_conv_cost
n_prof = tot_rev - t_opex

pbk = t_capex / n_prof if n_prof > 0 else 0.0
atr = tot_rev / t_capex if t_capex > 0 else 0.0
roi = (n_prof / t_capex) * 100.0 if t_capex > 0 else 0.0

chem_annual_cost = (t_ink_k*ink_p + t_slv_k*solv_p + t_adh_k*adh_p)
plastic_annual_cost = a_rm - chem_annual_cost

with tabs[5]:
    st.markdown("### 📈 Overall Plant Financials")
    cr1, cr2, cr3, cr4 = st.columns(4)
    cr1.metric("Gross Revenue", f"SAR {tot_rev:,.0f}")
    cr2.metric("Total OPEX & Cost", f"SAR {t_opex:,.0f}")
    cr3.metric("Net Profit", f"SAR {n_prof:,.0f}")
    cr4.metric("Payback Period", f"{pbk:.1f} Years")
    st.info(f"ℹ️ Total Cost includes Annual Depreciation of SAR {ann_dep:,.0f}")
    
    fig_pie = px.pie(
        names=["Plastics", "Chemicals", "Consumables", "HR & Admin", "Power", "Depreciation", "Net Profit"],
        values=[plastic_annual_cost, chem_annual_cost, a_cons, a_hr, t_pwr, ann_dep, n_prof if n_prof > 0 else 0],
        title="📊 Revenue Breakdown & Cost Allocation (SAR)", hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        wb = w.book
        
        title_fmt = wb.add_format({'bold': True, 'font_size': 16, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#002060', 'font_color': 'white', 'border': 1})
        head_fmt = wb.add_format({'bold': True, 'bg_color': '#4F81BD', 'font_color': 'white', 'border': 1, 'align': 'left'})
        sub_head_fmt = wb.add_format({'bold': True, 'bg_color': '#DCE6F1', 'border': 1, 'align': 'left'})
        txt_fmt = wb.add_format({'border': 1, 'align': 'left'})
        num_fmt = wb.add_format({'num_format': '#,##0', 'border': 1, 'align': 'right'})
        cur_fmt = wb.add_format({'num_format': '#,##0.00', 'border': 1, 'align': 'right'})
        pct_fmt = wb.add_format({'num_format': '0.00%', 'border': 1, 'align': 'right'})
        highlight_fmt = wb.add_format({'bold': True, 'bg_color': '#E2EFDA', 'num_format': '#,##0.00', 'border': 1, 'align': 'right'})
        profit_fmt = wb.add_format({'bold': True, 'bg_color': '#C6EFCE', 'font_color': '#006100', 'num_format': '#,##0.00', 'border': 1, 'align': 'right'})
        
        ws = wb.add_worksheet('Executive Financial Summary')
        ws.set_column('A:A', 40) 
        ws.set_column('B:H', 15) 
        ws.hide_gridlines(2) 
        
        ws.merge_range('A1:H2', 'Royan Plant - Executive Financial & Operational Summary', title_fmt)
        
        current_row = 3
        
        ws.write(current_row, 0, '1. CAPITAL INVESTMENT (الاستثمار والأصول)', head_fmt)
        ws.write(current_row, 1, 'SAR', head_fmt); current_row += 1
        
        capex_items = [
            ('Extruder Line', e_pr), ('Flexo CI Printing Line', f_pr), ('Lamination Line', l_pr),
            ('Slitter Machine', s_pr), ('Bag Making Machines', b_pr), ('Building (Hangar)', hng_pr),
            ('Chiller & Utilities', chl_pr + cmp_pr)
        ]
        start_capex = current_row + 1
        for name, val in capex_items:
            ws.write(current_row, 0, name, txt_fmt)
            ws.write(current_row, 1, val, cur_fmt)
            current_row += 1
            
        wc_req = ((t_opex - ann_dep) / 12.0) * 3
        ws.write(current_row, 0, 'Working Capital (كاش لتشغيل 3 أشهر)', sub_head_fmt)
        ws.write(current_row, 1, wc_req, cur_fmt); current_row += 1
        
        ws.write(current_row, 0, 'TOTAL PROJECT INVESTMENT (إجمالي الاستثمار)', sub_head_fmt)
        capex_total_row_excel = current_row + 1
        ws.write_formula(current_row, 1, f'=SUM(B{start_capex}:B{current_row})', highlight_fmt)
        current_row += 2
        
        ws.write(current_row, 0, '2. RAW MATERIALS PRICING (أسعار المواد)', head_fmt)
        ws.write(current_row, 1, 'SAR / Kg', head_fmt); current_row += 1
        
        mat_items = [('BOPP', p_b), ('PET', p_pt), ('PE', p_pe), ('ALU', p_al), ('Ink', ink_p), ('Solvent', solv_p), ('Adhesive', adh_p)]
        for name, val in mat_items:
            ws.write(current_row, 0, name, txt_fmt)
            ws.write(current_row, 1, val, cur_fmt)
            current_row += 1
        current_row += 1

        ws.write(current_row, 0, '3. ANNUAL OPERATING EXPENSES (مصاريف التشغيل السنوية)', head_fmt)
        ws.write(current_row, 1, 'SAR / Year', head_fmt); current_row += 1
        
        opex_start = current_row + 1
        opex_items = [
            ('Raw Materials (Plastics Only)', plastic_annual_cost), 
            ('Chemicals (Ink, Solv, Glue)', chem_annual_cost),
            ('Consumables & Plates', a_cons),
            ('Power Consumption', t_pwr),
            ('Payroll & HR', payroll * 12.0),
            ('Admin & General Expenses', adm_exp * 12.0),
            ('Annual Depreciation (إهلاك دفتري)', ann_dep)
        ]
        for name, val in opex_items:
            ws.write(current_row, 0, name, txt_fmt)
            ws.write(current_row, 1, val, cur_fmt)
            current_row += 1
            
        ws.write(current_row, 0, 'TOTAL ANNUAL OPEX (إجمالي المصاريف)', sub_head_fmt)
        opex_total_row_excel = current_row + 1
        ws.write_formula(current_row, 1, f'=SUM(B{opex_start}:B{current_row})', highlight_fmt)
        current_row += 2

        ws.write(current_row, 0, '4. PRICING & MARGINS PER PRODUCT (التسعير وهوامش الربح)', head_fmt)
        ws.write_row(current_row, 1, ['Target Tons', 'Mat. Cost/Kg', 'Mfg Cost/Kg', 'Total Cost/Kg', 'Actual Price', 'Net Profit/Kg', 'Margin %'], head_fmt)
        current_row += 1
        
        for d in dets:
            ws.write(current_row, 0, d['Product'], txt_fmt)
            ws.write(current_row, 1, d['Tons'], num_fmt)               
            ws.write(current_row, 2, d['Mat. Cost/Kg'], cur_fmt)      
            ws.write(current_row, 3, d['Mfg Cost/Kg'], cur_fmt)      
            ws.write(current_row, 4, d['Total Cost/Kg'], cur_fmt)      
            ws.write(current_row, 5, d['Sell Price'], highlight_fmt) 
            ws.write(current_row, 6, d['Profit/Kg'], cur_fmt) 
            ws.write(current_row, 7, d['Margin %'], pct_fmt) 
            current_row += 1
        current_row += 1

        ws.write(current_row, 0, '5. FINANCIAL SUMMARY (الخلاصة المالية السنوية)', head_fmt)
        ws.write(current_row, 1, 'SAR', head_fmt); current_row += 1
        
        ws.write(current_row, 0, 'Gross Annual Revenue (إجمالي الإيرادات)', sub_head_fmt)
        ws.write(current_row, 1, tot_rev, cur_fmt)
        gross_rev_row_excel = current_row + 1
        current_row += 1
        
        ws.write(current_row, 0, 'Total Annual Costs (إجمالي التكاليف)', sub_head_fmt)
        ws.write_formula(current_row, 1, f'=B{opex_total_row_excel}', cur_fmt)
        total_cost_row_excel = current_row + 1
        current_row += 1
        
        ws.write(current_row, 0, 'NET ANNUAL PROFIT (صافي الربح)', sub_head_fmt)
        ws.write_formula(current_row, 1, f'=B{gross_rev_row_excel}-B{total_cost_row_excel}', profit_fmt)
        net_profit_row_excel = current_row + 1
        current_row += 1
        
        ws.write(current_row, 0, 'Return on Investment (ROI)', txt_fmt)
        ws.write_formula(current_row, 1, f'=B{net_profit_row_excel}/B{capex_total_row_excel}', pct_fmt); current_row += 1 
        
        ws.write(current_row, 0, 'Payback Period (Years)', txt_fmt)
        ws.write_formula(current_row, 1, f'=B{capex_total_row_excel}/B{net_profit_row_excel}', cur_fmt)

    st.download_button("📥 Download Executive Summary Excel", buf.getvalue(), "Royan_Executive_Summary.xlsx", "application/vnd.ms-excel", use_container_width=True)

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
    
    sc = next((i["Total Cost/Kg"] for i in dets if i["Product"] == sr), 0)
    sg = next((i["GSM"] for i in dets if i["Product"] == sr), 0) # 🌟 يعمل هنا بنجاح تام
    
    mp = cq1.number_input("Margin %", 5, 100, 20)
    if st.button("Generate Offer"):
        fp = sc * (1.0 + (mp/100.0))
        st.info(f"**To:** {cn}\n\n**Product:** {sr} ({sg:,.1f} g/m²)\n\n**Price/Kg:** SAR {fp:,.2f}\n\n*Waheed Waleed Malik, Royan*")
