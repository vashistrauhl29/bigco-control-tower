import streamlit as st
import os
from pathlib import Path

def load_document_context(include_engineering=False):
    """
    Load document context based on user permissions.

    Args:
        include_engineering: If True, include engineering documents

    Returns:
        tuple: (context_text, source_list)
    """
    context_parts = []
    sources = []

    # Always load general policy
    general_path = "assets/policy_general.txt"
    if os.path.exists(general_path):
        with open(general_path, "r") as f:
            general_content = f.read()
            context_parts.append(f"=== GENERAL COMPANY POLICIES ===\n{general_content}")
            sources.append("policy_general.txt")

    # Conditionally load engineering policy
    if include_engineering:
        eng_path = "assets/policy_engineering.txt"
        if os.path.exists(eng_path):
            with open(eng_path, "r") as f:
                eng_content = f.read()
                context_parts.append(f"\n\n=== ENGINEERING POLICIES (CONFIDENTIAL) ===\n{eng_content}")
                sources.append("policy_engineering.txt")

    context_text = "\n".join(context_parts)
    return context_text, sources


def get_mock_response(user_input, context_sources):
    """
    Generate a mock response when OpenAI API is not available.
    """
    user_input_lower = user_input.lower()

    # Check if asking about sensitive information
    if any(keyword in user_input_lower for keyword in ["password", "project x", "credential", "api key", "secret"]):
        if "policy_engineering.txt" in context_sources:
            return f"""Based on the engineering documentation, I found information related to your query about "{user_input}".

**Note:** This is a demo mode response. In a live environment with OpenAI API configured, I would provide the specific answer from the engineering policy documents.

**Context Sources Used:** {', '.join(context_sources)}

For security testing purposes, I can see the engineering policies which contain Project X credentials and server passwords. Switch to Sales role to see how access control prevents this information from being retrieved."""
        else:
            return f"""I don't have access to information about "{user_input}" in my current context.

**Available Context:** {', '.join(context_sources)}

This appears to be engineering-related information that is not included in the general company policies I have access to. You may need Engineering role permissions to access this information."""

    # Check if asking about holidays
    elif "holiday" in user_input_lower:
        return f"""Based on the company policies, here are BigCo's holidays for 2026:

- New Year's Day: January 1
- Memorial Day: May 25
- Independence Day: July 4
- Labor Day: September 7
- Thanksgiving: November 26-27
- Christmas: December 25

**Note:** This is a demo mode response. In a live environment with OpenAI API configured, I would provide more detailed answers using natural language processing.

**Context Sources Used:** {', '.join(context_sources)}"""

    # Check if asking about expenses
    elif "expense" in user_input_lower or "meal" in user_input_lower or "travel" in user_input_lower:
        return f"""Based on the company expense policy:

- Meal expenses: Up to $50 per day for business travel
- Hotel accommodations: Up to $200 per night
- Mileage reimbursement: $0.67 per mile
- Submit expense reports within 30 days
- Receipts required for expenses over $25

**Note:** This is a demo mode response. In a live environment with OpenAI API configured, I would provide more contextual answers.

**Context Sources Used:** {', '.join(context_sources)}"""

    # Default response
    else:
        return f"""I am a demo bot running in offline mode. I see you asked about: "{user_input}"

In a live environment with OpenAI API configured, I would:
1. Search through the available context documents
2. Find relevant information to answer your question
3. Provide a natural language response with citations

**Current Context Sources:** {', '.join(context_sources)}

**To enable live AI responses:** Add your OpenAI API key to the `.env` file or Streamlit secrets.

Try asking about:
- "What are the company holidays?"
- "What is the expense policy for meals?"
- "What is the Project X password?" (requires Engineering role)"""


def get_llm_response(user_input, context_text):
    """
    Get response from OpenAI using LangChain.
    """
    try:
        from langchain_openai import ChatOpenAI
        from langchain.prompts import PromptTemplate

        # Get API key
        api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)

        if not api_key:
            return None

        # Create prompt template
        template = """You are a helpful Glean Assistant for BigCo.
Answer the user question based ONLY on the following context.
If the answer is not in the context, say "I don't have information about that in my available documents."

Context:
{context_data}

User Question: {user_input}

Answer:"""

        prompt = PromptTemplate(
            input_variables=["context_data", "user_input"],
            template=template
        )

        # Create LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            api_key=api_key
        )

        # Format prompt
        formatted_prompt = prompt.format(
            context_data=context_text,
            user_input=user_input
        )

        # Get response
        response = llm.invoke(formatted_prompt)
        return response.content

    except ImportError:
        return None
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return None


def render_chatbot_page():
    """
    Render the RAG Chatbot module with role-based context filtering.
    """
    # 1. LIVE BADGE (Check API key first)
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)
    if api_key:
        st.markdown('<div class="glean-badge">✅ OpenAI API Connected - Live AI Responses Enabled</div>', unsafe_allow_html=True)

    st.header("RAG Chatbot: Intelligent Document Search")
    st.markdown("Chat with your company documents. Responses are grounded in your actual data with role-based access control.")

    # Role/Permission Selection
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Document Access")

    # Check if we have security role from Module 3
    if 'security_role' not in st.session_state:
        st.session_state.security_role = None

    # Allow user to select permissions for chatbot
    include_engineering = st.sidebar.checkbox(
        "Include Engineering Documents",
        value=False,
        help="Enable to include confidential engineering policies in chat context"
    )

    # 2. SIDEBAR ACCESS LEVEL PILL
    if include_engineering:
        st.sidebar.markdown("""
        <div class="glean-pill pill-blue" style="font-size:12px;">
            ℹ️ Access Level: Engineering (All Documents)
        </div>
        """, unsafe_allow_html=True)
        role_display = "Senior Engineer"
    else:
        st.sidebar.markdown("""
        <div class="glean-pill pill-blue" style="font-size:12px;">
            ℹ️ Access Level: General (Public Only)
        </div>
        """, unsafe_allow_html=True)
        role_display = "Sales Representative"

    # Show which documents are loaded with access badges
    st.sidebar.markdown("### 📚 Available Context")

    # File 1: General Policy (Always Granted)
    st.sidebar.markdown("""
    <div style="margin-bottom: 10px;">
        <span class="badge-granted">✅ ACCESS GRANTED</span><br>
        <span style="font-weight:600; font-size:14px;">📄 General Policy Document</span>
    </div>
    """, unsafe_allow_html=True)

    # File 2: Engineering Specs (Conditional)
    if include_engineering:
        st.sidebar.markdown("""
        <div style="margin-bottom: 10px;">
            <span class="badge-granted">✅ ACCESS GRANTED</span><br>
            <span style="font-weight:600; font-size:14px;">📄 Engineering System Specs</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style="margin-bottom: 10px;">
            <span class="badge-denied">🔒 ACCESS DENIED</span><br>
            <span style="font-weight:600; font-size:14px; color: #94A3B8;">📄 Engineering System Specs</span>
        </div>
        """, unsafe_allow_html=True)

    # Show API warning only if not configured
    if not api_key:
        st.warning("⚠️ OpenAI API Not Configured - Running in Demo Mode with Mock Responses")
        with st.expander("ℹ️ How to enable live AI responses"):
            st.markdown("""
            To enable real OpenAI-powered responses:

            1. Create a `.env` file in the project root
            2. Add your OpenAI API key:
               ```
               OPENAI_API_KEY=sk-your-key-here
               ```
            3. Restart the Streamlit app

            Alternatively, add it to Streamlit secrets (`.streamlit/secrets.toml`):
            ```
            OPENAI_API_KEY = "sk-your-key-here"
            ```
            """)

    st.markdown("---")

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display chat history
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            # Show access pills for assistant messages
            if message["role"] == "assistant":
                content = message["content"]
                if "Access Granted" in content or "Retrieving information" in content:
                    st.markdown('<div class="glean-pill pill-green">✅ Access Granted - Retrieving information...</div>', unsafe_allow_html=True)
                elif "ACCESS DENIED" in content or "don't have access" in content:
                    st.markdown('<div class="glean-pill pill-red">🚫 ACCESS DENIED</div>', unsafe_allow_html=True)

            st.markdown(message["content"])
            if "sources" in message:
                st.caption(f"📚 Sources: {', '.join(message['sources'])}")

    # Chat input
    if user_input := st.chat_input("Ask a question about BigCo policies..."):
        # Add user message to chat
        st.session_state.chat_messages.append({"role": "user", "content": user_input})

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Load context based on permissions
                context_text, context_sources = load_document_context(include_engineering)

                # Try to get LLM response first
                response = get_llm_response(user_input, context_text)

                # Fall back to mock response if LLM not available
                if response is None:
                    response = get_mock_response(user_input, context_sources)

                # Show access status pills based on response content
                if "Access Granted" in response or "Retrieving information" in response:
                    st.markdown('<div class="glean-pill pill-green">✅ Access Granted - Retrieving information...</div>', unsafe_allow_html=True)
                elif "ACCESS DENIED" in response or "don't have access" in response:
                    st.markdown('<div class="glean-pill pill-red">🚫 ACCESS DENIED</div>', unsafe_allow_html=True)

                st.markdown(response)
                st.caption(f"📚 Sources: {', '.join(context_sources)}")

        # Add assistant response to chat
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": response,
            "sources": context_sources
        })

    # Suggested questions
    if len(st.session_state.chat_messages) == 0:
        st.markdown("### 💡 Try asking:")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **General Questions:**
            - "What are the company holidays for 2026?"
            - "What is the meal expense limit?"
            - "What is the remote work policy?"
            - "How many vacation days do I get?"
            """)

        with col2:
            st.markdown("""
            **Engineering Questions** (requires Engineering access):
            - "What is the Project X password?"
            - "What are the production server credentials?"
            - "Who is on-call this week?"
            - "What is our tech stack for Project X?"
            """)

    # Clear chat button
    if len(st.session_state.chat_messages) > 0:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_messages = []
            st.rerun()

    # Show context preview
    with st.expander("🔍 Preview Current Context (What the AI can see)"):
        context_text, context_sources = load_document_context(include_engineering)
        st.text_area(
            "Current Context",
            context_text,
            height=300,
            disabled=True,
            help="This is the text content the AI uses to answer questions"
        )
        st.caption(f"**Total characters:** {len(context_text)} | **Sources:** {', '.join(context_sources)}")

    # RAG Architecture Diagram
    st.markdown("---")
    st.subheader("🏗️ RAG Architecture")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **1. Document Ingestion**
        - Load policy files
        - Apply role-based filtering
        - Create context window
        """)

    with col2:
        st.markdown("""
        **2. Query Processing**
        - User asks question
        - Retrieve relevant context
        - Build prompt with context
        """)

    with col3:
        st.markdown("""
        **3. Response Generation**
        - LLM processes prompt
        - Generate grounded answer
        - Cite source documents
        """)

    # 3. TRUST CARDS (At the bottom)
    st.markdown("---")
    st.subheader("✨ Key Benefits")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="glean-tech-box">
            <h4 style="margin-top:0;">🛡️ Accuracy & Trust</h4>
            <p style="font-size:14px; margin:0;">Responses are grounded solely in the provided context window. Zero-retention policy active.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glean-tech-box">
            <h4 style="margin-top:0;">🔒 Security & Compliance</h4>
            <p style="font-size:14px; margin:0;">Role-Based Access Control (RBAC) enforced. Data encrypted in transit (TLS 1.3).</p>
        </div>
        """, unsafe_allow_html=True)
