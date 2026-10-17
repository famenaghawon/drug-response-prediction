import os
import subprocess
import sys
import urllib.request

# Define directories
DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

def download_drug_data():
    """Downloads the GDSC2 Excel file directly from the Sanger Institute."""
    url = "https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.5/GDSC2_fitted_dose_response_27Oct23.xlsx"
    dest = os.path.join(DATA_DIR, "GDSC2_fitted_dose_response_27Oct23.xlsx")
    
    if os.path.exists(dest):
        print(f"✅ Drug data already exists.")
        return
        
    print(f"⬇️ Downloading GDSC2 Drug Response Data (22 MB)...")
    urllib.request.urlretrieve(url, dest)
    print(f"✅ Successfully downloaded Drug data.")

def download_expression_data():
    import urllib.request
    # Paste your copied link here
    url = "https://github.com/famenaghawon/drug-response-prediction/releases/download/v1.0.0/Expression_Data_subset.csv"
    dest = os.path.join(DATA_DIR, "Expression_Data_subset.csv")
    
    if os.path.exists(dest):
        print(f"✅ Expression data already exists.")
        return
        
    print(f"⬇️ Downloading Expression Data from GitHub Releases...")
    urllib.request.urlretrieve(url, dest)
    print(f"✅ Successfully downloaded Expression Data.")

if __name__ == "__main__":
    print("🚀 Initializing Data Pipeline...")
    download_drug_data()
    download_expression_data()
    print("🎉 Data pipeline ready!")
