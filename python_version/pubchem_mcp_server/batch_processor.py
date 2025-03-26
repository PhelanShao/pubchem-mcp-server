"""
Batch Processing Module

Provides functionality for batch processing TSV files and generating XYZ structures.
"""

import os
import csv
import time
import logging
import argparse
from typing import Dict, List, Optional, Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Try to import RDKit, use None if not available
try:
    from rdkit import Chem
    from rdkit.Chem import AllChem
    RDKIT_AVAILABLE = True
except ImportError:
    logging.warning("Warning: RDKit is not installed or cannot be loaded. 3D structure generation will be limited.")
    RDKIT_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    """Create a Session with retry functionality"""
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def search_pubchem_by_smiles(smiles: str, session: requests.Session) -> Optional[str]:
    """Search PubChem using SMILES to get CID"""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/cids/TXT"
    try:
        response = session.get(url, timeout=30)
        if response.status_code == 200:
            cids = response.text.strip().split('\n')
            return cids[0] if cids else None
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def search_pubchem_by_inchikey(inchikey: str, session: requests.Session) -> Optional[str]:
    """Search PubChem using InChIKey to get CID"""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{inchikey}/cids/TXT"
    try:
        response = session.get(url, timeout=30)
        if response.status_code == 200:
            cids = response.text.strip().split('\n')
            return cids[0] if cids else None
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def download_sdf_from_pubchem(cid: str, session: requests.Session) -> Optional[str]:
    """Download 3D SDF structure of a compound from PubChem"""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/record/SDF/?record_type=3d&response_type=display&display_type=sdf"
    try:
        response = session.get(url, timeout=30)
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"Failed to download SDF for CID: {cid}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading SDF for CID: {cid}. Error: {e}")
        return None


def generate_3d_from_smiles(smiles: str) -> Optional[Any]:
    """Generate 3D structure from SMILES"""
    if not RDKIT_AVAILABLE:
        logger.error("RDKit not installed, cannot generate 3D structure from SMILES")
        return None
    
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        
        # Add hydrogen atoms
        mol = Chem.AddHs(mol)
        # Generate 3D conformation
        AllChem.EmbedMolecule(mol, randomSeed=42)
        # Optimize structure
        AllChem.MMFFOptimizeMolecule(mol)
        return mol
    except Exception as e:
        logger.error(f"Error generating 3D structure from SMILES: {e}")
        return None


def sdf_to_mol(sdf_content: str) -> Optional[Any]:
    """Create RDKit molecule object from SDF text content"""
    if not RDKIT_AVAILABLE:
        logger.error("RDKit not installed, cannot create molecule object from SDF")
        return None
    
    if sdf_content is None:
        return None
    
    try:
        mol = Chem.MolFromMolBlock(sdf_content, removeHs=False)
        if mol is None:
            return None
        
        # Check if hydrogen atoms exist, add if not
        has_hydrogens = any(atom.GetAtomicNum() == 1 for atom in mol.GetAtoms())
        if not has_hydrogens:
            mol = Chem.AddHs(mol)
            AllChem.EmbedMolecule(mol, randomSeed=42)
            AllChem.MMFFOptimizeMolecule(mol)
        
        return mol
    except Exception as e:
        logger.error(f"Error converting SDF to mol: {e}")
        return None


def mol_to_xyz(mol: Any, compound_info: Dict[str, str]) -> Optional[str]:
    """Convert RDKit molecule object to XYZ format string"""
    if not RDKIT_AVAILABLE:
        logger.error("RDKit not installed, cannot convert to XYZ format")
        return None
    
    if mol is None:
        return None
    
    try:
        # Get conformation
        conf = mol.GetConformer()
        # Build XYZ content
        xyz_content = f"{mol.GetNumAtoms()}\n"
        
        # Add info line
        info_parts = []
        for key, value in compound_info.items():
            if value:
                info_parts.append(f"{key}={value}")
        
        xyz_content += " ".join(info_parts) + "\n"
        
        # Add atom coordinates
        for i in range(mol.GetNumAtoms()):
            atom = mol.GetAtomWithIdx(i)
            pos = conf.GetAtomPosition(i)
            xyz_content += f"{atom.GetSymbol()} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}\n"
        
        return xyz_content
    except Exception as e:
        logger.error(f"Error converting mol to XYZ: {e}")
        return None


def clean_field(field: Optional[str]) -> str:
    """Clean field value, remove potentially harmful characters"""
    if field is None:
        return ""
    return field.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')


def process_tsv_file(tsv_file: str, output_dir: str, category: str = "") -> None:
    """Process a single TSV file"""
    session = requests_retry_session()
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(tsv_file, 'r', encoding='utf-8') as f:
            # Skip possible header line
            header_line = f.readline().strip()
            if header_line.startswith('id\t'):
                reader = csv.DictReader(f, delimiter='\t', fieldnames=header_line.split('\t'))
            else:
                f.seek(0)  # Go back to the beginning of the file
                reader = csv.DictReader(f, delimiter='\t')
            
            for row in reader:
                if 'id' not in row or not row['id']:
                    continue
                
                compound_id = row['id']
                compound_name = clean_field(row.get('name', ''))
                compound_formula = clean_field(row.get('formula', ''))
                compound_rt = clean_field(row.get('rt', ''))
                
                # Check SMILES column name, could be smiles or smiles.std
                smiles = None
                for key in ['smiles.std', 'smiles', 'SMILES']:
                    if key in row and row[key]:
                        smiles = clean_field(row[key])
                        break
                
                if not smiles:
                    logger.warning(f"No SMILES found for {compound_id}, skipping.")
                    continue
                
                # Check InChIKey column name
                inchikey = None
                for key in ['inchikey.std', 'inchikey', 'InChIKey']:
                    if key in row and row[key]:
                        inchikey = clean_field(row[key])
                        break
                
                # Build compound info dictionary
                compound_info = {
                    'id': compound_id,
                    'name': compound_name,
                    'formula': compound_formula,
                    'rt': compound_rt,
                    'smiles': smiles,
                    'inchikey': inchikey
                }
                
                # Output file path
                xyz_file_path = os.path.join(output_dir, f"{compound_id}.xyz")
                
                # Skip processing if file already exists
                if os.path.exists(xyz_file_path):
                    logger.info(f"File already exists for {compound_id}, skipping.")
                    continue
                
                # Try to get structure from PubChem
                pubchem_cid = None
                mol = None
                
                # First try searching by InChIKey
                if inchikey:
                    pubchem_cid = search_pubchem_by_inchikey(inchikey, session)
                
                # If InChIKey search fails, try searching by SMILES
                if not pubchem_cid:
                    pubchem_cid = search_pubchem_by_smiles(smiles, session)
                
                # If PubChem CID is found, download SDF
                if pubchem_cid:
                    logger.info(f"Found PubChem CID: {pubchem_cid} for {compound_id}")
                    compound_info['pubchem_cid'] = pubchem_cid
                    sdf_content = download_sdf_from_pubchem(pubchem_cid, session)
                    mol = sdf_to_mol(sdf_content)
                
                # If getting from PubChem fails, generate structure from SMILES
                if mol is None:
                    logger.info(f"Generating 3D structure from SMILES for {compound_id}")
                    mol = generate_3d_from_smiles(smiles)
                
                # Skip if still unable to get structure
                if mol is None:
                    logger.warning(f"Failed to generate structure for {compound_id}, skipping.")
                    continue
                
                # Convert to XYZ format
                xyz_content = mol_to_xyz(mol, compound_info)
                if xyz_content:
                    with open(xyz_file_path, 'w', encoding='utf-8') as xyz_file:
                        xyz_file.write(xyz_content)
                    logger.info(f"Successfully generated XYZ for {compound_id}")
                else:
                    logger.warning(f"Failed to generate XYZ for {compound_id}")
                
                # Avoid requesting PubChem too quickly
                time.sleep(0.5)
                
    except Exception as e:
        logger.error(f"Error processing {tsv_file}: {e}")


def process_all_data(data_dir: str, output_base_dir: str) -> None:
    """Process all TSV files in the data directory"""
    # Traverse data directory
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            # Only process successful TSV files
            if "_rtdata_" in file and ("_success.tsv" in file or "_failed.tsv" in file):
                folder_name = os.path.basename(root)
                tsv_file_path = os.path.join(root, file)
                
                # Determine output directory
                # Keep the same directory structure as input
                relative_path = os.path.relpath(root, data_dir)
                output_dir = os.path.join(output_base_dir, relative_path)
                
                logger.info(f"Processing: {tsv_file_path}")
                # Process TSV file
                process_tsv_file(tsv_file_path, output_dir)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Process RT data and generate XYZ structures.')
    parser.add_argument('--data_dir', type=str, required=True, help='Path to the directory with RT data folders')
    parser.add_argument('--output_dir', type=str, required=True, help='Path to the output directory')
    parser.add_argument('--single_file', type=str, help='Process a single TSV file (optional)', default=None)
    parser.add_argument('--single_folder', type=str, help='Process all TSV files in a single folder (optional)', default=None)
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    if args.single_file:
        # Process a single file
        folder_name = os.path.basename(os.path.dirname(args.single_file))
        output_folder = os.path.join(args.output_dir, folder_name)
        process_tsv_file(args.single_file, output_folder)
    elif args.single_folder:
        # Process all TSV files in a single folder
        folder_name = os.path.basename(args.single_folder)
        output_folder = os.path.join(args.output_dir, folder_name)
        for file in os.listdir(args.single_folder):
            if file.endswith('_success.tsv') or file.endswith('_failed.tsv'):
                tsv_file_path = os.path.join(args.single_folder, file)
                process_tsv_file(tsv_file_path, output_folder)
    else:
        # Process all data
        process_all_data(args.data_dir, args.output_dir)


if __name__ == "__main__":
    main()
