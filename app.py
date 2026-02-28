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
    p_al = c3.number_input("ALU SAR", value=17.0, step=0.1)
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
        e_tons_cap = (e_kg * net_hrs) / 1000.0
    with m2:
        f_s = st.number_input("Flexo Speed", value=350.0, step=10.0)
        f_w = st.number_input("Flexo Width", value=1.0, step=0.1)
        f_e = st.slider("Flexo Eff%", 1, 100, 80)
        f_k = st.number_input("Flexo kW", value=150.0, step=5.0)
        f_pr = st.number_input("Flexo CAPEX", value=8000000.0, step=50000.0)
        f_lm_cap = net_hrs * 60.0 * f_s * (f_e/100.0)
    with m3:
        l_s = st.number_input("Lam Speed", value=450.0, step=10.0)
        l_w = st.number_input("Lam Width", value=1.0, step=0.1)
        l_e = st.slider("Lam Eff%", 1, 100, 75)
        l_k = st.number_input("Lam kW", value=80.0, step=5.0)
        l_pr = st.number_input("Lam CAPEX", value=1200000.0, step=50000.0)
        l_lm_cap = net_hrs * 60.0 * l_s * (l_e/100.0)
    m4, m5 = st.columns(2)
    with m4:
        s_s = st.number_input("Slit Speed", value=400.0, step=10.0)
        s_w = st.number_input("Slit Width", value=1.0, step=0.1)
        s_e = st.slider("Slit Eff%", 1, 100, 50)
        s_k = st.number_input("Slit kW", value=40.0, step=5.0)
        s_pr = st.number_input("Slit CAPEX", value=800000.0, step=50000.0)
        s_lm_cap = net_hrs * 60.0 * s_s * (s_e/100.0)
    with m5:
        b_q = st.number_input("Bag Mach Qty", value=5, step=1)
        b_s = st.number_input("Bag Speed m/m", value=75.0, step=5.0)
        b_e = st.slider("Bag Eff%", 1, 100, 85)
        b_k = st.number_input("Bag kW Total", value=75.0, step=5.0)
        b_pr = st.number_input("Bag CAPEX", value=500000.0, step=50000.0)
        b_lm_cap = net_hrs * 60.0 * b_s * b_q * (b_e/100.0)

    u1, u2, u3 = st.columns(3)
    hng_pr = u1.number_input("Hangar CAPEX", value=4000000.0, step=50000.0)
    hng_dep_y = u1.number_input("Hangar Depr Yrs", value=25.0, step=1.0)
    chl_k = u2.number_input("Chiller kW", value=50.0, step=5.0)
    chl_pr = u2.number_input("Chiller CAPEX", value=500000.0, step=10000.0)
    chl_dep_y = u2.number_input("Chiller Depr Yrs", value=10.0, step=1.0)
    cmp_k = u3.number_input("Compressor kW", value=30.0, step=5.0)
    cmp_pr = u3.number_input("Compressor CAPEX", value=250000.0, step=10000.0)
    cmp_dep_y = u3.number_input("Comp. Depr Yrs", value=10.0, step=1.0)
    
    mac_dep_y = st.number_input("Machines Depreciation Yrs", value=10.0, step=1.0)
    dep_e, dep_f, dep_l, dep_s, dep_b = e_pr/mac_dep_y, f_pr/mac_dep_y, l_pr/mac_dep_y, s_pr/mac_dep_y, b_pr/mac_dep_y
    ann_dep = dep_e + dep_f + dep_l + dep_s + dep_b + (hng_pr/hng_dep_y) + (chl_pr/chl_dep_y) + (cmp_pr/cmp_dep_y)
    t_capex = e_pr + f_pr + l_pr + s_pr + b_pr + hng_pr + chl_pr + cmp_pr

    st.markdown("### 📊 Capacity Check")
    chart_gsm = st.number_input("Avg GSM for Chart", value=40.0, step=1.0)
    df_cap = pd.DataFrame({
        "Machine": ["Extruder", "Flexo", "Lam", "Slitter", "BagMk"],
        "Max Tons": [(e_kg*net_hrs/1000), (f_lm_cap*f_w*chart_gsm/1000000), (l_lm_cap*l_w*chart_gsm/1000000), (s_lm_cap*s_w*chart_gsm/1000000), (b_lm_cap*chart_gsm/1000000)]
    })
    st.plotly_chart(px.bar(df_cap, x="Machine", y="Max Tons", color="Machine", text_auto='.0f'), use_container_width=True)

# --- TAB 3: Consumables ---
with tabs[2]:
    st.subheader("🛠️ Consumables")
    cc1, cc2, cc3 = st.columns(3)
    pl_pr = cc1.number_input("Plate SAR", value=2500.0, step=100.0)
    pl_lf = cc1.number_input("Plate Life(m)", value=400000.0, step=10000.0)
    an_pr = cc1.number_input("Anilox SAR", value=15000.0, step=500.0)
    an_lf = cc1.number_input("Anilox Life(M)", value=200.0, step=10.0)
    bl_pr = cc2.number_input("Blade SAR/m", value=12.0, step=1.0)
    bl_qt = cc2.number_input("Blade m/Job", value=21.0, step=1.0)
    bl_lf = cc2.number_input("Blade Life(m)", value=33000.0, step=1000.0)
    es_pr = cc2.number_input("EndSeal SAR", value=150.0, step=10.0)
    tp_pr = cc3.number_input("Tape SAR/m²", value=85.0, step=5.0)
    tp_qt = cc3.number_input("Tape m²/Job", value=6.0, step=0.5)

# --- TAB 4: HR & OPEX ---
with tabs[3]:
    st.header("🏢 HR & OPEX (الموارد البشرية والمصاريف الإدارية)")
    
    st.markdown("#### 👥 1. Manpower & Payroll (القوى العاملة)")
    h1, h2, h3 = st.columns(3)
    
    with h1:
        st.markdown("**Production (Direct Labor)**")
        eng_q = st.number_input("Engineers Qty", value=3, step=1)
        eng_s = st.number_input("Engineer Salary", value=8000, step=500)
        opr_q = st.number_input("Operators Qty", value=6, step=1)
        opr_s = st.number_input("Operator Salary", value=4500, step=500)
        wrk_q = st.number_input("Workers/Helpers Qty", value=10, step=1)
        wrk_s = st.number_input("Worker Salary", value=2500, step=500)
        
    with h2:
        st.markdown("**Admin & Support (Indirect)**")
        adm_q = st.number_input("Admin/Sales Qty", value=5, step=1)
        adm_s = st.number_input("Admin Salary", value=8000, step=500)
        sau_q = st.number_input("Saudi (Nitaqat) Qty", value=5, step=1)
        sau_s = st.number_input("Saudi Salary", value=4000, step=500)
        
    with h3:
        st.markdown("**Overheads & Govt Fees**")
        adm_exp = st.number_input("Monthly Admin Exp (Rent, Office, etc.)", value=40000, step=1000)
        st.info("Hidden Costs: Iqama, GOSI, Medical Ins, Flights, EOSB")
        hidden_cost_pct = st.slider("Hidden Benefits % (Over Base Salary)", 0, 50, 20)

    # Calculations for HR
    t_eng = eng_q * eng_s
    t_opr = opr_q * opr_s
    t_wrk = wrk_q * wrk_s
    t_adm = adm_q * adm_s
    t_sau = sau_q * sau_s
    
    base_payroll = t_eng + t_opr + t_wrk + t_adm + t_sau
    gov_benefits_cost = base_payroll * (hidden_cost_pct / 100.0)
    payroll = base_payroll + gov_benefits_cost # Final payroll passed to Tab 5
    
    total_headcount = eng_q + opr_q + wrk_q + adm_q + sau_q
    saudization_pct = (sau_q / total_headcount) if total_headcount > 0 else 0
    
    st.markdown("---")
    st.markdown("#### 📊 HR Dashboard")
    hm1, hm2, hm3, hm4 = st.columns(4)
    hm1.metric("👥 Total Headcount", f"{total_headcount} Emp")
    hm2.metric("🇸🇦 Saudization %", f"{saudization_pct:.1%}", delta="Nitaqat Check")
    hm3.metric("💸 Total Monthly Payroll", f"SAR {payroll:,.0f}")
    hm4.metric("🏢 Total Monthly OPEX", f"SAR {payroll + adm_exp:,.0f}")
    
    # Chart for OPEX Breakdown
    df_hr = pd.DataFrame({
        "Category": ["Engineers", "Operators", "Workers", "Admin", "Saudis", "Gov Fees/Benefits", "Admin Expenses"],
        "Monthly Cost": [t_eng, t_opr, t_wrk, t_adm, t_sau, gov_benefits_cost, adm_exp]
    })
    fig_hr = px.pie(df_hr, names="Category", values="Monthly Cost", title="Monthly OPEX Breakdown", hole=0.4)
    st.plotly_chart(fig_hr, use_container_width=True)

# --- TAB 5: Recipes & Detailed Costing ---
with tabs[4]:
    st.markdown("### ⚙️ 1. Global Settings")
    t_tons = st.number_input("🎯 Target Tons", value=2500.0, step=100.0)
    c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    std_w = c_s1.number_input("Web Width", value=1.0, step=0.1)
    w_ink = c_s2.number_input("Wet Ink", value=5.0, step=0.1)
    i_loss = c_s3.number_input("Loss%", value=40.0, step=1.0)
    a_gsm = c_s4.number_input("Adh GSM", value=1.8, step=0.1)
    d_ink = w_ink * (1.0 - (i_loss/100.0))
    
    st.markdown("### ♻️ 2. Scrap & Waste Engine")
    cw1, cw2, cw3, cw4, cw5 = st.columns(5)
    w_ext = cw1.number_input("Extruder Waste %", value=3.0, step=0.5)
    w_flx = cw2.number_input("Flexo Waste %", value=4.0, step=0.5)
    w_lam = cw3.number_input("Lam Waste %", value=3.0, step=0.5)
    w_fin = cw4.number_input("Finishing Waste %", value=2.0, step=0.5)
    scrap_p = cw5.number_input("Scrap Resale (SAR/Kg)", value=1.5, step=0.1)
    
    st.markdown("### 📋 3. Product Portfolio")
    init_data = [
        {"Product": "1 Lyr", "Print": True, "L1": "BOPP", "M1": 40, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 20, "Price": 13.0},
        {"Product": "2 Lyr", "Print": True, "L1": "BOPP", "M1": 20, "L2": "BOPP", "M2": 20, "L3": "None", "M3": 0, "Mix%": 25, "Price": 13.0},
        {"Product": "3 Lyr", "Print": True, "L1": "PET", "M1": 12, "L2": "ALU", "M2": 7, "L3": "PE Lam", "M3": 50, "Mix%": 5, "Price": 15.0},
        {"Product": "Shrink Plain", "Print": False, "L1": "PE Shrink", "M1": 40, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 30, "Price": 5.0},
        {"Product": "Printed Shop. Bag", "Print": True, "L1": "PE Bag", "M1": 60, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 20, "Price": 10.0}
    ]
    df_rec = st.data_editor(pd.DataFrame(init_data), num_rows="dynamic", use_container_width=True)
    
    w_gsm, t_flexo_lm, t_lam_sqm, tons_ext, tons_flx, tons_lam, tons_slt, tons_bag = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    t_slt_lm, t_bag_lm, temp_dets = 0.0, 0.0, []
    t_ink_k, t_slv_k, t_adh_k = 0.0, 0.0, 0.0
    
    for _, r in df_rec.iterrows():
        pn, is_p, r_ton = str(r["Product"]).lower(), r.get("Print", True), t_tons*(r["Mix%"]/100.0)
        lp = (1 if r["M2"] > 0 and str(r["L2"]) != "None" else 0) + (1 if r["M3"] > 0 and str(r["L3"]) != "None" else 0)
        u_ext = any("pe" in str(r[l]).lower() for l in ["L1","L2","L3"])
        u_slt = any(x in pn for x in ["1 lyr","2 lyr","3 lyr","bopp"])
        u_bag = "bag" in pn
        
        y = 1.0
        if u_ext: y *= (1.0 - w_ext/100.0)
        if is_p: y *= (1.0 - w_flx/100.0)
        if lp > 0: y *= (1.0 - w_lam/100.0)**lp
        if u_slt or u_bag: y *= (1.0 - w_fin/100.0)
        
        gross_ton = r_ton / y if y > 0 else r_ton
        
        if u_ext: tons_ext += gross_ton
        if is_p: tons_flx += gross_ton
        if lp > 0: tons_lam += (gross_ton * lp)
        if u_slt: tons_slt += gross_ton
        if u_bag: tons_bag += gross_ton
        
        g1, g2, g3 = r["M1"]*mat_db[str(r["L1"])]["d"], r["M2"]*mat_db[str(r["L2"])]["d"], r["M3"]*mat_db[str(r["L3"])]["d"]
        tg = g1 + g2 + g3 + (lp*a_gsm) + (d_ink if is_p else 0)
        
        c_mat_ideal = ((g1/1000*mat_db[str(r["L1"])]["p"]) + (g2/1000*mat_db[str(r["L2"])]["p"]) + (g3/1000*mat_db[str(r["L3"])]["p"]) + (lp*a_gsm/1000*adh_p) + (w_ink/1000*ink_p if is_p else 0) + (w_ink*0.5/1000*solv_p if is_p else 0))/(tg/1000.0) if tg>0 else 0
        
        gross_mat_cost = c_mat_ideal / y if y > 0 else c_mat_ideal
        scrap_rev_kg = ((1.0/y) - 1.0) * scrap_p if y > 0 else 0
        net_mat_cost = gross_mat_cost - scrap_rev_kg
        
        l_len = (r_ton*1000000/tg)/std_w if tg>0 and std_w>0 else 0
        gross_len = l_len / y if y > 0 else l_len
        
        if is_p: 
            t_flexo_lm += gross_len
            t_ink_k += (gross_len * std_w * w_ink) / 1000.0
            t_slv_k += (gross_len * std_w * w_ink * 0.5) / 1000.0
        if lp > 0: 
            t_lam_sqm += (gross_len*std_w*lp)
            t_adh_k += (gross_len * std_w * a_gsm * lp) / 1000.0
        if u_slt: t_slt_lm += gross_len
        if u_bag: t_bag_lm += gross_len
        w_gsm += tg*(r["Mix%"]/100.0)
        
        temp_dets.append({"Product":r["Product"],"Printed":is_p,"Tons":r_ton,"GSM":tg,"GrossMatCost":gross_mat_cost,"NetMatCost":net_mat_cost, "Waste%": (1-y), "ScrapRev/Kg": scrap_rev_kg, "Price":r["Price"],"u_ext":u_ext,"lp":lp,"u_slt":u_slt,"u_bag":u_bag})

    ln_m = (t_tons*1000/w_gsm*1000)/std_w if w_gsm>0 and std_w>0 else 0
    a_cons = ((ln_m/(an_lf*1000000.0))*an_pr*8.0 if an_lf>0 else 0) + ((ln_m/bl_lf)*(bl_qt*bl_pr + es_pr*8.0) if bl_lf>0 else 0) + ((t_flexo_lm/pl_lf)*pl_pr if pl_lf>0 else 0) + ((j_mo*12.0)*tp_qt*tp_pr)
    
    re_h, rf_h, rl_h = (tons_ext*1000)/e_kg if e_kg>0 else 0, t_flexo_lm/(f_s*60*(f_e/100)) if f_s*f_e>0 else 0, (t_lam_sqm/std_w)/(l_s*60*(l_e/100)) if l_s*l_e*std_w>0 else 0
    rs_h, rb_h = t_slt_lm/(s_s*60*(s_e/100)) if s_s*s_e>0 else 0, t_bag_lm/(b_s*60*b_q*(b_e/100)) if b_s*b_q*b_e>0 else 0
    
    pe, pf, pl, ps, pb = re_h*e_kw*kw_p + dep_e, rf_h*f_k*kw_p + dep_f + a_cons, rl_h*l_k*kw_p + dep_l, rs_h*s_k*kw_p + dep_s, rb_h*b_k*kw_p + dep_b
    po = (payroll+adm_exp)*12 + (hng_pr/25) + (chl_pr/10) + (cmp_pr/10) + (net_hrs*(chl_k+cmp_k)*kw_p)
    r_e, r_f, r_l, r_s, r_b, r_o = pe/(tons_ext*1000) if tons_ext>0 else 0, pf/(tons_flx*1000) if tons_flx>0 else 0, pl/(tons_lam*1000) if tons_lam>0 else 0, ps/(tons_slt*1000) if tons_slt>0 else 0, pb/(tons_bag*1000) if tons_bag>0 else 0, po/(t_tons*1000) if t_tons>0 else 0

    dets = []
    for d in temp_dets:
        c_e = r_e if d["u_ext"] else 0
        c_f = r_f if d["Printed"] else 0
        c_l = r_l * d["lp"]
        c_s = r_s if d["u_slt"] else 0
        c_b = r_b if d["u_bag"] else 0
        t_cost = d["NetMatCost"] + c_e + c_f + c_l + c_s + c_b + r_o
        m_pct = (d["Price"] - t_cost) / d["Price"] if d["Price"] > 0 else 0
        
        dets.append({
            "Product": d["Product"], "Tons": d["Tons"], "Waste%": d["Waste%"], "GrossMatCost": d["GrossMatCost"], "NetMatCost": d["NetMatCost"], 
            "Extrdr": c_e, "Flexo": c_f, "Lam": c_l, "Slit": c_s, "BagMk": c_b, "OH": r_o,
            "TotalCost": t_cost, "Price": d["Price"], "Profit": d["Price"]-t_cost, "Margin%": m_pct, "ScrapRev/Kg": d["ScrapRev/Kg"], "GSM": d["GSM"]
        })
    
    st.markdown("### 📊 4. Detailed ABC Costing & Waste (SAR/Kg)")
    df_show = pd.DataFrame(dets)
    format_dict = {
        "Tons": "{:,.1f}", "Waste%": "{:,.1%}", "NetMatCost": "{:,.2f}", "Extrdr": "{:,.2f}", "Flexo": "{:,.2f}", 
        "Lam": "{:,.2f}", "Slit": "{:,.3f}", "BagMk": "{:,.2f}", "OH": "{:,.2f}", 
        "TotalCost": "{:,.2f}", "Price": "{:,.2f}", "Profit": "{:,.2f}", "Margin%": "{:,.2%}"
    }
    st.dataframe(df_show[["Product", "Tons", "Waste%", "NetMatCost", "Extrdr", "Flexo", "Lam", "Slit", "BagMk", "OH", "TotalCost", "Price", "Profit", "Margin%"]].style.format(format_dict), use_container_width=True)
    
    st.markdown("### 🧪 5. Monthly Chemicals")
    c_ch1, c_ch2, c_ch3 = st.columns(3)
    c_ch1.metric("🎨 Ink Kg/Mo", f"{t_ink_k/12:,.0f}")
    c_ch2.metric("🧪 Solv Kg/Mo", f"{t_slv_k/12:,.0f}")
    c_ch3.metric("🍯 Adh Kg/Mo", f"{t_adh_k/12:,.0f}")

    st.markdown("### 🚦 6. Line Balancing (Bottleneck Check)")
    cb1, cb2, cb3, cb4, cb5 = st.columns(5)
    if tons_ext <= e_tons_cap: cb1.success(f"Extruder\n\nCap: {e_tons_cap:,.0f} T\n\nReq: {tons_ext:,.0f} T")
    else: cb1.error(f"Extruder\n\nCap: {e_tons_cap:,.0f} T\n\nReq: {tons_ext:,.0f} T")
    
    if t_flexo_lm <= f_lm_cap: cb2.success(f"Flexo (M m)\n\nCap: {f_lm_cap/1000000:,.2f}\n\nReq: {t_flexo_lm/1000000:,.2f}")
    else: cb2.error(f"Flexo (M m)\n\nCap: {f_lm_cap/1000000:,.2f}\n\nReq: {t_flexo_lm/1000000:,.2f}")
    
    if (t_lam_sqm/std_w if std_w>0 else 0) <= l_lm_cap: cb3.success(f"Lam (M m)\n\nCap: {l_lm_cap/1000000:,.2f}\n\nReq: {(t_lam_sqm/std_w if std_w>0 else 0)/1000000:,.2f}")
    else: cb3.error(f"Lam (M m)\n\nCap: {l_lm_cap/1000000:,.2f}\n\nReq: {(t_lam_sqm/std_w if std_w>0 else 0)/1000000:,.2f}")

    if t_slt_lm <= s_lm_cap: cb4.success(f"Slit (M m)\n\nCap: {s_lm_cap/1000000:,.2f}\n\nReq: {t_slt_lm/1000000:,.2f}")
    else: cb4.error(f"Slit (M m)\n\nCap: {s_lm_cap/1000000:,.2f}\n\nReq: {t_slt_lm/1000000:,.2f}")

    if t_bag_lm <= b_lm_cap: cb5.success(f"BagMk (M m)\n\nCap: {b_lm_cap/1000000:,.2f}\n\nReq: {t_bag_lm/1000000:,.2f}")
    else: cb5.error(f"BagMk (M m)\n\nCap: {b_lm_cap/1000000:,.2f}\n\nReq: {t_bag_lm/1000000:,.2f}")

# --- TAB 6: P&L Summary & WORKING CAPITAL ---
with tabs[5]:
    total_rev = sum(d['Price']*d['Tons']*1000 for d in dets)
    total_scrap_rev = sum(d['ScrapRev/Kg']*d['Tons']*1000 for d in dets)
    total_all_cost = sum(d['TotalCost']*d['Tons']*1000 for d in dets)
    
    total_gross_mat = sum(d['GrossMatCost']*d['Tons']*1000 for d in dets)
    cash_opex = total_all_cost - ann_dep - total_gross_mat + total_scrap_rev
    
    st.markdown("### ⏳ Working Capital Cycle (دورة رأس المال العامل)")
    st.info("حدد أيام التحصيل والتخزين والدفع لمعرفة 'الكاش' المطلوب لبدء تشغيل المصنع دون تعثر.")
    wc_c1, wc_c2, wc_c3 = st.columns(3)
    ar_days = wc_c1.number_input("Receivable Days (أيام تحصيل العملاء)", value=60, step=15)
    inv_days = wc_c2.number_input("Inventory Days (أيام تخزين المواد)", value=45, step=15)
    ap_days = wc_c3.number_input("Payable Days (تسهيلات الموردين)", value=30, step=15)

    receivables = (total_rev / 365.0) * ar_days
    inventory = ((total_gross_mat + cash_opex) / 365.0) * inv_days
    payables = (total_gross_mat / 365.0) * ap_days
    working_capital = receivables + inventory - payables
    
    st.markdown("#### 💼 Working Capital Requirements")
    wc_m1, wc_m2, wc_m3, wc_m4 = st.columns(4)
    wc_m1.metric("Cash with Customers (+)", f"SAR {receivables:,.0f}")
    wc_m2.metric("Cash in Inventory (+)", f"SAR {inventory:,.0f}")
    wc_m3.metric("Supplier Credit (-)", f"SAR {payables:,.0f}")
    wc_m4.metric("💰 Required WC", f"SAR {working_capital:,.0f}")
    
    st.markdown("---")
    st.header("📈 Plant Financial Summary")
    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Product Revenue", f"SAR {total_rev:,.0f}")
    f2.metric("Scrap Recovery Rev.", f"SAR {total_scrap_rev:,.0f}")
    f3.metric("Total OPEX & CAPEX Depr", f"SAR {total_all_cost:,.0f}")
    f4.metric("Net Profit", f"SAR {total_rev-total_all_cost:,.0f}")
    
    st.warning(f"🏦 **Total Initial Investment Required:** SAR {t_capex + working_capital:,.0f} *(CAPEX: {t_capex:,.0f} + Working Capital: {working_capital:,.0f})*")
    
    st.markdown("### 💰 Net Profit Margin Chart")
    st.plotly_chart(px.bar(df_show, x="Product", y="Profit", color="Product", text_auto=".2f"), use_container_width=True)
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        df_show.drop(columns=['GSM', 'ScrapRev/Kg', 'GrossMatCost']).to_excel(w, sheet_name='Costing_Analysis', index=False)
    st.download_button("📥 Download Excel Summary", buf.getvalue(), "Royan_Summary.xlsx", use_container_width=True)

# --- TAB 7: Commercial ---
with tabs[6]:
    st.header("Commercial Offer")
    sr = st.selectbox("Select Product", [d['Product'] for d in dets])
    row = next(i for i in dets if i["Product"] == sr)
    if st.button("Generate"):
        st.info(f"**Customer:** Valued Client\n\n**Product:** {row['Product']} ({row['GSM']:,.1f} g/m²)\n\n**Price:** SAR {row['Price']:,.2f} / Kg\n\n*Waheed Waleed Malik, Royan*")
