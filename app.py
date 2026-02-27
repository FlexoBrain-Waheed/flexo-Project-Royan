import streamlit as st, pandas as pd, io, plotly.express as px

st.set_page_config(page_title="Royan Plant", layout="wide")
st.title("🏭 Royan Smart Plant Simulator")

tabs = st.tabs(["1. Materials", "2. Production & Chart", "3. Consumables", "4. HR & OPEX", "5. Recipes", "6. P&L", "7. Commercial"])

# --- TAB 1: Materials ---
with tabs[0]:
    st.subheader("📦 Raw Materials Pricing")
    c1, c2, c3 = st.columns(3)
    p_b = c1.number_input("BOPP SAR", value=6.0, step=0.1)
    d_b = c1.number_input("BOPP Den", value=0.91, step=0.01)
    p_pt = c2.number_input("PET SAR", value=6.3, step=0.1)
    d_pt = c2.number_input("PET Den", value=1.40, step=0.01)
    p_al = c3.number_input("ALU SAR", value=18.0, step=0.1)
    d_al = c3.number_input("ALU Den", value=2.70, step=0.01)
    
    st.markdown("#### 🧪 PE Extrusion Grades")
    c4, c5, c6, c7 = st.columns(4)
    p_pe_lam = c4.number_input("PE Lam SAR (3 Lyr)", value=4.0, step=0.1)
    p_pe_shrk = c5.number_input("PE Shrink SAR", value=3.4, step=0.1)
    p_pe_bag = c6.number_input("PE Bag SAR", value=3.0, step=0.1)
    d_pe = c7.number_input("PE Density (All)", value=0.92, step=0.01)
    
    mat_db = {
        "BOPP": {"p": p_b, "d": d_b}, "PET": {"p": p_pt, "d": d_pt}, "ALU": {"p": p_al, "d": d_al},
        "PE Lam": {"p": p_pe_lam, "d": d_pe}, "PE Shrink": {"p": p_pe_shrk, "d": d_pe},
        "PE Bag": {"p": p_pe_bag, "d": d_pe}, "None": {"p": 0.0, "d": 0.0}
    }
    st.markdown("---")
    ci1, ci2, ci3 = st.columns(3)
    ink_p = ci1.number_input("Ink/Kg", value=14.0, step=0.5)
    solv_p = ci2.number_input("Solvent/Kg", value=6.0, step=0.5)
    adh_p = ci3.number_input("Adhesive/Kg", value=12.0, step=0.5)

# --- TAB 2: Production ---
with tabs[1]:
    cw1, cw2, cw3 = st.columns(3)
    d_yr = cw1.number_input("Days/Yr", value=300, step=1)
    s_day = cw1.number_input("Shifts/Day", value=2, step=1)
    h_sh = cw1.number_input("Hrs/Shift", value=12, step=1)
    j_mo = cw2.number_input("Jobs/Mo", value=75, step=1)
    c_hrs = cw2.number_input("C.O. Hrs", value=2.0, step=0.5)
    kw_p = cw3.number_input("SAR/kWh", value=0.18, step=0.01)
    net_hrs = (d_yr * s_day * h_sh) - (j_mo * 12 * c_hrs)
    st.success(f"✅ Net Running Hours / Year: {net_hrs:,.0f}")
    
    st.markdown("### 1. Machine Parameters")
    m1, m2, m3 = st.columns(3)
    with m1:
        e_kg = st.number_input("Extruder Kg/h", value=500.0, step=10.0)
        e_kw = st.number_input("Extruder kW", value=300.0, step=5.0)
        e_pr = st.number_input("Extruder CAPEX", value=5000000.0, step=50000.0)
    with m2:
        f_s = st.number_input("Flexo Speed", value=350.0, step=10.0)
        f_w = st.number_input("Flexo Width", value=1.0, step=0.1)
        f_e = st.slider("Flexo Eff%", 1, 100, 80)
        f_k = st.number_input("Flexo kW", value=150.0, step=5.0)
        f_pr = st.number_input("Flexo CAPEX", value=8000000.0, step=50000.0)
    with m3:
        l_s = st.number_input("Lam Speed", value=450.0, step=10.0)
        l_w = st.number_input("Lam Width", value=1.0, step=0.1)
        l_e = st.slider("Lam Eff%", 1, 100, 75)
        l_k = st.number_input("Lam kW", value=80.0, step=5.0)
        l_pr = st.number_input("Lam CAPEX", value=1200000.0, step=50000.0)
    m4, m5 = st.columns(2)
    with m4:
        s_s = st.number_input("Slit Speed", value=400.0, step=10.0)
        s_w = st.number_input("Slit Width", value=1.0, step=0.1)
        s_e = st.slider("Slit Eff%", 1, 100, 50)
        s_k = st.number_input("Slit kW", value=40.0, step=5.0)
        s_pr = st.number_input("Slit CAPEX", value=800000.0, step=50000.0)
    with m5:
        b_q = st.number_input("Bag Mach Qty", value=5, step=1)
        b_s = st.number_input("Bag Speed m/m", value=75.0, step=5.0)
        b_e = st.slider("Bag Eff%", 1, 100, 85)
        b_k = st.number_input("Bag kW Total", value=75.0, step=5.0)
        b_pr = st.number_input("Bag CAPEX", value=500000.0, step=50000.0)

    st.markdown("### 2. Utilities")
    u1, u2, u3 = st.columns(3)
    hng_pr = u1.number_input("Hangar CAPEX", value=4000000.0, step=50000.0)
    hng_dep_y = u1.number_input("Hangar Depr Yrs", value=25.0, step=1.0)
    chl_k = u2.number_input("Chiller kW", value=50.0, step=5.0)
    chl_pr = u2.number_input("Chiller CAPEX", value=500000.0, step=10000.0)
    chl_dep_y = u2.number_input("Chiller Depr Yrs", value=10.0, step=1.0)
    cmp_k = u3.number_input("Compressor kW", value=30.0, step=5.0)
    cmp_pr = u3.number_input("Compressor CAPEX", value=250000.0, step=10000.0)
    cmp_dep_y = u3.number_input("Comp. Depr Yrs", value=10.0, step=1.0)
    
    chl_pc = net_hrs * chl_k * kw_p
    cmp_pc = net_hrs * cmp_k * kw_p
    
    mac_dep_y = st.number_input("Machines Depreciation Yrs", value=10.0, step=1.0)
    dep_e, dep_f, dep_l, dep_s, dep_b = e_pr/mac_dep_y, f_pr/mac_dep_y, l_pr/mac_dep_y, s_pr/mac_dep_y, b_pr/mac_dep_y
    ann_dep = dep_e + dep_f + dep_l + dep_s + dep_b + (hng_pr/hng_dep_y) + (chl_pr/chl_dep_y) + (cmp_pr/cmp_dep_y)
    t_capex = e_pr + f_pr + l_pr + s_pr + b_pr + hng_pr + chl_pr + cmp_pr

# --- TAB 3: Consumables ---
with tabs[2]:
    st.subheader("🛠️ Consumables")
    cc1, cc2, cc3 = st.columns(3)
    pl_pr = cc1.number_input("Plate SAR", value=2500.0, step=100.0)
    pl_lf = cc1.number_input("Plate Life (m)", value=400000.0, step=10000.0)
    an_pr = cc1.number_input("Anilox SAR", value=15000.0, step=500.0)
    an_lf = cc1.number_input("Anilox Life(M)", value=200.0, step=10.0)
    bl_pr = cc2.number_input("Blade SAR/m", value=12.0, step=1.0)
    bl_qt = cc2.number_input("Blade m/Job", value=21.0, step=1.0)
    bl_lf = cc2.number_input("Blade Life(m)", value=33000.0, step=1000.0)
    es_pr = cc2.number_input("EndSeal SAR", value=150.0, step=10.0)
    tp_pr = cc3.number_input("Tape SAR/m²", value=85.0, step=5.0)
    tp_qt = cc3.number_input("Tape m²/Job", value=6.0, step=0.5)

# --- TAB 4: HR ---
with tabs[3]:
    st.header("HR & OPEX")
    ch1, ch2, ch3, ch4 = st.columns(4)
    payroll = (ch1.number_input("Eng Qty", value=3, step=1)*ch1.number_input("Eng Sal", value=8000, step=100)) + \
              (ch2.number_input("Op Qty", value=6, step=1)*ch2.number_input("Op Sal", value=4500, step=100)) + \
              (ch3.number_input("Wrk Qty", value=10, step=1)*ch3.number_input("Wrk Sal", value=2500, step=100)) + \
              (ch4.number_input("Adm Qty", value=5, step=1)*ch4.number_input("Adm Sal", value=8000, step=100)) + \
              (st.number_input("Saudi Qty", value=5, step=1)*st.number_input("Saudi Sal", value=4000, step=100))
    adm_exp = st.number_input("Monthly Admin Exp", value=40000, step=1000)

# --- TAB 5: Recipes ---
with tabs[4]:
    st.markdown("### ⚙️ 1. Global Production Settings")
    # 🌟 تم إلغاء الحد الأدنى 2500، الآن يقبل أي رقم
    t_tons = st.number_input("🎯 Target Tons", value=2500.0, step=100.0)
    c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    std_w = c_s1.number_input("Web Width (m)", value=1.0, step=0.1)
    w_ink = c_s2.number_input("Wet Ink GSM", value=5.0, step=0.1)
    i_loss = c_s3.number_input("Ink Loss%", value=40.0, step=1.0)
    a_gsm = c_s4.number_input("Adh GSM", value=1.8, step=0.1)
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
        
        g1 = r["M1"]*mat_db[str(r["L1"])]["d"]
        g2 = r["M2"]*mat_db[str(r["L2"])]["d"]
        g3 = r["M3"]*mat_db[str(r["L3"])]["d"]
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

# --- TAB 6 & 7: P&L & Commercial ---
total_rev = sum(d['Price']*d['Tons']*1000 for d in dets)
total_rm_cost = sum(d['MatCost']*d['Tons']*1000 for d in dets)
total_operating_costs = p_e + p_f + p_l + p_s + p_b + p_o
net_profit_annual = total_rev - (total_rm_cost + total_operating_costs)

with tabs[5]:
    st.markdown("### 📈 Plant Financials")
    f1, f2, f3 = st.columns(3)
    f1.metric("Gross Revenue", f"SAR {total_rev:,.0f}")
    f2.metric("Total Cost", f"SAR {total_rm_cost + total_operating_costs:,.0f}")
    f3.metric("Net Profit", f"SAR {net_profit_annual:,.0f}")
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        wb = w.book
        head_fmt = wb.add_format({'bold':True,'bg_color':'#4F81BD','font_color':'white','border':1})
        num_fmt = wb.add_format({'num_format':'#,##0.00','border':1})
        ws = wb.add_worksheet('Summary')
        ws.write_row(0, 0, ['Revenue', total_rev, 'Total Cost', total_rm_cost+total_operating_costs, 'Net Profit', net_profit_annual], head_fmt)
        ws.write_row(2, 0, ['Product','Tons','Mat Cost','Mfg Cost','Total Cost','Price','Margin %'], head_fmt)
        for i, d in enumerate(dets):
            ws.write_row(3+i, 0, [d['Product'], d['Tons'], d['MatCost'], d['TotalCost']-d['MatCost'], d['TotalCost'], d['Price'], (d['Profit']/d['Price'] if d['Price']>0 else 0)], num_fmt)
    st.download_button("📥 Download Summary Excel", buf.getvalue(), "Royan_Summary.xlsx", use_container_width=True)

with tabs[6]:
    st.header("Commercial Offer")
    sr = st.selectbox("Select Product", [d['Product'] for d in dets])
    row = next(i for i in dets if i["Product"] == sr)
    if st.button("Generate Offer"):
        st.info(f"**Customer:** Valued Client\n\n**Product:** {sr} ({row['GSM']:,.1f} g/m²)\n\n**Price:** SAR {row['Price']:,.2f}/Kg\n\n*Waheed Waleed Malik, Royan*")
