import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

st.set_page_config(page_title="Flexo Smart Plant", page_icon="🏭", layout="wide")

st.title("🏭 محاكي مصنع الفلكسو الذكي المتكامل")
st.markdown("---")
st.info("نظام تفاعلي متسلسل يحاكي تكاليف وتشغيل خط إنتاج كامل (فلكسو CI ➔ لامنيشن Solventless ➔ قطاعة)")

# الأقسام المتسلسلة
tabs = st.tabs([
    "1. خلطة المواد الخام", 
    "2. خط الإنتاج والماكينات", 
    "3. المستهلكات الدقيقة", 
    "4. الموارد البشرية والإدارة", 
    "5. المبيعات (هياكل العميل)", 
    "6. لوحة القيادة المالية (Excel)"
])

# ==========================================
# 1. المواد الخام
# ==========================================
with tabs[0]:
    st.header("تسعير الخامات الأساسية (ريال/كجم)")
    c1, c2, c3, c4 = st.columns(4)
    price_bopp = c1.number_input("سعر BOPP", value=6.0)
    price_pet = c2.number_input("سعر PET", value=5.5)
    price_pe = c3.number_input("سعر PE", value=5.0)
    price_alu = c4.number_input("سعر ALU (ألمنيوم)", value=18.0)
    
    st.markdown("---")
    st.subheader("تكلفة الأحبار والغراء")
    ci1, ci2 = st.columns(2)
    ink_price = ci1.number_input("متوسط سعر الحبر (ريال/كجم)", value=15.0)
    adhesive_price = ci2.number_input("سعر غراء اللامنيشن Solventless", value=12.0)
    
    # متوسط تكلفة المواد المرجح (لغرض المحاكاة السريعة)
    avg_raw_mat_cost = (price_bopp + price_pet + price_pe) / 3 * 1000

# ==========================================
# 2. خط الإنتاج والماكينات (CAPEX & OEE)
# ==========================================
with tabs[1]:
    st.header("إعدادات الماكينات وتكاليف الاستثمار")
    
    col_mac1, col_mac2, col_mac3 = st.columns(3)
    
    with col_mac1:
        st.subheader("1. ماكينة الفلكسو CI")
        flexo_price = st.number_input("سعر الفلكسو", value=8000000)
        flexo_speed = st.slider("متوسط سرعة الطباعة (م/د)", 100, 600, 350)
        flexo_kw = st.number_input("استهلاك الطاقة (kW)", value=150)
        
    with col_mac2:
        st.subheader("2. ماكينة اللامنيشن (Solventless)")
        lam_price = st.number_input("سعر اللامنيشن", value=1200000)
        lam_speed = st.slider("سرعة اللامنيشن (م/د)", 100, 500, 300)
        lam_kw = st.number_input("طاقة اللامنيشن (kW)", value=80)
        
    with col_mac3:
        st.subheader("3. القطاعة (Slitter)")
        slit_price = st.number_input("سعر القطاعة", value=800000)
        slit_speed = st.slider("سرعة القطاعة (م/د)", 100, 600, 400)
        slit_kw = st.number_input("طاقة القطاعة (kW)", value=40)

    total_capex = flexo_price + lam_price + slit_price + 500000 # 500k تجهيزات ومبردات
    st.success(f"إجمالي الاستثمار في خط الإنتاج: {total_capex:,.0f} ريال")

# ==========================================
# 3. المستهلكات الدقيقة
# ==========================================
with tabs[2]:
    st.header("المستهلكات الفنية الخاصة بالفلكسو")
    st.info("يتم ربط هذه الأرقام بحجم الإنتاج السنوي لتحديد التكلفة الحقيقية الدقيقة للطن")
    
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        st.subheader("الأنيلوكس (Anilox)")
        anilox_price = st.number_input("سعر رول الأنيلوكس", value=15000)
        anilox_life = st.number_input("عمر الأنيلوكس (مليون متر)", value=200)
        
    with cc2:
        st.subheader("الدكتور بليد (Doctor Blade)")
        blade_price = st.number_input("سعر المتر (ريال)", value=12.0)
        blade_life = st.number_input("عمر البليد (ألف متر)", value=500)
        
    with cc3:
        st.subheader("أختام الحبر (End Seals)")
        endseal_price = st.number_input("سعر طقم الأختام (SealMax)", value=150.0)
        endseal_life = st.number_input("عمر الطقم (ساعات عمل)", value=72)
        
    st.markdown("---")
    c_solv1, c_solv2 = st.columns(2)
    solvent_ratio = c_solv1.number_input("نسبة استهلاك السولفنت للحبر (%)", value=100)
    solvent_price = c_solv2.number_input("سعر لتر السولفنت", value=6.0)

# ==========================================
# 4. الموارد البشرية والإدارة
# ==========================================
with tabs[3]:
    st.header("الهيكل التنظيمي والمصاريف الإدارية")
    
    ch1, ch2 = st.columns(2)
    
    with ch1:
        st.subheader("الفريق الفني والهندسي")
        engineers = st.number_input("عدد المهندسين (إنتاج/جودة/صيانة)", value=3)
        eng_salary = st.number_input("متوسط راتب المهندس", value=8000)
        operators = st.number_input("عدد فنيي الطباعة والتشغيل", value=6)
        op_salary = st.number_input("متوسط راتب الفني", value=4500)
        
    with ch2:
        st.subheader("الإدارة والمبيعات")
        sales_team = st.number_input("فريق المبيعات والتسويق", value=3)
        sales_salary = st.number_input("متوسط راتب المبيعات", value=6000)
        admin_staff = st.number_input("إدارة عليا ومالية وموارد بشرية", value=4)
        admin_salary = st.number_input("متوسط راتب الإداري", value=10000)
        
    st.markdown("---")
    admin_expenses = st.number_input("المصاريف الإدارية والعمومية (تراخيص، إيجار، ضيافة، سيارات) - شهرياً", value=40000)
    
    monthly_payroll = (engineers*eng_salary) + (operators*op_salary) + (sales_team*sales_salary) + (admin_staff*admin_salary)
    st.info(f"إجمالي الرواتب والمصاريف الإدارية الشهرية: {(monthly_payroll + admin_expenses):,.0f} ريال")

# ==========================================
# 5. المبيعات (هياكل العميل)
# ==========================================
with tabs[4]:
    st.header("تحليل محفظة منتجات العميل")
    st.write("بناءً على طلبات العميل الموزعة بين طبقة، طبقتين، و 3 طبقات:")
    
    client_data = [
        {"الفئة": "طبقة واحدة", "الهياكل": "38 mic label, 40 clear, 30 opp", "النسبة %": 60, "سعر البيع/كجم": 12.0},
        {"الفئة": "طبقتين", "الهياكل": "20 opp+20 met, 20 opp+20 opp, 20 opp+25 perl", "النسبة %": 30, "سعر البيع/كجم": 13.0},
        {"الفئة": "3 طبقات", "الهياكل": "12 pet+7 alu+50 pe, 12 pet+12 met+50 pe", "النسبة %": 10, "سعر البيع/كجم": 15.0},
    ]
    df_mix = st.data_editor(pd.DataFrame(client_data), use_container_width=True)
    
    target_annual_tons = st.number_input("الهدف البيعي السنوي للمصنع (طن)", value=1500)
    
    # حساب متوسط سعر البيع المرجح
    weighted_avg_price = sum((row["النسبة %"] / 100) * row["سعر البيع/كجم"] for index, row in df_mix.iterrows()) * 1000
    total_revenue = target_annual_tons * weighted_avg_price
    
    st.success(f"متوسط سعر بيع الطن: {weighted_avg_price:,.0f} ريال | الإيرادات السنوية المتوقعة: {total_revenue:,.0f} ريال")

# ==========================================
# 6. لوحة القيادة المالية (Excel)
# ==========================================
with tabs[5]:
    st.header("الخلاصة المالية ودراسة الجدوى (P&L)")
    
    # الحسابات السنوية المترابطة
    annual_raw_mat = target_annual_tons * avg_raw_mat_cost
    
    # حساب المستهلكات بناء على افتراض 15 مليون متر طولية سنويا (تقريبي لـ 1500 طن)
    est_annual_meters = target_annual_tons * 10000 
    annual_anilox = (est_annual_meters / (anilox_life * 1000000)) * anilox_price * 8 # 8 ألوان
    annual_blade = (est_annual_meters / (blade_life * 1000)) * blade_price * 8
    
    # حساب الـ End seals (بافتراض 6000 ساعة عمل للمصنع سنويا)
    annual_endseals = (6000 / endseal_life) * endseal_price * 8
    
    annual_consumables = annual_anilox + annual_blade + annual_endseals + (target_annual_tons * 200) # إضافة افتراضية للسولفنت
    
    annual_hr_admin = (monthly_payroll + admin_expenses) * 12
    annual_power = (flexo_kw + lam_kw + slit_kw) * 6000 * 0.18 # 6000 ساعة بسعر 0.18 ريال/كيلوواط
    
    total_cogs_opex = annual_raw_mat + annual_consumables + annual_hr_admin + annual_power
    net_profit = total_revenue - total_cogs_opex
    roi = (net_profit / total_capex) * 100 if total_capex > 0 else 0
    payback = total_capex / net_profit if net_profit > 0 else 0

    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    col_res1.metric("إجمالي الإيرادات", f"{total_revenue:,.0f} ريال")
    col_res2.metric("إجمالي التكاليف", f"{total_cogs_opex:,.0f} ريال")
    col_res3.metric("صافي الربح السنوي", f"{net_profit:,.0f} ريال")
    col_res4.metric("فترة استرداد رأس المال", f"{payback:.1f} سنوات")
    
    # رسم بياني لتوزيع التكاليف
    cost_data = pd.DataFrame({
        "البند": ["المواد الخام", "المستهلكات (أنيلوكس، بليد، أختام)", "الرواتب والإدارة", "الطاقة"],
        "القيمة": [annual_raw_mat, annual_consumables, annual_hr_admin, annual_power]
    })
    fig = px.pie(cost_data, values="القيمة", names="البند", title="توزيع التكاليف التشغيلية السنو
