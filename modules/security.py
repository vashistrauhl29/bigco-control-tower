import streamlit as st
import os

def render_security_page():
    """
    Render the Security Sandbox module demonstrating role-based access control.
    """
    st.header("Security Sandbox: Role-Based Document Permissions")
    st.markdown("Demonstrate how Glean enforces document-level security based on user roles.")

    # Sidebar: Role Selection
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎭 Simulate User Role")
    selected_role = st.sidebar.selectbox(
        "Current User Role:",
        ["Sales Representative", "Senior Engineer"],
        help="Select a role to simulate different permission levels"
    )

    # Store in session state
    if 'user_role' not in st.session_state:
        st.session_state.user_role = selected_role
    else:
        st.session_state.user_role = selected_role

    # Define permissions
    PERMISSIONS = {
        "Sales Representative": {
            "policy_general.txt": True,
            "policy_engineering.txt": False
        },
        "Senior Engineer": {
            "policy_general.txt": True,
            "policy_engineering.txt": True
        }
    }

    # 1. User Role Badge (Yellow/Pink Gradient)
    st.markdown(f"""
        <div class="pill-platform">
            🎭 Current User Role: {st.session_state.user_role}
        </div>
    """, unsafe_allow_html=True)

    # File Explorer Section
    st.markdown("---")
    st.subheader("📁 Document Access Control")
    st.markdown("The following documents are available in the system. Your access is based on your role.")

    # Get permissions for current role
    user_permissions = PERMISSIONS[selected_role]

    # Display files with access indicators using pastel pills
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glean-pill pill-green">✅ policy_general.txt - ACCESS GRANTED</div>', unsafe_allow_html=True)
        st.caption("📄 Company-wide policies (Holidays, Expenses, Remote Work)")

    with col2:
        if st.session_state.user_role == 'Senior Engineer':
            st.markdown('<div class="glean-pill pill-green">✅ policy_engineering.txt - ACCESS GRANTED</div>', unsafe_allow_html=True)
            st.caption("🔐 Confidential Engineering Documentation")
        else:
            st.markdown('<div class="glean-pill pill-red">🔒 policy_engineering.txt - ACCESS DENIED</div>', unsafe_allow_html=True)
            st.caption("🔐 Confidential Engineering Documentation")

    # Permission Summary Table
    st.markdown("---")
    st.subheader("📊 Permission Matrix")

    import pandas as pd
    permission_data = {
        "Document": ["policy_general.txt", "policy_engineering.txt"],
        "Access Level": ["Public", "Engineering Only"],
        "Sales Access": ["✅ Granted", "❌ Denied"],
        "Engineering Access": ["✅ Granted", "✅ Granted"]
    }
    df = pd.DataFrame(permission_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Interactive Query Testing
    st.markdown("---")
    st.subheader("🔍 Test Security Controls")
    st.markdown("Ask a question to see how role-based access control works in action.")

    # Text input for query
    user_query = st.text_input(
        "Ask a question:",
        placeholder="e.g., What is the secret Project X password?",
        help="Try asking about confidential information to test access controls"
    )

    # Suggested queries
    col_suggest1, col_suggest2 = st.columns(2)
    with col_suggest1:
        if st.button("💡 Try: Company holidays?"):
            user_query = "What are the company holidays?"
    with col_suggest2:
        if st.button("💡 Try: Project X password?"):
            user_query = "What is the secret Project X password?"

    # Process query if submitted
    if user_query:
        st.markdown("---")
        st.subheader("Response:")

        # Check if query is asking for sensitive information
        query_lower = user_query.lower()

        # Define sensitive keywords
        sensitive_keywords = [
            "project x", "password", "credential", "secret", "api key",
            "server", "staging", "production", "phoenix"
        ]

        is_sensitive_query = any(keyword in query_lower for keyword in sensitive_keywords)

        # Handle based on query type and role
        if is_sensitive_query:
            # Sensitive information requested
            if user_permissions["policy_engineering.txt"]:
                # Engineer role - has access
                st.success("✅ **Access Granted** - Retrieving information from engineering documents...")

                # Read and display relevant content from policy_engineering.txt
                try:
                    with open("assets/policy_engineering.txt", "r") as f:
                        content = f.read()

                    st.markdown("**Retrieved Context:**")
                    st.code(content, language="text")

                    # Extract specific answer based on query
                    if "password" in query_lower or "project x" in query_lower:
                        st.markdown("---")
                        st.markdown("**📋 Extracted Answer:**")
                        st.warning("""
                        **Project X Credentials Found:**

                        Production Database:
                        - Host: prod-db-01.bigco.internal
                        - Password: Ph0en!x_Pr0d_2026_Secure

                        Staging Environment:
                        - Host: staging-db-01.bigco.internal
                        - Password: St4g!ng_Ph0en1x_2026

                        ⚠️ This information is highly confidential and restricted to Engineering personnel only.
                        """)
                except FileNotFoundError:
                    st.error("Error: Engineering policy file not found.")
            else:
                # Sales role - access denied
                st.error("🚫 **ACCESS DENIED**")
                st.warning(f"""
                **Security Violation Detected**

                You do not have permission to view Engineering documents.

                - **Your Role:** {selected_role}
                - **Required Role:** Senior Engineer
                - **Document:** policy_engineering.txt
                - **Action:** Request denied

                This attempt has been logged for security audit purposes.
                """)

                # Show what documents are accessible
                st.info("""
                **💡 You have access to:**
                - policy_general.txt (Company-wide policies)

                For engineering-related questions, please contact your Engineering team lead.
                """)
        else:
            # General information query - check for general policy
            if user_permissions["policy_general.txt"]:
                st.success("✅ **Access Granted** - Retrieving information from general policies...")

                try:
                    with open("assets/policy_general.txt", "r") as f:
                        content = f.read()

                    st.markdown("**Retrieved Context:**")
                    st.code(content, language="text")

                    # Extract specific answer for common queries
                    if "holiday" in query_lower:
                        st.markdown("---")
                        st.markdown("**📋 Answer:**")
                        st.info("""
                        **Company Holidays 2026:**
                        - New Year's Day: January 1
                        - Memorial Day: May 25
                        - Independence Day: July 4
                        - Labor Day: September 7
                        - Thanksgiving: November 26-27
                        - Christmas: December 25
                        """)
                    elif "expense" in query_lower or "meal" in query_lower:
                        st.markdown("---")
                        st.markdown("**📋 Answer:**")
                        st.info("""
                        **Expense Policy:**
                        - Meal expenses: Up to $50 per day for business travel
                        - Hotel accommodations: Standard rate up to $200 per night
                        - Mileage reimbursement: $0.67 per mile
                        - Submit expense reports within 30 days
                        - Receipts required for expenses over $25
                        """)
                except FileNotFoundError:
                    st.error("Error: General policy file not found.")

    # Security Audit Log (visual demonstration)
    with st.expander("🔒 Security Audit Log (Last 5 Actions)"):
        audit_logs = [
            {"User": selected_role, "Action": "Accessed policy_general.txt", "Status": "✅ Allowed", "Timestamp": "2026-01-25 14:32:10"},
            {"User": selected_role, "Action": f"Queried: '{user_query[:50] if user_query else 'N/A'}'", "Status": "✅ Allowed" if user_permissions["policy_engineering.txt"] or not user_query else "❌ Denied", "Timestamp": "2026-01-25 14:32:15"},
            {"User": "Senior Engineer", "Action": "Accessed policy_engineering.txt", "Status": "✅ Allowed", "Timestamp": "2026-01-25 14:30:05"},
            {"User": "Sales Representative", "Action": "Attempted access to policy_engineering.txt", "Status": "❌ Denied", "Timestamp": "2026-01-25 14:28:42"},
            {"User": "Senior Engineer", "Action": "Downloaded policy_engineering.txt", "Status": "✅ Allowed", "Timestamp": "2026-01-25 14:25:18"},
        ]

        df_audit = pd.DataFrame(audit_logs)
        st.dataframe(df_audit, use_container_width=True, hide_index=True)

    # Key Features
    st.markdown("---")
    st.subheader("🛡️ Security Features Demonstrated")

    col_feat1, col_feat2, col_feat3 = st.columns(3)

    with col_feat1:
        st.markdown("""
        **Role-Based Access**
        - Dynamic permissions
        - Real-time validation
        - Audit logging
        """)

    with col_feat2:
        st.markdown("""
        **Document Filtering**
        - Pre-query filtering
        - Context isolation
        - No data leakage
        """)

    with col_feat3:
        st.markdown("""
        **Compliance Ready**
        - SOC 2 compliant
        - GDPR compatible
        - Full audit trail
        """)
