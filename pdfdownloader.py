"""
Module containing the pdfdownloader.

Purpose:
Automate the downloading of pdf files.

How:
Read links from excel file, download those assuming they are referring to pdf files.
Make a working copy of the excel file, mark status for links when downloads are attempted whether failed or succeeded.
"""

import logging
import os
import requests
from pathlib import Path
from typing import List, Dict, Tuple
from urllib.parse import urlparse

# System setup
log = logging.getLogger(__name__)


class DownloadError(Exception):
    """
    Exception raised for unfavourable results during download, such as it failing,
    getting the wrong file type or the process hanging indefintely.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def download_pdfs(urls: List[str], base_dir: str = "downloads") -> List[Dict[str, str]]:
    """
    Downloads multiple PDFs from URLs and returns results for further processing.

    Args:
        urls: List of PDF URLs
        base_dir: Directory to save files

    Returns:
        List of dicts: [{'url': str, 'path': str, 'status': 'success|error',\
        'message': str}]
    """

    Path(base_dir).mkdir(parents=True, exist_ok=True)
    results = []

    for url in urls:
        try:
            # Extract filename from URL or use generic name
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            if not filename or not filename.lower().endswith('.pdf'):
                filename = f"document_{len(results)+1}.pdf"

            filepath = os.path.join(base_dir, filename)

            # Download with progress feedback
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            # Verify content type is PDF
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' not in content_type:
                results.append({
                    'url': url,
                    'path': None,
                    'status': 'error',
                    'message': f"Not a PDF (content-type: {content_type})"
                })
                continue

            # Save file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            results.append({
                'url': url,
                'path': filepath,
                'status': 'success',
                'message': f"Downloaded {\
                response.headers.get('content-length', 'unknown')}\
                bytes."
            })
            logging.debug(f"✓ {filename} saved")

        except requests.RequestException as e:
            results.append({
                'url': url,
                'path': None,
                'status': 'error',
                'message': f"Download failed: {str(e)}"
            })
            logging.debug(f"✗ {url}: {str(e)}")

    return results
