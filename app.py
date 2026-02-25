import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Flexo Smart Plant", layout="wide")

st.title("محاكي مصنع الفلكسو الذكي")
st.markdown("---")

t1 = "1. المواد الخام"
t2 = "2. الماكينات"
t3 = "3. المستهلكات"
t4 = "4. الموارد البشرية"
t5 = "5. مبيعات العميل"
t6 = "6. دراسة الجدوى"

tabs = st.tabs([t1, t2, t3, t4, t5, t6])

# ==========================================
# 1. المواد الخام
# ==========================================
with tabs[0]:
    st.header("تسعير الخامات")
    c1, c2, c3, c4 = st.columns(4)
    price_bopp = c1.number_input("سعر BOPP", value=6.0)
    price_pet = c2.number_input("سعر PET", value=5.5)
    price_pe = c3.number_input("سعر PE", value=5.0)
    price_alu = c4.number_input("سعر ALU", value=18.0)
    
    st.markdown("---")
    ci1, ci2 = st.columns(2)
    ink_price = ci1.number_input("سعر الحبر", value=15.0)
    adhesive_price = ci2.number_input("سعر غراء اللامنيشن", value=12.0)
    
    avg_raw_mat_cost = (price_bopp + price_pet + price_pe) / 3 * 1000

# ==========================================
# 2. خط الإنتاج والماكينات
# ==========================================
with tabs[1]:
    st.header("إعدادات الماكينات")
    col_mac1, col_mac2, col_mac3 = st.columns(3)
    
    with col_mac1:
        st.subheader("ماكينة الفلكسو")
        flexo_price = st.number_input("سعر الفلكسو", value=8000000)
        flexo_speed = st.slider("سرعة الطباعة", 100, 600, 350)
        flexo_kw = st.number_input("طاقة الفلكسو kW", value=150)
        
    with col_mac2:
        st.subheader("ماكينة اللامنيشن")
        lam_price = st.number_input("سعر اللامنيشن", value=1200000)
        lam_speed = st.slider("سرعة اللامنيشن", 100, 500, 300)
        lam_kw = st.number_input("طاقة اللامنيشن kW", value=80)
        
    with col_mac3:
        st.subheader("القطاعة")
        slit_price = st.number_input("سعر القطاعة", value=800000)
        slit_speed = st.slider("سرعة القطاعة", 100, 600, 400)
        slit_kw = st.number_input("طاقة القطاعة kW", value=40)

    total_capex = flexo_price + lam_price + slit_price + 500000
    st.success(f"الاستثمار الكلي: {total_capex:,.0f} ريال")

# ==========================================
# 3. المستهلكات الدقيقة
# ==========================================
with tabs[2]:
    st.header("المستهلكات الفنية")
    cc1, cc2, cc3 = st.columns(3)
    
    with cc1:
        anilox_price = st.number_input("سعر الأنيلوكس", value=15000)
        anilox_life = st.number_input("عمر الأنيلوكس", value=200)
    with cc2:
        blade_price = st.number_input("سعر البليد", value=12.0)
        blade_life = st.number_input("عمر البليد", value=500)
    with cc3:
        endseal_price = st.number_input("سعر الأختام", value=150.0)
        endseal_life = st.number_input("عمر الأختام", value=72)
        
    st.markdown("---")
    c_solv1, c_solv2 = st.columns(2)
    solvent_ratio = c_solv1.number_input("نسبة السولفنت", value=100)
    solvent_price = c_solv2.number_input("سعر السولفنت", value=6.0)
    # ==========================================
# 4. الموارد البشرية والإدارة
# ==========================================
with tabs[3]:
    st.header("الموارد البشرية")
    ch1, ch2 = st.columns(2)
    
    with ch1:
        engineers = st.number_input("مهندسين", value=3)
        eng_salary = st.number_input("راتب المهندس", value=8000)
        operators = st.number_input("فنيين", value=6)
        op_salary = st.number_input("راتب الفني", value=4500)
        
    with ch2:
        sales_team = st.number_input("مبيعات", value=3)
        sales_salary = st.number_input("راتب المبيعات", value=6000)
        admin_staff = st.number_input("إداريين", value=4)
        admin_salary = st.number_input("راتب الإداري", value=10000)
        
    admin_expenses = st.number_input("مصاريف إدارية", value=40000)
    monthly_payroll = (engineers*eng_salary) + (operators*op_salary) + (sales_team*sales_salary) + (admin_staff*admin_salary)

# ==========================================
# 5. المبيعات (هياكل العميل)
# ==========================================
with tabs[4]:
    st.header("محفظة المبيعات")
    
    client_data = [
        {"الفئة": "طبقة", "النسبة": 60, "السعر": 12.0},
        {"الفئة": "طبقتين", "النسبة": 30, "السعر": 13.0},
        {"الفئة": "3 طبقات", "النسبة": 10, "السعر": 15.0},
    ]
    df_mix = st.data_editor(pd.DataFrame(client_data), use_container_width=True)
    target_annual_tons = st.number_input("الهدف السنوي (طن)", value=1500)
    
    weighted_avg_price = sum((row["النسبة"] / 100) * row["السعر"] for index, row in df_mix.iterrows()) * 1000
    total_revenue = target_annual_tons * weighted_avg_price

# ==========================================
# 6. لوحة القيادة المالية (Excel)
# ==========================================
with tabs[5]:
    st.header("دراسة الجدوى")
    
    annual_raw_mat = target_annual_tons * avg_raw_mat_cost
    est_annual_meters = target_annual_tons * 10000 
    
    annual_anilox = (est_annual_meters / (anilox_life * 1000000)) * anilox_price * 8
    annual_blade = (est_annual_meters / (blade_life * 1000)) * blade_price * 8
    annual_endseals = (6000 / endseal_life) * endseal_price * 8
    
    annual_consumables = annual_anilox + annual_blade + annual_endseals + (target_annual_tons * 200)
    annual_hr_admin = (monthly_payroll + admin_expenses) * 12
    annual_power = (flexo_kw + lam_kw + slit_kw) * 6000 * 0.18 
    
    total_cogs_opex = annual_raw_mat + annual_consumables + annual_hr_admin + annual_power
    net_profit = total_revenue - total_cogs_opex
    payback = total_capex / net_profit if net_profit > 0 else 0

    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    col_res1.metric("الإيرادات", f"{total_revenue:,.0f}")
    col_res2.metric("التكاليف", f"{total_cogs_opex:,.0f}")
    col_res3.metric("الربح", f"{net_profit:,.0f}")
    col_res4.metric("سنوات الاسترداد", f"{payback:.1f}")
    
    # الرسم البياني (تم تقصير العنوان لتجنب الخطأ)
    cost_data = pd.DataFrame({
        "البند": ["مواد خام", "مستهلكات", "رواتب وإدارة", "طاقة"],
        "القيمة": [annual_raw_mat, annual_consumables, annual_hr_admin, annual_power]
    })
    
    t_pie = "توزيع التكاليف"
    fig = px.pie(cost_data, values="القيمة", names="البند", title=t_pie, hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    # --- Excel ---
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        workbook = writer.book
        ws = workbook.add_worksheet('Financial')
        ws.right_to_left()
        
        fmt_head = workbook.add_format({'bold': True, 'bg_color': '#1F4E78', 'font_color': 'white', 'border': 1})
        fmt_money = workbook.add_format({'num_format': '#,##0', 'border': 1})
        
        ws.write('A1', 'البيان', fmt_head)
        ws.write('B1', 'القيمة', fmt_head)
        
        data_to_excel = [
            ("المبيعات", total_revenue),
            ("مواد خام", annual_raw_mat),
            ("مستهلكات", annual_consumables),
            ("رواتب", monthly_payroll * 12),
            ("إدارة", admin_expenses * 12),
            ("طاقة", annual_power),
            ("ربح", net_profit),
            ("رأس مال", total_capex)
        ]
        
        for row_num, (item, val) in enumerate(data_to_excel, start=1):
            ws.write(row_num, 0, item, fmt_money)
            ws.write(row_num, 1, val, fmt_money)
            
        ws.set_column('A:A', 30)
        ws.set_column('B:B', 20)

    st.download_button(
        label="📥 تحميل الإكسيل",
        data=buffer.getvalue(),
        file_name="Flexo_Plant.xlsx",
        mime="application/vnd.ms-excel",
        use_container_width=True
    )
