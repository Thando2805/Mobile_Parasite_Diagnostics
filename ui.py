import streamlit as st
import requests
import io
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Bio-Lens | Professional Diagnostic Suite",
    page_icon="🔬",
    layout="centered"
)

# 2. Uniform, High-Visibility Clinical Theme CSS
st.markdown("""
    <style>
    /* Global App Background & Uniform Typography */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Professional Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0B132B 0%, #1C2541 100%);
        border-radius: 16px;
        padding: 24px 22px;
        color: #FFFFFF;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(11, 19, 43, 0.2);
        border: 1px solid #334155;
    }
    .hero-title {
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF !important;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 13px;
        font-weight: 600;
        color: #94A3B8 !important;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    /* Uniform White Card Containers */
    .app-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 18px;
        border: 2px solid #CBD5E1;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }
    
    /* Uniform Step Header */
    .step-badge-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }
    .step-number {
        background-color: #0284C7;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 13px;
        padding: 4px 10px;
        border-radius: 20px;
    }
    .step-title {
        font-weight: 800;
        font-size: 18px;
        color: #0F172A !important;
        margin: 0;
    }
    .step-desc {
        font-size: 13px;
        font-weight: 600;
        color: #334155 !important;
        margin-bottom: 14px;
        margin-top: 0;
    }

    /* Uniform Widget Labels */
    .stSelectbox label, .stFileUploader label, .stRadio label, p, span {
        font-weight: 700 !important;
        color: #0F172A !important;
        font-size: 14px !important;
    }

    /* Dimension & Meta Pills */
    .meta-pill {
        background-color: #F1F5F9;
        border: 2px solid #CBD5E1;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        font-size: 13px;
        font-weight: 700;
        color: #0F172A;
    }
    
    /* Uniform Action Button */
    .stButton>button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px 24px !important;
        font-size: 16px !important;
        box-shadow: 0 6px 16px rgba(2, 132, 199, 0.35) !important;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0369A1 0%, #075985 100%) !important;
    }
    
    /* Clinical Results Boxes */
    .pathogen-box {
        background-color: #F0FDF4;
        border: 2px solid #86EFAC;
        border-radius: 14px;
        padding: 16px 18px;
    }
    .pathogen-label {
        font-size: 11px;
        color: #166534;
        text-transform: uppercase;
        font-weight: 800;
        margin: 0;
    }
    .pathogen-name {
        font-size: 19px;
        font-weight: 900;
        font-style: italic;
        color: #14532D;
        margin: 4px 0 0 0;
    }
    
    .confidence-box {
        background-color: #F1F5F9;
        border: 2px solid #CBD5E1;
        border-radius: 14px;
        padding: 16px 18px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Banner
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🔬 Mobile Parasite Diagnostics</div>
        <p class="hero-subtitle">Field-Ready AI Microscopic Identification Suite • ONNX Accelerated</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# STEP 01: SPECIMEN CONFIGURATION CARD
# ==========================================
st.markdown("""
    <div class="app-card">
        <div class="step-badge-row">
            <span class="step-number">01</span>
            <h3 class="step-title">Specimen Configuration</h3>
        </div>
        <p class="step-desc">Select diagnostic domain and input methodology for slide analysis.</p>
""", unsafe_allow_html=True)

domain = st.selectbox(
    "Select Diagnostic Domain",
    [
        "Malaria",
        "External Parasites",
        "Helminths",
        "Environmental & Waterborne Pathogens"
    ]
)

st.write("")
st.markdown("<p style='font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 8px;'>Image Acquisition Method:</p>", unsafe_allow_html=True)

tab_upload, tab_camera = st.tabs(["📁 Upload Image File", "📷 Live Rear Camera"])

uploaded_file = None

with tab_upload:
    up_file = st.file_uploader("Upload microscope slide image (PNG, JPG)", type=["png", "jpg", "jpeg"])
    if up_file is not None:
        uploaded_file = up_file

with tab_camera:
    st.markdown("""
        <div style='background-color: #E0F2FE; border: 1px solid #BAE6FD; border-radius: 10px; padding: 10px 14px; margin-bottom: 10px;'>
            <p style='color: #0369A1; font-size: 13px; font-weight: 700; margin: 0;'>💡 Field Tip: Ensure your mobile browser is set to use your phone's <b>Rear / Back Camera</b> to capture through the microscope eyepiece.</p>
        </div>
    """, unsafe_allow_html=True)
    cam_file = st.camera_input("Snap picture through microscope eyepiece (Rear Camera)")
    if cam_file is not None:
        uploaded_file = cam_file

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 02: SPECIMEN PREVIEW & EXECUTION
# ==========================================
if uploaded_file is not None:
    st.markdown("""
        <div class="app-card">
            <div class="step-badge-row">
                <span class="step-number">02</span>
                <h3 class="step-title">Specimen Preview & Scan</h3>
            </div>
            <p class="step-desc">Inspect visual integrity below before executing tensor inference.</p>
    """, unsafe_allow_html=True)
    
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    st.write("")
    img_w, img_h = image.size
    meta_c1, meta_c2 = st.columns(2)
    with meta_c1:
        st.markdown(f"""
            <div class="meta-pill">
                🖼️ Image Width<br><strong style="font-size: 15px; color: #0F172A;">{img_w} px</strong>
            </div>
        """, unsafe_allow_html=True)
    with meta_c2:
        st.markdown(f"""
            <div class="meta-pill">
                🖼️ Image Height<br><strong style="font-size: 15px; color: #0F172A;">{img_h} px</strong>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.write("")
    
    # Run Diagnostic Scan button positioned directly BELOW the picture box and dimensions
    if st.button("🚀 Run AI Diagnostic Scan", key="btn_scan"):
        with st.spinner("Waking cloud server & executing ONNX tensor inference..."):
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="JPEG")
            img_byte_arr.seek(0)
            try:
                backend_url = "https://mobile-parasite-diagnostics.onrender.com/api/v1/predict"
                files = {"file": ("slide.jpg", img_byte_arr, "image/jpeg")}
                data = {"domain": domain}
                
                response = requests.post(backend_url, files=files, data=data, timeout=60)
                if response.status_code == 200:
                    st.session_state['master_result'] = response.json()
                else:
                    st.error(f"Server Error [{response.status_code}]: {response.text}")
            except requests.exceptions.Timeout:
                st.error("⚠️ Request timed out. The server was sleeping—please click 'Run AI Diagnostic Scan' again.")
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Backend connection failed. Check your internet connection.")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 03: ANALYSIS RESULTS REPORT
# ==========================================
if 'master_result' in st.session_state:
    res = st.session_state['master_result']
    parasite_name = res.get('parasite_name', 'Unknown')
    conf_val = res.get('confidence', 0.0) * 100
    
    st.markdown("""
        <div class="app-card">
            <div class="step-badge-row">
                <span class="step-number" style="background-color: #059669;">03</span>
                <h3 class="step-title">Diagnostic Report</h3>
            </div>
            <p class="step-desc">Automated scientific classification output.</p>
    """, unsafe_allow_html=True)
    
    r_col1, r_col2 = st.columns([1.6, 1])
    with r_col1:
        st.markdown(f"""
            <div class="pathogen-box">
                <p class="pathogen-label">Identified Classification</p>
                <p class="pathogen-name">{parasite_name}</p>
            </div>
        """, unsafe_allow_html=True)
    with r_col2:
        st.markdown(f"""
            <div class="confidence-box">
                <p class="pathogen-label" style="color: #475569;">Confidence Level</p>
                <p style="font-size: 20px; font-weight: 900; color: #0284C7; margin: 2px 0 0 0;">{conf_val:.2f} %</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.markdown("<strong style='color: #0F172A; font-size: 14px;'>Model Confidence Distribution</strong>", unsafe_allow_html=True)
    st.progress(float(res.get('confidence', 0.0)))
    
    with st.expander("🔍 View Detailed Class Probability Breakdown"):
        probs = res.get('all_probabilities', {})
        for name, prob in probs.items():
            st.markdown(f"<strong style='color: #0F172A;'>{name}</strong>: `{prob * 100:.2f}%`", unsafe_allow_html=True)
            st.progress(float(prob))
            
    st.write("")
    if st.button("🔄 Clear / Scan New Slide", key="btn_clear"):
        del st.session_state['master_result']
        st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)