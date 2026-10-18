<div align="center">
  <h1>🧬 NEURO-RX: Advanced Drug Response Prediction Engine</h1>
  <p><em>A production-grade, multi-omics computational biology dashboard for precision oncology.</em></p>

  <!-- Badges -->
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python"></a>
  <a href="https://streamlit.io"><img src="https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg" alt="Streamlit"></a>
  <a href="https://scikit-learn.org"><img src="https://img.shields.io/badge/ML-Scikit--learn-F7931E.svg" alt="Scikit-Learn"></a>
  <a href="https://huggingface.co"><img src="https://img.shields.io/badge/Data-Hugging%20Face-yellow.svg" alt="Hugging Face"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  
  <br>

  <a href="https://drug-response-prediction.streamlit.app">
    <img src="https://img.shields.io/badge/🌐_Live_Demo-Launch_NEURO--RX-00E5FF?style=for-the-badge" alt="Live Demo">
  </a>
  <a href="https://doi.org/10.5281/zenodo.23448119">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.23448119.svg" alt="DOI">
  </a>
</div>


## 🎯 Project Overview

This platform is a sophisticated, end-to-end bioinformatics pipeline and interactive dashboard. It integrates **real multi-omics data** from the Genomics of Drug Sensitivity in Cancer (GDSC2) dataset with **rigorous statistical testing (FDR)** and **machine learning** to predict drug sensitivity (LN_IC50) across hundreds of cancer cell lines. 

Unlike standard tutorials, this project demonstrates the ability to handle **large-scale, real-world data** (a 230MB RNA-seq matrix with 41,143 genes) and apply rigorous statistical methodologies to extract biological meaning without data leakage.

### ⚡ Key Innovations
*   **Zero-Trust ML Pipeline:** Data is split 80/20 *before* statistical testing to strictly prevent data leakage.
*   **Cloud-Native Data Streaming:** Bypasses Streamlit's 1GB memory limits and startup timeouts by streaming a highly compressed Parquet file (91MB) directly from the **Hugging Face Hub**.
*   **Ultra-Futuristic UI:** A custom-engineered, glassmorphic dark-mode interface with animated canvas grids and neon telemetry.


## 🚀 Live Demo & Visuals

<p align="center">
  <a href="https://drug-response-prediction.streamlit.app">
    <img src="https://img.shields.io/badge/Experience_the_Live_App-Click_Here-7C4DFF?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
</p>

<div align="center">
  <table>
    <tr>
      <td align="center" width="50%">
        <b>🔬 Volcano Scan & Biomarker Discovery</b><br>
        <em>FDR-corrected Pearson correlations across 37k genes.</em>
      </td>
      <td align="center" width="50%">
        <b>🧠 Neural ML Core</b><br>
        <em>Random Forest IC50 predictor with interactive simulator.</em>
      </td>
    </tr>
  </table>
</div>


## 🛠 Technical Architecture

### 🔬 Data Pipeline & Cloud Integration
This project does not use synthetic placeholders. It connects directly to real GDSC data.

**The Challenge:** The raw RNA-seq matrix is over 230MB (6GB uncompressed). GitHub blocks files >100MB, and Streamlit Cloud times out if forced to download huge CSVs on boot.
**The Solution:** 
1. The CSV is converted to a highly compressed **Parquet** format (91MB) and hosted on Hugging Face.
2. The app uses `pandas.read_parquet()` to stream the data directly into memory during app startup.

```python
# Stream directly from Hugging Face Hub
url = "https://huggingface.co/datasets/famenaghawon/drug-response-data/resolve/main/Expression_Data.parquet"
df_expr = pd.read_parquet(url)
```

🧪 Methodological Rigor

1. Train/Test Split: 80/20 split performed before any statistical testing.
2. Imputation: Medians calculated exclusively on the training set and applied to the test set.
3. Multiple Testing: Benjamini-Hochberg (FDR) applied strictly to the training set to control False Discovery Rates.
4. Machine Learning: Random Forest Regressor validated using 5-Fold Cross-Validation.


📈 Results & Insights (Honest Metrics)

· Biomarker Discovery: Out of 37,215 genes scanned, we identified significant biomarkers using strict FDR correction.
· Model Performance:
  · Cross-Val R² (Train): 0.181
  · Test R² (Unseen): 0.115
  · Test RMSE: 1.139

Scientific Note: An R² of ~0.11-0.18 is highly realistic and consistent with state-of-the-art literature for single-omics drug response prediction. Predicting IC50 from gene expression alone is notoriously difficult due to the polygenic nature of drug resistance and high biological noise. The model successfully captures the underlying biological signal without overfitting.


## 💻 Quick Start (Local Development)

**1. Clone & Setup**
```bash
git clone https://github.com/famenaghawon/drug-response-prediction.git
cd drug-response-prediction
python -m venv .venv

# Windows:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

2. Fetch the Datasets (Optional for Local)
Note: The live Streamlit Cloud app streams data directly from Hugging Face. However, for local development, you can download the raw datasets to run the pipeline locally:

```bash
python download_data.py
```

3. Run the Dashboard

```bash
streamlit run app/dashboard.py
# App opens at http://localhost:8501
```

```

***

### Here is the Final, Complete `README.md`
I have added back the Developer Profile Picture, the local download instructions, and kept everything perfectly aligned with your Python 3.11 + Hugging Face architecture. 

You can copy and paste this entire block directly:

```markdown
<div align="center">
  <h1>🧬 NEURO-RX: Advanced Drug Response Prediction Engine</h1>
  <p><em>A production-grade, multi-omics computational biology dashboard for precision oncology.</em></p>

  <!-- Badges -->
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python"></a>
  <a href="https://streamlit.io"><img src="https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg" alt="Streamlit"></a>
  <a href="https://scikit-learn.org"><img src="https://img.shields.io/badge/ML-Scikit--learn-F7931E.svg" alt="Scikit-Learn"></a>
  <a href="https://huggingface.co"><img src="https://img.shields.io/badge/Data-Hugging%20Face-yellow.svg" alt="Hugging Face"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  
  <br>

  <a href="https://drug-response-prediction.streamlit.app">
    <img src="https://img.shields.io/badge/🌐_Live_Demo-Launch_NEURO--RX-00E5FF?style=for-the-badge" alt="Live Demo">
  </a>
  <a href="https://doi.org/10.5281/zenodo.23448119">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.23448119.svg" alt="DOI">
  </a>
</div>


## 🎯 Project Overview

This platform is a sophisticated, end-to-end bioinformatics pipeline and interactive dashboard. It integrates **real multi-omics data** from the Genomics of Drug Sensitivity in Cancer (GDSC2) dataset with **rigorous statistical testing (FDR)** and **machine learning** to predict drug sensitivity (LN_IC50) across hundreds of cancer cell lines. 

Unlike standard tutorials, this project demonstrates the ability to handle **large-scale, real-world data** (a raw 6GB RNA-seq matrix) and apply rigorous statistical methodologies to extract biological meaning without data leakage.

### ⚡ Key Innovations
*   **Zero-Trust ML Pipeline:** Data is split 80/20 *before* statistical testing to strictly prevent data leakage.
*   **Cloud-Native Data Streaming:** Bypasses Streamlit's 1GB memory limits and startup timeouts by streaming a highly compressed Parquet file (91MB) directly from the **Hugging Face Hub**.
*   **Ultra-Futuristic UI:** A custom-engineered, glassmorphic dark-mode interface with animated canvas grids and neon telemetry.


## 🚀 Live Demo & Visuals

<p align="center">
  <a href="https://drug-response-prediction.streamlit.app">
    <img src="https://img.shields.io/badge/Experience_the_Live_App-Click_Here-7C4DFF?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
</p>

<div align="center">
  <table>
    <tr>
      <td align="center" width="50%">
        <b>🔬 Volcano Scan & Biomarker Discovery</b><br>
        <em>FDR-corrected Pearson correlations across 37k genes.</em><br>
        <img src="assets/volcano.png" alt="Volcano Plot" width="400">
      </td>
      <td align="center" width="50%">
        <b>🧠 Neural ML Core</b><br>
        <em>Random Forest IC50 predictor with interactive simulator.</em><br>
        <img src="assets/ml.png" alt="ML Predictor" width="400">
      </td>
    </tr>
  </table>
</div>


## 🛠 Technical Architecture

### 🔬 Data Pipeline & Cloud Integration
This project does not use synthetic placeholders. It connects directly to real GDSC data.

**The Challenge:** The raw RNA-seq matrix is over 230MB (6GB uncompressed). GitHub blocks files >100MB, and Streamlit Cloud times out if forced to download huge CSVs on boot.
**The Solution:** 
1. The CSV is converted to a highly compressed **Parquet** format (91MB) and hosted on Hugging Face.
2. The app uses `pandas.read_parquet()` to stream the data directly into memory during app startup.

```python
# Stream directly from Hugging Face Hub
url = "https://huggingface.co/datasets/famenaghawon/drug-response-data/resolve/main/Expression_Data.parquet"
df_expr = pd.read_parquet(url)
```

🧪 Methodological Rigor

1. Train/Test Split: 80/20 split performed before any statistical testing.
2. Imputation: Medians calculated exclusively on the training set and applied to the test set.
3. Multiple Testing: Benjamini-Hochberg (FDR) applied strictly to the training set to control False Discovery Rates.
4. Machine Learning: Random Forest Regressor validated using 5-Fold Cross-Validation.


📈 Results & Insights (Honest Metrics)

· Biomarker Discovery: Out of 37,215 genes scanned, we identified significant biomarkers using strict FDR correction.
· Model Performance:
  · Cross-Val R² (Train): 0.181
  · Test R² (Unseen): 0.115
  · Test RMSE: 1.139

Scientific Note: An R² of ~0.11-0.18 is highly realistic and consistent with state-of-the-art literature for single-omics drug response prediction. Predicting IC50 from gene expression alone is notoriously difficult due to the polygenic nature of drug resistance and high biological noise. The model successfully captures the underlying biological signal without overfitting.


💻 Quick Start (Local Development)

1. Clone & Setup

```bash
git clone https://github.com/famenaghawon/drug-response-prediction.git
cd drug-response-prediction
python -m venv .venv

# Windows:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

2. Fetch the Datasets (Optional for Local)
Note: The live Streamlit Cloud app streams data directly from Hugging Face. However, for local development, you can download the raw datasets to run the pipeline locally:

```bash
python download_data.py
```

3. Run the Dashboard

```bash
streamlit run app/dashboard.py
# App opens at http://localhost:8501
```


📁 Project Structure

```text
drug-response-prediction/
├── app/
│   └── dashboard.py          # Main Streamlit application (NEURO-RX UI)
├── src/
│   ├── data_loader.py        # Hugging Face streaming & FDR logic
│   └── model.py              # Random Forest ML training pipeline
├── tests/
│   └── test_logic.py         # Pytest suite for ML pipeline integrity
├── data/                     # Local fallback (ignored by Git)
├── assets/                   # Dashboard screenshots and UI assets
├── download_data.py          # Data fetcher for local development
├── .github/workflows/        # CI/CD pipelines (Pytest & Flake8)
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation
```


🔮 Future Extensions

· Deep Learning: Integrate PyTorch neural networks (MLPs) to capture complex, nonlinear relationships between gene expression and drug response.
· Multi-Omics: Incorporate Copy Number Variations (CNV) and somatic mutation data alongside RNA-seq.
· Pathway Enrichment: Add GSEA (Gene Set Enrichment Analysis) to visualize affected biological pathways (e.g., EGFR signaling).


🤝 Contributing

Contributions are welcome! Please follow PEP 8 standards, add docstrings, and ensure all unit tests pass (pytest).


📚 Citation

If you use this platform or methodology in your research, please cite:

```bibtex
@software{amenaghawon_drugresponse_2026,
  author = {Amenaghawon, Freedom Evbakoe},
  title = {NEURO-RX: Advanced Drug Response Prediction Pipeline},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/famenaghawon/drug-response-prediction},
  version = {3.0},
  doi = {10.5281/zenodo.23448119}
}
```


👨‍🔬 Developer

<div align="center">
  <img src="assets/profile.jpg" alt="Developer Profile" width="150" style="border-radius: 50%; border: 3px solid #00e5ff;">
  <br>
  <strong>Freedom Evbakoe Amenaghawon</strong><br>
  <em>Computational Biologist & Data Scientist</em><br><br>
  <a href="https://github.com/famenaghawon">GitHub</a> • 
  <a href="https://orcid.org/0009-0003-1457-809X">ORCID</a> • 
  <a href="mailto:f.e.amenaghawon@gmail.com">Email</a>
</div>
<div align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"></a>
  <a href="https://streamlit.io"><img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"></a>
  <a href="https://plotly.com"><img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white"></a>
  <a href="https://scikit-learn.org"><img src="https://img.shields.io/badge/scikit_learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white"></a>
  <a href="https://huggingface.co"><img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black"></a>
</div>
<p align="center">
  <em>Advancing computational biology through real-world data science.</em>
</p>
