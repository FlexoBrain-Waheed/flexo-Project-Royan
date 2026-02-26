import streamlit as st, pandas as pd, io
st.set_page_config(page_title="NexFlexo Plant", layout="wide")
st.title("🏭 NexFlexo Smart Plant Simulator")

tabs = st.tabs(["1. Materials", "2. Production", "3. Consumables", "4. HR & OPEX", "5. Recipes", "6. P&L", "7. Commercial"])

# --- TAB 1 ---
with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    p_b, d_b = c1.number_input("BOPP SAR", 6.0), c1.number_input("BOPP Den", 0.91)
    # تم تعديل سعر PET هنا إلى 6.3 بناءً على صورتك
    p_pt, d_pt = c2.number_input("PET SAR", 6.3), c2.number_input("PET Den", 1.40)
    p_pe, d_pe = c3.number_input("PE SAR", 5.0), c3.number_input("PE Den", 0.92)
    p_al, d_al = c4.number_input("ALU SAR", 18.0), c4.number_input("ALU Den", 2.70)
    mat_db = {"BOPP":{"p":p_b,"d":d_b}, "PET":{"p":p_pt,"d":d_pt}, "PE":{"p":p_pe,"d":d_pe}, "ALU":{"p":p_al,"d":d_al}, "None":{"p":0.0,"d":0.0}}
    st.markdown("---")
    ci1, ci2, ci3 = st.columns(3)
    ink_p, solv_p, adh_p = ci1.number_input("Ink/Kg", 15.0), ci2.number_input("Solvent/Kg", 6.0), ci3.number_input("Adhesive/Kg", 12.0)

# --- TAB 2 ---
with tabs[1]:
    cw1, cw2 = st.columns(2)
    net_hrs = (cw1.number_input("Days",300) * cw1.number_input("Shifts",2) * cw1.number_input("Hrs/Sh",12)) - (cw2.number_input("Jobs/Mo",60) * 12 * cw2.number_input("C.O. Hrs",1.0))
    st.success(f"Net Hrs: {net_hrs}")
    kw_p = st.number_input("SAR/kWh", 0.18)
    
    def m_inp(c, n, sp, kw, pr, eff):
        s = c.number_input(f"{n} Spd", sp)
        w = c.number_input(f"{n} Wdth", 1.0)
        e = c.slider(f"{n} Eff%", 40, 100, eff)
        k = c.number_input(f"{n} kW", kw)
        p = c.number_input(f"{n} CAPEX", pr)
        lm = net_hrs * 60 * s * (e/100)
        sq = lm * w
        pc = net_hrs * k * kw_p
        c.info(f"📏 {lm:,.0f}m | 🔲 {sq:,.0f}m² | ⚡ SAR {pc:,.0f}")
        return lm, sq, pc, p

    m1, m2, m3 = st.columns(3)
    f_lm, f_sq, f_pc, f_pr = m_inp(m1, "Flexo", 300, 150.0, 8000000, 70)
    l_lm, l_sq, l_pc, l_pr = m_inp(m2, "Lam", 250, 80.0, 1200000, 75)
    s_lm, s_sq, s_pc, s_pr = m_inp(m3, "Slit", 400, 40.0, 800000, 80)
    
    c_cap1, c_cap2 = st.columns(2)
    t_capex = f_pr + l_pr + s_pr + 500000
    c_cap1.metric("Total CAPEX", f"SAR {t_capex:,.0f}")
    dep_y = c_cap2.number_input("Depreciation Yrs", 15.0)
    ann_dep = t_capex / dep_y if dep_y > 0 else 0
    t_pwr = f_pc + l_pc + s_pc

# --- TAB 3 ---
with tabs[2]:
    cc1, cc2, cc3 = st.columns(3)
    an_pr, an_lf = cc1.number_input("Anilox SAR", 15000), cc1.number_input("Anilox Life(M)", 200)
    bl_pr, bl_lf = cc2.number_input("Blade SAR/m", 12.0), cc2.number_input("Blade Life(k)", 500)
    es_pr, es_lf = cc3.number_input("EndSeal SAR", 150.0), cc3.number_input("EndSeal Hrs", 72)

# --- TAB 4 ---
with tabs[3]:
    ch1, ch2, ch3, ch4 = st.columns(4)
    eng_q, eng_s = ch1.number_input("Eng Qty", 3), ch1.number_input("Eng Sal", 8000)
    opr_q, opr_s = ch2.number_input("Op Qty", 6), ch2.number_input("Op Sal", 4500)
    wrk_q, wrk_s = ch3.number_input("Wrk Qty", 10), ch3.number_input("Wrk Sal", 2500)
    adm_q, adm_s = ch4.number_input("Adm Qty", 5), ch4.number_input("Adm Sal", 8000)
    
    payroll = (eng_q*eng_s) + (opr_q*opr_s) + (wrk_q*wrk_s) + (adm_q*adm_s)
    st.markdown("---")
    cp1, cp2, cp3 = st.columns(3)
    adm_exp = cp1.number_input("Monthly Admin Exp", 40000)
    cp2.metric("Total Monthly Payroll", f"SAR {payroll:,.0f}")
    cp3.metric("Annual Power Cost", f"SAR {t_pwr:,.0f}")

# --- TAB 5 ---
with tabs[4]:
    c_c1, c_c2, c_c3 = st.columns(3)
    w_ink, i_loss, a_gsm = c_c1.number_input("Wet Ink", 5.0), c_c2.number_input("Ink Loss%", 40.0), c_c3.number_input("Adh GSM", 1.8)
    d_ink = w_ink * (1.0 - (i_loss / 100.0))
    st.markdown("---")
    ct1, ct2 = st.columns(2)
    t_tons = ct1.number_input("Target Tons", 3600.0)
    std_w = ct2.number_input("Web Width (m)", 1.0)
    
    df_rec = st.data_editor(pd.DataFrame([
        {"Product": "1 Lyr", "L1": "BOPP", "M1": 38, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 60, "Price": 12.0},
        {"Product": "2 Lyr", "L1": "BOPP", "M1": 20, "L2": "BOPP", "M2": 20, "L3": "None", "M3": 0, "Mix%": 30, "Price": 13.0},
        {"Product": "3 Lyr", "L1": "PET", "M1": 12, "L2": "ALU", "M2": 7, "L3": "PE", "M3": 50, "Mix%": 10, "Price": 15.0}
    ]), num_rows="dynamic", use_container_width=True)
    
    w_gsm = w_rmc = w_sp = l_mix = t_ink_k = t_slv_k = t_adh_k = 0.0
    dets, m_nd = [], {}
    
    for _, r in df_rec.iterrows():
        g1, g2, g3 = r["M1"]*mat_db[r["L1"]]["d"], r["M2"]*mat_db[r["L2"]]["d"], r["M3"]*mat_db[r["L3"]]["d"]
        lp = (1 if r["M2"]>0 else 0) + (1 if r["M3"]>0 else 0)
        ag = lp * a_gsm
        tg = g1 + g2 + g3 + d_ink + ag
        
        c1, c2, c3 = (g1/1000)*mat_db[r["L1"]]["p"], (g2/1000)*mat_db[r["L2"]]["p"], (g3/1000)*mat_db[r["L3"]]["p"]
        ca, ci, cs = (ag/1000)*adh_p, (w_ink/1000)*ink_p, (w_ink*0.5/1000)*solv_p
        
        cpk = (c1+c2+c3+ca+ci+cs)/(tg/1000) if tg > 0 else 0.0
        r_ton = t_tons * (r["Mix%"]/100)
        l_len = 0.0
        
        if tg > 0:
            sq = (r_ton * 1000000) / tg
            if std_w > 0: l_len = sq / std_w
            t_ink_k += (sq * w_ink) / 1000
            t_slv_k += (sq * w_ink * 0.5) / 1000
            t_adh_k += (sq * ag) / 1000
            for lyr, mic in [("L1","M1"), ("L2","M2"), ("L3","M3")]:
                if r[lyr] != "None" and r[mic] > 0:
                    mk = f"{r[lyr]} {r[mic]}µ"
                    m_nd[mk] = m_nd.get(mk, 0.0) + l_len
                    
        mr = r["Mix%"] / 100.0
        w_gsm += tg * mr
        w_rmc += cpk * mr
        w
