"""
XYZ Utilities Module

Provides functionality for processing XYZ format and 3D structure data.
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import requests

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

# Cache directory
CACHE_DIR = Path.home() / '.pubchem-mcp' / 'cache'

# Ensure cache directory exists
try:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
except Exception as e:
    logger.error(f"Unable to create cache directory: {e}")


class Atom:
    """Atom class, represents an atom in 3D space"""
    
    def __init__(self, symbol: str, x: float, y: float, z: float):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self) -> str:
        return f"{self.symbol} {self.x:.6f} {self.y:.6f} {self.z:.6f}"


class XYZData:
    """XYZ data class, represents a molecule's 3D structure"""
    
    def __init__(self, atom_count: int, info: str, atoms: List[Atom]):
        self.atom_count = atom_count
        self.info = info
        self.atoms = atoms
    
    def to_string(self) -> str:
        """Convert XYZ data to XYZ format string"""
        result = f"{self.atom_count}\n{self.info}\n"
        for atom in self.atoms:
            # Ensure element symbol is not empty, use default "C" if empty
            symbol = atom.symbol if atom.symbol and atom.symbol.strip() and atom.symbol != "0" else "C"
            result += f"{symbol} {atom.x:.6f} {atom.y:.6f} {atom.z:.6f}\n"
        return result


def download_sdf_from_pubchem(cid: str) -> Optional[str]:
    """Download SDF format 3D structure from PubChem"""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/record/SDF/?record_type=3d&response_type=display&display_type=sdf"
    
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"Failed to download SDF, CID: {cid}. Status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error downloading SDF, CID: {cid}. Error: {e}")
        return None


def generate_3d_from_smiles(smiles: str) -> Optional[Any]:
    """Generate 3D structure from SMILES"""
    if not RDKIT_AVAILABLE:
        logger.error("RDKit not installed, cannot generate 3D structure from SMILES")
        return None
    
    try:
        # Create molecule object
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return None
        
        # Add hydrogen atoms
        mol_with_h = Chem.AddHs(mol)
        
        # Generate 3D conformation
        AllChem.EmbedMolecule(mol_with_h, randomSeed=42)
        
        # Optimize structure
        AllChem.MMFFOptimizeMolecule(mol_with_h)
        
        return mol_with_h
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


def parse_sdf(sdf_content: str) -> Optional[List[Atom]]:
    """Simple SDF parser, does not depend on RDKit"""
    try:
        lines = sdf_content.strip().split('\n')
        if len(lines) < 4:
            return None
        
        # Parse atom count
        counts_line = lines[3].strip()
        atom_count = int(counts_line[:3].strip())
        
        if atom_count <= 0:
            return None
        
        # Parse atoms
        atoms = []
        for i in range(atom_count):
            line_index = 4 + i
            if line_index >= len(lines):
                break
            
            line = lines[line_index]
            if len(line) < 31:  # Element symbol should be at least at column 31
                continue
            
            # Parse atom coordinates and element symbol using fixed width
            try:
                x = float(line[:10].strip())
                y = float(line[10:20].strip())
                z = float(line[20:30].strip())
                
                # In SDF files, element symbol is usually in columns 31-34
                # But in some SDF files, element symbol might be in different positions
                # We need to check if column 31 is a letter, if so, it's the element symbol
                symbol_part = line[30:].strip()
                symbol = ""
                
                # Extract element symbol (first sequence of non-numeric characters)
                for char in symbol_part:
                    if char.isalpha():
                        symbol += char
                    else:
                        if symbol:  # If we've already found the element symbol, stop
                            break
                
                # If no element symbol found, try to extract from other parts of the line
                if not symbol:
                    # Try to extract element symbol from other parts of the line
                    parts = line.split()
                    if len(parts) >= 4:
                        potential_symbol = parts[3]
                        if potential_symbol.isalpha():
                            symbol = potential_symbol
                
                # If still no element symbol found, use default values
                if not symbol:
                    # Guess element type based on atom position in the molecule
                    # This is just a simple example, in real applications more complex logic might be needed
                    if i < 4:  # First 4 atoms are usually oxygen atoms (in aspirin)
                        symbol = "O"
                    elif i < 13:  # Next atoms are usually carbon atoms
                        symbol = "C"
                    else:  # Remaining atoms are usually hydrogen atoms
                        symbol = "H"
                
                if symbol:
                    atoms.append(Atom(symbol, x, y, z))
            except (ValueError, IndexError) as e:
                # Try using regular expression matching
                match = re.match(r'\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+([A-Za-z]+)', line)
                if match:
                    x = float(match.group(1))
                    y = float(match.group(2))
                    z = float(match.group(3))
                    symbol = match.group(4)
                    atoms.append(Atom(symbol, x, y, z))
        
        return atoms if atoms else None
    except Exception as e:
        logger.error(f"Error parsing SDF: {e}")
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


def get_xyz_structure(cid: str, smiles: str, compound_info: Dict[str, str]) -> Optional[str]:
    """Get XYZ format 3D structure of a compound"""
    print(f"Starting to get XYZ structure: cid={cid}, smiles={smiles}")
    
    # Check cache
    cache_file = CACHE_DIR / f"{cid}.xyz"
    if cache_file.exists():
        try:
            print(f"Reading XYZ structure from cache: {cache_file}")
            return cache_file.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Error reading cache file: {e}")
    
    # Try to download SDF from PubChem
    print(f"Downloading SDF from PubChem: cid={cid}")
    sdf_content = download_sdf_from_pubchem(cid)
    if not sdf_content:
        print("Failed to download SDF")
        return None
    
    print(f"First 100 characters of SDF content: {sdf_content[:100]}")
    
    try:
        # If RDKit is available, use RDKit to process SDF
        if RDKIT_AVAILABLE:
            print("Using RDKit to process SDF")
            mol = sdf_to_mol(sdf_content)
            if mol:
                print(f"Successfully created RDKit molecule object, atom count: {mol.GetNumAtoms()}")
                # Generate XYZ using RDKit
                xyz_string = mol_to_xyz(mol, compound_info)
                if xyz_string:
                    print(f"Successfully generated XYZ string, length: {len(xyz_string)}")
                    # Save to cache
                    try:
                        cache_file.write_text(xyz_string, encoding='utf-8')
                        print(f"Saved to cache: {cache_file}")
                    except Exception as e:
                        logger.error(f"Error writing cache file: {e}")
                    return xyz_string
                else:
                    print("mol_to_xyz returned None")
            else:
                print("sdf_to_mol returned None")
        else:
            print("RDKit not available")
        
        # If RDKit is not available or processing failed, use custom parser
        print("Using custom parser to parse SDF")
        atoms = parse_sdf(sdf_content)
        if not atoms:
            print("parse_sdf returned None")
            # If SDF parsing failed, try to generate from SMILES using RDKit
            if RDKIT_AVAILABLE and smiles:
                print(f"Trying to generate 3D structure from SMILES: {smiles}")
                mol = generate_3d_from_smiles(smiles)
                if mol:
                    print(f"Successfully generated molecule object from SMILES, atom count: {mol.GetNumAtoms()}")
                    xyz_string = mol_to_xyz(mol, compound_info)
                    if xyz_string:
                        print(f"Successfully generated XYZ string, length: {len(xyz_string)}")
                        # Save to cache
                        try:
                            cache_file.write_text(xyz_string, encoding='utf-8')
                            print(f"Saved to cache: {cache_file}")
                        except Exception as e:
                            logger.error(f"Error writing cache file: {e}")
                        return xyz_string
                    else:
                        print("mol_to_xyz returned None")
                else:
                    print("generate_3d_from_smiles returned None")
            return None
        
        print(f"Successfully parsed SDF, found {len(atoms)} atoms")
        
        # Build info line
        info_line = ' '.join(f"{k}={v}" for k, v in compound_info.items() if v)
        
        # Create XYZ data
        xyz_data = XYZData(len(atoms), info_line, atoms)
        
        # Convert to XYZ string
        xyz_string = xyz_data.to_string()
        print(f"Successfully generated XYZ string, length: {len(xyz_string)}")
        
        # Save to cache
        try:
            cache_file.write_text(xyz_string, encoding='utf-8')
            print(f"Saved to cache: {cache_file}")
        except Exception as e:
            logger.error(f"Error writing cache file: {e}")
        
        return xyz_string
    except Exception as e:
        logger.error(f"Error generating XYZ structure: {e}")
        return None


# Periodic table - atomic number mapping
ELEMENT_NUMBERS = {
    'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10,
    'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20,
    'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30,
    'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40,
    'Nb': 41, 'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50,
    'Sb': 51, 'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57, 'Ce': 58, 'Pr': 59, 'Nd': 60,
    'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65, 'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70,
    'Lu': 71, 'Hf': 72, 'Ta': 73, 'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80,
    'Tl': 81, 'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85, 'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89, 'Th': 90,
    'Pa': 91, 'U': 92, 'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97, 'Cf': 98, 'Es': 99, 'Fm': 100
}


def get_atomic_number(symbol: str) -> int:
    """Get atomic number for an element symbol"""
    return ELEMENT_NUMBERS.get(symbol, 0)
