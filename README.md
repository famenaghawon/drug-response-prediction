# 💊 Advanced Drug Response Prediction & Multi-Omics Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-orange.svg)](https://plotly.com)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--learn-yellow.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Deployment](https://img.shields.io/badge/Deployed-Streamlit%20Cloud-purple.svg)](https://drug-response-prediction.streamlit.app)
[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Click_Here-FF4B4B?style=for-the-badge)](https://drug-response-prediction.streamlit.app)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23448119.svg)](https://doi.org/10.5281/zenodo.23448119)

## 🎯 Project Overview

<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/2771/2771778.png" width="120" alt="Precision Medicine">
  <br>
  <em>A production-grade computational biology dashboard for precision oncology</em>
</p>

This platform is a sophisticated, end-to-end bioinformatics pipeline and interactive dashboard. It integrates **real multi-omics data** from the Genomics of Drug Sensitivity in Cancer (GDSC2) dataset with **rigorous statistical testing (FDR)** and **machine learning** to predict drug sensitivity (IC50) across hundreds of cancer cell lines. 

Unlike standard tutorials, this project demonstrates the ability to handle **large-scale, real-world data** (a raw 6GB RNA-seq matrix) and apply rigorous statistical methodologies to extract biological meaning.

---

## 🚀 Live Demo

<p align="center">
  <a href="https://drug-response-prediction.streamlit.app">
    <img src="https://img.shields.io/badge/🌐_Live_Demo-Click_Here-FF4B4B?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
</p>

Live App: [https://drug-response-prediction.streamlit.app](https://drug-response-prediction.streamlit.app)

<p align="center">
  <img src="assets/dashboard.png" alt="Dashboard Screenshot" width="800">
  <br>
  <em>Interactive dashboard with real GDSC data</em>
</p>

---

## 📊 Interactive Visualizations

### 🔬 Multi-Dimensional Analysis

| Visualization | Purpose | Key Insight |
| :---: | :--- | :--- |
| ![Volcano Plot](assets/volcano.png) | **Biomarker Discovery** | Identifies significant genes using Pearson correlation with capped Y-axis for visual clarity. |
| ![Dose-Response](assets/dose.png) | **Drug Efficacy** | Displays the real LN(IC50) distribution across 900+ cell lines for selected EGFR inhibitors. |
| ![ML Predictor](assets/ml.png) | **Predictive Modeling** | Interactive Random Forest simulator showing Predicted vs. Actual IC50 with error margins. |

### 🎯 Key Features

<div align="center">
  <table>
    <tr>
      <td align="center" width="33%">
        <img src="https://cdn-icons-png.flaticon.com/512/3067/3067256.png" width="60" alt="Machine Learning">
        <br>
        <strong>Real ML Pipeline</strong>
        <br>
        Random Forest with 5-Fold CV
      </td>
      <td align="center" width="33%">
        <img src="https://cdn-icons-png.flaticon.com/512/3067/3067256.png" width="60" alt="Visualization">
        <br>
        <strong>Statistical Rigor</strong>
        <br>
        Benjamini-Hochberg FDR Correction
      </td>
      <td align="center" width="33%">
        <img src="https://cdn-icons-png.flaticon.com/512/3067/3067256.png" width="60" alt="Deployment">
        <br>
        <strong>Scalable Architecture</strong>
        <br>
        Chunked processing of 6GB data
      </td>
    </tr>
  </table>
</div>

---

## 🛠 Technical Implementation

### 🔬 Real Data Integration & Pipeline

This project does not use synthetic placeholders. It connects directly to the **GDSC2** dataset (Genomics of Drug Sensitivity in Cancer).

```python
# The pipeline automatically handles missing data and formats
df_resp = pd.read_excel("GDSC2_fitted_dose_response_27Oct23.xlsx")
df_expr = pd.read_csv("Expression_Data_subset.csv", index_col=0)

# Correlating 41,143 genes against IC50 for a specific drug
corr, p_value = stats.pearsonr(gene_expression, ic50_values)
```

📈 Advanced Data Pipeline

· 6GB RNA-seq Processing: Uses a custom filter_data.py script to chunk, filter, and pivot a massive raw RNA-seq matrix into a usable ~50MB matrix of 41,143 genes × 943 cell lines.
· Automated Data Fetching: download_data.py automatically retrieves the pre-processed datasets via GitHub Releases for fast cloud deployment.
· Real-time Analytics: Fully interactive Plotly visualizations with dynamic hover templates and threshold lines.

🧪 Key Analyses

1. Differential Expression: Correlates 41,143 real genes with drug LN(IC50) values.
2. Multiple Testing Correction: Implements strict Benjamini-Hochberg (FDR) to control false discovery rates.
3. Machine Learning: Uses Random Forest Regressors validated with 5-Fold Cross-Validation to predict IC50 from top correlated genes.

---

🚀 Quick Start

📦 Installation & Data Fetching

```bash
# Clone repository
git clone https://github.com/famenaghawon/drug-response-prediction
cd drug-response-prediction

# Create virtual environment
python -m venv .venv

# Activate on Windows:
.venv\Scripts\Activate.ps1
# Activate on macOS/Linux:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Fetch the required datasets (Automated)
python download_data.py
```

🎮 Run Locally

```bash
# Launch the dashboard
streamlit run app/dashboard.py

# Open browser at: http://localhost:8501
```

☁ Deploy to Streamlit Cloud

1. Push code to GitHub (ensure data/ is in .gitignore).
2. Visit share.streamlit.io.
3. Connect your repository.
4. Streamlit will automatically run download_data.py to fetch the datasets from the cloud and launch the app.

---

📁 Project Structure

```text
drug-response-prediction/
├── app/
│   └── dashboard.py          # Main Streamlit application
├── src/
│   ├── data_loader.py        # Data processing and FDR logic
│   └── model.py              # Machine learning training logic
├── tests/
│   └── test_logic.py         # Unit tests for ML pipeline
├── data/
│   └── raw/                  # Directory for datasets (ignored by Git)
├── assets/                   # Dashboard screenshots and images
├── .github/workflows/        # CI/CD pipelines for testing
├── filter_data.py            # Script to chunk & pivot the 6GB raw data
├── download_data.py          # Automated data fetcher for cloud deployment
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation
└── .gitignore                # Git exclusion rules
```

---

🔬 Scientific Relevance

This project demonstrates computational approaches for:

<div align="center">
  <table>
    <tr>
      <td><strong>Precision Oncology</strong></td>
      <td>Identifying patient-specific drug sensitivities using real genomic profiles</td>
    </tr>
    <tr>
      <td><strong>Biomarker Discovery</strong></td>
      <td>Applying FDR correction to find true genetic predictors of treatment response</td>
    </tr>
    <tr>
      <td><strong>Drug Repurposing</strong></td>
      <td>Analyzing efficacy across 900+ cancer cell lines for EGFR inhibitors</td>
    </tr>
    <tr>
      <td><strong>Scalable ML</strong></td>
      <td>Building robust predictors that handle high-dimensional biological noise</td>
    </tr>
  </table>
</div>---

📈 Results & Insights

🏆 Key Findings (Real Data)

1. Biomarker Discovery: Identified 90 statistically significant genes (Raw p < 0.05) associated with Erlotinib sensitivity across 929 cell lines.
2. FDR Rigor: Demonstrated that while individual genes show strong trends, strict FDR correction (Benjamini-Hochberg) highlights the complexity of polygenic drug response.
3. Model Performance: The model successfully captures biological signal. The Random Forest Regressor achieves a Test R² of ~0.12 and an RMSE of ~1.30.

(Note: An R² of 0.12 is realistic and expected when predicting a noisy biological phenotype like IC50 from a subset of just 20 genes).

📊 Model Performance (Honest Metrics)

Machine Learning Model:

· Algorithm: Random Forest Regressor
· Validation: 5-Fold Cross-Validation
· Target: LN(IC50)
· Features: Top 20 Correlated Genes

---

🏗 Future Extensions

🔮 Planned Features

· Deep Learning: Integrate PyTorch neural networks (e.g., Multi-Layer Perceptrons) to capture nonlinear relationships.
· Multi-Omics Integration: Incorporate copy number variations (CNV) and somatic mutation data alongside RNA-seq.
· Pathway Enrichment: Add GSEA (Gene Set Enrichment Analysis) to visualize affected biological pathways (e.g., EGFR signaling).

---

🤝 Contributing

We welcome contributions! Here's how to help:

1. Fork the repository
2. Create a feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

📋 Code Guidelines

· Follow PEP 8 style guide
· Add docstrings to functions
· Include unit tests for new features
· Update documentation accordingly

---

📚 Citation

If you use this project in your research, please cite:

```bibtex
@software{amenaghawon_drugresponse_2025,
  author = {Amenaghawon, Freedom Evbakoe},
  title = {Advanced Drug Response Prediction Pipeline},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/famenaghawon/drug-response-prediction},
  version = {2.0},
  doi = {10.5281/zenodo.23448119}
}
```

---

👨‍🔬 Developer

<p align="center">
  <img src="assets/profile.jpg" alt="Developer" width="150" style="border-radius: 50%;">
  <br>
  <strong>Freedom Evbakoe Amenaghawon</strong>
  <br>
  <em>Computational Biologist & Data Scientist</em>
</p>📞 Contact Information

· GitHub: @famenaghawon
· ORCID: 0009-0003-1457-809X
· Email: f.e.amenaghawon@gmail.com
· LinkedIn: famenaghawon

---

🏆 Certifications & Skills

Technical Skills:

· Python (Advanced)
· Machine Learning (Scikit-learn, Cross-Validation)
· Data Engineering (Chunking, Large-scale data processing)
· Biostatistics (Pearson Correlation, FDR)
· Data Visualization (Plotly, Streamlit)
· Cloud Deployment

Tools:

· Streamlit, Plotly, Scikit-learn
· Pandas, NumPy, Statsmodels
· Git, GitHub, Streamlit Cloud
· Jupyter, VS Code

---

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

🌟 Acknowledgments

🎓 Educational Resources

· Streamlit Documentation
· Plotly Python Graphing Library
· Scikit-learn User Guide
· GDSC (Genomics of Drug Sensitivity in Cancer) Datasets

🛠 Tools & Frameworks

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</p>---

<p align="center">
  <strong>🎯 Precision Oncology Pipeline • Version 2.0 • 2025</strong>
  <br>
  <em>Advancing computational biology through real-world data science</em>
</p><p align="center">
  <a href="#-advanced-drug-response-prediction--multi-omics-analysis-platform">Back to Top ↑</a>
</p>
