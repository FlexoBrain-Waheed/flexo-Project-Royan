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
    ink_p, solv_p, adh_p = ci1.number_input("Ink/Kg", 14.0), ci2.number_input("Solvent/Kg", 6.0), ci3.number_input("Adhesive/Kg", 12.0)

# --- TAB 2: Production & Capacity Chart ---
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
    with m2:
        f_s, f_w, f_e = st.number_input("Flexo Speed", 350.0), st.number_input("Flexo Width", 1.0), st.slider("Flexo Eff%", 1, 100, 80)
        f_k, f_pr = st.number_input("Flexo kW", 150.0), st.number_input("Flexo CAPEX", 8000000.0)
    with m3:
        l_s, l_w, l_e = st.number_input("Lam Speed", 450.0), st.number_input("Lam Width", 1.0), st.slider("Lam Eff%", 1, 100, 75)
        l_k, l_pr = st.number_input("Lam kW", 80.0), st.number_input("Lam CAPEX", 1200000.0)
    m4, m5 = st.columns(2)
    with m4:
        s_s, s_w, s_e = st.number_input("Slit Speed", 400.0), st.number_input("Slit Width", 1.0), st.slider("Slit Eff%", 1, 100, 50)
        s_k, s_pr = st.number_input("Slit kW", 40.0), st.number_input("Slit CAPEX", 800000.0)
    with m5:
        b_q, b_s, b_e = st.number_input("Bag Mach Qty", 5), st.number_input("Bag Speed m/m", 75.0), st.slider("Bag Eff%", 1, 100, 85)
        b_k, b_pr = st.number_input("Bag kW Total", 75.0), st.number_input("Bag CAPEX", 500000.0)

    u1, u2, u3 = st.columns(3)
    hng_pr, hng_dep_y = u1.number_input("Hangar CAPEX", 4000000.0), u1.number_input("Hangar Depr Yrs", 25.0)
    chl_k, chl_pr, chl_dep_y = u2.number_input("Chiller kW", 50.0), u2.number_input("Chiller CAPEX", 500000.0), u2.number_input("Chiller Depr Yrs", 10.0)
    cmp_k, cmp_pr, cmp_dep_y = u3.number_input("Compressor kW", 30.0), u3.number_input("Compressor CAPEX", 250000.0), u3.number_input("Comp. Depr Yrs", 10.0)
    
    mac_dep_y = st.number_input("Machines Depreciation Yrs", 10.0)
    dep_e, dep_f, dep_l, dep_s, dep_b = e_pr/mac_dep_y, f_pr/mac_dep_y, l_pr/mac_dep_y, s_pr/mac_dep_y, b_pr/mac_dep_y
    ann_dep = dep_e + dep_f + dep_l + dep_s + dep_b + (hng_pr/hng_dep_y) + (chl_pr/chl_dep_y) + (cmp_pr/cmp_dep_y)
    t_capex = e_pr + f_pr + l_pr + s_pr + b_pr + hng_pr + chl_pr + cmp_pr

    st.markdown("### 📊 Capacity Check (Tons/Year)")
    chart_gsm = st.number_input("Estimated GSM for Capacity Graph", 40.0)
    df_cap = pd.DataFrame({
        "Machine": ["Extruder", "Flexo", "Lamination", "Slitter", "Bag Making"],
        "Max Capacity (Tons)": [
            (e_kg*net_hrs/1000), 
            (net_hrs*60*f_s*(f_e/100)*f_w*chart_gsm/1000000),
            (net_hrs*60*l_s*(l_e/100)*l_w*chart_gsm/1000000),
            (net_hrs*60*s_s*(s_e/100)*s_w*chart_gsm/1000000),
            (net_hrs*60*b_s*b_q*(b_e/100)*chart_gsm/1000000)
        ]
    })
    st.plotly_chart(px.bar(df_cap, x="Machine", y="Max Capacity (Tons)", color="Machine", text_auto='.0f'), use_container_width=True)

# --- TAB 3: Consumables ---
with tabs[2]:
    cc1, cc2, cc3 = st.columns(3)
    pl_pr, pl_lf = cc1.number_input("Plate SAR", 2500.0), cc1.number_input("Plate Life(m)", 400000.0)
    an_pr, an_lf = cc1.number_input("Anilox SAR", 15000.0), cc1.number_input("Anilox Life(M)", 200.0)
    bl_pr, bl_qt, bl_lf = cc2.number_input("Blade SAR/m", 12.0), cc2.number_input("Blade m/Job", 21.0), cc2.number_input("Blade Life(m)", 33000.0)
    es_pr = cc2.number_input("EndSeal SAR", 150.0)
    tp_pr, tp_qt = cc3.number_input("Tape SAR/m²", 85.0), cc3.number_input("Tape m²/Job", 6.0)

# --- TAB 4: HR ---
with tabs[3]:
    payroll = (st.number_input("Eng Total", 24000)+st.number_input("Op Total", 27000)+st.number_input("Wrk Total", 25000)+st.number_input("Adm Total", 40000)+st.number_input("Saudi Total", 20000))
    adm_exp = st.number_input("Monthly Admin Exp", 40000)

# --- TAB 5: Recipes & Profit Chart ---
with tabs[4]:
    st.markdown("### ⚙️ 1. Global Production Settings")
    t_tons = st.number_input("🎯 Target Tons", value=2500.0, step=100.0)
    std_w, w_ink, i_loss, a_gsm = st.number_input("Web Width", 1.0), st.number_input("Wet Ink", 5.0), st.number_input("Loss%", 40.0), st.number_input("Adh GSM", 1.8)
    d_ink = w_ink * (1.0 - (i_loss/100.0))
    
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
    
    for _, r in df_rec.iterrows():
        pn, is_p, r_ton = str(r["Product"]).lower(), r.get("Print", True), t_tons*(r["Mix%"]/100.0)
        lp = (1 if r["M2"] > 0 and str(r["L2"]) != "None" else 0) + (1 if r["M3"] > 0 and str(r["L3"]) != "None" else 0)
        u_ext = any("pe" in str(r[l]).lower() for l in ["L1","L2","L3"])
        u_slt = any(x in pn for x in ["1 lyr","2 lyr","3 lyr","bopp"])
        u_bag = "bag" in pn
        
        if u_ext: tons_ext += r_ton
        if is_p: tons_flx += r_ton
        if lp > 0: tons_lam += (r_ton * lp)
        if u_slt: tons_slt += r_ton
        if u_bag: tons_bag += r_ton
        
        g1, g2, g3 = r["M1"]*mat_db[str(r["L1"])]["d"], r["M2"]*mat_db[str(r["L2"])]["d"], r["M3"]*mat_db[str(r["L3"])]["d"]
        tg = g1 + g2 + g3 + (lp*a_gsm) + (d_ink if is_p else 0)
        c_mat = ((g1/1000*mat_db[str(r["L1"])]["p"]) + (g2/1000*mat_db[str(r["L2"])]["p"]) + (g3/1000*mat_db[str(r["L3"])]["p"]) + (lp*a_gsm/1000*adh_p) + (w_ink/1000*ink_p if is_p else 0) + (w_ink*0.5/1000*solv_p if is_p else 0))/(tg/1000.0) if tg>0 else 0
        l_len = (r_ton*1000000/tg)/std_w if tg>0 else 0
        if is_p: t_flexo_lm += l_len
        if lp > 0: t_lam_sqm += (l_len*std_w*lp)
        if u_slt: t_slt_lm += l_len
        if u_bag: t_bag_lm += l_len
        w_gsm += tg*(r["Mix%"]/100.0)
        temp_dets.append({"Product":r["Product"],"Printed":is_p,"Tons":r_ton,"GSM":tg,"MatCost":c_mat,"Price":r["Price"],"u_ext":u_ext,"lp":lp,"u_slt":u_slt,"u_bag":u_bag,"l_len":l_len})

    ln_m = (t_tons*1000/w_gsm*1000)/std_w if w_gsm>0 else 0
    a_cons = ((ln_m/(an_lf*1000000.0))*an_pr*8.0 if an_lf>0 else 0) + ((ln_m/bl_lf)*(bl_qt*bl_pr + es_pr*8.0) if bl_lf>0 else 0) + ((t_flexo_lm/pl_lf)*pl_pr if pl_lf>0 else 0) + ((j_mo*12.0)*tp_qt*tp_pr)
    
    re_h, rf_h, rl_h = (tons_ext*1000)/e_kg if e_kg>0 else 0, t_flexo_lm/(f_s*60*(f_e/100)) if f_s*f_e>0 else 0, (t_lam_sqm/std_w)/(l_s*60*(l_e/100)) if l_s*l_e>0 else 0
    rs_h, rb_h = t_slt_lm/(s_s*60*(s_e/100)) if s_s*s_e>0 else 0, t_bag_lm/(b_s*60*b_q*(b_e/100)) if b_s*b_q*b_e>0 else 0
    
    p_e, p_f, p_l, p_s, p_b = re_h*e_kw*kw_p + dep_e, rf_h*f_k*kw_p + dep_f + a_cons, rl_h*l_k*kw_p + dep_l, rs_h*s_k*kw_p + dep_s, rb_h*b_k*kw_p + dep_b
    p_o = (payroll+adm_exp)*12 + (hng_pr/25) + (chl_pr/10) + (cmp_pr/10) + (net_hrs*80*kw_p)
    r_e, r_f, r_l, r_s, r_b, r_o = p_e/(tons_ext*1000) if tons_ext>0 else 0, p_f/(tons_flx*1000) if tons_flx>0 else 0, p_l/(tons_lam*1000) if tons_lam>0 else 0, p_s/(tons_slt*1000) if tons_slt>0 else 0, p_b/(tons_bag*1000) if tons_bag>0 else 0, p_o/(t_tons*1000) if t_tons>0 else 0

    dets = []
    for d in temp_dets:
        tc = d["MatCost"] + (r_e if d["u_ext"] else 0) + (r_f if d["Printed"] else 0) + (r_l*d["lp"]) + (r_s if d["u_slt"] else 0) + (r_b if d["u_bag"] else 0) + r_o
        dets.append({"Product":d["Product"],"Tons":d["Tons"],"MatCost":d["MatCost"],"TotalCost":tc,"Price":d["Price"],"Profit":d["Price"]-tc,"GSM":d["GSM"]})
    
    st.markdown("### 💰 Net Profit per Product (SAR/Kg)")
    st.plotly_chart(px.bar(pd.DataFrame(dets), x="Product", y="Profit", color="Product", text_auto=".2f"), use_container_width=True)
    num_cols = ["Tons", "MatCost", "TotalCost", "Price", "Profit"]
    st.dataframe(pd.DataFrame(dets)[["Product"]+num_cols].style.format({c: "{:,.2f}" for c in num_cols}), use_container_width=True)

# --- TAB 6: P&L Summary ---
with tabs[5]:
    total_rev = sum(d['Price']*d['Tons']*1000 for d in dets)
    total_all_cost = sum(d['TotalCost']*d['Tons']*1000 for d in dets)
    st.header("Plant Financial Summary")
    f1, f2, f3 = st.columns(3)
    f1.metric("Revenue", f"SAR {total_rev:,.0f}")
    f2.metric("Total Cost", f"SAR {total_all_cost:,.0f}")
    f3.metric("Net Profit", f"SAR {total_rev-total_all_cost:,.0f}")
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        pd.DataFrame(dets).to_excel(w, sheet_name='Analysis')
    st.download_button("📥 Download Excel Summary", buf.getvalue(), "Royan_Summary.xlsx", use_container_width=True)

with tabs[6]:
    st.header("Commercial Offer")
    row = next(i for i in dets if i["Product"] == st.selectbox("Product", [d['Product'] for d in dets]))
    if st.button("Generate"):
        st.info(f"**Customer:** Valued Client\n**Product:** {row['Product']}\n**Price:** SAR {row['Price']:,.2f}/Kg\n\n*Royan Plant Simulator*")
