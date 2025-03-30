import numpy as np
import streamlit as st
import pandas as pd
from math import sqrt

st.set_page_config(page_title="PRP Calculator", layout="wide")
st.title("Platelet-Rich Plasma (PRP) Preparation Calculator")

tab1, tab2, tab3, tab4 = st.tabs(["Radius Calculator", "RPM/RCF Calculator", "Yield Calculator", "Dosage Calculator"])

with tab1:
    st.header("Centrifuge Radius Calculator")
    st.markdown("""
    Calculate the radii for centrifugation (Rmin, Rmid, Rhct, Rmax) based on your centrifuge geometry.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        angle = st.selectbox("Centrifuge Angle", ["Horizontal (swing-bucket)", "45° (fixed-angle)"])
        l1 = st.number_input("L1: Distance from rotor hub to tube top (cm)", min_value=0.0, value=2.0, step=0.1)
        l2 = st.number_input("L2: Length of centrifuge tube (cm)", min_value=0.0, value=10.0, step=0.1)
    with col2:
        h1 = st.number_input("H1: Height of blood column (cm)", min_value=0.0, value=8.0, step=0.1)
        hct = st.number_input("Hematocrit (%)", min_value=0.0, max_value=100.0, value=45.0, step=0.1)
    
    # Calculate radii
    a = 1.414 if angle == "45° (fixed-angle)" else 1.0
    
    rmin = l1 + (l2 - h1)/a
    rmid = l1 + ((l2 - h1) + h1/2)/a
    rhct = l1 + ((l2 - h1) + (h1 * (1 - hct/100)))/a
    rmax = l1 + l2/a
    
    st.subheader("Calculated Radii")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Rmin (top of fluid)", f"{rmin:.2f} cm")
    with col2:
        st.metric("Rmid (midpoint)", f"{rmid:.2f} cm")
    with col3:
        st.metric("Rhct (buffy coat)", f"{rhct:.2f} cm")
    with col4:
        st.metric("Rmax (bottom)", f"{rmax:.2f} cm")

with tab2:
    st.header("RPM/RCF Calculator")
    st.markdown("""
    Convert between RPM and RCF (relative centrifugal force) using the formula:  
    **RCF = 1.118 × 10⁻⁵ × r × RPM²**  
    where r is the radius in cm (use Rhct for most accurate PRP calculations)
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        radius = st.number_input("Radius (cm)", min_value=0.0, value=9.0, step=0.1)
        rcf = st.number_input("RCF (g-force)", min_value=0.0, value=1000.0, step=1.0)
        if st.button("Calculate RPM from RCF"):
            rpm = sqrt(rcf / (1.118e-5 * radius))
            st.success(f"Required RPM: {rpm:.0f}")
    
    with col2:
        rpm_input = st.number_input("RPM", min_value=0.0, value=3153.0, step=1.0)
        if st.button("Calculate RCF from RPM"):
            calculated_rcf = 1.118e-5 * radius * rpm_input**2
            st.success(f"Resulting RCF: {calculated_rcf:.1f} g")

with tab3:
    st.header("PRP Yield Calculator")
    st.markdown("""
    Calculate the mean yield and confidence interval for your PRP preparation method.  
    **Yield (%) = (PRP Volume × PRP Platelets) / (Blood Volume × Blood Platelets) × 100**
    """)
    
    st.write("Enter data for up to 20 samples:")
    
    # Create editable dataframe
    sample_data = pd.DataFrame(columns=["BV (ml)", "BP (k/μL)", "PV (ml)", "PP (k/μL)", "Yield (%)"])
    edited_data = st.data_editor(sample_data, num_rows="dynamic", height=300)
    
    if st.button("Calculate Yield Statistics"):
        if len(edited_data) > 0:
            # Calculate yields
            edited_data["Yield (%)"] = (edited_data["PV (ml)"] * edited_data["PP (k/μL)"]) / \
                                     (edited_data["BV (ml)"] * edited_data["BP (k/μL)"]) * 100
            
            # Calculate statistics
            mean_yield = edited_data["Yield (%)"].mean()
            std_dev = edited_data["Yield (%)"].std()
            n = len(edited_data)
            ci = 1.96 * (std_dev / sqrt(n)) if n > 1 else 0
            ci_percent = (ci / mean_yield) * 100 if mean_yield != 0 else 0
            
            st.subheader("Yield Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean Yield", f"{mean_yield:.1f}%")
            with col2:
                st.metric("Standard Deviation", f"{std_dev:.1f}%")
            with col3:
                st.metric("95% CI", f"±{ci:.1f}%")
            with col4:
                st.metric("CI as % of Mean", f"{ci_percent:.1f}%")
            
            st.write("Sample Data with Calculated Yields:")
            st.dataframe(edited_data)
        else:
            st.warning("Please enter at least one sample")

with tab4:
    st.header("PRP Dosage Calculator")
    st.markdown("""
    Calculate platelet dosage or required blood volume based on your PRP preparation method.
    """)
    
    calc_mode = st.radio("Calculation Mode", 
                        ["Calculate Dose from Blood Volume", 
                         "Calculate Blood Volume from Desired Dose"])
    
    if calc_mode == "Calculate Dose from Blood Volume":
        col1, col2 = st.columns(2)
        with col1:
            bv = st.number_input("Blood Volume (ml)", min_value=0.0, value=20.0, step=1.0)
            bp = st.number_input("Blood Platelets (k/μL)", min_value=0.0, value=250.0, step=1.0)
        with col2:
            pv = st.number_input("PRP Volume (ml)", min_value=0.0, value=5.0, step=0.1)
            yield_pct = st.number_input("Yield (%)", min_value=0.0, max_value=100.0, value=65.0, step=0.1)
        
        if st.button("Calculate PRP Platelets and Dose"):
            pp = (bv * bp * yield_pct / 100) / pv
            dose = pv * pp * 1000  # Convert to millions
            
            st.subheader("Results")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("PRP Platelet Concentration", f"{pp:.0f} k/μL")
            with col2:
                st.metric("Total Platelet Dose", f"{dose:,.0f} million")
            
            # Optional: Dose per kg
            weight = st.number_input("Patient Weight (kg)", min_value=0.0, value=70.0, step=0.1)
            dose_per_kg = dose / weight
            st.metric("Dose per kg", f"{dose_per_kg:,.0f} million/kg")
    
    else:  # Calculate Blood Volume from Desired Dose
        col1, col2 = st.columns(2)
        with col1:
            desired_dose = st.number_input("Desired Dose (million platelets)", min_value=0.0, value=1000.0, step=10.0)
            bp = st.number_input("Blood Platelets (k/μL)", min_value=0.0, value=200.0, step=1.0)
        with col2:
            pv = st.number_input("PRP Volume (ml)", min_value=0.0, value=10.0, step=0.1)
            yield_pct = st.number_input("Yield (%)", min_value=0.0, max_value=100.0, value=67.0, step=0.1)
        
        if st.button("Calculate Required Blood Volume"):
            pp = desired_dose / (pv * 1000)  # Convert back to k/μL
            bv = (pv * pp * 100) / (bp * yield_pct)
            
            st.subheader("Results")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Required Blood Volume", f"{bv:.1f} ml")
            with col2:
                st.metric("Expected PRP Platelets", f"{pp:.0f} k/μL")
            
            # Show dose per kg if weight provided
            weight = st.number_input("Patient Weight (kg)", min_value=0.0, value=70.0, step=0.1)
            if weight > 0:
                dose_per_kg = desired_dose / weight
                st.metric("Dose per kg", f"{dose_per_kg:,.0f} million/kg")

st.sidebar.markdown("""
### About PRPCalc
This calculator helps standardize PRP preparation by:
1. Calculating appropriate centrifugation parameters
2. Determining method yield and consistency
3. Estimating platelet dosage without hematology analyzer

**Key Formulas:**
- RCF = 1.118 × 10⁻⁵ × r × RPM²
- Yield = (PV × PP) / (BV × BP) × 100
- Dose = PV × PP × 1000 (million platelets)
""")
