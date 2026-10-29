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

# 2. Expert Designer CSS Styling (Unified Cards & High Contrast)
st.markdown("""
    <style>
    /* Global App Background */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    /* Executive Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0A192F 0%, #1E3A8A 100%);
        border-radius: 20px;
        padding: 28px 24px;
        color: #FFFFFF;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(10, 25, 47, 0.15);
        border: 1px solid #334155;
    }
    .hero-title {
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF !important;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 14px;
        font-weight: 600;
        color: #94A3B8 !important;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    /* Unified Master Card Container */
    .master-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 26px;
        margin-bottom: 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
    }
    
    /* Step Header inside Cards */
    .step-header-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 6px;
    }
    .step-number {
        background-color: #0284C7;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 13px;
        padding: 5px 12px;
        border-radius: 20px;
    }
    .step-title {
        font-weight: 800;
        font-size: 19px;
        color: #0F172A !important;
        margin: 0;
    }
    .step-desc {
        font-size: 14px;
        font-weight: 600;
        color: #475569 !important;
        margin-bottom: 20px;
        margin-top: 0;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 14px;
    }

    /* Form Labels */
    .custom-label {
        font-size: 14px;
        font-weight: 700;
        color: #0F172A !important;
        margin-bottom: 6px;
        margin-top: 12px;
        display: block;
    }

    /* Dimension Pills */
    .meta-pill {
        background-color: #F8FAFC;
        border: 2px solid #E2E8F0;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        font-size: 13px;
        font-weight: 700;
        color: #0F172A;
    }
    
    /* Custom Action Button */
    .stButton>button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px 24px !important;
        font-size: 16px !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.3) !important;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0369A1 0%, #075985 100%) !important;
    }
    
    /* Diagnostic Result Boxes */
    .pathogen-box {
        background-color: #F0FDF4;
        border: 2px solid #86EFAC;
        border-radius: 16px;
        padding: 20px;
    }
    .pathogen-label {
        font-size: 12px;
        color: #166534;
        text-transform: uppercase;
        font-weight: 800;
        margin: 0;
    }
    .pathogen-name {
        font-size: 20px;
        font-weight: 900;
        font-style: italic;
        color: #14532D;
        margin: 4px 0 0 0;
    }
    
    .confidence-box {
        background-color: #F8FAFC;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
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

# Initialize session state
if 'acquisition_mode' not in st.session_state:
    st.session_state['acquisition_mode'] = 'Upload Image'

# ==========================================
# STEP 01: SPECIMEN CONFIGURATION CARD
# ==========================================
st.markdown("""
    <div class="master-card">
        <div class="step-header-row">
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

st.markdown("<span class='custom-label'>Image Acquisition Method:</span>", unsafe_allow_html=True)

col_m1, col_m2 = st.columns(2)
with col_m1:
    if st.button("📁 Upload File", use_container_width=True):
        st.session_state['acquisition_mode'] = 'Upload Image'
        if 'master_result' in st.session_state:
            del st.session_state['master_result']
with col_m2:
    if st.button("📷 Live Camera", use_container_width=True):
        st.session_state['acquisition_mode'] = 'Use Camera'
        if 'master_result' in st.session_state:
            del st.session_state['master_result']

uploaded_file = None
st.write("")

if st.session_state['acquisition_mode'] == 'Upload Image':
    uploaded_file = st.file_uploader(
        "Upload microscope slide image",
        type=["png", "jpg", "jpeg"]
    )
else:
    uploaded_file = st.camera_input("Snap picture through microscope eyepiece")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 02: SPECIMEN PREVIEW & EXECUTION
# ==========================================
if uploaded_file is not None:
    st.markdown("""
        <div class="master-card">
            <div class="step-header-row">
                <span class="step-number">02</span>
                <h3 class="step-title">Specimen Preview & Scan</h3>
            </div>
            <p class="step-desc">Inspect visual integrity before executing tensor inference.</p>
    """, unsafe_allow_html=True)
    
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    st.write("")
    img_w, img_h = image.size
    meta_c1, meta_c2 = st.columns(2)
    with meta_c1:
        st.markdown(f"""
            <div class="meta-pill">
                🖼️ Image Width<br><strong style="font-size: 16px; color: #0F172A;">{img_w} px</strong>
            </div>
        """, unsafe_allow_html=True)
    with meta_c2:
        st.markdown(f"""
            <div class="meta-pill">
                🖼️ Image Height<br><strong style="font-size: 16px; color: #0F172A;">{img_h} px</strong>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.write("")
    
    if st.button("🚀 Run AI Diagnostic Scan", use_container_width=True):
        with st.spinner("Waking cloud server & executing ONNX tensor inference (First request may take ~30s if asleep)..."):
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
                st.error("⚠️ Request timed out. The server might be waking up from sleep—please click 'Run AI Diagnostic Scan' again.")
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
        <div class="master-card">
            <div class="step-header-row">
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
                <p class="pathogen-label" style="color: #334155;">Confidence Level</p>
                <p style="font-size: 22px; font-weight: 900; color: #0284C7; margin: 2px 0 0 0;">{conf_val:.2f}%</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.markdown("<strong style='color: #0F172A;'>Model Confidence Distribution</strong>", unsafe_allow_html=True)
    st.progress(float(res.get('confidence', 0.0)))
    
    with st.expander("🔍 View Detailed Class Probability Breakdown"):
        probs = res.get('all_probabilities', {})
        for name, prob in probs.items():
            st.markdown(f"<strong style='color: #0F172A;'>{name}</strong>: `{prob * 100:.2f}%`", unsafe_allow_html=True)
            st.progress(float(prob))
            
    st.write("")
    if st.button("🔄 Clear / Scan New Slide", use_container_width=True):
        del st.session_state['master_result']
        st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)