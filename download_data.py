import os
import subprocess
import sys

# Define directories
DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

def install_gdown():
    """Ensure gdown is installed to handle Google Drive downloads safely."""
    try:
        import gdown
    except ImportError:
        print("📦 Installing gdown for Google Drive support...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
        import gdown

def download_drug_data():
    """Downloads the GDSC2 Excel file directly from the Sanger Institute."""
    url = "https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.5/GDSC2_fitted_dose_response_27Oct23.xlsx"
    dest = os.path.join(DATA_DIR, "GDSC2_fitted_dose_response_27Oct23.xlsx")
    
    if os.path.exists(dest):
        print(f"✅ Drug data already exists.")
        return
        
    print(f"⬇️ Downloading GDSC2 Drug Response Data (22 MB)...")
    import urllib.request
    urllib.request.urlretrieve(url, dest)
    print(f"✅ Successfully downloaded Drug data.")

def download_expression_data():
    """Downloads the filtered CSV from Google Drive using gdown."""
    install_gdown()
    import gdown
    
    file_id = "1zrdFIPgWrBeMAbv8XG0KcuTVHBesp5Tc"
    dest = os.path.join(DATA_DIR, "Expression_Data_subset.csv")
    
    if os.path.exists(dest):
        print(f"✅ Expression data already exists.")
        return
        
    print(f"⬇️ Downloading Expression Data from Google Drive (This may take a minute)...")
    # gdown handles the virus scan warning automatically
    url = f"https://drive.google.com/uc?id={file_id}"
    
    try:
        gdown.download(url, dest, quiet=False)
        print(f"✅ Successfully downloaded Expression Data.")
    except Exception as e:
        print(f"❌ Failed to download expression data: {e}")
        print("Please ensure the Google Drive link permissions are set to 'Anyone with the link'.")

if __name__ == "__main__":
    print("🚀 Initializing Data Pipeline...")
    download_drug_data()
    download_expression_data()
    print("🎉 Data pipeline ready! You can now run `streamlit run app/dashboard.py`")
