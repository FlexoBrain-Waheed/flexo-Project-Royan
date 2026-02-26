import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="NexFlexo Smart Plant", layout="wide")
st.title("🏭 NexFlexo Smart Plant Simulator")
st.markdown("---")

tabs = st.tabs([
    "1. Raw Materials", "2. Production (OEE)", "3. Consumables", 
    "4. HR & OPEX", "5. Recipes", "6. P&L Dashboard", "7. Commercial"
])

# --- TAB 1 ---
with tabs[0]:
    st.header("Raw Materials (Price & Density)")
    c1, c2, c3, c4 = st.columns(4)
    p_bopp = c1.number_input("BOPP Price/Kg", 6.0)
    d_bopp = c1.number_input("BOPP Density", 0.91)
    p_pet = c2.number_input("PET Price/Kg", 5.5)
    d_pet = c2.number_input("PET Density", 1.40)
    p_pe = c3.number_input("PE Price/Kg", 5.0)
    d_pe = c3.number_input("PE Density", 0.92)
    p_alu = c4.number_input("ALU Price/Kg", 18.0)
    d_alu = c4.number_input("ALU Density", 2.70)

    mat_db = {
        "BOPP": {"p": p_bopp, "d": d_bopp},
        "PET": {"p": p_pet, "d": d_pet},
        "PE": {"p": p_pe, "d": d_pe},
        "ALU": {"p": p_alu, "d": d_alu},
        "None": {"p": 0.0, "d": 0.0}
    }
    
    st.markdown("---")
    ci1, ci2, ci3 = st.columns(3)
    ink_price = ci1.number_input("Ink Price/Kg", 15.0)
    solvent_price = ci2.number_input("Solvent Price/Kg", 6.0)
    adhesive_price = ci3.number_input("Adhesive Price/Kg", 12.0)

# --- TAB 2 ---
with tabs[1]:
    st.header("Production Capacity & OEE")
    col_w1, col_w2 = st.columns(2)
    work_days = col_w1.number_input("Working Days/Year", 300)
    shifts_day = col_w1.number_input("Shifts/Day", 2)
    hrs_shift = col_w1.number_input("Hours/Shift", 12)
    total_avail_hrs = work_days * shifts_day * hrs_shift
    
    jobs_month = col_w2.number_input("Jobs/Month", 60)
    hrs_per_changeover = col_w2.number_input("Hours/Changeover", 1.0)
    total_downtime = (jobs_month * 12) * hrs_per_changeover
    net_running_hrs = total_avail_hrs - total_downtime

    st.success(f"Available: {total_avail_hrs} Hrs | Net Running: {net_running_hrs} Hrs")
    st.markdown("---")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.subheader("1. Flexo CI")
        f_speed = st.number_input("Flexo Speed (m/min)", 300)
        f_width = st.number_input("Flexo Web Width (m)", 1.0)
        f_eff = st.slider("Flexo Efficiency %", 40, 100, 70)
        f_price = st.number_input("Flexo Price (SAR)", 8000000)
        f_lin_m = net_running_hrs * 60 * f_speed * (f_eff / 100)
        f_sq_m = f_lin_m * f_width
        st.info(f"📏 Linear: {f_lin_m:,.0f} m\n🔲 Area: {f_sq_m:,.0f} Sq.m")

    with m2:
        st.subheader("2. Lamination")
        l_speed = st.number_input("Lam Speed (m/min)", 250)
        l_width = st.number_input("Lam Web Width (m)", 1.0)
        l_eff = st.slider("Lam Efficiency %", 40, 100, 75)
        l_price = st.number_input("Lam Price (SAR)", 1200000)
        l_lin_m = net_running_hrs * 60 * l_speed * (l_eff / 100)
        l_sq_m = l_lin_m * l_width
        st.info(f"📏 Linear: {l_lin_m:,.0f} m\n🔲 Area: {l_sq_m:,.0f} Sq.m")

    with m3:
        st.subheader("3. Slitter")
        s_speed = st.number_input("Slitter Speed (m/min)", 400)
        s_width = st.number_input("Slitter Web Width (m)", 1.0)
        s_eff = st.slider("Slitter Efficiency %", 40, 100, 80)
        s_price = st.number_input("Slitter Price (SAR)", 800000)
        s_lin_m = net_running_hrs * 60 * s_speed * (s_eff / 100)
        s_sq_m = s_lin_m * s_width
        st.info(f"📏 Linear: {s_lin_m:,.0f} m\n🔲 Area: {s_sq_m:,.0f} Sq.m")

    total_capex = f_price + l_price + s_price + 500000 

# --- TAB 3 ---
with tabs[2]:
    st.header("Consumables")
    cc1, cc2, cc3 = st.columns(3)
    anilox_price = cc1.number_input("Anilox Roller Price", 15000)
    anilox_life = cc1.number_input("Anilox Life (Million m)", 200)
    blade_price = cc2.number_input("Doctor Blade Price/m", 12.0)
    blade_life = cc2.number_input("Blade Life (1000 m)", 500)
    endseal_price = cc3.number_input("End Seals Price", 150.0)
    endseal_life = cc3.number_input("End Seals Life (Hrs)", 72)

# --- TAB 4 ---
with tabs[3]:
    st.header("HR & Admin (OPEX)")
    ch1, ch2, ch3 = st.columns(3)
    engineers = ch1.number_input("Engineers Qty", 3)
    eng_salary = ch1.number_input("Engineer Salary", 8000)
    operators = ch2.number_input("Operators Qty", 6)
    op_salary = ch2.number_input("Operator Salary", 4500)
    admin_sales = ch3.number_input("Admin & Sales Qty", 5)
    as_salary = ch3.number_input("Admin/Sales Salary", 8000)
    
    st.markdown("---")
    admin_expenses = st.number_input("Monthly Admin Expenses", 40000)
    power_cost_annual = st.number_input("Annual Power Cost", 400000)
    monthly_payroll = (engineers*eng_salary) + (operators*op_salary) + (admin_sales*as_salary)

# --- TAB 5 ---
with tabs[4]:
    st.header("Recipes & Production Mix")
    col_c1, col_c2, col_c3 = st.columns(3)
    wet_ink_gsm = col_c1.number_input("Wet Ink Applied (g/m²)", value=5.0)
    ink_loss_percent = col_c2.number_input("Ink Evaporation Loss %", value=40)
    adh_gsm_per_pass = col_c3.number_input("Adhesive per Lam Pass", value=1.8)
    
    dry_ink_gsm = wet_ink_gsm * (1 - (ink_loss_percent / 100))
    solvent_ratio = 0.5 
    
    st.markdown("---")
    target_sales_tons = st.number_input("Target Annual Sales (Tons)", 1200)
    
    recipe_data = [
        {"Structure": "1 Layer", "L1": "BOPP", "Mic_1": 38, "L2": "None", "Mic_2": 0, "L3": "None", "Mic_3": 0, "Mix_%": 60, "Sell_Price": 12.0},
        {"Structure": "2 Layers", "L1": "BOPP", "Mic_1": 20, "L2": "BOPP", "Mic_2": 20, "L3": "None", "Mic_3": 0, "Mix_%": 30, "Sell_Price": 13.0},
        {"Structure": "3 Layers", "L1": "PET", "Mic_1": 12, "L2": "ALU", "Mic_2": 7, "L3": "PE", "Mic_3": 50, "Mix_%": 10, "Sell_Price": 15.0}
    ]
    df_recipes = st.data_editor(pd.DataFrame(recipe_data), num_rows="dynamic", use_container_width=True)
    
    weighted_avg_gsm = 0
    weighted_avg_rm_cost = 0 
    weighted_avg_sell_price = 0
    lamination_mix_ratio = 0 
    
    total_annual_ink_kg = 0
    total_annual_solv_kg = 0
    total_annual_adh_kg = 0
    
    details = []

    for idx, row in df_recipes.iterrows():
        gsm1 = row["Mic_1"] * mat_db[row["L1"]]["d"]
        gsm2 = row["Mic_2"] * mat_db[row["L2"]]["d"]
        gsm3 = row["Mic_3"] * mat_db[row["L3"]]["d"]
        base_mat_gsm = gsm1 + gsm2 + gsm3

        lam_passes = 0
        if row["L2"] != "None" and row["Mic_2"] > 0: lam_passes += 1
        if row["L3"] != "None" and row["Mic_3"] > 0: lam_passes += 1
        adh_gsm = lam_passes * adh_gsm_per_pass
        
        total_gsm = base_mat_gsm + dry_ink_gsm + adh_gsm
        
        c1 = (gsm1/1000) * mat_db[row["L1"]]["p"]
        c2 = (gsm2/1000) * mat_db[row["L2"]]["p"]
        c3 = (gsm3/1000) * mat_db[row["L3"]]["p"]
        c_adh = (adh_gsm/1000) * adhesive_price
        c_ink = (wet_ink_gsm/1000) * ink_price
        solvent_gsm = wet_ink_gsm * solvent_ratio
        c_solv = (solvent_gsm/1000) * solvent_price 
        
        total_cost_m2 = c1 + c2 + c3 + c_adh + c_ink + c_solv
        cost_per_kg = total_cost_m2 / (total_gsm / 1000) if total_gsm > 0 else 0
        
        recipe_tons = target_sales_tons * (row["Mix_%"] / 100)
        if total_gsm > 0:
            recipe_sqm = (recipe_tons * 1000000) / total_gsm
            total_annual_ink_kg += (recipe_sqm * wet_ink_gsm) / 1000
            total_annual_solv_kg += (recipe_sqm * solvent_gsm) / 1000
            total_annual_adh_kg += (recipe_sqm * adh_gsm) / 1000
        
        mix_ratio = row["Mix_%"] / 100
        weighted_avg_gsm += total_gsm * mix_ratio
        weighted_avg_rm_cost += cost_per_kg * mix_ratio
        weighted_avg_sell_price += row["Sell_Price"] * mix_ratio
        
        if lam_passes > 0: lamination_mix_ratio += mix_ratio

        details.append({
            "Structure": row["Structure"], "Target (Tons)": recipe_tons,
            "Base GSM": round(base_mat_gsm, 1), "Glue GSM": round(adh_gsm, 1),
            "Dry Ink GSM": round(dry_ink_gsm, 1), "Final GSM": round(total_gsm, 1),
            "Cost (SAR/Kg)": round(cost_per_kg, 2), "Margin (SAR/Kg)": round(row["Sell_Price"] - cost_per_kg, 2)
        })

    st.markdown("### 📊 Production Breakdown")
    st.dataframe(pd.DataFrame(details), use_container_width=True)
    total_revenue = target_sales_tons * weighted_avg_sell_price * 1000

    st.markdown("---")
    st.subheader("💧 Monthly Chemical Consumption")
    col_chem1, col_chem2, col_chem3 = st.columns(3)
    col_chem1.metric("🎨 Wet Ink (Kg/Month)", f"{total_annual_ink_kg / 12:,.0f} Kg")
    col_chem2.metric("🧪 Solvent (Kg/Month)", f"{total_annual_solv_kg / 12:,.0f} Kg")
    col_chem3.metric("🍯 Adhesive (Kg/Month)", f"{total_annual_adh_kg / 12:,.0f} Kg")

    st.markdown("---")
    st.subheader("🚦 Line Balancing & Bottleneck Check")
    flexo_max_tons = (f_sq_m * weighted_avg_gsm) / 1000000
    slit_max_tons = (s_sq_m * weighted_avg_gsm) / 1000000
    lam_max_tons = (l_sq_m * weighted_avg_gsm) / 1000000 / lamination_mix_ratio if lamination_mix_ratio > 0 else 9999999 

    cb1, cb2, cb3 = st.columns(3)
    def render_capacity(col, name, max_tons, target):
        if target > max_tons: col.error(f"❌ **{name}**\n\nMax: {max_tons:,.0f} T")
        else: col.success(f"✅ **{name}**\n\nMax: {max_tons:,.0f} T")

    render_capacity(cb1, "Flexo", flexo_max_tons, target_sales_tons)
    render_capacity(cb2, "Lamination", lam_max_tons, target_sales_tons)
    render_capacity(cb3, "Slitter", slit_max_tons, target_sales_tons)

# --- TAB 6 & 7 (Finance & Quotation) ---
annual_raw_mat = target_sales_tons * 1000 * weighted_avg_rm_cost
est_annual_meters = target_sales_tons * (1000 / weighted_avg_gsm) * 1000 if weighted_avg_gsm > 0 else 0 
annual_anilox = (est_annual_meters / (anilox_life * 1000000)) * anilox_price * 8 if anilox_life > 0 else 0
annual_blade = (est_annual_meters / (blade_life * 1000)) * blade_price * 8 if blade_life > 0 else 0
annual_endseals = (net_running_hrs / endseal_life) * endseal_price * 8 if endseal_life > 0 else 0

annual_consumables = annual_anilox + annual_blade + annual_endseals 
annual_hr_admin = (monthly_payroll + admin_expenses) * 12
total_cogs_opex = annual_raw_mat + annual_consumables + annual_hr_admin + power_cost_annual
net_profit = total_revenue - total_cogs_opex
payback = total_capex / net_profit if net_profit > 0 else 0

asset_turnover = total_revenue / total_capex if total_capex > 0 else 0
roi = (net_profit / total_capex) * 100 if total_capex > 0 else 0

with tabs[5]:
    st.header("P&L Dashboard & Official Report")
    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    col_res1.metric("Revenue (SAR)", f"{total_revenue:,.0f}")
    col_res2.metric("Total OPEX (SAR)", f"{total_cogs_opex:,.0f}")
    col_res3.metric("Net Profit (SAR)", f"{net_profit:,.0f}")
    col_res4.metric("Payback (Years)", f"{payback:.1f}")
    
    # ==========================================
    # SUPER EXCEL GENERATOR (Feasibility Study)
    # ==========================================
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        
        # 1. Executive Summary
        df_exec = pd.DataFrame({
            "Key Financial Indicators": ["Total CAPEX (Investment)", "Annual Target Sales (Tons)", "Annual Revenue", "Total OPEX", "Net Profit", "ROI (%)", "Payback Period (Years)", "Asset Turnover Ratio"],
            "Value": [total_capex, target_sales_tons, total_revenue, total_cogs_opex, net_profit, f"{roi:.1f}%", round(payback, 2), round(asset_turnover, 2)]
        })
        df_exec.to_excel(writer, sheet_name='1. Executive Summary', index=False)
        
        # 2. Operations
        df_ops = pd.DataFrame({
            "Operational Metrics": ["Net Running Hours / Year", "Target Tons", "Flexo Max Capacity (Tons)", "Lam Max Capacity (Tons)", "Slitter Max Capacity (Tons)"],
            "Value": [net_running_hrs, target_sales_tons, flexo_max_tons, lam_max_tons if lamination_mix_ratio > 0 else "No Lam Needed", slit_max_tons]
        })
        df_ops.to_excel(writer, sheet_name='2. Plant Operations', index=False)
        
        # 3. Product Portfolio
        df_mix_export = pd.DataFrame(details)
        df_mix_export.to_excel(writer, sheet_name='3. Product Portfolio', index=False)
        
        # 4. OPEX Breakdown
        df_opex = pd.DataFrame({
            "Expense Category": ["Materials (Films, Ink, Glue, Solvent)", "Consumables (Anilox, Blades, Seals)", "Payroll (HR)", "Admin & Rent", "Power Cost"],
            "Annual Amount (SAR)": [annual_raw_mat, annual_consumables, monthly_payroll * 12, admin_expenses * 12, power_cost_annual]
        })
        df_opex.to_excel(writer, sheet_name='4. OPEX Breakdown', index=False)
        
        # 5. Chemicals Consumption
        df_chem = pd.DataFrame({
            "Chemical": ["Wet Ink", "Solvent", "Adhesive"],
            "Monthly (Kg)": [round(total_annual_ink_kg/12, 1), round(total_annual_solv_kg/12, 1), round(total_annual_adh_kg/12, 1)],
            "Annual (Kg)": [round(total_annual_ink_kg, 1), round(total_annual_solv_kg, 1), round(total_annual_adh_kg, 1)]
        })
        df_chem.to_excel(writer, sheet_name='5. Chemicals', index=False)

        # Formatting Excel nicely
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            worksheet.set_column('A:A', 40)
            worksheet.set_column('B:I', 20)

    st.markdown("---")
    st.info("💡 Download the **Comprehensive Feasibility Report** in Excel. It includes 5 detailed sheets covering Executives, Operations, Products, Costs, and Chemicals.")
    st.download_button(
        label="📥 Download Full Feasibility Report (Excel)", 
        data=buffer.getvalue(), 
        file_name="NexFlexo_Feasibility_Report.xlsx", 
        mime="application/vnd.ms-excel", 
        use_container_width=True
    )

with tabs[6]:
    st.header("Commercial & Turnover")
    
    st.subheader("🔄 1. Financial Turnover Metrics")
    c_t1, c_t2, c_t3 = st.columns(3)
    c_t1.metric("Annual Turnover", f"SAR {total_revenue:,.0f}")
    c_t2.metric("Asset Turnover Ratio", f"{asset_turnover:.2f}x")
    c_t3.metric("ROI", f"{roi:.1f}%")
    
    st.markdown("---")
    st.subheader("📄 2. Smart Quotation Builder")
    
    col_q1, col_q2 = st.columns(2)
    client_name = col_q1.text_input("Customer Name", "Valued Client")
    
    recipe_names = [item["Structure"] for item in details]
    selected_recipe = col_q2.selectbox("Select Product for Quotation", recipe_names)
    
    selected_cost = 0
    selected_gsm = 0
    for item in details:
        if item["Structure"] == selected_recipe:
            selected_cost = item["Cost (SAR/Kg)"]
            selected_gsm = item["Final Total GSM"] if "Final Total GSM" in item else item.get("Final GSM", 0)
            break
            
    margin_pct = col_q1.number_input("Desired Profit Margin (%)", 5, 100, 20)
    quoted_price = selected_cost * (1 + (margin_pct/100))
    
    if st.button("Generate Official Offer"):
        st.markdown("### 🧾 Official Quotation")
        st.info(f'''
        **From:** NexFlexo  
        **To:** {client_name}  
        
        **Product Specifications:** - Structure: {selected_recipe}  
        - Total GSM: {selected_gsm} g/m²  
        
        **Commercial Offer:** - Price per Kg: **SAR {quoted_price:.2f}** *Best Regards,* *Waheed Waleed Malik* *Owner, NexFlexo*
        ''')
