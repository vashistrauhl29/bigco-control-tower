import streamlit as st
import time

def render_agents_page():
    """
    Render the Agentic Workflows module with Sales and Support agent simulations.
    """
    st.header("Agentic Workflows: AI-Powered Automation")

    # Live Badge (Using unified CSS class)
    st.markdown('<div class="glean-badge">✅ LIVE AI CONNECTION</div>', unsafe_allow_html=True)

    st.markdown("Watch AI agents autonomously execute multi-step workflows to accelerate business processes.")

    # Glean Workflow Diagram
    st.subheader("How Glean's Agentic Workflow Works")

    # Use Graphviz for workflow diagram
    st.graphviz_chart('''
        digraph {
            rankdir=LR;
            bgcolor="transparent";

            // Nodes Styling (Glean Rounded Boxes)
            node [shape=box, style="filled,rounded", fontname="PolySans Neutral", fontsize=12, margin=0.25, penwidth=0];
            edge [fontname="PolySans Neutral", fontsize=10, color="#64748B", arrowsize=0.8];

            // Define Nodes with Specific Glean Colors
            User [label="User Query", fillcolor="#2750DD", fontcolor="white"];
            Search [label="Search\\n(Enterprise Graph)", fillcolor="#10B981", fontcolor="white"];
            Plan [label="Plan\\n(Reasoning)", fillcolor="#F59E0B", fontcolor="white"];
            Execute [label="Execute\\n(Tools/APIs)", fillcolor="#8B5CF6", fontcolor="white"];
            Response [label="Response", fillcolor="#06B6D4", fontcolor="white"];

            // Edges
            User -> Search [color="#2750DD"];
            Search -> Plan [color="#10B981"];
            Plan -> Execute [color="#F59E0B"];
            Execute -> Response [color="#8B5CF6"];
        }
    ''')

    workflow_html = """
    <div style="font-family: 'PolySans Neutral', sans-serif; font-size: 16px; color: #0F172A; line-height: 1.8; margin-top: 1rem;">
        <div style="font-weight: 600; margin-bottom: 0.5rem;">Workflow Breakdown:</div>
        <ol style="margin-left: 1.5rem;">
            <li><span style="font-weight: 600;">User Query</span> - User submits a natural language request</li>
            <li><span style="font-weight: 600;">Search</span> - Glean searches across all connected data sources</li>
            <li><span style="font-weight: 600;">Plan</span> - Agentic reasoning determines the best action sequence</li>
            <li><span style="font-weight: 600;">Execute</span> - Agent autonomously executes multi-step workflow</li>
            <li><span style="font-weight: 600;">Response</span> - Structured output delivered to the user</li>
        </ol>
    </div>
    """
    st.markdown(workflow_html, unsafe_allow_html=True)

    st.markdown("---")

    # Create tabs for different agents
    tab1, tab2 = st.tabs(["🤝 Deal Velocity Agent (Sales)", "🎫 Ticket Deflector Agent (Support)"])

    # =====================
    # TAB 1: SALES AGENT
    # =====================
    with tab1:
        st.subheader("Deal Velocity Agent")
        st.markdown("""
        This agent automatically generates executive briefings by pulling data from Salesforce,
        analyzing email communications, and identifying next best actions.
        """)

        # Input section
        st.markdown("---")
        deal_name = st.text_input(
            "Enter Deal Name:",
            value="Acme Corp Enterprise Expansion",
            help="The name of the sales opportunity to analyze"
        )

        # Action button
        if st.button("🚀 Generate Executive Brief", type="primary", use_container_width=True):
            # Simulation with status updates
            with st.status("🤖 Agent working...", expanded=True) as status:
                st.write("🔌 Connecting to Salesforce Graph API...")
                time.sleep(1)
                st.write("📊 Retrieving Opportunity Stage: Negotiation...")
                time.sleep(1)
                st.write("📧 Analyzing last 15 emails in Outlook...")
                time.sleep(1)
                st.write("✍️ Drafting Executive Brief...")
                time.sleep(1)
                status.update(label="Complete", state="complete", expanded=False)

            # SHOW THE SUCCESS PILL
            st.markdown('<div class="glean-pill pill-green">✅ Executive Brief Ready</div>', unsafe_allow_html=True)

            # Display the generated brief
            st.markdown("---")
            st.markdown("### 📋 Executive Brief")

            brief_content = f"""
## Deal Summary: {deal_name}

**Opportunity ID:** OPP-2026-1847
**Current Stage:** Negotiation
**Deal Value:** $850,000 ARR
**Close Date:** March 15, 2026
**Probability:** 75%

---

### 🎯 Key Stakeholders

| Name | Title | Engagement Level | Last Contact |
|------|-------|------------------|--------------|
| Sarah Chen | VP of Engineering | 🟢 Champion | Jan 23, 2026 |
| Michael Rodriguez | CTO | 🟡 Interested | Jan 20, 2026 |
| Jennifer Kim | Procurement Director | 🟠 Skeptical | Jan 18, 2026 |
| David Thompson | CEO | 🔵 Aware | Jan 10, 2026 |

---

### 📊 Deal Intelligence

**Recent Activity (Last 7 Days):**
- 12 email exchanges with Sarah Chen (Engineering)
- 2 product demo sessions completed
- 1 pricing negotiation meeting
- 3 technical questions answered via Slack

**Key Concerns Identified:**
1. ⚠️ Integration timeline with existing Azure infrastructure
2. ⚠️ Data residency requirements (GDPR compliance)
3. ⚠️ Pricing for 500+ user deployment

**Positive Signals:**
- ✅ Technical evaluation completed successfully
- ✅ Champion (Sarah) actively selling internally
- ✅ Budget approved by finance team
- ✅ Legal review in progress

---

### 🎬 Next Best Actions

**Priority 1 - URGENT (Next 48 hours):**
1. **Schedule executive alignment call** with CTO Michael Rodriguez
   - *Rationale:* He mentioned concerns about timeline in last email
   - *Suggested Time:* Thursday 2pm PT (checked his calendar - available)
   - *Agenda:* Address integration timeline, showcase Azure connector

**Priority 2 - THIS WEEK:**
2. **Send custom ROI calculator** to Procurement Director Jennifer Kim
   - *Rationale:* She requested "hard numbers" on cost savings
   - *Action:* Use the deal parameters to generate personalized ROI model

3. **Prepare security & compliance documentation**
   - *Rationale:* Legal review requires SOC 2, GDPR, and ISO certifications
   - *Action:* Package compliance docs and schedule walkthrough

**Priority 3 - NEXT WEEK:**
4. **Propose pilot program** starting with Engineering team (50 users)
   - *Rationale:* Reduces risk, builds internal advocates
   - *Action:* Draft pilot proposal with success metrics

---

### 💡 AI-Generated Insights

**Win Probability Analysis:** 75% → 85% if we address CTO concerns this week

**Competitive Intelligence:** Acme Corp also evaluating Notion AI (discovered via LinkedIn activity)

**Recommended Discount:** Offer 10% discount for annual prepayment to accelerate close

**Risk Factors:**
- 🚨 Procurement Director showing hesitation on pricing
- 🚨 Deal pushed from Q4 2025 to Q1 2026 (previous delay)

---

*Generated by Glean Deal Velocity Agent | {time.strftime("%B %d, %Y at %I:%M %p")}*
            """

            st.markdown(brief_content)

            # Action buttons
            st.markdown("---")
            st.markdown("### Next Actions")

            # Use standard Streamlit columns
            btn_col1, btn_col2 = st.columns([1, 1])

            with btn_col1:
                # Native Download Button (Guaranteed to work)
                st.download_button(
                    label="📥 Download Brief",
                    data=brief_content,
                    file_name="Executive_Brief.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            with btn_col2:
                # Simple Disabled Button for Salesforce (Visual only, no logic to break)
                st.button(
                    "☁️ Synced to Salesforce",
                    disabled=True,
                    use_container_width=True,
                    help="Integration active: Opportunity ID #OPP-2026-1847"
                )

            # Note: We removed the Email button to prevent 'mailto' rendering issues.

    # =====================
    # TAB 2: SUPPORT AGENT
    # =====================
    with tab2:
        st.subheader("Ticket Deflector Agent")
        st.markdown("""
        This agent intercepts support tickets, searches the knowledge base, and automatically
        drafts responses to deflect tickets before they reach human agents.
        """)

        # Input section
        st.markdown("---")
        ticket_issue = st.text_input(
            "Enter Ticket Issue:",
            value="User cannot access the VPN from remote branch",
            help="Describe the support issue to resolve"
        )

        # Action button
        if st.button("🔧 Resolve Ticket", type="primary", use_container_width=True):
            # Simulation with status updates
            with st.status("🤖 Agent working...", expanded=True) as status:
                st.write("🎫 Intercepting Zendesk Ticket #4920...")
                time.sleep(1)
                st.write("🔍 Querying Knowledge Base (Jira + Confluence)...")
                time.sleep(1)
                st.write("📚 Found relevant article: 'VPN Troubleshooting Guide'...")
                time.sleep(1)
                st.write("✍️ Drafting resolution...")
                time.sleep(1)
                status.update(label="Complete", state="complete", expanded=False)

            # SHOW THE SUCCESS PILL
            st.markdown('<div class="glean-pill pill-green">✅ Ticket Resolved</div>', unsafe_allow_html=True)

            # Display the resolution
            st.markdown("---")

            # User Reply Section
            st.markdown("### 📧 User Reply (Auto-Generated)")
            st.info(f"""
**Subject:** Re: Ticket #4920 - {ticket_issue}

Hi there,

Thank you for contacting BigCo IT Support! I've reviewed your issue regarding VPN access from your remote branch location.

Based on our knowledge base, here's the solution to get you connected:

**Step 1: Verify Network Settings**
- Ensure you're connected to a stable internet connection (not guest WiFi)
- Check that your firewall isn't blocking ports 443 and 1194

**Step 2: Update VPN Client**
- Download the latest VPN client: https://bigco.internal/vpn-download
- Current version: 5.2.1 (Released Jan 2026)
- Your version may be outdated if installed before December 2025

**Step 3: Use Correct Server Address**
- Remote branches should connect to: **vpn-remote.bigco.com**
- (NOT vpn.bigco.com - that's for HQ only)
- Enter your standard Active Directory credentials

**Step 4: Clear DNS Cache**
```
Windows: ipconfig /flushdns
Mac: sudo dscacheutil -flushcache
```

**If the issue persists:**
- Try connecting to our backup VPN server: **vpn-backup.bigco.com**
- Contact your local IT coordinator for branch-specific firewall rules
- Our 24/7 helpdesk is available at: support@bigco.com or ext. 5555

This solution has worked for 94% of similar VPN connectivity issues. Please let me know if you're still experiencing problems!

Best regards,
**BigCo IT Support (Powered by Glean AI)**
Ticket #4920 | Priority: Medium | Auto-Resolved
            """)

            st.download_button(
                label="📥 Download User Reply",
                data=f"Subject: Re: Ticket #4920 - {ticket_issue}\n\n[Email content here]",
                file_name="ticket_4920_user_reply.txt",
                mime="text/plain"
            )

            st.markdown("---")

            # Internal Note Section
            st.markdown("### 🔒 Internal Note (For Support Admin)")
            st.warning(f"""
**TICKET METADATA**
- **Ticket ID:** #4920
- **Category:** Network/VPN
- **Priority:** Medium
- **User:** john.doe@bigco.com (Sales - Remote Branch: Austin, TX)
- **Submitted:** Jan 25, 2026 at 2:15 PM
- **Auto-Resolved:** Jan 25, 2026 at 2:17 PM (2 min response time)

---

**TECHNICAL SUMMARY**

**Root Cause Analysis:**
User attempting to connect to primary VPN endpoint (vpn.bigco.com) which is optimized for HQ traffic. Remote branches experience latency issues and timeouts when using this endpoint.

**Solution Applied:**
Redirected user to geographically distributed VPN server (vpn-remote.bigco.com) with lower latency for remote locations.

**Knowledge Base Articles Referenced:**
1. KB-1847: "VPN Connection Troubleshooting for Remote Branches"
2. KB-2103: "Common VPN Client Configuration Errors"
3. KB-2891: "Network Port Requirements for VPN"

**Confidence Score:** 89% (High)

**Similar Tickets (Last 30 Days):** 23 tickets with same pattern
- 22 resolved with same solution (95% success rate)
- 1 escalated (firewall issue requiring network admin)

---

**RECOMMENDED ACTIONS**
⚠️ **Alert:** This is the 23rd VPN remote access ticket this month
💡 **Suggestion:** Add prominent notice about vpn-remote.bigco.com on employee portal
📊 **Analytics:** Austin branch accounts for 40% of VPN tickets (infrastructure issue?)

**Escalation:** NOT REQUIRED (auto-resolved with high confidence)
**Follow-up:** Automated email sent. Will check user response in 24 hours.

---

*Agent: Glean Ticket Deflector v2.1 | Knowledge Sources: 3 | Processing Time: 2.4s*
            """)

            # Metrics
            st.markdown("---")
            st.markdown("### 📊 Deflection Metrics")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Tickets Deflected Today", "47", delta="12%")
            with col2:
                st.metric("Avg Response Time", "2.1 min", delta="-45s")
            with col3:
                st.metric("Agent Hours Saved", "6.2 hrs", delta="1.8 hrs")
            with col4:
                st.metric("User Satisfaction", "4.7/5.0", delta="0.3")

    # Summary section at bottom
    st.markdown("---")
    st.subheader("🎯 Workflow Automation Benefits")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Deal Velocity Agent Impact:**
        - ⚡ 10x faster brief generation (2 min vs 2 hours)
        - 🎯 35% increase in win rate with AI insights
        - 📈 Sellers spend 60% more time selling, not researching
        - 🔄 Automatically syncs with Salesforce, Outlook, Slack
        """)

    with col2:
        st.markdown("""
        **Ticket Deflector Agent Impact:**
        - 🤖 67% of tickets auto-resolved without human touch
        - ⏱️ 2 minute avg response time (was 4 hours)
        - 💰 $180K annual savings in support costs
        - 😊 Higher customer satisfaction (instant answers)
        """)
