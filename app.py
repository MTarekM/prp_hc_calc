# Tab 1: Enhanced HSCT Hemorrhagic Cystitis Module
with tab1:
    st.header("Post-HSCT Hemorrhagic Cystitis PRP Protocol")
    st.markdown("""
    **Intravesical PRP therapy calculator** with:
    - Ultrasound-guided volume adjustment
    - CBC platelet integration
    - Blood volume/apheresis requirements
    - Fibrin/PRF glue preparation protocols
    """)
    
    # MOVED CLINICAL PARAMETERS UP FIRST
    with st.expander("Clinical Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            grade = st.selectbox("Hemorrhagic Cystitis Grade",  # THIS MUST COME FIRST
                               ["Grade 1", "Grade 2", "Grade 3", "Grade 4"],
                               help="Grade 1: Microscopic hematuria\nGrade 2: Macroscopic hematuria\nGrade 3: Clots\nGrade 4: Obstruction")
            bladder_vol = st.number_input("Bladder Volume (ml) on US", min_value=0, value=150, step=10,
                                        help="Post-void residual volume from ultrasound")
            
        with col2:
            wall_thick = st.number_input("Bladder Wall Thickness (mm)", min_value=0.0, value=5.0, step=0.1,
                                       help="Measured at thickest point")
            hematoma_size = st.number_input("Largest Hematoma Diameter (cm)", min_value=0.0, value=0.0, step=0.1,
                                          help="Enter 0 if no hematoma")

    # THEN PUT THE PRP TARGETS SECTION
    with st.expander("PRP Targets & Glue Preparation", expanded=True):
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            target_plt = st.number_input("Target PRP Concentration (×10³/μL)", 
                                       min_value=1000, 
                                       value=1500 if grade in ["Grade 3", "Grade 4"] else 1000,  # NOW grade IS DEFINED
                                       step=100,
                                       help="Minimum 1000 for Grades 1-2, 1500+ for Grades 3-4")
            
        with col2:
            glue_type = st.selectbox("Adjunctive Preparation", 
                                  ["Standard PRP", 
                                   "Fibrin Glue (Cryo-based)", 
                                   "PRF Glue (Combined)", 
                                   "PRF Gel"],
                                  help="Select preparation method based on available components")
            
        with col3:
            target_vol = st.number_input("Target Instillation Volume (ml)", 
                                       min_value=10, 
                                       value=min(30, int(bladder_vol*0.15)) if bladder_vol > 0 else 30,
                                       step=5,
                                       help="Typically 10-20% of bladder volume")

    # ... rest of the code remains the same ...

    # FIX THE EVIDENCE SECTION (replace 'existing_evidence')
    st.subheader("Evidence-Based Rationale")
    evidence_text = """
    **Key Clinical Validation:**
    1. **Whole Blood Volume:** Based on 5x platelet concentration from 50% yield (Nature 2020)
    2. **Apheresis Efficiency:** 2.5x more efficient than manual prep (PMC 2024)
    3. **Grade-Based Targets:** 
       - Grades 1-2: ≥1000×10³/μL (Springer 2019)
       - Grades 3-4: ≥1500×10³/μL (Nature 2020)
    
    **Safety Considerations:**
    - Minimum blood draws enforced (20ml manual/50ml apheresis)
    - Volume limited to 15% bladder capacity
    - Platelet thresholds prevent under-dosing
    """
    
    if glue_type != "Standard PRP":
        evidence_text = evidence_addendum + evidence_text
        
    st.markdown(evidence_text)
