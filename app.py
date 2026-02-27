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
        "BOPP": {"p": p_b, "d": d_b}, "PET": {"p": p_pt, "d": d_pt}, "ALU": {"p": p_al, "d": d_al},
        "PE Lam": {"p": p_pe_lam, "d": d_pe}, "PE Shrink": {"p": p_pe_shrk, "d": d_pe},
        "PE Bag": {"p": p_pe_bag, "d": d_pe}, "None": {"p": 0.0, "d": 0.0}
    }
    st.markdown("---")
    ci1, ci2, ci3 = st.columns(3)
    ink_p, solv_p, adh_p = ci1.number_input("Ink/Kg", 14.0), ci2.number_input("Solvent/Kg", 6.0), ci3.number_input("Adhesive/Kg", 12.0)

# --- TAB 2 ---
with tabs[1]:
    cw1, cw2, cw3 = st.columns(3)
    d_yr, s_day, h_sh = cw1.number_input("Days/Yr", 300), cw1.number_input("Shifts/Day", 2), cw1.number_input("Hrs/Shift", 12)
    j_mo, c_hrs, kw_p = cw2.number_input("Jobs/Mo", 75), cw2.number_input("C.O. Hrs", 2.0), cw3.number_input("SAR/kWh", 0.18)
    net_hrs = (d_yr * s_day * h_sh) - (j_mo * 12 * c_hrs)
    st.success(f"✅ Net Running Hours / Year: {net_hrs:,.0f}")
    
    st.markdown("### 1. Machine Parameters")
    m1, m2, m3 = st.columns(3)
    with m1:
        e_kg, e_kw, e_pr = st.number_input("Extruder Kg/h", 500.0), st.number_input("Extruder kW", 300.0), st.number_input("Extruder CAPEX", 5000000.0)
        e_tons = (e_kg * net_hrs) / 1000.0
    with m2:
        f_s, f_w, f_e = st.number_input("Flexo Speed", 350.0), st.number_input("Flexo Width", 1.0), st.slider("Flexo Eff%", 40, 100, 80)
        f_k, f_pr = st.number_input("Flexo kW", 150.0), st.number_input("Flexo CAPEX", 8000000.0)
        f_lm_max = net_hrs * 60.0 * f_s * (f_e/100.0)
    with m3:
        l_s, l_w, l_e = st.number_input("Lam Speed", 450.0), st.number_input("Lam Width", 1.0), st.slider("Lam Eff%", 40, 100, 75)
        l_k, l_pr = st.number_input("Lam kW", 80.0), st.number_input("Lam CAPEX", 1200000.0)
        l_lm_max = net_hrs * 60.0 * l_s * (l_e/100.0)
        
    m4, m5 = st.columns(2)
    with m4:
        s_s, s_w, s_e = st.number_input("Slit Speed", 400.0), st.number_input("Slit Width", 1.0), st.slider("Slit Eff%", 40, 100, 50)
        s_k, s_pr = st.number_input("Slit kW", 40.0), st.number_input("Slit CAPEX", 800000.0)
        s_lm_max = net_hrs * 60.0 * s_s * (s_e/100.0)
    with m5:
        b_q, b_s, b_e = st.number_input("Bag Mach Qty", 5), st.number_input("Bag Speed m/m", 75.0), st.slider("Bag Eff%", 40, 100, 85)
        b_k, b_pr = st.number_input("Bag kW Total", 75.0), st.number_input("Bag CAPEX", 500000.0)
        b_lm_max = net_hrs * 60.0 * b_s * b_q * (b_e/100.0)

    st.markdown("### 2. Utilities")
    u1, u2, u3 = st.columns(3)
    hng_pr, hng_dep_y = u1.number_input("Hangar CAPEX", 4000000.0), u1.number_input("Hangar Depr Yrs", 25.0)
    chl_k, chl_pr, chl_dep_y = u2.number_input("Chiller kW", 50.0), u2.number_input("Chiller CAPEX", 500000.0), u2.number_input("Chiller Depr Yrs", 10.0)
    cmp_k, cmp_pr, cmp_dep_y = u3.number_input("Compressor kW", 30.0), u3.number_input("Compressor CAPEX", 250000.0), u3.number_input("Comp. Depr Yrs", 10.0)
    
    chl_pc = net_hrs * chl_k * kw_p
    cmp_pc = net_hrs * cmp_k * kw_p
    
    mac_dep_y = st.number_input("Machines Depreciation Yrs", 10.0)
    dep_e, dep_f, dep_l, dep_s, dep_b = e_pr/mac_dep_y, f_pr/mac_dep_y, l_pr/mac_dep_y, s_pr/mac_dep_y, b_pr/mac_dep_y
    ann_dep = dep_e + dep_f + dep_l + dep_s + dep_b + (hng_pr/hng_dep_y) + (chl_pr/chl_dep_y) + (cmp_pr/cmp_dep_y)
    t_capex = e_pr + f_pr + l_pr + s_pr + b_pr + hng_pr + chl_pr + cmp_pr

# --- TAB 3 ---
with tabs[2]:
    st.subheader("🛠️ Consumables")
    cc1, cc2, cc3 = st.columns(3)
    pl_pr, pl_lf = cc1.number_input("Plate SAR", 2500.0), cc1.number_input("Plate Life (m)", 400000.0)
    an_pr, an_lf = cc1.number_input("Anilox SAR", 15000.0), cc1.number_input("Anilox Life(M)", 200.0)
    bl_pr, bl_qt, bl_lf = cc2.number_input("Blade SAR/m", 12.0), cc2.number_input("Blade m/Job", 21.0), cc2.number_input("Blade Life(m)", 33000.0)
    # 🌟 التعديل: إضافة es_pr الذي تسبب في الخطأ
    es_pr = cc2.number_input("EndSeal SAR", 150.0)
    tp_pr, tp_qt = cc3.number_input("Tape SAR/m²", 85.0), cc3.number_input("Tape m²/Job", 6.0)

# --- TAB 4 ---
with tabs[3]:
    st.header("HR & OPEX")
    ch1, ch2, ch3, ch4 = st.columns(4)
    payroll = (ch1.number_input("Eng Qty", 3)*ch1.number_input("Eng Sal", 8000)) + (ch2.number_input("Op Qty", 6)*ch2.number_input("Op Sal", 4500)) + (ch3.number_input("Wrk Qty", 10)*ch3.number_input("Wrk Sal", 2500)) + (ch4.number_input("Adm Qty", 5)*ch4.number_input("Adm Sal", 8000)) + (st.number_input("Saudi Qty", 5)*st.number_input("Saudi Sal", 4000))
    adm_exp = st.number_input("Monthly Admin Exp", 40000)

# --- TAB 5 ---
with tabs[4]:
    st.markdown("### ⚙️ 1. Global Production Settings")
    t_tons = st.number_input("🎯 Target Tons", min_value=2500.0, value=2500.0, step=100.0)
    c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    std_w, w_ink, i_loss, a_gsm = c_s1.number_input("Web Width (m)", 1.0), c_s2.number_input("Wet Ink GSM", 5.0), c_s3.number_input("Ink Loss%", 40.0), c_s4.number_input("Adh GSM", 1.8)
    d_ink = w_ink * (1.0 - (i_loss/100.0))
    
    st.markdown("### 📋 2. Product Portfolio")
    init_data = [
        {"Product": "1 Lyr", "Print": True, "L1": "BOPP", "M1": 40, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 20, "Price": 13.0},
        {"Product": "2 Lyr", "Print": True, "L1": "BOPP", "M1": 20, "L2": "BOPP", "M2": 20, "L3": "None", "M3": 0, "Mix%": 25, "Price": 13.0},
        {"Product": "3 Lyr", "Print": True, "L1": "PET", "M1": 12, "L2": "ALU", "M2": 7, "L3": "PE Lam", "M3": 50, "Mix%": 5, "Price": 15.0},
        {"Product": "Shrink Plain", "Print": False, "L1": "PE Shrink", "M1": 40, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 30, "Price": 5.0},
        {"Product": "Printed Shop. Bag", "Print": True, "L1": "PE Bag", "M1": 60, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 20, "Price": 10.0}
    ]
    df_rec = st.data_editor(pd.DataFrame(init_data), num_rows="dynamic", use_container_width=True)
    
    w_gsm, t_ink_k, t_slv_k, t_adh_k, t_flexo_lm_req, t_lam_sqm_req = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    tons_ext, tons_flx, tons_lam, tons_slt, tons_bag = 0.0, 0.0, 0.0, 0.0, 0.0
    t_slt_lm_req, t_bag_lm_req, temp_dets = 0.0, 0.0, []
    
    for _, r in df_rec.iterrows():
        p_name, is_printed, r_ton = str(r["Product"]).lower(), r.get("Print", True), t_tons*(r["Mix%"]/100.0)
        lp = (1 if r["M2"] > 0 and str(r["L2"]) != "None" else 0) + (1 if r["M3"] > 0 and str(r["L3"]) != "None" else 0)
        u_ext = any("pe" in str(r[l]).lower() for l in ["L1","L2","L3"])
        u_slt = any(x in p_name for x in ["1 lyr","2 lyr","3 lyr","bopp"])
        u_bag = "bag" in p_name
        
        if u_ext: tons_ext += r_ton
        if is_printed: tons_flx += r_ton
        if lp > 0: tons_lam += (r_ton * lp)
        if u_slt: tons_slt += r_ton
        if u_bag: tons_bag += r_ton
        
        g1, g2, g3 = r["M1"]*mat_db[str(r["L1"])]["d"], r["M2"]*mat_db[str(r["L2"])]["d"], r["M3"]*mat_db[str(r["L3"])]["d"]
        ag, tg = lp * a_gsm, g1 + g2 + g3 + (lp*a_gsm) + (d_ink if is_printed else 0)
        c_mat_kg = ((g1/1000.0*mat_db[str(r["L1"])]["p"]) + (g2/1000.0*mat_db[str(r["L2"])]["p"]) + (g3/1000.0*mat_db[str(r["L3"])]["p"]) + (ag/1000.0*adh_p) + (w_ink/1000.0*ink_p if is_printed else 0) + (w_ink*0.5/1000.0*solv_p if is_printed else 0))/(tg/1000.0) if tg>0 else 0
        
        l_len = 0.0
        if tg > 0:
            sq = (r_ton*1000000.0)/tg
            if std_w > 0: l_len = sq/std_w
            if is_printed: t_flexo_lm_req += l_len; t_ink_k += (sq*w_ink)/1000.0; t_slv_k += (sq*w_ink*0.5)/1000.0
            if lp > 0: t_lam_sqm_req += (sq*lp)
            if u_slt: t_slt_lm_req += l_len
            if u_bag: t_bag_lm_req += l_len
        w_gsm += tg*(r["Mix%"]/100.0)
        temp_dets.append({"Product":r["Product"],"Printed":is_printed,"Tons":r_ton,"Length(m)":l_len,"GSM":tg,"MatCost":c_mat_kg,"Price":r["Price"],"u_ext":u_ext,"lp":lp,"u_slt":u_slt,"u_bag":u_bag})

    ln_m = (t_tons*1000.0/w_gsm*1000.0)/std_w if w_gsm>0 and std_w>0 else 0
    a_cons = ((ln_m/(an_lf*1000000.0))*an_pr*8.0 if an_lf>0 else 0) + ((ln_m/bl_lf)*(bl_qt*bl_pr + es_pr*8.0) if bl_lf>0 else 0) + ((t_flexo_lm_req/pl_lf)*pl_pr if pl_lf>0 else 0) + ((j_mo*12.0)*tp_qt*tp_pr)
    
    req_e_h, req_f_h, req_l_h = (tons_ext*1000.0)/e_kg if e_kg>0 else 0, t_flexo_lm_req/(f_s*60.0*(f_e/100.0)) if f_s*f_e>0 else 0, (t_lam_sqm_req/std_w)/(l_s*60.0*(l_e/100.0)) if l_s*l_e*std_w>0 else 0
    req_s_h, req_b_h = t_slt_lm_req/(s_s*60.0*(s_e/100.0)) if s_s*s_e>0 else 0, t_bag_lm_req/(b_s*60.0*b_q*(b_e/100.0)) if b_s*b_q*b_e>0 else 0
    
    p_e, p_f, p_l, p_s, p_b = req_e_h*e_kw*kw_p + dep_e, req_f_h*f_k*kw_p + dep_f + a_cons, req_l_h*l_k*kw_p + dep_l, req_s_h*s_k*kw_p + dep_s, req_b_h*b_k*kw_p + dep_b
    p_o = (payroll + adm_exp)*12.0 + (hng_pr/25.0) + (chl_pr/10.0) + (cmp_pr/10.0) + (net_hrs*(chl_k+cmp_k)*kw_p)
    r_e, r_f, r_l, r_s, r_b, r_o = p_e/(tons_ext*1000) if tons_ext>0 else 0, p_f/(tons_flx*1000) if tons_flx>0 else 0, p_l/(tons_lam*1000) if tons_lam>0 else 0, p_s/(tons_slt*1000) if tons_slt>0 else 0, p_b/(tons_bag*1000) if tons_bag>0 else 0, p_o/(t_tons*1000) if t_tons>0 else 0

    dets = []
    for d in temp_dets:
        c_e, c_f, c_l, c_s, c_b = (r_e if d["u_ext"] else 0), (r_f if d["Printed"] else 0), (r_l*d["lp"]), (r_s if d["u_slt"] else 0), (r_b if d["u_bag"] else 0)
        t_m = c_e + c_f + c_l + c_s + c_b + r_o
        dets.append({"Product":d["Product"],"Tons":d["Tons"],"Length(m)":d["Length(m)"],"MatCost":d["MatCost"],"Extrdr":c_e,"Flexo":c_f,"Lam":c_l,"Slit":c_s,"BagMk":c_b,"OH":r_o,"TotalCost":d["MatCost"]+t_m,"Price":d["Price"],"Profit":d["Price"]-(d["MatCost"]+t_m),"GSM":d["GSM"]})
    
    st.markdown("### 📊 3. Full Breakdown (SAR/Kg)")
    df_f = pd.DataFrame(dets)
    num_cols = ["Tons", "MatCost", "Extrdr", "Flexo", "Lam", "Slit", "BagMk", "OH", "TotalCost", "Price", "Profit"]
    st.dataframe(df_f[["Product"] + num_cols].style.format({c: "{:,.2f}" for c in num_cols}), use_container_width=True)

# --- TAB 6 & 7 ---
total_rev = sum(d['Price']*d['Tons']*1000 for d in dets)
total_rm_cost = sum(d['MatCost']*d['Tons']*1000 for d in dets)
total_operating_costs = p_e + p_f + p_l + p_s + p_b + p_o
net_profit_annual = total_rev - (total_rm_cost + total_operating_costs)

with tabs[5]:
    st.markdown("### 📈 Plant Financials")
    f1, f2, f3 = st.columns(3)
    f1.metric("Gross Revenue", f"SAR {total_rev:,.0f}")
    f2.metric("Total OPEX & Materials", f"SAR {total_rm_cost + total_operating_costs:,.0f}")
    f3.metric("Net Profit", f"SAR {net_profit_annual:,.0f}")
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        wb = w.book
        title_f = wb.add_format({'bold':True,'font_size':14,'bg_color':'#002060','font_color':'white','align':'center'})
        head_f = wb.add_format({'bold':True,'bg_color':'#4F81BD','font_color':'white','border':1})
        num_f = wb.add_format({'num_format':'#,##0.00','border':1})
        ws = wb.add_worksheet('Summary')
        ws.merge_range('A1:G1', 'Royan Plant Financial Summary', title_f)
        ws.write_row(2, 0, ['Investment', t_capex, 'Revenue', total_rev, 'Net Profit', net_profit_annual], head_f)
        ws.write(5, 0, 'Detailed Product Analysis', head_f)
        ws.write_row(6, 0, ['Product','Tons','Mat Cost','Mfg Cost','Total Cost','Price','Margin %'], head_f)
        for i, d in enumerate(dets):
            ws.write_row(7+i, 0, [d['Product'], d['Tons'], d['MatCost'], d['TotalCost']-d['MatCost'], d['TotalCost'], d['Price'], (d['Profit']/d['Price'] if d['Price']>0 else 0)], num_f)
    st.download_button("📥 Download Summary Excel", buf.getvalue(), "Royan_Summary.xlsx", use_container_width=True)

with tabs[6]:
    st.header("Commercial Offer")
    sr = st.selectbox("Select Product", [d['Product'] for d in dets])
    row = next(i for i in dets if i["Product"] == sr)
    if st.button("Generate Offer"):
        st.info(f"**Customer:** Valued Client\n\n**Product:** {sr} ({row['GSM']:,.1f} g/m²)\n\n**Price:** SAR {row['Price']:,.2f}/Kg\n\n*Waheed Waleed Malik, Royan*")
