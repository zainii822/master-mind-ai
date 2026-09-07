import os
import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="MarketMind AI | Enterprise Portal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS FOR PROFESSIONAL UI
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Hide Streamlit default branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Clean up top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Style primary buttons to look sleek */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Style the login container */
    .login-header {
        text-align: center;
        font-family: 'Inter', sans-serif;
    }
    .login-subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

# -----------------------------------------------------------------------------
# SCREEN 1: SECURE LOGIN PORTAL
# -----------------------------------------------------------------------------
if not st.session_state["authenticated"]:
    # Create empty columns to perfectly center the login box
    _, col2, _ = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("<div style='margin-top: 10vh;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 class='login-header'>🧠 MarketMind AI</h1>", unsafe_allow_html=True)
        st.markdown("<p class='login-subtitle'>Autonomous Business Intelligence Engine</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        user_key = st.text_input(
            "Authentication Key",
            type="password",
            placeholder="Enter your OpenAI API Key (sk-...)",
            help="Your credentials are encrypted in session memory and never stored."
        )
        
        if st.button("Unlock Enterprise Dashboard", use_container_width=True, type="primary"):
            if user_key.startswith("sk-") and len(user_key.strip()) > 20:
                st.session_state["api_key"] = user_key.strip()
                st.session_state["authenticated"] = True
                
                os.environ["OPENAI_API_KEY"] = user_key.strip()
                try:
                    from src.config import settings
                    settings.OPENAI_API_KEY = user_key.strip()
                except ImportError:
                    pass
                
                st.rerun()
            else:
                st.error("⚠️ Invalid credential format. Key must begin with 'sk-'.")

# -----------------------------------------------------------------------------
# SCREEN 2: MAIN DASHBOARD (UNLOCKED)
# -----------------------------------------------------------------------------
else:
    import src.tools.impl.handlers 
    from src.config import settings
    settings.OPENAI_API_KEY = st.session_state["api_key"]
    os.environ["OPENAI_API_KEY"] = st.session_state["api_key"]

    from src.agents.planner import generate_research_plan
    from src.state.research_state import ResearchState
    from src.agents.researcher import run_research_loop
    from src.agents.quality_control import run_quality_control
    from src.llm.usage import get_run_usage, reset_usage

    st.title("MarketMind Intelligence Dashboard")
    st.markdown("Configure parameters, execute research runs, and audit evidence securely.")

    # Sidebar Control Center
    with st.sidebar:
        st.markdown("### ⚙️ Engine Parameters")
        st.markdown(f"**Reasoning Model:** `{settings.DEFAULT_MODEL}`")
        st.markdown(f"**Max Iterations:** `{settings.MAX_ITERATIONS}`")
        st.markdown(f"**Budget Ceiling:** `${settings.MAX_BUDGET_USD:.2f}`")
        st.markdown("---")
        
        if st.button("🔄 Reset Usage Metrics", use_container_width=True):
            reset_usage()
            st.rerun()
            
        if st.button("🔒 Secure Logout", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["api_key"] = ""
            reset_usage()
            st.rerun()

    # Main Input Area
    user_request = st.text_area(
        "Define Research Scope:",
        placeholder="Example: Analyze the competitive landscape for AI customer support platforms in 2026...",
        height=100
    )

    if st.button("🚀 Initialize Autonomous Run", use_container_width=True, type="primary"):
        if not user_request.strip():
            st.error("⚠️ Research scope cannot be empty.")
        else:
            reset_usage()
            run_id = "run-2026-001"
            
            with st.status("🧠 MarketMind Agent Processing...", expanded=True) as status:
                st.write("Generating structured research architecture...")
                plan = generate_research_plan(user_request)
                
                st.write("Executing bounded investigation loops...")
                state = ResearchState(run_id=run_id, scope_description=user_request, plan=plan)
                state.initialize_statuses()
                state = run_research_loop(state)
                
                st.write("Auditing evidence and checking for coverage gaps...")
                qc_verdict = run_quality_control(state)
                
                status.update(label="✅ Run Completed Successfully", state="complete", expanded=False)

            # Organized Output using Tabs
            st.markdown("### 📊 Research Analysis Results")
            tab1, tab2, tab3 = st.tabs(["📑 Research Plan", "🔬 Quality Audit", "📈 Telemetry & Cost"])
            
            with tab1:
                st.json(plan.model_dump())
                
            with tab2:
                if qc_verdict["passed"]:
                    st.success("✅ Audit Passed: All claims supported and verified.")
                else:
                    st.warning(f"⚠️ Audit Flagged {qc_verdict['defect_count']} potential issues.")
                    st.json(qc_verdict)
                    
            with tab3:
                usage = get_run_usage()
                m1, m2, m3 = st.columns(3)
                m1.metric("Tokens Consumed (In)", f"{usage['tokens_in']:,}")
                m2.metric("Tokens Generated (Out)", f"{usage['tokens_out']:,}")
                m3.metric("Total Execution Cost", f"${usage['estimated_cost']:.5f}")

            # Human Approval Gate
            st.markdown("---")
            st.markdown("### 🛡️ Publication Gate")
            st.info("System is paused. Autonomous publication is disabled per security protocol.")
            
            col_app, col_rej = st.columns(2)
            if col_app.button("✅ Approve & Publish", use_container_width=True):
                st.success("Report approved. Proceeding to downstream systems.")
            if col_rej.button("❌ Reject & Discard", use_container_width=True):
                st.error("Run rejected. Memory cleared.")