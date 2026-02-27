import streamlit as st, pandas as pd, io, plotly.express as px

st.set_page_config(page_title="Royan Plant", layout="wide")
st.title("🏭 Royan Smart Plant Simulator")

tabs = st.tabs(["1. Materials", "2. Production & Chart", "3. Consumables", "4. HR & OPEX", "5. Recipes", "6. P&L", "7. Commercial"])

# --- TAB 1 ---
with tabs[0]:
    st.subheader("📦 Raw Materials Pricing")
    c1, c2, c3 = st.columns(3)
    p_b, d_b = c1.number_input("BOPP SAR", 6.0), c1.number_input("BOPP Den", 0.91)
    p_pt, d_pt = c2.number_input("PET SAR", 6.3), c2.number_input("PET Den", 1.40)
    p_al, d_al = c3.number_input("ALU SAR", 18.0), c3.number_input("ALU Den", 2.70)
    
    st.markdown("#### 🧪 PE Extrusion Grades")
    c4, c5, c6, c7 = st.columns(4)
    p_pe_lam = c4.number_input("PE Lam SAR (3 Lyr)", 4.0)
    p_pe_shrk = c5.number_input("PE Shrink SAR", 3.4)
    p_pe_bag = c6.number_input("PE Bag SAR", 3.0)
    d_pe = c7.number_input("PE Density (All)", 0.92)
    
    mat_db = {
        "BOPP": {"p": p_b, "d": d_b}, 
        "PET": {"p": p_pt, "d": d_pt}, 
        "ALU": {"p": p_al, "d": d_al},
        "PE Lam": {"p": p_pe_lam, "d": d_pe},
        "PE Shrink": {"p": p_pe_shrk, "d": d_pe},
        "PE Bag": {"p": p_pe_bag, "d": d_pe},
        "None": {"p": 0.0, "d": 0.0}
    }
    
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
    with m2:
        f_s = st.number_input("Flexo Speed", 350.0)
        f_w = st.number_input("Flexo Width", 1.0)
        f_e = st.slider("Flexo Eff%", 40, 100, 80)
        f_k = st.number_input("Flexo kW", 150.0)
        f_pr = st.number_input("Flexo CAPEX", 8000000.0)
        f_lm = net_hrs * 60.0 * f_s * (f_e/100.0)
        f_sq = f_lm * f_w
    with m3:
        l_s = st.number_input("Lam Speed", 450.0)
        l_w = st.number_input("Lam Width", 1.0)
        l_e = st.slider("Lam Eff%", 40, 100, 75)
        l_k = st.number_input("Lam kW", 80.0)
        l_pr = st.number_input("Lam CAPEX", 1200000.0)
        l_lm = net_hrs * 60.0 * l_s * (l_e/100.0)
        l_sq = l_lm * l_w
        
    st.markdown("### 2. Finishing")
    m4, m5 = st.columns(2)
    with m4:
        s_s = st.number_input("Slit Speed", 400.0)
        s_w = st.number_input("Slit Width", 1.0)
        s_e = st.slider("Slit Eff%", 40, 100, 50)
        s_k = st.number_input("Slit kW", 40.0)
        s_pr = st.number_input("Slit CAPEX", 800000.0)
        s_lm = net_hrs * 60.0 * s_s * (s_e/100.0)
        s_sq = s_lm * s_w
    with m5:
        b_q = st.number_input("Mach Qty", 5)
        b_s = st.number_input("Bag Speed m/m", 75.0)
        b_e = st.slider("Bag Eff%", 40, 100, 85)
        b_k = st.number_input("Total kW (all)", 75.0)
        b_pr = st.number_input("Bag CAPEX", 500000.0)
        b_lm = net_hrs * 60.0 * b_s * b_q * (b_e/100.0)
        b_sq = b_lm * 1.0
        
    st.markdown("### 3. Utilities & Facilities")
    u1, u2, u3 = st.columns(3)
    with u1:
        st.subheader("Building (Hangar)")
        hng_pr = st.number_input("Hangar CAPEX", 4000000.0)
        hng_dep_y = st.number_input("Hangar Depr Yrs", 25.0)
    with u2:
        chl_k = st.number_input("Chiller kW", 50.0)
        chl_pr = st.number_input("Chiller CAPEX", 500000.0)
        chl_dep_y = st.number_input("Chiller Depr Yrs", 10.0)
        chl_pc = net_hrs * chl_k * kw_p
    with u3:
        cmp_k = st.number_input("Compressor kW", 30.0)
        cmp_pr = st.number_input("Compressor CAPEX", 250000.0)
        cmp_dep_y = st.number_input("Comp. Depr Yrs", 10.0)
        cmp_pc = net_hrs * cmp_k * kw_p

    c_cap1, c_cap2 = st.columns(2)
    mac_capex = e_pr + f_pr + l_pr + s_pr + b_pr
    t_capex = mac_capex + hng_pr + chl_pr + cmp_pr
    c_cap1.metric("Total CAPEX", f"SAR {t_capex:,.0f}")
    
    mac_dep_y = c_cap2.number_input("Machines Depreciation Yrs", 10.0)
    dep_e = e_pr / mac_dep_y if mac_dep_y > 0 else 0.0
    dep_f = f_pr / mac_dep_y if mac_dep_y > 0 else 0.0
    dep_l = l_pr / mac_dep_y if mac_dep_y > 0 else 0.0
    dep_s = s_pr / mac_dep_y if mac_dep_y > 0 else 0.0
    dep_b = b_pr / mac_dep_y if mac_dep_y > 0 else 0.0
    hng_dep = hng_pr / hng_dep_y if hng_dep_y > 0 else 0.0
    chl_dep = chl_pr / chl_dep_y if chl_dep_y > 0 else 0.0
    cmp_dep = cmp_pr / cmp_dep_y if cmp_dep_y > 0 else 0.0
    ann_dep = dep_e + dep_f + dep_l + dep_s + dep_b + hng_dep + chl_dep + cmp_dep

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
    eng_q, eng_s = ch1.number_input("Eng Qty", 3), ch1.number_input("Eng Sal", 8000)
    opr_q, opr_s = ch2.number_input("Op Qty", 6), ch2.number_input("Op Sal", 4500)
    wrk_q, wrk_s = ch3.number_input("Wrk Qty", 10), ch3.number_input("Wrk Sal", 2500)
    adm_q, adm_s = ch4.number_input("Adm Qty", 5), ch4.number_input("Adm Sal", 8000)
    sau_q, sau_s = st.number_input("Saudi Qty", 5), st.number_input("Saudi Sal", 4000)
    payroll = (eng_q*eng_s) + (opr_q*opr_s) + (wrk_q*wrk_s) + (adm_q*adm_s) + (sau_q*sau_s)
    adm_exp = st.number_input("Monthly Admin Exp", 40000)

# --- TAB 5 ---
with tabs[4]:
    st.markdown("### ⚙️ 1. Global Production Settings")
    c_set1, c_set2, c_set3, c_set4, c_set5 = st.columns(5)
    # 🌟 التعديل المطلوب: السماح بالبدء من 2500 طن
    t_tons = c_set1.number_input("🎯 Target Tons", min_value=2500.0, value=2500.0, step=100.0)
    std_w = c_set2.number_input("📏 Web Width (m)", 1.0)
    w_ink = c_set3.number_input("🎨 Wet Ink GSM", 5.0)
    i_loss = c_set4.number_input("💧 Ink Loss%", 40.0)
    a_gsm = c_set5.number_input("🍯 Adh GSM", 1.8)
    d_ink = w_ink * (1.0 - (i_loss / 100.0))
    
    st.markdown("### 📋 2. Product Portfolio (Recipes)")
    init_data = [
        {"Product": "1 Lyr", "Print": True, "L1": "BOPP", "M1": 40, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 20, "Price": 13.0},
        {"Product": "2 Lyr", "Print": True, "L1": "BOPP", "M1": 20, "L2": "BOPP", "M2": 20, "L3": "None", "M3": 0, "Mix%": 25, "Price": 13.0},
        {"Product": "3 Lyr", "Print": True, "L1": "PET", "M1": 12, "L2": "ALU", "M2": 7, "L3": "PE Lam", "M3": 50, "Mix%": 5, "Price": 15.0},
        {"Product": "Shrink Plain", "Print": False, "L1": "PE Shrink", "M1": 40, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 30, "Price": 5.0},
        {"Product": "Printed Shop. Bag", "Print": True, "L1": "PE Bag", "M1": 60, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 20, "Price": 10.0}
    ]
    df_rec = st.data_editor(pd.DataFrame(init_data), num_rows="dynamic", use_container_width=True)
    
    w_gsm, w_flexo_gsm, w_rmc, w_sp = 0.0, 0.0, 0.0, 0.0
    t_ink_k, t_slv_k, t_adh_k, t_pe_req_tons = 0.0, 0.0, 0.0, 0.0
    t_flexo_lm_req, t_lam_sqm_req, t_total_sqm_req = 0.0, 0.0, 0.0
    tons_ext, tons_flx, tons_lam, tons_slt, tons_bag = 0.0, 0.0, 0.0, 0.0, 0.0
    t_slt_lm_req, t_bag_lm_req = 0.0, 0.0
    temp_dets, m_nd = [], {}
    
    for _, r in df_rec.iterrows():
        p_name, is_printed = r["Product"].lower(), r.get("Print", True)
        r_ton = t_tons * (r["Mix%"]/100.0)
        lp = (1 if r["M2"] > 0 and str(r["L2"]) != "None" else 0) + (1 if r["M3"] > 0 and str(r["L3"]) != "None" else 0)
        use_ext = any("pe" in str(r[l]).lower() for l in ["L1", "L2", "L3"])
        use_flx, use_slt, use_bag = is_printed, any(x in p_name for x in ["1 lyr", "2 lyr", "3 lyr", "bopp"]), "bag" in p_name
        
        if use_ext: tons_ext += r_ton
        if use_flx: tons_flx += r_ton
        if lp > 0: tons_lam += (r_ton * lp)
        if use_slt: tons_slt += r_ton
        if use_bag: tons_bag += r_ton
        
        g1, g2, g3 = r["M1"]*mat_db[str(r["L1"])]["d"], r["M2"]*mat_db[str(r["L2"])]["d"], r["M3"]*mat_db[str(r["L3"])]["d"]
        pe_gsm = (g1 if "pe" in str(r["L1"]).lower() else 0) + (g2 if "pe" in str(r["L2"]).lower() else 0) + (g3 if "pe" in str(r["L3"]).lower() else 0)
        ag = lp * a_gsm
        tg = g1 + g2 + g3 + ag + (d_ink if is_printed else 0.0)
        
        c1, c2, c3 = (g1/1000.0)*mat_db[str(r["L1"])]["p"], (g2/1000.0)*mat_db[str(r["L2"])]["p"], (g3/1000.0)*mat_db[str(r["L3"])]["p"]
        ca, ci, cs = (ag/1000.0)*adh_p, ((w_ink/1000.0)*ink_p if is_printed else 0), ((w_ink*0.5/1000.0)*solv_p if is_printed else 0)
        c_mat_kg = (c1+c2+c3+ca+ci+cs)/(tg/1000.0) if tg > 0 else 0.0
        
        l_len = 0.0
        if tg > 0:
            sq = (r_ton * 1000000.0) / tg
            t_total_sqm_req += sq
            if std_w > 0: l_len = sq / std_w
            if is_printed:
                t_flexo_lm_req += l_len
                t_ink_k += (sq * w_ink) / 1000.0
                t_slv_k += (sq * w_ink * 0.5) / 1000.0
            if lp > 0: t_lam_sqm_req += (sq * lp)
            if use_slt: t_slt_lm_req += l_len
            if use_bag: t_bag_lm_req += l_len
            t_pe_req_tons += r_ton * (pe_gsm / tg)
            for lyr, mic in [("L1","M1"), ("L2","M2"), ("L3","M3")]:
                if str(r[lyr]) != "None" and r[mic] > 0:
                    mk = f"{r[lyr]} {r[mic]}µ"
                    m_nd[mk] = m_nd.get(mk, 0.0) + l_len
                    
        mr = r["Mix%"] / 100.0
        w_gsm, w_flexo_gsm, w_rmc, w_sp = w_gsm + tg*mr, w_flexo_gsm + (g1+d_ink if is_printed else 0)*mr, w_rmc + c_mat_kg*mr, w_sp + r["Price"]*mr
        temp_dets.append({"Product": r["Product"], "Printed": is_printed, "Tons": r_ton, "Length(m)": l_len, "GSM": tg, "Mat Cost/Kg": c_mat_kg, "Price": r["Price"], "u_ext": use_ext, "u_flx": use_flx, "lam_passes": lp, "u_slt": use_slt, "u_bag": use_bag})
        
    esm = t_tons * (1000.0/w_gsm) * 1000.0 if w_gsm > 0 else 0.0
    ln_m = esm / std_w if std_w > 0 else esm
    a_an, a_tp = (ln_m / (an_lf*1000000.0)) * an_pr * 8.0 if an_lf > 0 else 0.0, (j_mo * 12.0) * tp_qt * tp_pr
    a_bl_es = (ln_m / bl_lf) * (bl_qt*bl_pr + es_pr*8.0) if bl_lf > 0 else 0.0
    a_pl = (t_flexo_lm_req / pl_lf) * pl_pr if pl_lf > 0 else 0.0
    a_cons, a_hr = a_an + a_bl_es + a_pl + a_tp, (payroll + adm_exp) * 12.0
    
    req_e_hrs = (tons_ext * 1000.0) / e_kg if e_kg > 0 else 0.0
    req_f_hrs = t_flexo_lm_req / (f_s * 60.0 * (f_e/100.0)) if (f_s * f_e) > 0 else 0.0
    req_l_hrs = (t_lam_sqm_req / std_w) / (l_s * 60.0 * (l_e/100.0)) if (l_s * l_e * std_w) > 0 else 0.0
    req_s_hrs = t_slt_lm_req / (s_s * 60.0 * (s_e/100.0)) if (s_s * s_e) > 0 else 0.0
    req_b_hrs = t_bag_lm_req / (b_s * 60.0 * b_q * (b_e/100.0)) if (b_s * b_q * b_e) > 0 else 0.0
    
    act_e_pc, act_f_pc, act_l_pc, act_s_pc, act_b_pc = req_e_hrs*e_kw*kw_p, req_f_hrs*f_k*kw_p, req_l_hrs*l_k*kw_p, req_s_hrs*s_k*kw_p, req_b_hrs*b_k*kw_p
    pool_ext, pool_flx, pool_lam, pool_slt, pool_bag = act_e_pc + dep_e, act_f_pc + dep_f + a_cons, act_l_pc + dep_l, act_s_pc + dep_s, act_b_pc + dep_b
    pool_oh = a_hr + hng_dep + chl_dep + cmp_dep + chl_pc + cmp_pc 
    
    r_e, r_f, r_l, r_s, r_b, r_o = pool_ext/(tons_ext*1000) if tons_ext>0 else 0, pool_flx/(tons_flx*1000) if tons_flx>0 else 0, pool_lam/(tons_lam*1000) if tons_lam>0 else 0, pool_slt/(tons_slt*1000) if tons_slt>0 else 0, pool_bag/(tons_bag*1000) if tons_bag>0 else 0, pool_oh/(t_tons*1000) if t_tons>0 else 0

    dets = []
    for d in temp_dets:
        c_ext, c_flx, c_lam, c_slt, c_bag = (r_e if d["u_ext"] else 0), (r_f if d["u_flx"] else 0), (r_l * d["lam_passes"]), (r_s if d["u_slt"] else 0), (r_b if d["u_bag"] else 0)
        t_mfg = c_ext + c_flx + c_lam + c_slt + c_bag + r_o
        dets.append({"Product": d["Product"], "Printed": "✅" if d["Printed"] else "❌", "Tons": d["Tons"], "Mat Cost": d["Mat Cost/Kg"], "Extrdr": c_ext, "Flexo": c_flx, "Lam": c_lam, "Slit": c_slt, "BagMk": c_bag, "OH": r_o, "Total Cost": d["Mat Cost/Kg"] + t_mfg, "Price": d["Price"], "Profit": d["Price"]-(d["Mat Cost/Kg"]+t_mfg), "GSM": d["GSM"]})
        
    st.markdown("### 📊 3. Absorbed Costing & Margins")
    df_dets = pd.DataFrame(dets)
    st.dataframe(df_dets[["Product", "Tons", "Mat Cost", "Extrdr", "Flexo", "Lam", "Slit", "BagMk", "OH", "Total Cost", "Price", "Profit"]].style.format("{:,.2f}"), use_container_width=True)

# --- TAB 6 & 7 ---
tot_rev, a_rm = t_tons * 1000.0 * w_sp, t_tons * 1000.0 * w_rmc
t_pwr = act_e_pc + act_f_pc + act_l_pc + act_s_pc + act_b_pc + chl_pc + cmp_pc
t_opex = a_rm + pool_ext + pool_flx + pool_lam + pool_slt + pool_bag + pool_oh
n_prof = tot_rev - t_opex

with tabs[5]:
    st.markdown("### 📈 Plant Financials")
    c_f1, c_f2, c_f3 = st.columns(3)
    c_f1.metric("Gross Revenue", f"SAR {tot_rev:,.0f}")
    c_f2.metric("Total OPEX", f"SAR {t_opex:,.0f}")
    c_f3.metric("Net Profit", f"SAR {n_prof:,.0f}")
    
    # 🪄 EXCEL GENERATOR
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        wb = w.book
        title_fmt = wb.add_format({'bold': True, 'font_size': 16, 'bg_color': '#002060', 'font_color': 'white', 'border': 1, 'align': 'center'})
        head_fmt = wb.add_format({'bold': True, 'bg_color': '#4F81BD', 'font_color': 'white', 'border': 1})
        num_fmt = wb.add_format({'num_format': '#,##0.00', 'border': 1})
        
        ws = wb.add_worksheet('Royan Summary')
        ws.merge_range('A1:K2', 'Royan Plant Executive Summary', title_fmt)
        ws.write(3, 0, '1. INVESTMENT', head_fmt); ws.write(3, 1, t_capex, num_fmt)
        ws.write(4, 0, '2. ANNUAL REVENUE', head_fmt); ws.write(4, 1, tot_rev, num_fmt)
        ws.write(5, 0, '3. ANNUAL OPEX', head_fmt); ws.write(5, 1, t_opex, num_fmt)
        ws.write(6, 0, '4. NET PROFIT', head_fmt); ws.write(6, 1, n_prof, num_fmt)
        
        start_r = 9
        ws.write_row(start_r, 0, ['Product', 'Tons', 'Mat Cost', 'Mfg Cost', 'Total Cost', 'Sell Price', 'Margin %'], head_fmt)
        for i, d in enumerate(dets):
            m_pct = d['Profit']/d['Price'] if d['Price']>0 else 0
            ws.write_row(start_r+1+i, 0, [d['Product'], d['Tons'], d['Mat Cost'], d['Total Cost']-d['Mat Cost'], d['Total Cost'], d['Price'], m_pct], num_fmt)
            
    st.download_button("📥 Download Royan Executive Summary", buf.getvalue(), "Royan_Summary.xlsx", "application/vnd.ms-excel", use_container_width=True)

with tabs[6]:
    st.header("Commercial Offer")
    cq1, cq2 = st.columns(2)
    cn = cq1.text_input("Customer", "Valued Client")
    pl = [i["Product"] for i in dets]
    sr = cq2.selectbox("Product", pl)
    row = next(i for i in dets if i["Product"] == sr)
    if st.button("Generate Offer"):
        st.info(f"**To:** {cn}\n\n**Product:** {sr}\n\n**Price/Kg:** SAR {row['Price']:,.2f}\n\n*Waheed Waleed Malik, Royan*")
