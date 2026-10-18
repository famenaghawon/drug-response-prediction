import os
import sys
import streamlit as st


# ============================================================
# PATH FIX: Allows Python to find the 'src' folder from the 'app' folder
# ============================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="NEURO-RX :: Drug Response Intelligence",
    layout="wide",
    page_icon="🧬",
    initial_sidebar_state="expanded"
)


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')


from src.data_loader import load_gdsc_data, process_biomarkers
from src.model import train_drug_model


# ============================================================
# 🌌 ULTRA-FUTURISTIC CSS SYSTEM
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;600&display=swap');


    /* ---------- GLOBAL CANVAS ---------- */
    .stApp {
        background:
            radial-gradient(ellipse at 15% 10%, rgba(0, 200, 255, 0.10) 0%, transparent 45%),
            radial-gradient(ellipse at 85% 85%, rgba(160, 0, 255, 0.10) 0%, transparent 45%),
            radial-gradient(ellipse at 50% 50%, rgba(0, 255, 180, 0.05) 0%, transparent 60%),
            linear-gradient(180deg, #04070d 0%, #080c17 50%, #04070d 100%);
        background-attachment: fixed;
        font-family: 'Rajdhani', sans-serif;
        color: #d8e6ff;
    }


    /* Animated grid overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient(rgba(0, 200, 255, 0.045) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 200, 255, 0.045) 1px, transparent 1px);
        background-size: 48px 48px;
        pointer-events: none;
        z-index: 0;
        animation: gridDrift 24s linear infinite;
    }
    @keyframes gridDrift {
        0% { background-position: 0 0, 0 0; }
        100% { background-position: 48px 48px, 48px 48px; }
    }


    .block-container { padding-top: 1.5rem; padding-bottom: 3rem; position: relative; z-index: 1; }


    /* ---------- HERO ---------- */
    .hero-wrap { text-align: center; padding: 2rem 1rem 1.5rem 1rem; position: relative; }
    .hero-tag {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 4px;
        color: #00e5ff;
        padding: 6px 18px;
        border: 1px solid rgba(0, 229, 255, 0.35);
        border-radius: 30px;
        background: rgba(0, 229, 255, 0.06);
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        box-shadow: 0 0 24px rgba(0, 229, 255, 0.25), inset 0 0 12px rgba(0, 229, 255, 0.08);
    }
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.2rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: 3px;
        background: linear-gradient(120deg, #00e5ff 0%, #7c4dff 40%, #ff00e5 70%, #00e5ff 100%);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 8s ease infinite;
        text-shadow: 0 0 80px rgba(124, 77, 255, 0.4);
        line-height: 1.15;
    }
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    .sub-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #6d86ad;
        letter-spacing: 2.5px;
        margin-top: 0.8rem;
        text-transform: uppercase;
    }
    .sub-title span { color: #00e5ff; }


    /* ---------- METRIC CARDS (HOLOGRAPHIC) ---------- */
    .metric-card {
        position: relative;
        background: linear-gradient(135deg, rgba(12, 22, 40, 0.92) 0%, rgba(20, 35, 60, 0.85) 100%);
        border: 1px solid rgba(0, 229, 255, 0.22);
        border-radius: 16px;
        padding: 1.4rem 1.2rem;
        margin-bottom: 1rem;
        overflow: hidden;
        backdrop-filter: blur(12px);
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.06),
            0 0 24px rgba(0, 229, 255, 0.06);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, #00e5ff, #7c4dff, transparent);
        animation: scanLine 3s linear infinite;
    }
    @keyframes scanLine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 229, 255, 0.5);
        box-shadow:
            0 12px 40px rgba(0, 0, 0, 0.6),
            0 0 40px rgba(0, 229, 255, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #7c9ac4;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.4rem;
    }
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
        background: linear-gradient(135deg, #00e5ff, #7c4dff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 1px;
    }
    .metric-value.danger {
        background: linear-gradient(135deg, #ff4d6d, #ff00e5);
        -webkit-background-clip: text; background-clip: text;
    }
    .metric-value.success {
        background: linear-gradient(135deg, #00ffa3, #00e5ff);
        -webkit-background-clip: text; background-clip: text;
    }
    .metric-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #4d6888;
        margin-top: 0.35rem;
        letter-spacing: 0.5px;
    }


    /* ---------- SECTION HEADERS ---------- */
    .section-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #e0f0ff;
        letter-spacing: 2px;
        margin: 1rem 0 1.2rem 0;
        padding-left: 1rem;
        border-left: 3px solid #00e5ff;
        text-shadow: 0 0 20px rgba(0, 229, 255, 0.4);
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .section-header::before {
        content: "▸";
        color: #00e5ff;
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }


    /* ---------- TABS ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(8, 14, 26, 0.6);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(0, 229, 255, 0.15);
        backdrop-filter: blur(10px);
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        color: #6d86ad;
        background: transparent;
        border-radius: 10px;
        padding: 10px 20px;
        border: 1px solid transparent;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #00e5ff;
        background: rgba(0, 229, 255, 0.06);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.15), rgba(124, 77, 255, 0.15)) !important;
        color: #00e5ff !important;
        border: 1px solid rgba(0, 229, 255, 0.4) !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.2), inset 0 0 12px rgba(0, 229, 255, 0.05);
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }


    /* ---------- SIDEBAR ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #060a12 0%, #0a1120 100%);
        border-right: 1px solid rgba(0, 229, 255, 0.15);
    }
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        font-family: 'Orbitron', sans-serif;
        color: #00e5ff;
        letter-spacing: 2px;
        font-size: 1rem;
        border-bottom: 1px solid rgba(0, 229, 255, 0.2);
        padding-bottom: 0.6rem;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] li {
        color: #a8bbd4;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.92rem;
    }


    /* ---------- INPUTS ---------- */
    .stSelectbox > div > div {
        background: rgba(10, 18, 32, 0.9) !important;
        border: 1px solid rgba(0, 229, 255, 0.25) !important;
        border-radius: 10px !important;
        color: #d8e6ff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
    }
    .stSelectbox label {
        font-family: 'JetBrains Mono', monospace !important;
        color: #7c9ac4 !important;
        font-size: 0.72rem !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
    }


    /* ---------- BUTTONS ---------- */
    .stButton > button, .stDownloadButton > button {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 2px;
        font-weight: 600;
        text-transform: uppercase;
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.12), rgba(124, 77, 255, 0.12));
        color: #00e5ff;
        border: 1px solid rgba(0, 229, 255, 0.4);
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 0 rgba(0, 229, 255, 0);
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.25), rgba(124, 77, 255, 0.25));
        border-color: #00e5ff;
        box-shadow: 0 0 24px rgba(0, 229, 255, 0.5);
        transform: translateY(-2px);
    }


    /* ---------- ALERTS / INFO ---------- */
    .stAlert {
        background: rgba(10, 18, 32, 0.85) !important;
        border: 1px solid rgba(0, 229, 255, 0.25) !important;
        border-left: 3px solid #00e5ff !important;
        border-radius: 10px !important;
        color: #a8bbd4 !important;
        font-family: 'Rajdhani', sans-serif !important;
        backdrop-filter: blur(10px);
    }


    /* ---------- DATAFRAME ---------- */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 0 24px rgba(0, 229, 255, 0.05);
    }


    /* ---------- METRICS (native) ---------- */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(12, 22, 40, 0.9), rgba(20, 35, 60, 0.85));
        border: 1px solid rgba(0, 229, 255, 0.22);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    [data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: #7c9ac4 !important;
        font-size: 0.7rem !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif !important;
        color: #00e5ff !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
    }


    /* ---------- SPINNER ---------- */
    .stSpinner > div {
        border-top-color: #00e5ff !important;
    }


    /* ---------- FOOTER ---------- */
    .footer {
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        color: #3d5673;
        font-size: 0.72rem;
        letter-spacing: 2px;
        margin-top: 3rem;
        padding: 1.5rem;
        border-top: 1px solid rgba(0, 229, 255, 0.12);
        text-transform: uppercase;
    }
    .footer span { color: #00e5ff; }
    .footer .heart { color: #ff00e5; animation: heartbeat 1.6s ease-in-out infinite; }
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.25); }
    }


    /* ---------- SCROLLBAR ---------- */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #04070d; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00e5ff, #7c4dff);
        border-radius: 4px;
    }


    /* ---------- HIDE STREAMLIT CHROME ---------- */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 🧬 HERO SECTION
# ============================================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-tag">◉ NEURO-RX v3.0 // Precision Oncology Intelligence</div>
    <h1 class="main-title">DRUG RESPONSE<br>PREDICTION ENGINE</h1>
    <p class="sub-title">
        GDSC Real-Data <span>◆</span> Train/Test Split <span>◆</span> FDR Statistics <span>◆</span> Neural ML Core
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# 📊 DATA LOAD (P0-3 & P1-5 FIXES)
# ============================================================

# 1. Add caching HERE in the UI layer, keeping the backend pure
@st.cache_data(show_spinner="⚡ Streaming pharmacogenomic data...")
def cached_load_data():
    return load_gdsc_data()

# 2. Wrap in try/except with accurate error message
try:
    df_resp, df_expr = cached_load_data()
except Exception as e:
    # Fixes P1-5: Accurate error message pointing to Hugging Face
    st.error(f"🚨 Data stream failed. Please verify your network connection or Hugging Face dataset URLs. Details: {e}")
    st.stop()


if df_resp is not None and df_expr is not None:


    # ------------------------------------------------------------
    # SIDEBAR
    # ------------------------------------------------------------
    with st.sidebar:
        st.markdown("## ⚙ Control Deck")
        available_drugs = df_resp['Drug'].unique()
        default_drugs = ['Erlotinib', 'Gefitinib', 'Afatinib', 'Osimertinib']
        selected_drug = st.selectbox(
            "Target Compound",
            [d for d in default_drugs if d in available_drugs] or available_drugs
        )


        st.markdown("---")
        st.markdown("## 🧪 Methodology")
        st.info(
            "**Data Leakage Protocol:** 80/20 split enforced *before* "
            "statistical testing. FDR is computed strictly on the training partition."
        )


        st.markdown("---")
        st.markdown("## 📡 System Status")
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#6d86ad; line-height:2;">
        <span style="color:#00ffa3;">●</span> GDSC Interface &nbsp; <span style="color:#00e5ff;">ONLINE</span><br>
        <span style="color:#00ffa3;">●</span> FDR Engine &nbsp;&nbsp;&nbsp;&nbsp; <span style="color:#00e5ff;">ACTIVE</span><br>
        <span style="color:#00ffa3;">●</span> ML Core &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span style="color:#00e5ff;">READY</span><br>
        <span style="color:#ff00e5;">◉</span> Encryption &nbsp;&nbsp;&nbsp;&nbsp; <span style="color:#ff00e5;">QUANTUM</span>
        </div>
        """, unsafe_allow_html=True)


    # ------------------------------------------------------------
    # PROCESS
    # ------------------------------------------------------------
    with st.spinner("⚡ Running biomarker computation pipeline..."):
        train_df, test_df, results_df = process_biomarkers(df_resp, df_expr, selected_drug)


    if results_df is None:
        st.error(f"Insufficient matched cell lines for **{selected_drug}**. Pipeline halted.")
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "◈ VOLCANO SCAN",
            "◈ DOSE-RESPONSE",
            "◈ ML PREDICTOR",
            "◈ INTEGRITY"
        ])


        # ============================================================
        # TAB 1 — VOLCANO
        # ============================================================
        with tab1:
            st.markdown(f'<div class="section-header">Biomarker Discovery :: {selected_drug}</div>', unsafe_allow_html=True)


            col1, col2 = st.columns([3, 1])


            with col1:
                results_df['plot_y'] = np.clip(results_df['-log10_P_Raw'], 0, 12)


                fig = px.scatter(
                    results_df, x='Correlation', y='plot_y',
                    color='Significant', hover_name='Gene',
                    color_discrete_map={True: '#ff00e5', False: '#2a3f5f'},
                    labels={'plot_y': '-log10(Raw P-value)', 'Correlation': 'Pearson Correlation (r)'},
                    title=f"Volcano Scan :: Gene Expression vs {selected_drug} IC50",
                    template='plotly_dark'
                )
                fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="#00ffa3",
                              annotation_text="P=0.05", annotation_font_color="#00ffa3")
                fig.add_vline(x=0.2, line_dash="dash", line_color="#00ffa3")
                fig.add_vline(x=-0.2, line_dash="dash", line_color="#00ffa3")


                fig.update_traces(marker=dict(size=7, line=dict(width=0.5, color='rgba(0,229,255,0.35)')))
                fig.update_layout(
                    height=520,
                    margin=dict(l=0, r=0, t=50, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(4,7,13,0.6)',
                    font=dict(family='Rajdhani', color='#a8bbd4'),
                    title_font=dict(family='Orbitron', size=14, color='#00e5ff'),
                    legend=dict(
                        bgcolor='rgba(10,18,32,0.8)',
                        bordercolor='rgba(0,229,255,0.3)',
                        borderwidth=1,
                        font=dict(family='JetBrains Mono', size=10)
                    ),
                    xaxis=dict(gridcolor='rgba(0,229,255,0.07)', zerolinecolor='rgba(0,229,255,0.2)'),
                    yaxis=dict(gridcolor='rgba(0,229,255,0.07)', zerolinecolor='rgba(0,229,255,0.2)')
                )
                st.plotly_chart(fig, use_container_width=True)


            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Genes Scanned</div>
                    <div class="metric-value">{len(results_df):,}</div>
                    <div class="metric-sub">HIGH-DIMENSIONAL SPACE</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Significant Biomarkers</div>
                    <div class="metric-value success">{results_df['Significant'].sum():,}</div>
                    <div class="metric-sub">FDR &lt; 0.05 THRESHOLD</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Train Cell Lines</div>
                    <div class="metric-value danger">{len(train_df)}</div>
                    <div class="metric-sub">HELD-OUT TEST: {len(test_df)}</div>
                </div>
                """, unsafe_allow_html=True)


                st.download_button(
                    "⤓ EXPORT BIOMARKERS",
                    results_df.to_csv(index=False),
                    "biomarkers.csv",
                    use_container_width=True
                )


        # ============================================================
        # TAB 2 — DOSE RESPONSE
        # ============================================================
        with tab2:
            st.markdown(f'<div class="section-header">Dose-Response Analysis :: {selected_drug}</div>', unsafe_allow_html=True)


            fig_hist = px.histogram(
                pd.concat([train_df, test_df]), x='IC50', nbins=30,
                title=f"LN(IC50) Distribution :: All Matched Cell Lines",
                labels={'IC50': 'LN(IC50)'},
                color_discrete_sequence=['#00e5ff'],
                template='plotly_dark'
            )
            fig_hist.update_traces(
                marker=dict(line=dict(width=1, color='rgba(124,77,255,0.6)'))
            )
            fig_hist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(4,7,13,0.6)',
                font=dict(family='Rajdhani', color='#a8bbd4'),
                title_font=dict(family='Orbitron', size=14, color='#00e5ff'),
                xaxis=dict(gridcolor='rgba(0,229,255,0.07)'),
                yaxis=dict(gridcolor='rgba(0,229,255,0.07)'),
                height=450
            )
            st.plotly_chart(fig_hist, use_container_width=True)


            st.markdown('<div class="section-header">Top 10 Most Sensitive Cell Lines</div>', unsafe_allow_html=True)
            sensitive = pd.concat([train_df, test_df]).nsmallest(10, 'IC50')[['Cell_Line', 'IC50']]
            st.dataframe(sensitive, use_container_width=True)


        # ============================================================
        # TAB 3 — ML PREDICTOR
        # ============================================================
        with tab3:
            st.markdown('<div class="section-header">Neural ML Core :: IC50 Prediction</div>', unsafe_allow_html=True)
            st.markdown(
                "<p style='font-family:JetBrains Mono; color:#6d86ad; font-size:0.82rem; letter-spacing:1px;'>"
                "RANDOM FOREST MODEL :: TRAINED EXCLUSIVELY ON TRAINING PARTITION</p>",
                unsafe_allow_html=True
            )


            top_genes = results_df[results_df['Significant']]['Gene'].head(20).tolist()
            if len(top_genes) < 5:
                top_genes = results_df['Gene'].head(20).tolist()


            model, metrics, pred_df = train_drug_model(train_df, test_df, top_genes)


            # Metric strip
            st.markdown('<div class="section-header">Performance Telemetry</div>', unsafe_allow_html=True)
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Cross-Val R² (Train)", f"{metrics['cv_r2_mean']:.3f}")
            col_b.metric("Test R² (Unseen)", f"{metrics['test_r2']:.3f}")
            col_c.metric("Test RMSE", f"{metrics['test_rmse']:.3f}")


            st.markdown("---")


            col_ml1, col_ml2 = st.columns(2)


            with col_ml1:
                st.markdown('<div class="section-header">Predicted vs Actual</div>', unsafe_allow_html=True)
                fig_pred = px.scatter(
                    pred_df, x='Actual', y='Predicted',
                    trendline="ols", trendline_color_override="#ff00e5",
                    labels={'Actual': 'Actual LN(IC50)', 'Predicted': 'Predicted LN(IC50)'},
                    template='plotly_dark', color_discrete_sequence=['#00e5ff']
                )
                fig_pred.update_traces(marker=dict(size=9, line=dict(width=1, color='rgba(0,229,255,0.5)')))
                fig_pred.update_layout(
                    height=420,
                    margin=dict(l=0, r=0, t=20, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(4,7,13,0.6)',
                    font=dict(family='Rajdhani', color='#a8bbd4'),
                    xaxis=dict(gridcolor='rgba(0,229,255,0.07)'),
                    yaxis=dict(gridcolor='rgba(0,229,255,0.07)')
                )
                st.plotly_chart(fig_pred, use_container_width=True)


            with col_ml2:
                st.markdown('<div class="section-header">🔮 Prediction Simulator</div>', unsafe_allow_html=True)
                st.markdown(
                    "<p style='font-family:JetBrains Mono; color:#6d86ad; font-size:0.8rem;'>"
                    "SELECT AN UNSEEN TEST-SET CELL LINE</p>",
                    unsafe_allow_html=True
                )


                test_cell = st.selectbox("Cell Line ID", test_df['Cell_Line'].unique())
                cell_idx = test_df[test_df['Cell_Line'] == test_cell].index[0]
                actual_val = test_df.loc[cell_idx, 'IC50']


                train_medians = train_df[top_genes].median()
                cell_features = test_df.loc[[cell_idx], top_genes].fillna(train_medians)
                predicted_val = model.predict(cell_features.values)[0]


                col_sim1, col_sim2 = st.columns(2)
                col_sim1.metric("Actual LN(IC50)", f"{actual_val:.3f}")
                col_sim2.metric(
                    "Predicted LN(IC50)",
                    f"{predicted_val:.3f}",
                    delta=f"{predicted_val - actual_val:.3f} (Error)"
                )


        # ============================================================
        # TAB 4 — INTEGRITY
        # ============================================================
        with tab4:
            st.markdown('<div class="section-header">Pipeline Integrity Protocols</div>', unsafe_allow_html=True)


            st.markdown("""
            <div style="background:rgba(10,18,32,0.7); border:1px solid rgba(0,229,255,0.2);
                        border-radius:14px; padding:1.5rem; font-family:'Rajdhani',sans-serif;
                        color:#a8bbd4; line-height:2; backdrop-filter:blur(10px);">
                <div style="font-family:'Orbitron'; color:#00e5ff; font-size:0.85rem;
                            letter-spacing:2px; margin-bottom:0.8rem;">◆ METHODOLOGICAL RIGOR</div>
                <b style="color:#e0f0ff;">▸ Train/Test Split:</b> 80/20 split enforced <i>before</i> statistical testing to eliminate data leakage.<br>
                <b style="color:#e0f0ff;">▸ Imputation:</b> Medians computed on training partition, propagated to test partition.<br>
                <b style="color:#e0f0ff;">▸ Multiple Testing:</b> Benjamini-Hochberg (FDR) applied strictly to the training set.<br>
                <b style="color:#e0f0ff;">▸ ML Validation:</b> 5-Fold Cross-Validation on train; final metrics on unseen test.
            </div>
            """, unsafe_allow_html=True)


            st.markdown('<div class="section-header">Top Biomarkers (FDR &lt; 0.05)</div>', unsafe_allow_html=True)


            sig_genes = results_df[results_df['P_Value_FDR'] < 0.05].head(10)
            if sig_genes.empty:
                st.info(
                    "No gene passed the strict FDR < 0.05 threshold. This is common in "
                    "high-dimensional biology (41k genes) due to severe multiple-testing penalty."
                )
            else:
                st.dataframe(sig_genes[['Gene', 'Correlation', 'P_Value_FDR']], use_container_width=True)


else:
    st.warning("⚠ Data loading failed. Verify `data/raw/` directory integrity.")


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    NEURO-RX INTELLIGENCE PLATFORM <span>◆</span>
    ENGINEERED BY <span>FREEDOM EVBAKOE AMENAGHAWON</span> <span>◆</span>
    GDSC REAL-DATA INTEGRATION <span>◆</span>
    POWERED BY STREAMLIT <span class="heart">♥</span>
</div>
""", unsafe_allow_html=True)
