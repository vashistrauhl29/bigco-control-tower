import streamlit.components.v1 as components
import streamlit as st
import base64
import os
from pathlib import Path
from modules.roi_engine import render_roi_page
from modules.security import render_security_page
from modules.agents import render_agents_page
from modules.chatbot import render_chatbot_page

st.set_page_config(
    page_title="BigCo Deployment Control Tower",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_custom_css():
    # 1. FONT LOADER
    def get_font_base64(file_path):
        if not os.path.exists(file_path):
            filename = os.path.basename(file_path)
            if os.path.exists(filename): file_path = filename
            else: return ""
        try:
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except Exception: return ""

    font_neutral = get_font_base64("assets/fonts/Glean1.ttf")
    font_median = get_font_base64("assets/fonts/Glean3.ttf")

    st.markdown(f"""
        <style>
        /* --- 1. GLOBAL RESET --- */
        @font-face {{ font-family: 'PolySans Neutral'; src: url(data:font/ttf;base64,{font_neutral}) format('truetype'); font-weight: 400; }}
        /* Map Bold Neutral to Median to prevent faux-bold (hazy text) */
        @font-face {{ font-family: 'PolySans Neutral'; src: url(data:font/ttf;base64,{font_median}) format('truetype'); font-weight: 700; }}
        @font-face {{ font-family: 'PolySans Neutral'; src: url(data:font/ttf;base64,{font_median}) format('truetype'); font-weight: 600; }}
        
        @font-face {{ font-family: 'PolySans Median'; src: url(data:font/ttf;base64,{font_median}) format('truetype'); font-weight: 700; }}

        /* --- 2. INTELLIGENT FONT TARGETING --- */
        /* Apply to the Main App Container so mostly everything inherits it */
        .stApp {{ 
            font-family: 'PolySans Neutral', sans-serif !important;
            color: #0F172A !important;
            background: linear-gradient(180deg, #FFFFFF 0%, #F0F4FF 100%) !important; 
            background-attachment: fixed !important; 
        }}
        
        /* Apply to Specific Text Elements (Safe List) */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'PolySans Median', sans-serif !important;
            letter-spacing: -0.3px !important;
        }}
        
        p, a, li, label, input, textarea, select, button {{
            font-family: 'PolySans Neutral', sans-serif !important;
            letter-spacing: -0.3px !important;
        }}
        
        /* Apply to Streamlit Specific Text Containers */
        .stMarkdown, .stWidgetLabel, .stTextInput, .stSelectbox {{
            font-family: 'PolySans Neutral', sans-serif !important;
        }}

        /* --- SIDEBAR SPECIFIC OVERRIDES --- */
        section[data-testid="stSidebar"] * {{
            font-family: 'PolySans Neutral', sans-serif !important;
        }}
        
        /* Restore Material Icons Font - Specific Fix for Collapse Button */
        section[data-testid="stSidebar"] button[kind="header"] *,
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] *,
        [data-testid="stSidebarNav"] span,
        .material-symbols-rounded {{
            font-family: 'Material Symbols Rounded' !important;
        }}

        .stCheckbox label p {{
            font-family: 'PolySans Neutral', sans-serif !important;
        }}
        /* Target the Radio Button Label "Select Module:" specifically */
        section[data-testid="stSidebar"] .stRadio > label {{
            font-weight: 700 !important;
            font-size: 14px !important;
        }}

        /* REDUCE TOP PADDING */
        .block-container {{
            padding-top: 3.5rem !important;
        }}

        /* --- 3. ICON PROTECTION (Critical Fix) --- */
        /* Explicitly protect the Material Symbols font used by Streamlit icons */
        .material-symbols-rounded {{
            font-family: 'Material Symbols Rounded' !important;
            font-weight: normal !important;
            font-style: normal !important;
            letter-spacing: normal !important;
            text-transform: none !important;
            white-space: nowrap !important;
            direction: ltr !important;
        }}

        /* --- 4. TABS: DYNAMIC TEXT COLOUR --- */
        button[data-baseweb="tab"] {{
            border-radius: 999px !important;
            padding: 10px 32px !important;
            border: none !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            margin-right: 8px !important;
            transition: all 0.2s ease;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            background: linear-gradient(90deg, #2750DD 0%, #7C3AED 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 12px rgba(39, 80, 221, 0.3);
        }}
        /* Target paragraph inside tab specifically */
        button[data-baseweb="tab"][aria-selected="true"] p {{ color: #FFFFFF !important; }}

        button[data-baseweb="tab"][aria-selected="false"] {{
            background: #EFF6FF !important;
            color: #64748B !important;
        }}

        /* --- 5. BUTTONS: ALWAYS WHITE TEXT --- */
        div.stButton > button {{
            border-radius: 99px !important;
            background: linear-gradient(90deg, #2750DD 0%, #7C3AED 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            padding: 12px 28px !important;
            font-weight: 600 !important;
        }}
        div.stButton > button p {{ color: #FFFFFF !important; }}

        /* --- 6. PILLS & CARDS --- */
        .glean-pill {{
            display: inline-flex; align-items: center; justify-content: center;
            padding: 8px 24px; border-radius: 999px; font-weight: 700; font-size: 14px;
            color: #0F172A !important; margin-bottom: 8px; border: 1px solid rgba(255,255,255,0.5);
        }}
        .pill-platform {{
            display: inline-flex; align-items: center; justify-content: center;
            padding: 10px 24px; border-radius: 999px; font-weight: 700; font-size: 15px;
            color: #0F172A !important;
            background: linear-gradient(90deg, #EEF8A2 0%, #F5E1F9 100%);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.6);
            margin-bottom: 12px;
        }}
        .pill-green {{ background: linear-gradient(90deg, #DCFCE7 0%, #86EFAC 100%); }}
        .pill-red {{ background: linear-gradient(90deg, #FEE2E2 0%, #FCA5A5 100%); }}
        .pill-blue {{ background: linear-gradient(90deg, #E0F2FE 0%, #7DD3FC 100%); }}
        .pill-mixed {{ background: linear-gradient(90deg, #FEF9C3 0%, #FBCFE8 100%); }}

        .badge-granted {{
            background: linear-gradient(90deg, #10B981 0%, #059669 100%);
            color: white; padding: 6px 16px; border-radius: 99px;
            font-size: 12px; font-weight: 700; display: inline-block;
            margin-bottom: 5px; box-shadow: 0 2px 5px rgba(16, 185, 129, 0.2);
        }}
        .badge-denied {{
            background: linear-gradient(90deg, #EF4444 0%, #B91C1C 100%);
            color: white; padding: 6px 16px; border-radius: 99px;
            font-size: 12px; font-weight: 700; display: inline-block;
            margin-bottom: 5px; box-shadow: 0 2px 5px rgba(239, 68, 68, 0.2);
        }}

        .glean-badge {{
            background: linear-gradient(90deg, #10B981 0%, #059669 100%);
            color: white !important; padding: 4px 12px; border-radius: 99px;
            font-size: 12px; font-weight: 700; display: inline-block; margin-bottom: 10px;
        }}

        .glean-info-box {{
            background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px;
            padding: 12px; color: #1E40AF !important; font-size: 14px; margin-bottom: 20px;
        }}

        .glean-tech-box {{
            background: radial-gradient(circle at top right, #F8FAFC 0%, #E2E8F0 100%);
            border: 1px solid #CBD5E1; border-radius: 12px; padding: 20px;
        }}

        .glean-card-primary {{
            background: linear-gradient(135deg, #2750DD 0%, #7C3AED 100%);
            border-radius: 16px; padding: 24px; color: white !important;
            box-shadow: 0 10px 15px -3px rgba(39, 80, 221, 0.2); margin-bottom: 20px;
        }}
        .glean-lime-text {{
            color: #D8FD49 !important;
        }}
        .glean-card-primary h3 {{ color: rgba(255,255,255,1.0) !important; font-size: 22px !important; margin: 0 0 10px 0 !important; text-transform: uppercase; letter-spacing: 1.2px !important; }}
        .glean-card-primary h1 {{ color: white !important; font-size: 36px !important; margin: 0 0 10px 0 !important; font-weight: 700 !important; }}

        .glean-card-secondary {{
            background: linear-gradient(135deg, #0EA5E9 0%, #B8D73E 100%);
            border-radius: 16px; padding: 24px; color: white !important;
            box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.2); margin-bottom: 20px;
        }}
        .glean-card-secondary h3 {{ color: rgba(255,255,255,1.0) !important; font-size: 22px !important; margin: 0 0 10px 0 !important; text-transform: uppercase; letter-spacing: 1.2px !important; }}
        .glean-card-secondary h1 {{ color: white !important; font-size: 36px !important; margin: 0 0 10px 0 !important; font-weight: 700 !important; }}

        div[data-baseweb="tab-highlight"] {{ display: none !important; }}
        div[data-baseweb="tab-list"] {{ gap: 12px; padding-bottom: 12px; background: transparent !important; }}
        div[data-testid="stSliderTickBarMin"], div[data-testid="stSliderTickBarMax"] {{ background: transparent !important; color: #0F172A !important; }}
        div[data-baseweb="select"] * {{ color: #0F172A !important; opacity: 1 !important; }}
        </style>
    """, unsafe_allow_html=True)


def render_glean_header():
    """
    Render custom Glean-themed navigation header.
    """
    header_html = """
    <div style="
        background: #FFFFFF;
        border-bottom: 1px solid #E2E8F0;
        padding: 1rem 2rem;
        margin: -6rem -6rem 2rem -6rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        z-index: 9999;
        position: relative;
    ">
        <div style="display: flex; align-items: center; gap: 3rem;">
            <div style="
                font-family: 'PolySans Median', sans-serif;
                font-size: 1.5rem;
                font-weight: 700;
                color: #2750DD;
            ">
                glean
            </div>
            <nav style="display: flex; gap: 2rem; align-items: center;">
                <a href="#" style="
                    text-decoration: none;
                    color: #0F172A;
                    font-weight: 500;
                    font-size: 0.95rem;
                ">Product</a>
                <a href="#" style="
                    text-decoration: none;
                    color: #0F172A;
                    font-weight: 500;
                    font-size: 0.95rem;
                ">Solutions</a>
                <a href="#" style="
                    text-decoration: none;
                    color: #0F172A;
                    font-weight: 500;
                    font-size: 0.95rem;
                ">Resources</a>
            </nav>
        </div>
        <div>
            <button style="
                background-color: #2750DD;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.5rem 1.5rem;
                font-weight: 600;
                font-size: 0.95rem;
                cursor: pointer;
                font-family: 'PolySans Neutral', sans-serif;
            ">Sign In</button>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


# Load custom styling
load_custom_css()

# Fix scroll-to-middle bug (force focus reset)
st.empty()

# Main title with custom styling
st.markdown("""
    <h1 style='font-family: "PolySans Median", sans-serif; font-weight: 700; font-size: 48px; color: #0F172A; margin-bottom: 0px;'>
        BigCo Deployment Control Tower
    </h1>
    <p style='font-family: "PolySans Neutral", sans-serif; font-size: 18px; color: #64748B; margin-bottom: 30px;'>
        Outcomes & Value Engineering Dashboard
    </p>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
selected_module = st.sidebar.radio(
    "Select Module:",
    ["ROI Engine", "Agentic Workflows", "Security Sandbox", "RAG Chatbot"]
)

# Render selected module
if selected_module == "ROI Engine":
    render_roi_page()

elif selected_module == "Agentic Workflows":
    render_agents_page()

elif selected_module == "Security Sandbox":
    render_security_page()

elif selected_module == "RAG Chatbot":
    # 1. Force an invisible element at the top to anchor the scroll
    st.markdown('<div id="top-anchor" style="position: absolute; top: 0; left: 0; width: 1px; height: 1px;"></div>', unsafe_allow_html=True)
    
    # 2. Inject CSS to stop auto-scroll behavior
    st.markdown("""
        <style>
            /* Stop the browser from scrolling to the focus element */
            .stApp {
                overflow-anchor: none !important;
            }
            /* Ensure the top anchor is prioritized */
            #top-anchor {
                scroll-snap-align: start;
            }
        </style>
        <script>
            // Hard force scroll to top on load with retries to override Streamlit
            function forceTop() {
                window.scrollTo(0, 0);
                // Try standard main container
                var main = window.parent.document.querySelector(".main");
                if (main) { main.scrollTop = 0; }
                // Try modern Streamlit container
                var scroller = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
                if (scroller) { scroller.scrollTop = 0; }
            }
            
            // Execute multiple times to catch race conditions
            forceTop();
            setTimeout(forceTop, 50);
            setTimeout(forceTop, 150);
            setTimeout(forceTop, 300);
        </script>
    """, unsafe_allow_html=True)

    render_chatbot_page()
