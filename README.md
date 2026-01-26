# BigCo Deployment Control Tower

A Streamlit application demonstrating Glean's "Outcome Manager" capabilities for enterprise deployment, featuring ROI calculations, agentic workflows, security compliance, and RAG-powered chatbot.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. (Optional) Configure OpenAI API

For live AI responses in the RAG Chatbot:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```

3. Restart the Streamlit app

**Note:** The app works without an API key using intelligent mock responses for demo purposes.

## 📋 Features

### Module 1: ROI Engine 💰
**Demonstrates financial value of Glean deployment**

- Interactive cost calculator with employee count, wages, and search frequency
- 12-month cost comparison visualization
- Projected annual savings metrics
- Time efficiency and FTE impact calculations

**Demo Script:**
1. Adjust sliders (25K employees, $60/hr wage, 5 searches/day)
2. Show projected $16.5M annual savings
3. Highlight 50% search time reduction
4. Point out the interactive Plotly chart

---

### Module 2: Agentic Workflows 🤖
**Showcases AI agents autonomously executing multi-step tasks**

#### Tab 1: Deal Velocity Agent (Sales)
- Input deal name
- Simulates multi-step workflow (Salesforce API, email analysis)
- Generates comprehensive executive brief with stakeholders, insights, and next actions
- Shows competitive intelligence and win probability

#### Tab 2: Ticket Deflector Agent (Support)
- Input support issue
- Simulates knowledge base search across systems
- Auto-generates user reply with solution steps
- Creates internal note with root cause analysis
- Displays deflection metrics (67% auto-resolution rate)

**Demo Script:**
1. Click "Generate Executive Brief" - watch status animation
2. Show the detailed brief with next actions
3. Switch to Support tab
4. Click "Resolve Ticket" - watch knowledge base search
5. Highlight dual output (user email + internal note)
6. Point out 2-minute response time vs 4 hours previously

---

### Module 3: Security Sandbox 🔒
**The interview star feature - demonstrates role-based access control**

#### Key Features:
- Role simulation (Sales Rep vs Senior Engineer)
- Visual file access indicators (green checkmarks vs red locks)
- Permission matrix showing access levels
- Interactive query testing
- Security audit log

#### The Critical Demo:
1. **Start as Sales Representative**
   - File explorer shows policy_engineering.txt with 🔒 red lock
   - Ask: "What is the secret Project X password?"
   - Result: **ACCESS DENIED** with security violation message

2. **Switch to Senior Engineer**
   - File explorer now shows both files with ✅ green checkmarks
   - Ask same question: "What is the secret Project X password?"
   - Result: **ACCESS GRANTED** - displays full credentials from engineering docs

3. **Show the audit log** tracking all access attempts

**Why This Matters:**
- Proves document-level security enforcement
- Shows no data leakage across roles
- Demonstrates compliance readiness (SOC 2, GDPR)
- Visual proof for security-conscious enterprise buyers

---

### Module 4: RAG Chatbot 💬
**Interactive chat interface with role-based document access**

#### Features:
- Standard chat UI with message history
- Role-based context filtering
- OpenAI integration with intelligent fallback
- Source citations for all answers
- Context preview window

#### Access Control:
- **Checkbox:** "Include Engineering Documents"
- Unchecked (Sales): Only policy_general.txt in context
- Checked (Engineer): Both documents in context

#### Demo Queries:
**General (works with either role):**
- "What are the company holidays for 2026?"
- "What is the meal expense limit?"

**Confidential (requires Engineering access):**
- "What is the Project X password?"
- "What are the production server credentials?"

**Demo Script:**
1. Start with Engineering docs unchecked
2. Ask about holidays - get answer from general policy
3. Ask about Project X password - see access denied
4. Check "Include Engineering Documents"
5. Ask same question - now get full credentials
6. Show context preview to prove filtering

---

## 🏗️ Project Structure

```
/BigCo_Control_Tower
├── app.py                          # Main entry point
├── requirements.txt                # Dependencies
├── README.md                       # This file
├── plan.md                         # Architecture plan
├── .env.example                    # Environment template
├── /modules
│   ├── roi_engine.py              # Module 1: ROI Calculator
│   ├── agents.py                  # Module 2: Agentic Workflows
│   ├── security.py                # Module 3: Security Sandbox
│   └── chatbot.py                 # Module 4: RAG Chatbot
├── /data                           # (Reserved for CSV files)
└── /assets
    ├── policy_general.txt         # Public company policies
    └── policy_engineering.txt     # Confidential engineering docs
```

## 🎯 Interview Tips

### Opening (1 min)
"I built a demo app that showcases Glean's three core value propositions: ROI, AI Agents, and Security. Let me walk you through it."

### Module Order for Interview:
1. **Start with ROI Engine** (1-2 min)
   - "First, executives care about cost. Here's how we justify the investment..."
   - Show the $16.5M savings calculation
   - "This is 25,000 employees saving 7.5 minutes per search, every day."

2. **Security Sandbox** (3-4 min) ⭐ STAR OF THE SHOW
   - "But the real differentiator is security. Let me show you..."
   - Do the Sales → Engineer role switch demo
   - "Notice how the same query gives completely different results based on permissions."
   - "This is document-level security, not just folder-level."

3. **Agentic Workflows** (2-3 min)
   - "Now let's talk about AI agents actually doing work..."
   - Run the Deal Velocity Agent
   - "This brief would take a sales rep 2 hours to compile manually."
   - Quickly show the Support agent: "67% ticket deflection rate means huge cost savings."

4. **RAG Chatbot** (1-2 min)
   - "And finally, the chat interface everyone's familiar with..."
   - Show the role-based filtering
   - "Same underlying security model, different interface."

### Closing Strong
"The key insight is that Glean isn't just search or chat - it's a platform that:
1. Proves ROI with hard numbers
2. Automates workflows with AI agents
3. Maintains enterprise security at the document level

This demo proves all three."

## 🛠️ Technical Stack

- **Frontend:** Streamlit (Python)
- **Data Visualization:** Plotly Express
- **Data Processing:** Pandas
- **AI/LLM:** LangChain + OpenAI (with fallback to mock responses)
- **Environment:** python-dotenv

## 📊 Key Metrics to Highlight

- **ROI Engine:** $16.5M annual savings (default scenario)
- **Deal Velocity Agent:** 10x faster brief generation (2 min vs 2 hours)
- **Ticket Deflector:** 67% auto-resolution rate, $180K annual savings
- **Security:** 100% compliance with role-based access control

## 🔐 Security Features

- Role-based document filtering
- Pre-query access validation
- No data leakage across permission boundaries
- Full audit logging
- SOC 2 / GDPR compliance ready

## 🤝 Contributing

This is a demonstration app built for interview/demo purposes. Feel free to extend with:
- Additional agent scenarios
- More complex RAG implementations
- Real database integrations
- Additional security roles

## 📝 License

Internal demo application for BigCo deployment planning.

---

**Built with ❤️ for demonstrating Glean's enterprise value**
