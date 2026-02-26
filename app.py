import streamlit as st, pandas as pd, io
st.set_page_config(page_title="NexFlexo Plant", layout="wide")
st.title("🏭 NexFlexo Smart Plant Simulator")

tabs = st.tabs(["1. Materials", "2. Production", "3. Consumables", "4. HR & OPEX", "5. Recipes", "6. P&L", "7. Commercial"])

# --- TAB 1 ---
with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    p_b, d_b = c1.number_input("BOPP SAR", 6.0), c1.number_input("BOPP Den", 0.91)
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
    d_yr = cw1.number_input("Days", 300)
    s_day = cw1.number_input("Shifts", 2)
    h_sh = cw1.number_input("Hrs/Sh", 12)
    j_mo = cw2.number_input("Jobs/Mo", 100)
    c_hrs = cw2.number_input("C.O. Hrs", 2.0)
    
    net_hrs = (d_yr * s_day * h_sh) - (j_mo * 12 * c_hrs)
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

# --- TAB 3 (UPDATED CONSUMABLES) ---
with tabs[2]:
    cc1, cc2, cc3 = st.columns(3)
    an_pr = cc1.number_input("Anilox SAR/Col", 15000.0)
    an_lf = cc1.number_input("Anilox Life (M m)", 200.0)
    
    bl_pr = cc2.number_input("Blade SAR/m", 12.0)
    bl_qt = cc2.number_input("Blade m/Change", 21.0)
    es_pr = cc2.number_input("EndSeal SAR/Col", 150.0)
    bl_lf = cc2.number_input("Blade/Seal Life(m)", 33000.0)
    
    tp_pr = cc3.number_input("Mount Tape SAR/m²", 85.0)
    tp_qt = cc3.number_input("Tape m²/Job", 6.0)

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
        {"Product": "1 Lyr", "L1": "BOPP", "M1": 38, "L2": "None", "M2": 0, "L3": "None", "M3": 0, "Mix%": 50, "Price": 12.0},
        {"Product": "2 Lyr", "L1": "BOPP", "M1": 20, "L2": "BOPP", "M2": 20, "L3": "None", "M3": 0, "Mix%": 30, "Price": 13.0},
        {"Product": "3 Lyr", "L1": "PET", "M1": 12, "L2": "ALU", "M2": 7, "L3": "PE", "M3": 50, "Mix%": 20, "Price": 15.0}
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
        w_sp += r["Price"] * mr
        if lp > 0: l_mix += mr
            
        dets.append({"Product":r["Product"], "Tons":r_ton, "Length(m)":round(l_len,0), "GSM":round(tg,1), "Cost/Kg":round(cpk,2), "Margin":round(r["Price"]-cpk,2)})
        
    st.dataframe(pd.DataFrame(dets), use_container_width=True)
    if m_nd: st.dataframe(pd.DataFrame([{"Material": k, "Meters": f"{v:,.0f}"} for k, v in m_nd.items()]), use_container_width=True)
    
    ck1, ck2, ck3 = st.columns(3)
    ck1.metric("Ink Kg/Mo", f"{t_ink_k/12:,.0f}"); ck2.metric("Solv Kg/Mo", f"{t_slv_k/12:,.0f}"); ck3.metric("Adh Kg/Mo", f"{t_adh_k/12:,.0f}")
    
    fx_max, sl_max = (f_sq * w_gsm)/1000000, (s_sq * w_gsm)/1000000
    lm_max = (l_sq * w_gsm)/1000000/l_mix if l_mix > 0 else 999999
    
    cb1, cb2, cb3 = st.columns(3)
    cb1.success(f"Flexo Max: {fx_max:,.0f} T") if t_tons <= fx_max else cb1.error(f"Flexo Max: {fx_max:,.0f} T")
    cb2.success(f"Lam Max: {lm_max:,.0f} T") if t_tons <= lm_max else cb2.error(f"Lam Max: {lm_max:,.0f} T")
    cb3.success(f"Slit Max: {sl_max:,.0f} T") if t_tons <= sl_max else cb3.error(f"Slit Max: {sl_max:,.0f} T")

# --- TAB 6 & 7 (UPDATED CALCULATIONS) ---
tot_rev = t_tons * 1000 * w_sp
a_rm = t_tons * 1000 * w_rmc
esm = t_tons * (1000/w_gsm) * 1000 if w_gsm > 0 else 0
ln_m = esm / std_w if std_w > 0 else esm

a_an = (ln_m/(an_lf*1000000)*an_pr*8 if an_lf>0 else 0)
a_bl_es = (ln_m/bl_lf)*(bl_qt*bl_pr + es_pr*8) if bl_lf>0 else 0
a_tp = (j_mo * 12) * tp_qt * tp_pr
a_cons = a_an + a_bl_es + a_tp

a_hr = (payroll + adm_exp) * 12
t_opex = a_rm + a_cons + a_hr + t_pwr + ann_dep
n_prof = tot_rev - t_opex
pbk = t_capex / n_prof if n_prof > 0 else 0
atr = tot_rev / t_capex if t_capex > 0 else 0
roi = (n_prof / t_capex) * 100 if t_capex > 0 else 0

with tabs[5]:
    cr1, cr2, cr3, cr4 = st.columns(4)
    cr
