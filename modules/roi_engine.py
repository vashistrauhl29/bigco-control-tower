import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time

def render_roi_page():
    # Spacer
    st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)

    # Use the new "Platform Overview" Pill for the Header
    st.markdown('<div class="pill-platform">💎 ROI & Value Engine</div>', unsafe_allow_html=True)

    # --- Controls ---
    col1, col2 = st.columns(2)
    with col1:
        employees = st.selectbox(
            "Number of Employees", 
            [2500, 5000, 10000, 25000], 
            index=3,
            format_func=lambda x: f"{x:,}"
        )
        wage = st.number_input("Avg Hourly Wage ($)", value=60)
        # Callback to format cost with commas
        if "roi_imp_cost" not in st.session_state:
            st.session_state.roi_imp_cost = "50,000"

        def format_cost():
            try:
                value = int(st.session_state.roi_imp_cost.replace(",", ""))
                st.session_state.roi_imp_cost = f"{value:,}"
            except ValueError:
                pass

        # Use text_input with callback for auto-formatting
        cost_input = st.text_input(
            "Est. Implementation Cost ($)", 
            key="roi_imp_cost",
            on_change=format_cost,
            help="One-time setup/training fees (e.g., 50,000)"
        )
        try:
            implementation_cost = int(cost_input.replace(",", ""))
        except ValueError:
            implementation_cost = 0
    with col2:
        search_time = st.number_input("Daily Search Time (Hours/Employee)", value=1.8)
        efficiency = st.slider("Glean Efficiency Gain (%)", 10, 50, 40)
        adoption = 0.7 # Fixed conservative factor

    # --- Calculations ---
    work_days = 22
    active_employees = employees * adoption

    daily_saved_hours = search_time * (efficiency / 100)
    # Savings applies only to ACTIVE employees
    monthly_gross_savings = daily_saved_hours * wage * work_days * active_employees

    # Cost applies to ALL employees (you buy seats for everyone)
    license_cost_per_user = 30
    monthly_license_cost = license_cost_per_user * employees

    monthly_net_savings = monthly_gross_savings - monthly_license_cost
    annual_net_savings = (monthly_net_savings * 12) - implementation_cost

    # --- Result Cards (HTML) ---
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="glean-card-primary">
            <h3 style="color:rgba(255,255,255,1); margin:0; font-size:36px;">Projected Annual Net Savings</h3>
            <h1 style="color:white; margin:10px 0; font-size:36px;">${annual_net_savings:,.0f}</h1>
            <div style="color:#D8FD49; font-weight:700;">⬆ {efficiency}% Efficiency Model</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="glean-card-secondary">
            <h3 style="color:rgba(255,255,255,1); margin:0; font-size:36px;">Monthly Net Savings</h3>
            <h1 style="color:white; margin:10px 0; font-size:36px;">${monthly_net_savings:,.0f}</h1>
            <div style="color:rgba(255,255,255,0.9);">After License Costs</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Cumulative Graph (Payback Logic) ---
    months = list(range(11))
    # Month 0 starts at negative Implementation Cost
    # Month 1 = -Imp + NetSavings, etc.
    cumulative_savings = [-implementation_cost + (monthly_net_savings * m) for m in months]

    # Find Payback Month (First month where value > 0)
    payback_month = next((m for m, val in enumerate(cumulative_savings) if val > 0), None)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=cumulative_savings,
        mode='lines+markers',
        name='Net Cash Flow',
        line=dict(color='#2750DD', width=3),
        # TRANSPARENT BLUE FILL
        fill='tozeroy',
        fillcolor='rgba(52, 60, 237, 0.2)'
    ))

    # Add "Break Even" Annotation if applicable
    if payback_month:
        fig.add_vline(x=payback_month, line_width=1, line_dash="dash", line_color="#10B981")
        fig.add_annotation(
            x=payback_month, 
            y=0, 
            text="<b>Break Even</b>", 
            showarrow=True, 
            arrowhead=1,
            arrowwidth=3,
            arrowcolor="#10B981",
            font=dict(color="#10B981", size=15),
            ay=-44
        )

    fig.update_layout(
        title="Cumulative Net Cash Flow (Year 1)",
        xaxis_title="Month",
        yaxis_title="Net Savings ($)",
        font=dict(family="PolySans Neutral", color="#0F172A"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Logic Breakdown ---
    with st.expander("View Calculation Logic"):
        breakdown_html = f"""
        <div style="font-family: 'PolySans Neutral', sans-serif; color: #0F172A; line-height: 1.8;">
            <p><strong>Methodology:</strong> 70% Active Adoption Rate assumed.</p>
            <ul style="list-style: none; padding-left: 0;">
                <li style="margin-bottom: 8px;">
                    1. <strong>Gross Savings:</strong> {employees:,} employees × 0.7 adoption × {daily_saved_hours:.2f} hrs × ${wage}/hr × 22 days =
                    <span style="font-weight: 800; font-size: 1.1em; color: #2750DD;">${monthly_gross_savings:,.0f}</span>
                </li>
                <li style="margin-bottom: 8px;">
                    2. <strong>License Cost:</strong> {employees:,} employees × ${license_cost_per_user}/mo =
                    <span style="font-weight: 800; font-size: 1.1em; color: #EF4444;">-${monthly_license_cost:,.0f}</span>
                </li>
                <li style="margin-bottom: 8px;">
                     3. <strong>Implementation Cost:</strong> One-time setup fee =
                     <span style="font-weight: 800; font-size: 1.1em; color: #F59E0B;">-${implementation_cost:,.0f}</span>
                </li>
                <li style="margin-top: 12px; border-top: 1px solid #E2E8F0; padding-top: 8px;">
                    4. <strong>Net Monthly Impact:</strong>
                    <span style="font-weight: 800; font-size: 1.2em; color: #10B981;">${monthly_net_savings:,.0f}</span>
                </li>
            </ul>
        </div>
        """
        st.markdown(breakdown_html, unsafe_allow_html=True)
