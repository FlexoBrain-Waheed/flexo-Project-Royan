import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Flexo Smart Plant", layout="wide")

st.title("🏭 Flexo Smart Plant Simulator")
st.markdown("---")

tabs = st.tabs([
    "1. Raw Materials", 
    "2. Production & OEE", 
    "3. Consumables", 
    "4. HR & OPEX", 
    "5. Sales Mix", 
    "6. P&L Dashboard"
])

# ==========================================
# 1. Raw Materials
# ==========================================
with tabs[0]:
    st.header("Raw Materials (Price & Density)")
    
    mat_data = [
        {"Material": "BOPP", "Density (g/cm3)": 0.91, "Price/Kg": 6.0},
        {"Material": "PET", "Density (g/cm3)": 1.40, "Price/Kg": 5.5},
        {"Material": "PE", "Density (g/cm3)": 0.92, "Price/Kg": 5.0}
    ]
    st.info("Edit prices and densities directly in the table below:")
    df_mat = st.data_editor(pd.DataFrame(mat_data), use_container_width=True)
    
    avg_price_kg = df_mat["Price/Kg"].mean()
    avg_raw_mat_cost_ton = avg_price_kg * 1000 
    
    st.markdown("---")
    c_ink1, c_ink2 = st.columns(2)
    ink_price = c_ink1.number_input("Ink Price/Kg", value=15.0)
    adhesive_price = c_ink2.number_input("Solventless Adhesive Price/Kg", value=12.0)

# ==========================================
# 2. Production & OEE
# ==========================================
with tabs[1]:
    st.header("Production Capacity & OEE")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Working Schedule")
        work_days = st.number_input("Working Days/Year", value=300)
        shifts_day = st.number_input("Shifts/Day", value=2)
        hrs_shift = st.number_input("Hours/Shift", value=12)
        total_avail_hrs = work_days * shifts_day * hrs_shift
        
    with col2:
        st.subheader("Changeovers (Downtime)")
        jobs_month = st.number_input("Jobs/Month", value=60)
        hrs_per_changeover = st.number_input("Hours/Changeover", value=1.0)
        total_downtime = (jobs_month * 12) * hrs_per_changeover
        net_running_hrs = total_avail_hrs - total_downtime
        
    with col3:
        st.subheader("Machine Specs")
        flexo_speed = st.number_input("Avg Speed (m/min)", value=300)
        web_width = st.number_input("Avg Web Width (meter)", value=1.0)
        avg_gsm = st.number_input("Avg Structure Weight (GSM)", value=60)
        
    annual_linear_meters = net_running_hrs * 60 * flexo_speed
    annual_sqm = annual_linear_meters * web_width
    annual_tons_capacity = (annual_sqm * avg_gsm) / 1000000

    st.success(f"Total Available: {total_avail_hrs} Hrs | Total Downtime: {total_downtime} Hrs | Net Running: {net_running_hrs} Hrs")
    st.info(f"Max Production Capacity: {annual_tons_capacity:,.0f} Tons/Year")
    
    st.markdown("---")
    st.subheader("CAPEX (Machines Investment)")
    cm1, cm2, cm3 = st.columns(3)
    flexo_price = cm1.number_input("Flexo CI Price", value=8000000)
    lam_price = cm2.number_input("Lamination (Solventless) Price", value=1200000)
    slit_price = cm3.number_input("Slitter Price", value=800000)
    total_capex = flexo_price + lam_price + slit_price + 500000 

# ==========================================
# 3. Consumables
# ==========================================
with tabs[2]:
    st.header("Consumables")
    cc1, cc2, cc3 = st.columns(3)
    
    with cc1:
        anilox_price = st.number_input("Anilox Roller Price", value=15000)
        anilox_life = st.number_input("Anilox Life (Million m)", value=200)
    with cc2:
        blade_price = st.number_input("Doctor Blade Price/m", value=12.0)
        blade_life = st.number_input("Blade Life (1000 m)", value=500)
    with cc3:
        endseal_price = st.number_input("End Seals Price", value=150.0)
        endseal_life = st.number_input("End Seals Life (Hrs)", value=72)

# ==========================================
# 4. HR & OPEX
# ==========================================
with tabs[3]:
    st.header("HR & Admin (OPEX)")
    ch1, ch2, ch3 = st.columns(3)
    
    with ch1:
        engineers = st.number_input("Engineers Qty", value=3)
        eng_salary = st.number_input("Engineer Salary", value=8000)
    with ch2:
        operators = st.number_input("Operators Qty", value=6)
        op_salary = st.number_input("Operator Salary", value=4500)
    with ch3:
        admin_sales = st.number_input("Admin & Sales Qty", value=5)
        as_salary = st.number_input("Admin/Sales Salary", value=8000)
        
    st.markdown("---")
    admin_expenses = st.number_input("Monthly Admin Expenses (Rent, etc.)", value=40000)
    power_cost_annual = st.number_input("Annual Power Cost", value=400000)
    
    monthly_payroll = (engineers*eng_salary) + (operators*op_salary) + (admin_sales*as_salary)

# ==========================================
# 5. Sales Mix
# ==========================================
with tabs[4]:
    st.header("Sales Mix & Revenue")
    
    client_data = [
        {"Structure": "1 Layer", "Mix %": 60, "Price/Kg": 12.0},
        {"Structure": "2 Layers", "Mix %": 30, "Price/Kg": 13.0},
        {"Structure": "3 Layers", "Mix %": 10, "Price/Kg": 15.0}
    ]
    df_mix = st.data_editor(pd.DataFrame(client_data), use_container_width=True)
    
    target_sales_tons = st.number_input("Target Annual Sales (Tons)", value=1200)
    
    if target_sales_tons > annual_tons_capacity:
        st.error(f"Warning: Sales Target ({target_sales_tons} T) exceeds Machine Capacity ({annual_tons_capacity:,.0f} T)!")
        
    weighted_avg_price = sum((row["Mix %"] / 100) * row["Price/Kg"] for index, row in df_mix.iterrows()) * 1000
    total_revenue = target_sales_tons * weighted_avg_price

# ==========================================
# 6. P&L Dashboard & Excel
# ==========================================
with tabs[5]:
    st.header("P&L Dashboard")
    
    annual_raw_mat = target_sales_tons * avg_raw_mat_cost_ton
    est_annual_meters = target_sales_tons * (1000 / avg_gsm) * 1000 if avg_gsm > 0 else 0 
    
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
