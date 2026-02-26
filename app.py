import streamlit as st, pandas as pd, io

st.set_page_config(page_title="NexFlexo Smart Plant", layout="wide")
st.title("🏭 NexFlexo Smart Plant Simulator")

tabs = st.tabs(["1. Raw Materials", "2. Production & Power", "3. Consumables", "4. HR & OPEX", "5. Recipes", "6. P&L Dashboard", "7. Commercial"])

# --- TAB 1 ---
with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    p_bopp, d_bopp = c1.number_input("BOPP Price", 6.0), c1.number_input("BOPP Den", 0.91)
    p_pet, d_pet = c2.number_input("PET Price", 5.5), c2.number_input("PET Den", 1.40)
    p_pe, d_pe = c3.number_input("PE Price", 5.0), c3.number_input("PE Den", 0.92)
    p_alu, d_alu = c4.number_input("ALU Price", 18.0), c4.number_input("ALU Den", 2.70)
    mat_db = {"BOPP": {"p": p_bopp, "d": d_bopp}, "PET": {"p": p_pet, "d": d_pet}, "PE": {"p": p_pe, "d": d_pe}, "ALU": {"p": p_alu, "d": d_alu}, "None": {"p": 0.0, "d": 0.0}}
    ci1, ci2, ci3 = st.columns(3)
    ink_p, solv_p, adh_p = ci1.number_input("Ink/Kg", 15.0), ci2.number_input("Solvent/Kg", 6.0), ci3.number_input("Adhesive/Kg", 12.0)

# --- TAB 2 ---
with tabs[1]:
    cw1, cw2 = st.columns(2)
    net_run_hrs = (cw1.number_input("Days/Yr",300)*cw1.number_input("Shifts/Day",2)*cw1.number_input("Hrs/Shift",12)) - (cw2.number_input("Jobs/Mo",60)*12*cw2.number_input("Changeover Hrs",1.0))
    st.success(f"Net Running Hours: {net_run_hrs} Hrs")
    kw_price = st.number_input("SAR / kWh", 0.18)
    
    def m_inp(col, n, sp, kw, pr, eff=70):
        s = col.number_input(f"{n} Speed", sp)
        w = col.number_input(f"{n} Width", 1.0)
        e = col.slider(f"{n} Eff %", 40, 100, eff)
        k = col.number_input(f"{n} kW", kw)
        p = col.number_input(f"{n} CAPEX", pr)
        lm = net_run_hrs * 60 * s * (e/100); sqm = lm * w; pc = net_run_hrs * k * kw_price
        col.info(f"📏 {lm:,.0f} m | 🔲 {sqm:,.0f} m² | ⚡ SAR {pc:,.0f}")
        return lm, sqm, pc, p

    m1, m2, m3 = st.columns(3)
    with m1: f_lm, f_sqm, f_pc, f_pr = m_inp(st, "Flexo", 300, 150.0, 8000000)
    with m2: l_lm, l_sqm, l_pc, l_pr = m_inp(st, "Lam", 250, 80.0, 1200000, 75)
    with m3: s_lm, s_sqm, s_pc, s_pr = m_inp(st, "Slit", 400, 40.0, 800000, 80)
    total_capex = f_pr + l_pr + s_pr + 500000
    pwr_cost = f_pc + l_pc + s_pc

# --- TAB 3 ---
with tabs[2]:
    cc1, cc2, cc3 = st.columns(3)
    an_pr, an_lf = cc1.number_input("Anilox SAR", 15000), cc1.number_input("Anilox Life(M)", 200)
    bl_pr, bl_lf = cc2.number_input("Blade SAR/m", 12.0), cc2.number_input("Blade Life(k)", 500)
    es_pr, es_lf = cc3.number_input("EndSeal SAR", 150.0), cc3.number_input("EndSeal Hrs", 72)

# --- TAB 4 ---
with tabs[3]:
    ch1, ch2, ch3, ch4 = st.columns(4)
    eng, eng_s = ch1.number_input("Eng Qty", 3), ch1.number_input("Eng Sal", 8000)
    opr, opr_s = ch2.number_input("Op Qty", 6), ch2.number_input("Op Sal", 4500)
    wrk, wrk_s = ch3.number_input("Worker Qty", 8), ch3.number_input("Worker Sal", 2500)
    adm, adm_s = ch4.number_input("Admin Qty", 5), ch4.number_input("Admin Sal", 8000)
    st.markdown("---")
    c_p1, c_p2 = st.columns(2)
    admin_exp = c_p1.number_input("Monthly Admin Exp", 40000)
    c_p2.metric("Annual Power Cost", f"SAR {pwr_cost:,.0f}")
    payroll = (eng*eng_s) + (opr*opr_s) + (wrk*wrk_s) + (adm*adm_s)

# --- TAB 5 ---
with tabs[4]:
    c_c1, c_c2, c_c3 = st.columns(3)
    w_ink, i_loss, a_gsm = c_c1.number_input("Wet Ink", 5.0), c_c2.number_input("Ink Loss%", 40), c_c3.number_input("Adh GSM", 1.8)
    d_ink = w_ink * (1 - i_loss/100)
    tgt_tons = st.number_input("Target Tons", 3600)
    
    df_rec = st.data_editor(pd.DataFrame([
        {"Product":"1 Lyr","L1":"BOPP","M1":38,"L2":"None","M2":0,"L3":"None","M3":0,"Mix%":60,"Price":12.0},
        {"Product":"2 Lyr","L1":"BOPP","M1":20,"L2":"BOPP","M2":20,"L3":"None","M3":0,"Mix%":30,"Price":13.0},
        {"Product":"3 Lyr","L1":"PET","M1":12,"L2":"ALU","M2":7,"L3":"PE","M3":50,"Mix%":10,"Price":15.0}
    ]), num_rows="dynamic", use_container_width=True)
    
    w_gsm = w_rmc = w_sp = l_mix = t_ink = t_slv = t_adh = 0
    dets = []
    
    for _, r in df_rec.iterrows():
        g1, g2, g3 = r["M1"]*mat_db[r["L1"]]["d"], r["M2"]*mat_db[r["L2"]]["d"], r["M3"]*mat_db[r["L3"]]["d"]
        lp = (1 if r["M2"]>0 else 0) + (1 if r["M3"]>0 else 0)
        ag = lp * a_gsm; tg = g1+g2+g3+d_ink+ag
        c1, c2, c3 = (g1/1000)*mat_db[r["L1"]]["p"], (g2/1000)*mat_db[r["L2"]]["p"], (g3/1000)*mat_db[r["L3"]]["p"]
        ca, ci, cs = (ag/1000)*adh_p, (w_ink/1000)*ink_p, (w_ink*0.5/1000)*solv_p
        cpk = (c1+c2+c3+ca+ci+cs)/(tg/1000) if tg>0 else 0
        r_ton = tgt_tons * (r["Mix%"]/100)
        if tg>0:
            sq = (r_ton*1000000)/tg
            t_ink += (sq*w_ink)/1000; t_slv += (sq*w_ink*0.5)/1000; t_adh += (sq*ag)/1000
        
        mr = r["Mix%"]/100
        w_gsm += tg*mr; w_rmc += cpk*mr; w_sp += r["Price"]*mr
        if lp>0: l_mix += mr
        dets.append({"Product":r["Product"],"Tons":r_ton,"Final GSM":round(tg,1),"Cost/Kg":round(cpk,2),"Margin":round(r["Price"]-cpk,2)})
        
    st.dataframe(pd.DataFrame(dets), use_container_width=True)
    c_k1, c_k2, c_k3 = st.columns(3)
    c_k1.metric("Ink (Kg/Mo)", f"{t_ink/12:,.0f}"); c_k2.metric("Solv (Kg/Mo)", f"{t_slv/12:,.0f}"); c_k3.metric("Adh (Kg/Mo)", f"{t_adh/12:,.0f}")
    
    fx_max, sl_max = (f_sqm*w_gsm)/1000000, (s_sqm*w_gsm)/1000000
    lm_max = (l_sqm*w_gsm)/1000000/l_mix if l_mix>0 else 999999
    
    cb1, cb2, cb3 = st.columns(3)
    cb1.success(f"Flexo Max: {fx_max:,.0f} T") if tgt_tons<=fx_max else cb1.error(f"Flexo Max: {fx_max:,.0f} T")
    cb2.success(f"Lam Max: {lm_max:,.0f} T") if tgt_tons<=lm_max else cb2.error(f"Lam Max: {lm_max:,.0f} T")
    cb3.success(f"Slit Max: {sl_max:,.0f} T") if tgt_tons<=sl_max else cb3.error(f"Slit Max: {sl_max:,.0f} T")

# --- CALCS & TABS 6/7 ---
tot_rev = tgt_tons * 1000 * w_sp
a_rm = tgt_tons * 1000 * w_rmc
esm = tgt_tons * (1000/w_gsm) * 1000 if w_gsm>0 else 0
a_cons = ((esm/(an_lf*1000000))*an_pr*8 if an_lf>0 else 0) + ((esm/(bl_lf*1000))*bl_pr*8 if bl_lf>0 else 0) + ((net_run_hrs/es_lf)*es_pr*8 if es_lf>0 else 0)
a_hr = (payroll + admin_exp) * 12
t_opex = a_rm + a_cons + a_hr + pwr_cost
n_prof = tot_rev - t_opex
pbk = total_capex/n_prof if n_prof>0 else 0
atr = tot_rev/total_capex if total_capex>0 else 0
roi = (n_prof/total_capex)*100 if total_capex>0 else 0

with tabs[5]:
    cr1, cr2, cr3, cr4 = st.columns(4)
    cr1.metric("Rev", f"{tot_rev:,.0f}"); cr2.metric("OPEX", f"{t_opex:,.0f}"); cr3.metric("Profit", f"{n_prof:,.0f}"); cr4.metric("Payback", f"{pbk:.1f}y")
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        pd.DataFrame({"Metric":["CAPEX","Tons","Rev","OPEX","Profit","ROI%","Payback"],"Val":[total_capex,tgt_tons,tot_rev,t_opex,n_prof,f"{roi:.1f}%",pbk]}).to_excel(w,sheet_name='1.Exec',index=False)
        pd.DataFrame({"Metric":["Net Hrs","Tons","Flexo Max","Lam Max","Slit Max"],"Val":[net_run_hrs,tgt_tons,fx_max,lm_max,sl_max]}).to_excel(w,sheet_name='2.Ops',index=False)
        pd.DataFrame(dets).to_excel(w,sheet_name='3.Mix',index=False)
        pd.DataFrame({"Item":["Mats","Consumables","HR","Admin","Power"],"SAR":[a_rm,a_cons,payroll*12,admin_exp*12,pwr_cost]}).to_excel(w,sheet_name='4.OPEX',index=False)
        pd.DataFrame({"Chem":["Ink","Solvent","Adhesive"],"Mo Kg":[t_ink/12,t_slv/12,t_adh/12],"Yr Kg":[t_ink,t_slv,t_adh]}).to_excel(w,sheet_name='5.Chem',index=False)
    st.download_button("📥 Excel Report", buf.getvalue(), "NexFlexo.xlsx", "application/vnd.ms-excel", use_container_width=True)

with tabs[6]:
    ct1, ct2, ct3 = st.columns(3)
    ct1.metric("Turnover", f"SAR {tot_rev:,.0f}"); ct2.metric("Asset Turn", f"{atr:.2f}x"); ct3.metric("ROI", f"{roi:.1f}%")
    st.markdown("---")
    cq1, cq2 = st.columns(2)
    cn = cq1.text_input("Customer", "Valued Client")
    sr = cq2.selectbox("Product", [i["Product"] for i in dets])
    sc, sg = next(((i["Cost/Kg"], i["Final GSM"]) for i in dets if i["Product"]==sr), (0,0))
    mp = cq1.number_input("Margin %", 5, 100, 20)
    if st.button("Generate Offer"):
        st.info(f"**To:** {cn}\n\n**Product:** {sr} ({sg} g/m²)\n\n**Price/Kg:** SAR {sc*(1+mp/100):.2f}\n\n*Waheed Waleed Malik, NexFlexo*")
