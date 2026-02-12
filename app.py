import streamlit as st
import os, json, re, shutil, tempfile, time
from dotenv import load_dotenv
from agents import V2SAgent
from utils1 import save_generated_code, create_project_zip

# CRITICAL: Load FIRST
load_dotenv()
st.set_page_config(page_title="V2S Architect Pro", layout="wide", initial_sidebar_state="expanded", page_icon="⚡")

# State Management
if "blueprint" not in st.session_state: st.session_state.blueprint = None
if "zip_path" not in st.session_state: st.session_state.zip_path = None
if "full_code" not in st.session_state: st.session_state.full_code = ""

# DARK OCEAN THEME - Dark Blue + Deep Green + Grey
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Times+New+Roman:wght@300;400;500;600;700&display=swap');

/* Global - Dark Blue Base */
.stApp {
    background: linear-gradient(135deg, #0a0e17 0%, #0f141a 40%, #1a1f26 80%, #0a0e17 100%);
    background-attachment: fixed;
    color: #d1d5db;
}

/* Typography - Times New Roman */
h1, h2, h3, h4, h5, h6, .stMarkdown, label { 
    font-family: 'Times New Roman', serif !important; 
}

/* Header - Deep Blue */
.header-title {
    font-family: 'Times New Roman', serif !important; font-size: 3.8rem !important; font-weight: 700 !important;
    background: linear-gradient(135deg, #1e3a8a 0%, #0f4c75 50%, #0c4a6e 100%);
    -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
    text-align: center; text-shadow: 0 4px 20px rgba(30, 58, 138, 0.5); line-height: 1.1; margin-bottom: 0.5rem;
}
.header-subtitle { 
    font-family: 'Times New Roman', serif !important; font-size: 1.4rem !important; 
    color: #94a3b8 !important; text-align: center; font-weight: 400; margin-bottom: 3rem;
}

/* Cards - Dark Grey */
.card {
    background: rgba(15, 20, 26, 0.9) !important; backdrop-filter: blur(20px);
    border: 1px solid rgba(30, 58, 138, 0.4) !important; border-radius: 20px !important; padding: 2.5rem !important;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(30, 58, 138, 0.2);
}

/* Buttons - Dark Green */
.stButton > button {
    background: linear-gradient(135deg, #166534 0%, #14532d 50%, #14532d 100%) !important; color: white !important;
    border: none !important; border-radius: 15px !important; font-family: 'Times New Roman', serif !important;
    font-weight: 600 !important; font-size: 1.1rem !important; padding: 1rem 2rem !important;
    box-shadow: 0 12px 35px rgba(22, 101, 52, 0.4) !important; transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.stButton > button:hover { 
    transform: translateY(-3px) !important; 
    box-shadow: 0 20px 45px rgba(22, 101, 52, 0.6) !important; 
}

/* Metrics - Dark Grey */
[data-testid="metric-container"] { 
    background: rgba(26, 31, 38, 0.8) !important; 
    border: 1px solid rgba(30, 58, 138, 0.4) !important; border-radius: 15px !important; 
}

/* Sidebar - Dark Blue */
section[data-testid="stSidebar"] > div { 
    background: linear-gradient(180deg, rgba(10, 14, 23, 0.95) 0%, rgba(26, 31, 38, 0.95) 100%) !important; 
    border-right: 1px solid rgba(30, 58, 138, 0.3) !important; 
}

/* Status & Progress */
div[data-testid="stStatusWidget"] { 
    background: rgba(15, 20, 26, 0.9) !important; border-radius: 15px !important; 
    border: 1px solid rgba(30, 58, 138, 0.3) !important; 
}

/* Code Blocks */
div[data-testid="stCode"] { 
    border-radius: 12px !important; border: 1px solid rgba(30, 58, 138, 0.3) !important; 
}

/* Text Readability */
.stMarkdown, p, div { color: #d1d5db !important; }
</style>
""", unsafe_allow_html=True)

# Agent (AFTER dotenv)
agent = V2SAgent(os.getenv("GEMINI_API_KEY"))

# Sidebar - Professional
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
        <h2 style="font-family: 'Times New Roman'; color: #d1d5db; font-weight: 700; margin: 0;">V2S Architect</h2>
        <p style="color: #94a3b8; font-size: 1rem; font-family: 'Times New Roman';">Autonomous Synthesis Pro</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1: st.metric("AI Engine", "Gemini 2.5", "Flash")
    with col2: st.metric("Status", "Production", "Ready")
    
    st.markdown("---")
    st.success("✅ **Pipeline Active**")
    st.caption("*Hand-drawn → Production Verilog*")

# Eye-catching Header
st.markdown('<h1 class="header-title">Autonomous System Synthesis</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-subtitle">Transform architectural sketches into production-ready repositories</p>', unsafe_allow_html=True)

# Main Layout - FIXED
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="card"><h3 style="color: #d1d5db; font-family: \'Times New Roman\';">📋 Architecture Input</h3></div>', unsafe_allow_html=True)
    
    # File upload with validation
    uploaded_file = st.file_uploader(
        "Upload VLSI/System Sketch", 
        type=["png", "jpg", "jpeg"],
        help="Hand-drawn or block diagrams (Max 5MB)",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        file_size = len(uploaded_file.getbuffer())
        if file_size > 5 * 1024 * 1024:
            st.error("❌ File too large (Max 5MB)")
            st.stop()
            
        st.image(uploaded_file, caption="📷 Input Architecture", use_container_width=True)
        
        col_btn1, col_btn2 = st.columns([4, 1])
        with col_btn1:
            if st.button("🚀 **Execute Synthesis Pipeline**", type="primary", use_container_width=True):
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    tmp.write(uploaded_file.getbuffer())
                    temp_path = tmp.name
                
                try:
                    with st.status("🔄 **Autonomous Pipeline Active**", expanded=True) as status:
                        # Phase 1: Clean Workspace
                        if os.path.exists("outputs"):
                            shutil.rmtree("outputs")
                        os.makedirs("outputs")
                        st.markdown("**<span style='color: #10b981'>✅ Workspace cleared</span>**", unsafe_allow_html=True)
                        
                        # Phase 2: Blueprint Extraction (ERROR HANDLED)
                        st.markdown("**🔍 Phase 1: Blueprint Extraction**")
                        raw_json = agent.analyze_diagram(temp_path)
                        try:
                            clean_json = re.sub(r'```json\n?|\n?```', '', raw_json).strip()
                            blueprint = json.loads(clean_json)
                            st.session_state.blueprint = blueprint
                            st.success("✅ Architecture blueprint extracted")
                        except Exception as e:
                            st.error(f"❌ Blueprint failed: {str(e)[:100]}")
                            st.code(raw_json[:600], language="json")
                            st.stop()
                        
                        # Phase 3: Code Synthesis
                        st.markdown("**🔨 Phase 2: Code Generation**")
                        full_text = ""
                        placeholder = st.empty()
                        
                        for chunk in agent.generate_all_code_stream(clean_json):  # Use clean_json
                            if hasattr(chunk, 'text') and chunk.text:
                                full_text += chunk.text
                                placeholder.code(full_text[-800:], language="verilog")
                        
                        st.session_state.full_code = full_text
                        
                        # Phase 4: Production Package
                        st.markdown("**📦 Phase 3: Production Packaging**")
                        pattern = r"---FILE_START:\s*(.+?)\s*---\s*(.+?)\s*---FILE_END---"
                        matches = re.findall(pattern, full_text, re.DOTALL | re.MULTILINE)
                        
                        files_generated = 0
                        for filename, content in matches:
                            save_generated_code(filename, content)
                            files_generated += 1
                        
                        # Auto README
                        readme = agent.generate_readme(clean_json, full_text)
                        save_generated_code("README.md", readme)
                        
                        st.session_state.zip_path = create_project_zip()
                        st.balloons()
                        st.markdown(f"**✨ Complete! Generated {files_generated + 1} files**")
                        
                finally:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                
                status.update(label="🎉 **Synthesis Complete**", state="complete")

with col_right:
    st.markdown('<div class="card"><h3 style="color: #d1d5db; font-family: \'Times New Roman\';">📊 Live Workspace</h3></div>', unsafe_allow_html=True)
    
    if st.session_state.blueprint:
        st.markdown("**🗺️ Architecture Blueprint**")
        mermaid_code = st.session_state.blueprint.get('mermaid_code', 'graph TD\nA[Input] --> B[Processor]\nB --> C[Output]')
        st.code(mermaid_code, language="mermaid")
        
        if st.session_state.zip_path and os.path.exists(st.session_state.zip_path):
            file_size = os.path.getsize(st.session_state.zip_path) / (1024 * 1024)
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Files Generated", len(os.listdir("outputs")), "Complete")
            with col_m2:
                st.metric("Package Size", f"{file_size:.1f} MB", "Ready")
            
            with open(st.session_state.zip_path, "rb") as f:
                st.download_button(
                    label="📥 **Download Production Package**",
                    data=f,
                    file_name=f"v2s_synthesis_pro.zip",
                    mime="application/zip",
                    use_container_width=True
                )
    else:
        st.info("👆 **Upload sketch** to activate autonomous synthesis")

# Professional Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #94a3b8; font-family: 'Times New Roman'; font-size: 1rem;">
    Production-ready autonomous code synthesis pipeline | Powered by Gemini 2.5 Flash
</div>
""", unsafe_allow_html=True)
