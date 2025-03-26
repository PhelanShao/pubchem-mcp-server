#!/usr/bin/env python3
"""
PubChem MCP Server

A Model Context Protocol (MCP) server that provides access to PubChem data.
This server allows language models to query molecular structures and properties from the PubChem database.
"""

import json
import sys
import os
import logging
import traceback
import requests
import re
from datetime import datetime
from typing import Dict, Any, Optional, List

# Ensure unbuffered I/O
os.environ['PYTHONUNBUFFERED'] = '1'

# Set up logging
log_dir = os.path.expanduser("~/.pubchem-mcp")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"pubchem_mcp_server_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("pubchem_mcp_server")

# Global cache
_cache: Dict[str, Dict[str, str]] = {}

# Create HTTP session
def create_session() -> requests.Session:
    """Create a requests session with retry functionality"""
    session = requests.Session()
    retry_strategy = requests.adapters.Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# PubChem API functions
def get_pubchem_data(query: str, format: str = 'JSON', include_3d: bool = False) -> str:
    """
    Get PubChem compound data
    
    Args:
        query: Compound name or PubChem CID
        format: Output format, options: "JSON", "CSV", or "XYZ", default: "JSON"
        include_3d: Whether to include 3D structure information (only valid when format is "XYZ"), default: False
        
    Returns:
        Formatted compound data string
    """
    logger.info(f"Getting PubChem data: query={query}, format={format}, include_3d={include_3d}")
    
    if not query or not query.strip():
        return "Error: query cannot be empty."
    
    query_str = query.strip()
    is_cid = re.match(r'^\d+$', query_str) is not None
    cache_key = f"cid:{query_str}" if is_cid else f"name:{query_str.lower()}"
    identifier_path = f"cid/{query_str}" if is_cid else f"name/{query_str}"
    cid = query_str if is_cid else None
    
    # Check cache
    if cache_key in _cache:
        logger.info(f"Getting data from cache: {cache_key}")
        data = _cache[cache_key]
        if not cid:
            cid = data.get('CID')
            if not cid:
                return "Error: Could not find CID in cached data"
    else:
        # Define properties to retrieve
        properties = [
            'IUPACName',
            'MolecularFormula',
            'MolecularWeight',
            'CanonicalSMILES',
            'InChI',
            'InChIKey'
        ]
        
        # Build API URL
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{identifier_path}/property/{','.join(properties)}/JSON"
        
        try:
            session = create_session()
            response = session.get(url, timeout=180)
            response.raise_for_status()
            result = response.json()
            props = result.get('PropertyTable', {}).get('Properties', [{}])[0]
            
            if not props:
                return "Error: compound not found or no data available."
            
            if not cid:
                cid = str(props.get('CID'))
                if not cid:
                    return "Error: Could not find CID in the response"
            
            # Create data dictionary
            data = {
                'IUPACName': props.get('IUPACName', ''),
                'MolecularFormula': props.get('MolecularFormula', ''),
                'MolecularWeight': str(props.get('MolecularWeight', '')),
                'CanonicalSMILES': props.get('CanonicalSMILES', ''),
                'InChI': props.get('InChI', ''),
                'InChIKey': props.get('InChIKey', ''),
                'CID': cid
            }
            
            # Update cache
            _cache[cache_key] = data
            if cid and f"cid:{cid}" !=