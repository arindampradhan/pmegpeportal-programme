#!/usr/bin/env python3
"""
PMEGP PDF Downloader
Automatically downloads project profile PDFs from the PMEGP website
"""

import os
import pandas as pd
import requests
from pathlib import Path
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pdf_download.log'),
        logging.StreamHandler()
    ]
)

class PMEGPPDFDownloader:
    """Downloads PMEGP project profile PDFs"""
    
    def __init__(self, config_path='config.yml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.csv_file = self.config['data_source']['csv_file']
        self.base_url = self.config['data_source']['pdf_base_url']
        self.download_dir = Path(self.config['data_source']['pdf_download_dir'])
        self.max_workers = self.config['processing']['max_concurrent_downloads']
        self.retry_attempts = self.config['processing']['retry_attempts']
        self.timeout = self.config['processing']['timeout_seconds']
        
        # Create download directory
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
    def load_project_data(self):
        """Load project data from CSV"""
        try:
            df = pd.read_csv(self.csv_file)
            logging.info(f"Loaded {len(df)} projects from CSV")
            return df
        except Exception as e:
            logging.error(f"Error loading CSV: {e}")
            return None
    
    def download_pdf(self, row):
        """Download individual PDF file"""
        serial_num = row['Serial Number']
        pdf_url = row['PDF Link']
        filename = row['PDF Filename']
        
        # Create safe filename
        safe_filename = f"{serial_num:04d}_{filename}"
        file_path = self.download_dir / safe_filename
        
        # Skip if already downloaded
        if file_path.exists():
            logging.info(f"Already exists: {safe_filename}")
            return True
        
        # Attempt download with retries
        for attempt in range(self.retry_attempts):
            try:
                response = requests.get(
                    pdf_url, 
                    timeout=self.timeout,
                    headers={'User-Agent': 'PMEGP-Analysis-Tool/1.0'}
                )
                response.raise_for_status()
                
                # Save file
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                logging.info(f"Downloaded: {safe_filename} ({len(response.content)} bytes)")
                return True
                
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed for {filename}: {e}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        logging.error(f"Failed to download after {self.retry_attempts} attempts: {filename}")
        return False
    
    def download_all(self, limit=None):
        """Download all PDFs using thread pool"""
        df = self.load_project_data()
        if df is None:
            return
        
        # Limit for testing
        if limit:
            df = df.head(limit)
        
        logging.info(f"Starting download of {len(df)} PDFs...")
        
        success_count = 0
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.download_pdf, row) for _, row in df.iterrows()]
            
            for future in futures:
                if future.result():
                    success_count += 1
        
        logging.info(f"Download complete: {success_count}/{len(df)} files successful")
    
    def get_download_status(self):
        """Get download status report"""
        df = self.load_project_data()
        if df is None:
            return
        
        downloaded_files = list(self.download_dir.glob("*.pdf"))
        total_projects = len(df)
        downloaded_count = len(downloaded_files)
        
        status = {
            'total_projects': total_projects,
            'downloaded_count': downloaded_count,
            'download_percentage': (downloaded_count / total_projects) * 100,
            'missing_count': total_projects - downloaded_count
        }
        
        logging.info(f"Download Status: {downloaded_count}/{total_projects} "
                    f"({status['download_percentage']:.1f}%) complete")
        
        return status

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Download PMEGP project PDFs')
    parser.add_argument('--limit', type=int, help='Limit number of downloads for testing')
    parser.add_argument('--status', action='store_true', help='Show download status')
    
    args = parser.parse_args()
    
    downloader = PMEGPPDFDownloader()
    
    if args.status:
        downloader.get_download_status()
    else:
        downloader.download_all(limit=args.limit)

if __name__ == "__main__":
    main()
