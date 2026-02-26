import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Flexo Smart Plant", layout="wide")

st.title("🏭 Flexo Smart Plant Simulator")
st.markdown("---")

tabs = st.tabs([
    "1. Raw Materials", 
    "2. Production (OEE)", 
    "3. Consumables", 
    "4. HR & OPEX", 
    "5. Recipes & Line Balance", 
    "6. P&L Dashboard"
])

# ==========================================
# 1. Raw Materials Master Data
# ==========================================
with tabs[0]:
    st.header("Raw Materials (Price & Density)")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        p_bopp = st.number_input("BOPP Price/Kg", 6.0)
        d_bopp = st.number_input("BOPP Density (g/cm3)", 0.91)
    with c2: 
        p_pet = st.number_input("PET Price/Kg", 5.5)
        d_pet = st.number_input("PET Density (g/cm3)", 1.40)
    with c3: 
        p_pe = st.number_input("PE Price/Kg", 5.0)
        d_pe = st.number_input("PE Density (g/cm3)", 0.92)
    with c4: 
        p_alu = st.number_input("ALU Price/Kg", 18.0)
        d_alu = st.number_input("ALU Density (g/cm3)", 2.70)

    mat_db = {
        "BOPP": {"p": p_bopp, "d": d_bopp},
        "PET": {"p": p_pet, "d": d_pet},
        "PE": {"p": p_pe, "d": d_pe},
        "ALU": {"p": p_alu, "d": d_alu},
        "None": {"p": 0.0, "d": 0.0}
    }
    
    st.markdown("---")
    ci1, ci2 = st.columns(2)
    ink_price = ci1.number_input("Ink Price/Kg", 15.0)
    adhesive_price = ci2.number_input("Adhesive Price/Kg", 12.0)

# ==========================================
# 2. Production & OEE (Machines Capacity)
# ==========================================
with tabs[1]:
    st.header("Production Capacity & OEE")
    
    # Working Schedule
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.subheader("Working Schedule")
        work_days = st.number_input("Working Days/Year", 300)
        shifts_day = st.number_input("Shifts/Day", 2)
        hrs_shift = st.number_input("Hours/Shift", 12)
        total_avail_hrs = work_days * shifts_day * hrs_shift
    with col_w2:
        st.subheader("Changeovers (Downtime)")
        jobs_month = st.number_input("Jobs/Month", 60)
        hrs_per_changeover = st.number_input("Hours/Changeover", 1.0)
        total_downtime = (jobs_month * 12) * hrs_per_changeover
        net_running_hrs = total_avail_hrs - total_downtime

    st.success(f"Available: {total_avail_hrs} Hrs | Downtime: {total_downtime} Hrs | Net Running: {net_running_hrs} Hrs")
    st.markdown("---")
    
    # Individual Machine Capacities
    st.header("Machines Speeds & Output (Area)")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.subheader("1. Flexo CI")
        f_speed = st.number_input("Flexo Speed (m/min)", 300)
        f_width = st.number_input("Flexo Web Width (m)", 1.0)
        f_price = st.number_input("Flexo Price (SAR)", 8000000)
        
        f_lin_m = net_running_hrs * 60 * f_speed
        f_sq_m = f_lin_m * f_width
        st.info(f"📏 Linear: {f_lin_m:,.0f} m\n\n🔲 Area: {f_sq_m:,.0f} Sq.m")

    with m2:
        st.subheader("2. Lamination")
        l_speed = st.number_input("Lam Speed (m/min)", 250)
        l_width = st.number_input("Lam Web Width (m)", 1.0)
        l_price = st.number_input("Lam Price (SAR)", 1200000)
        
        l_lin_m = net_running_hrs * 60 * l_speed
        l_sq_m = l_lin_m * l_width
        st.info(f"📏 Linear: {l_lin_m:,.0f} m\n\n🔲 Area: {l_sq_m:,.0f} Sq.m")

    with m3:
        st.subheader("3. Slitter")
        s_speed = st.number_input("Slitter Speed (m/min)", 400)
        s_width = st.number_input("Slitter Web Width (m)", 1.0)
        s_price = st.number_input("Slitter Price (SAR)", 800000)
        
        s_lin_m = net_running_hrs * 60 * s_speed
        s_sq_m = s_lin_m * s_width
        st.info(f"📏 Linear: {s_lin_m:,.0f} m\n\n🔲 Area: {s_sq_m:,.0f} Sq.m")

    total_capex = f_price + l_price + s_price + 500000 

# ==========================================
# 3. Consumables
# ==========================================
with tabs[2]:
    st.header("Consumables")
    cc1, cc2, cc3 = st.columns(3)
    
    with cc1:
        anilox_price = st.number_input("Anilox Roller Price", 15000)
        anilox_life = st.number_input("Anilox Life (Million m)", 200)
    with cc2:
        blade_price = st.number_input("Doctor Blade Price/m", 12.0)
        blade_life = st.number_input("Blade Life (1000 m)", 500)
    with cc3:
        endseal_price = st.number_input("End Seals Price", 150.0)
        endseal_life = st.number_input("End Seals Life (Hrs)", 72)

# ==========================================
# 4. HR & OPEX
# ==========================================
with tabs[3]:
    st.header("HR & Admin (OPEX)")
    ch1, ch2, ch3 = st.columns(3)
    
    with ch1:
        engineers = st.number_input("Engineers Qty", 3)
        eng_salary = st.number_input("Engineer Salary", 8000)
    with ch2:
        operators = st.number_input("Operators Qty", 6)
        op_salary = st.number_input("Operator Salary", 4500)
    with ch3:
        admin_sales = st.number_input("Admin & Sales Qty", 5)
        as_salary = st.number_input("Admin/Sales Salary", 8000)
        
    st.markdown("---")
    admin_expenses = st.number_input("Monthly Admin Expenses (Rent, etc.)", 40000)
    power_cost_annual = st.number_input("Annual Power Cost", 400000)
    monthly_payroll = (engineers*eng_salary) + (operators*op_salary) + (admin_sales*as_salary)

# ==========================================
# 5. Recipes & Line Balance (Bottleneck Check)
# ==========================================
with tabs[4]:
    st.header("Recipes & Production Mix")
    st.info("💡 The system calculates exact GSM, then checks if your machines can handle the target Tons.")
    
    target_sales_tons = st.number_input("Target Annual Sales (Tons)", 1200)
    
    recipe_data = [
        {"Structure": "1 Layer (Label)", "L1": "BOPP", "Mic_1": 38, "L2": "None", "Mic_2": 0, "L3": "None", "Mic_3": 0, "Mix_%": 60, "Sell_Price": 12.0},
        {"Structure": "2 Layers (Snacks)", "L1": "BOPP", "Mic_1": 20, "L2": "BOPP", "Mic_2": 20, "L3": "None", "Mic_3": 0, "Mix_%": 30, "Sell_Price": 13.0},
        {"Structure": "3 Layers (Pouch)", "L1": "PET", "Mic_1": 12, "L2": "ALU", "Mic_2": 7, "L3": "PE", "Mic_3": 50, "Mix_%": 10, "Sell_Price": 15.0}
    ]
    df_recipes = st.data_editor(pd.DataFrame(recipe_data), num_rows="dynamic", use_container_width=True)
    
    if df_recipes["Mix_%"].sum() != 100:
        st.error("⚠️ Mix % must equal exactly 100%!")
    
    weighted_avg_gsm = 0
    weighted_avg_rm_cost = 0 
    weighted_avg_sell_price = 0
    lamination_mix_ratio = 0 # To track how much % actually goes to Lamination
    
    details = []

    for idx, row in df_recipes.iterrows():
        gsm1 = row["Mic_1"] * mat_db[row["L1"]]["d"]
        gsm2 = row["Mic_2"] * mat_db[row["L2"]]["d"]
        gsm3 = row["Mic_3"] * mat_db[row["L3"]]["d"]

        lam_passes = 0
        if row["L2"] != "None" and row["Mic_2"] > 0: lam_passes += 1
        if row["L3"] != "None" and row["Mic_3"] > 0: lam_passes += 1
        
        adh_gsm = lam_passes * 2.0 
        ink_gsm = 3.0 
        total_gsm = gsm1 + gsm2 + gsm3 + adh_gsm + ink_gsm
        
        c1 = (gsm1/1000) * mat_db[row["L1"]]["p"]
        c2 = (gsm2/1000) * mat_db[row["L2"]]["p"]
        c3 = (gsm3/1000) * mat_db[row["L3"]]["p"]
        c_adh = (adh_gsm/1000) * adhesive_price
        c_ink = (ink_gsm/1000) * ink_price
        
        total_cost_m2 = c1 + c2 + c3 + c_adh + c_ink
        cost_per_kg = total_cost_m2 / (total_gsm / 1000) if total_gsm > 0 else 0
        
        mix_ratio = row["Mix_%"] / 100
        weighted_avg_gsm += total_gsm * mix_ratio
        weighted_avg_rm_cost += cost_per_kg * mix_ratio
        weighted_avg_sell_price += row["Sell_Price"] * mix_ratio
        
        if lam_passes > 0:
            lamination_mix_ratio += mix_ratio

        details.append({
            "Structure": row["Structure"],
            "Target (Tons)": target_sales_tons * mix_ratio,
            "GSM": round(total_gsm, 1),
            "Cost (SAR/Kg)": round(cost_per_kg, 2),
            "Margin (SAR/Kg)": round(row["Sell_Price"] - cost_per_kg, 2)
        })

    st.dataframe(pd.DataFrame(details), use_container_width=True)
    total_revenue = target_sales_tons * weighted_avg_sell_price * 1000

    # ==========================================
    # BOTTLENECK ANALYSIS (Line Balancing)
    # ==========================================
    st.markdown("---")
    st.subheader("🚦 Line Balancing & Bottleneck Check")
    st.write("Does your machine capacity support the Target Sales based on this specific Mix?")
    
    # Calculate Max Tons each machine can produce based on this specific mix GSM
    flexo_max_tons = (f_sq_m * weighted_avg_gsm) / 1000000
    slit_max_tons = (s_sq_m * weighted_avg_gsm) / 1000000
    
    # Lamination Max Equivalent Plant Tons (It only processes the laminated %)
    if lamination_mix_ratio > 0:
        lam_max_tons = (l_sq_m * weighted_avg_gsm) / 1000000 / lamination_mix_ratio
    else:
        lam_max_tons = 9999999 # Unlimited if 0% laminated products

    cb1, cb2, cb3 = st.columns(3)
    
    def render_capacity(col, name, max_tons, target):
        if target > max_tons:
            col.error(f"❌ **{name}**\n\nMax: {max_tons:,.0f} T\n\n*(OVERLOAD)*")
        else:
            col.success(f"✅ **{name}**\n\nMax: {max_tons:,.0f} T\n\n*(OK)*")

    render_capacity(cb1, "Flexo Capability", flexo_max_tons, target_sales_tons)
    render_capacity(cb2, "Lamination Capability", lam_max_tons, target_sales_tons)
    render_capacity(cb3, "Slitter Capability", slit_max_tons, target_sales_tons)
    
    plant_bottleneck = min(flexo_max_tons, lam_max_tons, slit_max_tons)
    if target_sales_tons > plant_bottleneck:
        st.warning(f"⚠️ **Action Required:** Your target is {target_sales_tons} T, but your bottleneck limits the plant to **{plant_bottleneck:,.0f} T**. You need to increase shifts, increase machine speed, or change the sales mix!")

# ==========================================
# 6. P&L Dashboard & Excel
# ==========================================
with tabs[5]:
    st.header("P&L Dashboard")
    
    annual_raw_mat = target_sales_tons * 1000 * weighted_avg_rm_cost
    est_annual_meters = target_sales_tons * (1000 / weighted_avg_gsm) * 1000 if weighted_avg_gsm > 0 else 0 
    
    annual_anilox = (est_annual_meters / (anilox_life * 1000000)) * anilox_price * 8 if anilox_life > 0 else 0
    annual_blade = (est_annual_meters / (blade_life * 1000)) * blade_price * 8 if blade_life > 0 else 0
    annual_endseals = (net_running_hrs / endseal_life) * endseal_price * 8 if endseal_life > 0 else 0
    
    annual_consumables = annual_anilox + annual_blade + annual_endseals + (target_sales_tons * 200)
    annual_hr_admin = (monthly_payroll + admin_expenses) * 12
    
    total_cogs_opex = annual_raw_mat + annual_consumables + annual_hr_admin + power_cost_annual
    net_profit = total_revenue - total_cogs_opex
    payback = total_capex / net_profit if net_profit > 0 else 0

    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    col_res1.metric("Revenue (SAR)", f"{total_revenue:,.0f}")
    col_res2.metric("Total OPEX (SAR)", f"{total_cogs_opex:,.0f}")
    col_res3.metric("Net Profit (SAR)", f"{net_profit:,.0f}")
    col_res4.metric("Payback (Years)", f"{payback:.1f}")
    
    cost_data = pd.DataFrame({
        "Item": ["Raw Material", "Consumables", "HR & Admin", "Power"],
        "Value": [annual_raw_mat, annual_consumables, annual_hr_admin, power_cost_annual]
    })
    fig = px.pie(cost_data, values="Value", names="Item", title="OPEX Breakdown", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        workbook = writer.book
        ws = workbook.add_worksheet('P&L')
        
        fmt_head = workbook.add_format({'bold': True, 'bg_color': '#1F4E78', 'font_color': 'white', 'border': 1})
        fmt_money = workbook.add_format({'num_format': '#,##0', 'border': 1})
        
        ws.write('A1', 'Item', fmt_head)
        ws.write('B1', 'Amount (SAR)', fmt_head)
        
        data_to_excel = [
            ("Total Target Sales (Tons)", target_sales_tons),
            ("Total Revenue", total_revenue),
            ("Raw Materials Cost", annual_raw_mat),
            ("Consumables (Anilox, Blades, Seals)", annual_consumables),
            ("Payroll (HR)", monthly_payroll * 12),
            ("Admin & Rent", admin_expenses * 12),
            ("Power Cost", power_cost_annual),
            ("Net Profit", net_profit),
            ("Total CAPEX", total_capex)
        ]
        
        for row_num, (item, val) in enumerate(data_to_excel, start=1):
            ws.write(row_num, 0, item, fmt_money)
            ws.write(row_num, 1, val, fmt_money)
            
        ws.set_column('A:A', 35)
        ws.set_column('B:B', 20)

    st.download_button(
        label="📥 Download P&L (Excel)",
        data=buffer.getvalue(),
        file_name="Flexo_Plant_PNL.xlsx",
        mime="application/vnd.ms-excel",
        use_container_width=True
    )
