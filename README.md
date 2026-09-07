streamlit Deploy Link : https://master-mind-ai-bcdfsxamln2bel6kbwdk7j.streamlit.app/
# 🧠 MarketMind AI: Autonomous Business Research Agent

MarketMind AI is an enterprise-grade, multi-agent business intelligence system designed for bounded, structured market analysis and automated research reporting. Built without heavy orchestration frameworks (such as CrewAI or LangGraph), it relies on native Python pipelines, strict Pydantic schema validation, and OpenAI structured outputs to guarantee reliability and performance.

---

## 🏗️ System Architecture

---

## ✨ Core Capabilities

* **🔒 Secure Enterprise Portal:** Pre-flight API key authentication stored strictly within session memory (`st.session_state`) without plaintext leaks.
* **📋 Structured Planning:** Converts raw user scope into actionable, typed research plans with defined objectives and sub-questions using OpenAI Structured Outputs.
* **🛡️ Adversarial Tool Dispatcher:** Strictly checks function parameters, execution permissions, and safety bounds prior to executing tools.
* **🔬 Automated Quality Control:** Audits collected evidence claims against initial objectives to catch coverage gaps or unverified assumptions.
* **📈 Real-Time Telemetry:** Tracks input/output token consumption and calculates precise USD run costs against strict budget ceilings.
* **🤝 Human-in-the-Loop Governance:** Enforces explicit human review and approval gates before reports can be published.

---

## 🚀 Quickstart Guide

### 1. Installation
Clone the repository to your local machine and install the required dependencies:
```bash
git clone [https://github.com/Usman-Sultan7/marketmind-ai.git](https://github.com/Usman-Sultan7/marketmind-ai.git)
cd marketmind
pip install -r requirements.txt
2. Environment Configuration
Create a .env file in the root marketmind directory:

Code snippet
OPENAI_API_KEY=sk-proj-your-api-key-here
DEFAULT_MODEL=gpt-4o-mini
PLANNING_MODEL=gpt-4o
MAX_ITERATIONS=10
MAX_BUDGET_USD=1.00
3. Run the Application Locally
Launch the control center through Streamlit:

Bash
python -m streamlit run app.py

---

### **How to add this to your project:**
1. In your VS Code project folder for **MarketMind AI**, right-click and create a new file named **`README.md`**.
2. Paste the text above into the file and save it (`Ctrl + S`).
3. Push it to GitHub using your terminal:
   ```powershell
   git add README.md
   git commit -m "docs: add professional README for MarketMind AI capstone"
   git push
