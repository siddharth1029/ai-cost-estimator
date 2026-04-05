import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import base64

st.set_page_config(page_title="Build Wise • Build Right", page_icon="🏗️", layout="wide")

# ====================== EYE-CATCHING CSS ======================
st.markdown("""
<style>
    .main-header {
        font-size: 56px; font-weight: 900;
        background: linear-gradient(90deg, #0f766e, #f59e0b, #14b8a6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .result-card {
        background: linear-gradient(135deg, #0f766e, #14b8a6);
        color: white; border-radius: 25px; padding: 30px; box-shadow: 0 25px 50px rgba(15,118,110,0.4);
    }
    .loading-container {
        text-align: center; padding: 80px 40px;
        background: linear-gradient(135deg, #0f766e, #f59e0b);
        border-radius: 30px; color: white;
    }
    .crane {
        font-size: 90px; animation: craneMove 2.5s infinite alternate ease-in-out;
    }
    @keyframes craneMove {
        0% { transform: translateX(-30px) rotate(-8deg); }
        100% { transform: translateX(30px) rotate(8deg); }
    }
    .costing-note {
        background: #fef3c7; border-left: 8px solid #f59e0b;
        padding: 20px; border-radius: 15px; font-size: 18px; font-weight: 600; color: #92400e;
    }
    .formula { font-family: monospace; font-size: 14px; background: #f1f5f9; padding: 4px 8px; border-radius: 6px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🏗️ Build Wise</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size:24px;color:#14b8a6;font-weight:600;">Build Right • AI-Powered • Indian Standards</p>', unsafe_allow_html=True)
st.markdown("---")

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("📋 Project Inputs")
    project_name = st.text_input("Project Name", "Luxury 3BHK Villa - Indore")
    
    location_type = st.selectbox("Location Type", 
        ["Urban","Semi-Urban","Rural","Remote","Hilly/Difficult"], index=1)
    location_factor = {"Urban":1.0,"Semi-Urban":1.08,"Rural":1.15,"Remote":1.25,"Hilly/Difficult":1.40}[location_type]

    building_type = st.selectbox("Building Type", ["Residential","Commercial"])
    if building_type == "Residential":
        bhk = st.selectbox("BHK", ["1 BHK","2 BHK","3 BHK","4 BHK","5 BHK","6 BHK"], index=2)
        bhk_factor = {"1 BHK":1.00,"2 BHK":1.08,"3 BHK":1.15,"4 BHK":1.22,"5 BHK":1.30,"6 BHK":1.40}[bhk]
    else:
        bhk_factor = 1.0

    col1, col2 = st.columns(2)
    with col1: length = st.number_input("Length (m)", 1.0, value=15.0, step=0.5)
    with col2: width = st.number_input("Width (m)", 1.0, value=12.0, step=0.5)
    
    floors = st.number_input("Number of Floors", 1, value=2)
    material_quality = st.selectbox("Material Quality", ["Low (₹14,000)","Medium (₹16,000)","High (₹20,000)"], index=1)
    base_rate = {"Low (₹14,000)":14000,"Medium (₹16,000)":16000,"High (₹20,000)":20000}[material_quality]
    
    foundation_type = st.selectbox("Foundation Type", ["Shallow","Raft","Deep","Pile"])
    foundation_factor = {"Shallow":1.0,"Raft":1.1,"Deep":1.2,"Pile":1.3}[foundation_type]
    
    soil_type = st.selectbox("Soil Type", ["Clay","Sand","Rock"])
    soil_factor = {"Clay":1.15,"Sand":1.10,"Rock":0.95}[soil_type]
    
    estimation_type = st.multiselect("Estimation Type", ["Plinth Rate","Detailed Estimate"], default=["Plinth Rate","Detailed Estimate"])

    if st.button("🚀 Calculate Smart Estimate", use_container_width=True, type="primary"):
        st.session_state.calculate = True

# ====================== CALCULATIONS ======================
if st.session_state.get("calculate", False):
    # ==================== LOADING SCREEN WITH ANIMATED CRANE ====================
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <div class="loading-container">
            <div class="crane">🏗️</div>
            <h2 style="font-size:36px;margin:20px 0;">Estimation is in Progress...</h2>
            <p style="font-size:20px;">Our AI is calculating every cost component using latest Indian standards</p>
            <div style="margin:40px auto;width:400px;height:12px;background:rgba(255,255,255,0.3);border-radius:9999px;overflow:hidden;">
                <div style="height:100%;width:0%;background:linear-gradient(90deg,#fff,#fef08c);animation:progress 3.8s linear forwards;"></div>
            </div>
            <p style="margin-top:25px;font-size:18px;">🧱 Building your transparent estimate...</p>
        </div>
        <style>@keyframes progress{0%{width:0%}100%{width:100%}}</style>
        """, unsafe_allow_html=True)
        time.sleep(3.8)
        placeholder.empty()

    # ==================== ACTUAL CALCULATIONS ====================
    plinth_area_per_floor = length * width
    total_plinth_area = plinth_area_per_floor * floors

    plinth_data = {}
    detailed_data = {}
    material_data = {}

    # Plinth Rate Estimation
    if "Plinth Rate" in estimation_type:
        base_cost = total_plinth_area * base_rate * bhk_factor
        foundation_portion = 0.12 * base_cost
        foundation_adjustment = foundation_portion * (foundation_factor * soil_factor - 1)
        adjusted_cost = base_cost + foundation_adjustment
        transport_cost = base_cost * (location_factor - 1)
        subtotal = adjusted_cost + transport_cost
        contingency = 0.05 * subtotal
        contractor_profit = 0.12 * subtotal
        gst = 0.18 * (subtotal + contractor_profit)
        final_plinth_cost = subtotal + contingency + contractor_profit + gst

        plinth_data = {
            "Plinth Area per Floor": (plinth_area_per_floor, f"{length} × {width}"),
            "Total Plinth Area": (total_plinth_area, f"Area per floor × {floors}"),
            "Base Cost": (base_cost, f"Total Area × ₹{base_rate} × {bhk_factor}"),
            "Foundation Portion (12%)": (foundation_portion, "12% of Base Cost"),
            "Foundation Adjustment": (foundation_adjustment, f"Foundation Portion × ({foundation_factor} × {soil_factor} - 1)"),
            "Adjusted Cost": (adjusted_cost, "Base Cost + Foundation Adjustment"),
            "Transport Cost": (transport_cost, f"Base Cost × ({location_factor} - 1)"),
            "Subtotal": (subtotal, "Adjusted Cost + Transport Cost"),
            "Contingency (5%)": (contingency, "5% of Subtotal"),
            "Contractor Profit (12%)": (contractor_profit, "12% of Subtotal"),
            "GST (18%)": (gst, "18% of (Subtotal + Profit)"),
            "Final Plinth Cost": (final_plinth_cost, "Subtotal + Contingency + Profit + GST")
        }

    # Detailed Estimation
    if "Detailed Estimate" in estimation_type:
        area = total_plinth_area
        cement = 0.4 * area * 400
        steel = 40 * area * 70
        sand = 0.5 * area * 1500
        aggregate = 0.8 * area * 1200
        bricks = 500 * area * 8
        tmc = cement + steel + sand + aggregate + bricks

        labour = 0.25 * tmc
        services = 0.23 * tmc
        finishing = 0.31 * tmc
        doors_windows = 0.08 * tmc
        misc = 0.05 * tmc
        tdc = tmc + labour + services + finishing + doors_windows + misc

        foundation_portion = 0.12 * tdc
        foundation_adjustment = foundation_portion * (foundation_factor * soil_factor - 1)
        transport_cost = tmc * (location_factor - 1)
        subtotal = tdc + foundation_adjustment + transport_cost
        contingency = 0.05 * subtotal
        contractor_profit = 0.12 * subtotal
        gst = 0.18 * (subtotal + contractor_profit)
        final_detailed_cost = subtotal + contingency + contractor_profit + gst

        material_data = {
            "Cement": (cement, "0.4 × Area × 400"),
            "Steel": (steel, "40 × Area × 70"),
            "Sand": (sand, "0.5 × Area × 1500"),
            "Aggregate": (aggregate, "0.8 × Area × 1200"),
            "Bricks": (bricks, "500 × Area × 8")
        }

        detailed_data = {
            "Total Material Cost (TMC)": (tmc, "Sum of all materials"),
            "Labour (25% of TMC)": (labour, "25% of TMC"),
            "Services (23% of TMC)": (services, "23% of TMC"),
            "Finishing (31% of TMC)": (finishing, "31% of TMC"),
            "Doors & Windows (8% of TMC)": (doors_windows, "8% of TMC"),
            "Miscellaneous (5% of TMC)": (misc, "5% of TMC"),
            "Total Direct Cost (TDC)": (tdc, "TMC + Labour + Services + Finishing + D&W + Misc"),
            "Foundation Adjustment": (foundation_adjustment, f"12% of TDC × ({foundation_factor} × {soil_factor} - 1)"),
            "Transport Cost": (transport_cost, f"TMC × ({location_factor} - 1)"),
            "Subtotal": (subtotal, "TDC + Foundation Adj. + Transport"),
            "Contingency (5%)": (contingency, "5% of Subtotal"),
            "Contractor Profit (12%)": (contractor_profit, "12% of Subtotal"),
            "GST (18%)": (gst, "18% of (Subtotal + Profit)"),
            "Final Detailed Cost": (final_detailed_cost, "Subtotal + Contingency + Profit + GST")
        }

    # Comparison
    difference = abs(final_plinth_cost - final_detailed_cost) if "Plinth Rate" in estimation_type and "Detailed Estimate" in estimation_type else 0
    percentage_diff = (difference / ((final_plinth_cost + final_detailed_cost)/2)) * 100 if difference > 0 else 0

    # ====================== OUTPUT UI ======================
    st.success(f"✅ Estimation Completed for **{project_name}**")

    st.markdown("### 📐 Area Calculation")
    st.info(f"**Plinth Area per Floor** = {length} m × {width} m = **{plinth_area_per_floor:,.1f} m²**\n\n"
             f"**Total Plinth Area** = {plinth_area_per_floor:,.1f} m² × {floors} floors = **{total_plinth_area:,.0f} m²**")

    st.markdown("### 📊 Final Cost Estimates")
    c1, c2 = st.columns(2)
    with c1:
        if "Plinth Rate" in estimation_type:
            st.markdown(f'<div class="result-card"><h3>Plinth Rate</h3><h1 style="font-size:58px;">₹{final_plinth_cost:,.0f}</h1></div>', unsafe_allow_html=True)
    with c2:
        if "Detailed Estimate" in estimation_type:
            st.markdown(f'<div class="result-card"><h3>Detailed Estimate</h3><h1 style="font-size:58px;">₹{final_detailed_cost:,.0f}</h1></div>', unsafe_allow_html=True)

    st.markdown('<div class="costing-note"><strong>Very Costing We Have Used as Output Data</strong><br>All calculations are based on current market rates & Indian standards.</div>', unsafe_allow_html=True)

    # ====================== FULL DETAILED BREAKDOWN ======================
    st.markdown("### 🔍 Complete Step-by-Step Breakdown")

    tab1, tab2 = st.tabs(["Plinth Rate Estimation", "Detailed Estimation"])

    with tab1:
        if "Plinth Rate" in estimation_type:
            df_plinth = pd.DataFrame({
                "Component": list(plinth_data.keys()),
                "Formula": [v[1] for v in plinth_data.values()],
                "Amount (₹)": [f"₹{v[0]:,.0f}" for v in plinth_data.values()]
            })
            st.dataframe(df_plinth, use_container_width=True, hide_index=True)

    with tab2:
        if "Detailed Estimate" in estimation_type:
            st.subheader("Material Costs")
            df_mat = pd.DataFrame({
                "Material": list(material_data.keys()),
                "Formula": [v[1] for v in material_data.values()],
                "Cost (₹)": [f"₹{v[0]:,.0f}" for v in material_data.values()]
            })
            st.dataframe(df_mat, use_container_width=True, hide_index=True)

            st.subheader("Other Components")
            df_det = pd.DataFrame({
                "Component": list(detailed_data.keys()),
                "Formula": [v[1] for v in detailed_data.values()],
                "Amount (₹)": [f"₹{v[0]:,.0f}" for v in detailed_data.values()]
            })
            st.dataframe(df_det, use_container_width=True, hide_index=True)

    # Comparison Chart
    if "Plinth Rate" in estimation_type and "Detailed Estimate" in estimation_type:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=["Plinth Rate", "Detailed Estimate"], 
                           y=[final_plinth_cost, final_detailed_cost],
                           marker_color=['#0f766e', '#f59e0b'],
                           text=[f"₹{final_plinth_cost:,.0f}", f"₹{final_detailed_cost:,.0f}"],
                           textposition="auto"))
        fig.update_layout(title="Cost Comparison", height=420, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        st.metric("Difference", f"₹{difference:,.0f}", f"{percentage_diff:.1f}% Variation")

    # ====================== AUTO ANIMATION + DOWNLOAD ======================
    st.balloons()
    st.snow()   # Sparkling effect

    st.markdown("### 📥 Download Your Full Report")
    col_d1, col_d2 = st.columns(2)
    
    # Prepare full data for CSV
    all_data = {"Project Name": project_name, "Total Plinth Area (m²)": total_plinth_area}
    if "Plinth Rate" in estimation_type:
        for k, v in plinth_data.items():
            all_data[f"Plinth - {k}"] = v[0]
    if "Detailed Estimate" in estimation_type:
        for k, v in material_data.items():
            all_data[f"Detailed - Material {k}"] = v[0]
        for k, v in detailed_data.items():
            all_data[f"Detailed - {k}"] = v[0]
    
    df_full = pd.DataFrame([all_data])

    with col_d1:
        csv = df_full.to_csv(index=False).encode()
        st.download_button(
            label="📊 Download Complete CSV Report",
            data=csv,
            file_name=f"{project_name.replace(' ', '_')}_Full_Estimate.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_d2:
        # Simple HTML report for PDF printing
        html_report = f"""
        <h1>Build Wise Estimate - {project_name}</h1>
        <h2>Total Plinth Area: {total_plinth_area:,.0f} m²</h2>
        <h3>Final Plinth Cost: ₹{final_plinth_cost:,.0f}</h3>
        <h3>Final Detailed Cost: ₹{final_detailed_cost:,.0f}</h3>
        <p><strong>Very Costing We Have Used as Output Data</strong></p>
        <p>Generated on {time.strftime('%d %b %Y')}</p>
        """
        st.download_button(
            label="📄 Download HTML Report (Print as PDF)",
            data=html_report,
            file_name=f"{project_name.replace(' ', '_')}_Report.html",
            mime="text/html",
            use_container_width=True
        )

    st.caption("✅ All formulas and component costs are shown above for complete transparency.")

else:
    st.info("👈 Fill the sidebar and click **Calculate Smart Estimate** to see full detailed report with every formula.")

st.markdown("---")
st.markdown("<p style='text-align:center;color:#64748b;'>Build Wise • Build Right © 2026 | AI-Powered Indian Construction Estimator</p>", unsafe_allow_html=True)