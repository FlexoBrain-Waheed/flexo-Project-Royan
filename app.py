import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="NexFlexo Smart Plant", layout="wide")
st.title("🏭 NexFlexo Smart Plant Simulator")

tabs = st.tabs([
    "1. Raw Materials", "2. Production & Power", "3. Consumables", 
    "4. HR & OPEX", "5. Recipes", "6. P&L Dashboard", "7. Commercial"
])

# --- TAB 1 ---
with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    p_bopp = c1.number_input("BOPP Price", 6.0)
    d_bopp = c1.number_input("BOPP Den", 0.91)
    
    p_pet = c2.number_input("PET Price", 5.5)
    d_pet = c2.number_input("PET Den", 1.40)
    
    p_pe = c3.number_input("PE Price", 5.0)
    d_pe = c3.number_input("PE Den", 0.92)
    
    p_alu = c4.number_input("ALU Price", 18.0)
    d_alu = c4.number_input("ALU Den", 2.70)
    
    mat_db = {
        "BOPP": {"p": p_bopp, "d": d_bopp},
        "PET": {"p": p_pet, "d": d_pet},
        "PE": {"p": p_pe, "d": d_pe},
        "ALU": {"p": p_alu, "d": d_alu},
        "None": {"p": 0.0, "d": 0.0}
    }
    
    ci1, ci2, ci3 = st.columns(3)
    ink_p = ci1.number_input("Ink/Kg", 15.0)
    solv_p = ci2.number_input("Solvent/Kg", 6.0)
    adh_p = ci3.number_input("Adhesive/Kg", 12.0)

# --- TAB 2 ---
with tabs[1]:
    cw1, cw2 = st.columns(2)
    d_yr = cw1.number_input("Days/Yr", 300)
    s_day = cw1.number_input("Shifts
