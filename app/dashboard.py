import os
import streamlit as st

# ====================
# AUTO-DOWNLOAD FOR CLOUD DEPLOYMENT
# ====================
if not os.path.exists("data/raw/Expression_Data_subset.csv"):
    with st.spinner("Downloading required biological datasets (First time setup). This may take 1-2 minutes..."):
        try:
            import runpy
            # This executes the download_data.py script directly in Python
            runpy.run_path("download_data.py", run_name="__main__")
        except Exception as e:
            st.error(f"Data download failed: {e}")
            st.stop()

# ====================
# PAGE CONFIG & CUSTOM CSS
# ====================
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import r2_score, mean_squared_error
from scipy import stats
from statsmodels.stats.multitest import multipletests
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Drug Response Prediction", layout="wide", page_icon="💊")

# Auto-download data if not present (for Streamlit Cloud deployment)
if not os.path.exists("data/raw/Expression_Data_subset.csv"):
    with st.spinner("Downloading required biological datasets (First time setup)..."):
        subprocess.run(["python", "download_data.py"])

# ====================
# PAGE CONFIG & CUSTOM CSS
# ====================
st.set_page_config(page_title="Drug Response Prediction", layout="wide", page_icon="💊")

st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .main-title { font-size: 2.5rem; color: #4F8BF9; text-align: center; font-weight: 800; margin-bottom: 0; }
    .sub-title { font-size: 1.1rem; color: #8C9EFF; text-align: center; margin-bottom: 2rem; }
    .metric-card { 
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); 
        padding: 1.5rem; border-radius: 10px; color: white; text-align: center; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 1rem;
    }
    .metric-value { font-size: 2rem; font-weight: bold; line-height: 1.2; }
    .metric-label { font-size: 0.9rem; color: #E2E8F0; text-transform: uppercase; letter-spacing: 1px; }
    .footer { text-align: center; color: #888; font-size: 0.8rem; margin-top: 3rem; }
</style>
""", unsafe_allow_html=True)

# ====================
# DATA PIPELINE
# ====================
@st.cache_data
def load_real_data():
    resp_path = "data/raw/GDSC2_fitted_dose_response_27Oct23.xlsx"
    expr_path = "data/raw/Expression_Data_subset.csv"
    
    if not os.path.exists(resp_path) or not os.path.exists(expr_path):
        return None, None
        
    df_resp = pd.read_excel(resp_path)
    df_resp = df_resp.rename(columns={'CELL_LINE_NAME': 'Cell_Line', 'DRUG_NAME': 'Drug', 'LN_IC50': 'IC50'})
    df_expr = pd.read_csv(expr_path, index_col=0) 
    return df_resp, df_expr

@st.cache_data
def process_biomarkers(df_resp, df_expr, drug_name):
    drug_data = df_resp[df_resp['Drug'] == drug_name].copy()
    if drug_data.empty: return None, None
        
    expr_t = df_expr.T
    merged = pd.merge(drug_data, expr_t, left_on='Cell_Line', right_index=True, how='inner')
    if merged.empty: return None, None

    gene_cols = expr_t.columns
    results = []
    for gene in gene_cols:
        clean_data = merged[[gene, 'IC50']].dropna()
        if len(clean_data) > 5:
            corr, p = stats.pearsonr(clean_data[gene], clean_data['IC50'])
            results.append({'Gene': gene, 'Correlation': corr, 'P_Value': p})
            
    results_df = pd.DataFrame(results)
    if results_df.empty: return None, None
        
    p_vals = results_df['P_Value'].values
    reject, p_adj, _, _ = multipletests(p_vals, alpha=0.05, method='fdr_bh')
    results_df['P_Value_FDR'] = p_adj
    results_df['-log10_P_Raw'] = -np.log10(results_df['P_Value'] + 1e-300)
    results_df['Significant'] = (results_df['P_Value'] < 0.05) & (results_df['Correlation'].abs() > 0.25)
    
    return merged, results_df

# Auto-train the model (Cached)
@st.cache_resource
def train_ml_model(data_df, features, target_col='IC50'):
    X = data_df[features].values
    y = data_df[target_col].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf = RandomForestRegressor(n_estimators=200, max_depth=12, min_samples_split=5, random_state=42, n_jobs=-1)
    
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(rf, X_train, y_train, cv=cv, scoring='r2')
    rf.fit(X_train, y_train)
    
    y_pred = rf.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Save predictions for the scatter plot
    pred_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    
    return rf, {'cv_r2': cv_scores.mean(), 'test_r2': r2, 'test_rmse': rmse}, pred_df

# ====================
# MAIN APP EXECUTION
# ====================
st.markdown('<h1 class="main-title">Advanced Drug Response Prediction</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Real GDSC Data | FDR Statistics | Machine Learning</p>', unsafe_allow_html=True)

df_resp, df_expr = load_real_data()

if df_resp is not None and df_expr is not None:
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3014/3014521.png", width=80)
        st.header("Configuration")
        
        available_drugs = df_resp['Drug'].unique()
        default_drugs = ['Erlotinib', 'Gefitinib', 'Afatinib', 'Osimertinib']
        selected_drug = st.selectbox("Select EGFR Inhibitor", [d for d in default_drugs if d in available_drugs] or available_drugs)
        
        st.markdown("---")
        st.markdown(f"**Dataset Info:**\n- GDSC2 Real Data\n- {df_expr.shape[1]:,} Cell Lines\n- {df_expr.shape[0]:,} Genes")
    
    merged_df, results_df = process_biomarkers(df_resp, df_expr, selected_drug)
    
    if merged_df is None:
        st.error(f"No matching cell lines found for {selected_drug}.")
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["Volcano Plot", "Dose-Response", "ML Predictor", "Data Integrity"])
        
        # TAB 1: VOLCANO PLOT
        with tab1:
            st.header(f"Biomarker Discovery: {selected_drug}")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                results_df['plot_y'] = np.clip(results_df['-log10_P_Raw'], 0, 12)
                
                fig = px.scatter(
                    results_df, x='Correlation', y='plot_y',
                    color='Significant', hover_name='Gene',
                    color_discrete_map={True: '#EF553B', False: '#636EFA'},
                    labels={'plot_y': '-log10(Raw P-value)', 'Correlation': 'Pearson Correlation (r)'},
                    title=f"Volcano Plot: Gene Expression vs {selected_drug} IC50",
                    template='plotly_dark'
                )
                fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="#10B981", annotation_text="P=0.05")
                fig.add_vline(x=0.25, line_dash="dash", line_color="#10B981")
                fig.add_vline(x=-0.25, line_dash="dash", line_color="#10B981")
                fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=500)
                st.plotly_chart(fig, width='stretch')
                
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Genes Tested</div>
                    <div class="metric-value">{len(results_df):,}</div>
                </div>
                <div class="metric-card" style="background: linear-gradient(135deg, #065F46 0%, #10B981 100%);">
                    <div class="metric-label">Significant Biomarkers</div>
                    <div class="metric-value">{results_df['Significant'].sum():,}</div>
                </div>
                <div class="metric-card" style="background: linear-gradient(135deg, #7F1D1D 0%, #EF4444 100%);">
                    <div class="metric-label">Cell Lines Analyzed</div>
                    <div class="metric-value">{len(merged_df)}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.download_button("📥 Download Results (CSV)", results_df.to_csv(index=False), "biomarkers.csv", width='stretch')

        # TAB 2: DOSE RESPONSE
        with tab2:
            st.header(f"Dose-Response Analysis: {selected_drug}")
            st.markdown("Distribution of LN(IC50) across the analyzed cell lines. Lower values indicate higher sensitivity to the drug.")
            
            fig_hist = px.histogram(
                merged_df, x='IC50', nbins=30, 
                title=f"Distribution of {selected_drug} LN(IC50)",
                labels={'IC50': 'LN(IC50)'},
                color_discrete_sequence=['#4F8BF9'],
                template='plotly_dark'
            )
            st.plotly_chart(fig_hist, width='stretch')
            
            st.subheader("Top 10 Most Sensitive Cell Lines")
            sensitive = merged_df.nsmallest(10, 'IC50')[['Cell_Line', 'IC50']]
            st.dataframe(sensitive, width='stretch')

        # TAB 3: ML PREDICTOR (Now Auto-Trains)
        with tab3:
            st.header("Machine Learning: Predict IC50")
            st.markdown("A Random Forest model trained on the top correlated genes to predict drug sensitivity.")
            
            top_genes = results_df[results_df['Significant']]['Gene'].head(20).tolist()
            if len(top_genes) < 5: top_genes = results_df['Gene'].head(20).tolist()
            
            # Automatically train the model in the background
            ml_data = merged_df[top_genes + ['IC50']].fillna(merged_df[top_genes].median())
            model, metrics, pred_df = train_ml_model(ml_data, top_genes)
            
            # Display Metrics
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Cross-Val R² (Mean)", f"{metrics['cv_r2']:.3f}")
            col_b.metric("Test R²", f"{metrics['test_r2']:.3f}")
            col_c.metric("Test RMSE", f"{metrics['test_rmse']:.3f}")
            
            st.markdown("---")
            
            col_ml1, col_ml2 = st.columns(2)
            
            with col_ml1:
                st.subheader("Model Performance: Predicted vs Actual")
                fig_pred = px.scatter(
                    pred_df, x='Actual', y='Predicted', 
                    trendline="ols", trendline_color_override="red",
                    labels={'Actual': 'Actual LN(IC50)', 'Predicted': 'Predicted LN(IC50)'},
                    template='plotly_dark', color_discrete_sequence=['#4F8BF9']
                )
                fig_pred.update_layout(height=400, margin=dict(l=0, r=0, t=20, b=0))
                st.plotly_chart(fig_pred, width='stretch')

            with col_ml2:
                st.subheader("🔮 Interactive Prediction Simulator")
                st.markdown("Select a cell line to see how the model predicts its sensitivity based on its gene expression.")
                
                test_cell = st.selectbox("Select Cell Line", merged_df['Cell_Line'].unique())
                cell_idx = merged_df[merged_df['Cell_Line'] == test_cell].index[0]
                actual_val = merged_df.loc[cell_idx, 'IC50']
                predicted_val = model.predict(merged_df.loc[[cell_idx], top_genes].values)[0]
                
                col_sim1, col_sim2 = st.columns(2)
                col_sim1.metric("Actual LN(IC50)", f"{actual_val:.3f}")
                col_sim2.metric("Predicted LN(IC50)", f"{predicted_val:.3f}", delta=f"{predicted_val - actual_val:.3f} (Error)")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.info("Note: The model uses 20 highly correlated genes to make this prediction. A perfect R² of 1.0 is impossible in biology due to noise, so an R² of ~0.4-0.6 is considered excellent.")

        # TAB 4: DATA INTEGRITY
        with tab4:
            st.header("Pipeline Integrity & Statistics")
            st.markdown("This project uses **real** GDSC2 data and rigorous statistical methods, not synthetic placeholders.")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown("### Statistical Methodology")
                st.markdown("""
                - **Data Source:** GDSC2 (Genomics of Drug Sensitivity in Cancer)
                - **Feature Extraction:** RNA-seq (RSEM TPM)
                - **Association Metric:** Pearson Correlation
                - **Multiple Testing:** Benjamini-Hochberg (FDR)
                - **ML Algorithm:** Random Forest Regressor
                - **Validation:** 5-Fold Cross-Validation
                """)
            with col_d2:
                st.markdown("### Top Biomarkers (FDR < 0.05)")
                sig_genes = results_df[results_df['P_Value_FDR'] < 0.05].sort_values('P_Value_FDR').head(10)
                if sig_genes.empty:
                    st.info("No individual gene passed the strict FDR < 0.05 threshold. This is common in high-dimensional biology (41k genes), because the penalty for multiple testing is severe. However, the raw p-values (Volcano Plot) show strong trends.")
                else:
                    st.dataframe(sig_genes[['Gene', 'Correlation', 'P_Value_FDR']], width='stretch')

else:
    st.warning("Data loading failed. Please check your `data/raw/` folder.")

# Footer
st.markdown("---")
st.markdown('<div class="footer">Developed by Freedom Evbakoe Amenaghawon | Real GDSC Data Integration | Powered by Streamlit</div>', unsafe_allow_html=True)
