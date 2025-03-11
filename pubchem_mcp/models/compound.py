"""化合物数据模型"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class CompoundProperty:
    """化合物属性"""
    molecular_formula: str
    molecular_weight: float
    canonical_smiles: str
    isomeric_smiles: str
    inchi: str
    inchi_key: str
    iupac_name: str
    xlogp: float
    exact_mass: float
    monoisotopic_mass: float
    tpsa: float
    complexity: float
    charge: int
    hbond_donor_count: int
    hbond_acceptor_count: int
    rotatable_bond_count: int
    heavy_atom_count: int
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CompoundProperty':
        """从API响应字典创建属性对象"""
        return cls(
            molecular_formula=data.get("MolecularFormula", ""),
            molecular_weight=float(data.get("MolecularWeight", 0)),
            canonical_smiles=data.get("CanonicalSMILES", ""),
            isomeric_smiles=data.get("IsomericSMILES", ""),
            inchi=data.get("InChI", ""),
            inchi_key=data.get("InChIKey", ""),
            iupac_name=data.get("IUPACName", ""),
            xlogp=float(data.get("XLogP", 0)),
            exact_mass=float(data.get("ExactMass", 0)),
            monoisotopic_mass=float(data.get("MonoisotopicMass", 0)),
            tpsa=float(data.get("TPSA", 0)),
            complexity=float(data.get("Complexity", 0)),
            charge=int(data.get("Charge", 0)),
            hbond_donor_count=int(data.get("HBondDonorCount", 0)),
            hbond_acceptor_count=int(data.get("HBondAcceptorCount", 0)),
            rotatable_bond_count=int(data.get("RotatableBondCount", 0)),
            heavy_atom_count=int(data.get("HeavyAtomCount", 0))
        )

@dataclass
class Structure:
    """化合物结构"""
    sdf: str
    xyz: Optional[str] = None
    mol: Optional[str] = None
    pdb: Optional[str] = None
    cif: Optional[str] = None
    is_3d: bool = True
    
    def to_dict(self) -> Dict:
        """转换为字典表示"""
        return {
            "sdf": self.sdf[:500] + "..." if len(self.sdf) > 500 else self.sdf,
            "xyz": self.xyz,
            "mol": self.mol,
            "pdb": self.pdb,
            "cif": self.cif,
            "is_3d": self.is_3d
        }

@dataclass
class Compound:
    """化合物数据模型"""
    cid: int
    properties: CompoundProperty
    synonyms: List[str] = field(default_factory=list)
    structures: Optional[Structure] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """转换为字典表示"""
        result = {
            "cid": self.cid,
            "properties": {
                "molecular_formula": self.properties.molecular_formula,
                "molecular_weight": self.properties.molecular_weight,
                "canonical_smiles": self.properties.canonical_smiles,
                "isomeric_smiles": self.properties.isomeric_smiles,
                "inchi": self.properties.inchi,
                "inchi_key": self.properties.inchi_key,
                "iupac_name": self.properties.iupac_name,
                "xlogp": self.properties.xlogp,
                "exact_mass": self.properties.exact_mass,
                "monoisotopic_mass": self.properties.monoisotopic_mass,
                "tpsa": self.properties.tpsa,
                "complexity": self.properties.complexity,
                "charge": self.properties.charge,
                "hbond_donor_count": self.properties.hbond_donor_count,
                "hbond_acceptor_count": self.properties.hbond_acceptor_count,
                "rotatable_bond_count": self.properties.rotatable_bond_count,
                "heavy_atom_count": self.properties.heavy_atom_count
            },
            "created_at": self.created_at.isoformat()
        }
        
        if self.synonyms:
            result["synonyms"] = self.synonyms
            
        if self.structures:
            result["structures"] = self.structures.to_dict()
            
        return result
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Compound':
        """从字典创建化合物对象"""
        properties = CompoundProperty.from_dict(data.get("properties", {}))
        
        structures = None
        if "structures" in data:
            structures = Structure(
                sdf=data["structures"].get("sdf", ""),
                xyz=data["structures"].get("xyz"),
                mol=data["structures"].get("mol"),
                pdb=data["structures"].get("pdb"),
                cif=data["structures"].get("cif"),
                is_3d=data["structures"].get("is_3d", True)
            )
            
        return cls(
            cid=data["cid"],
            properties=properties,
            synonyms=data.get("synonyms", []),
            structures=structures,
            created_at=datetime.fromisoformat(data["created_at"]) 
                if "created_at" in data else datetime.now()
        )