"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.downloadSDFFromPubChem = downloadSDFFromPubChem;
exports.generate3DFromSMILES = generate3DFromSMILES;
exports.sdfToMol = sdfToMol;
exports.parseSDF = parseSDF;
exports.molToXYZData = molToXYZData;
exports.xyzDataToString = xyzDataToString;
exports.getXYZStructure = getXYZStructure;
const axios_1 = __importDefault(require("axios"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const os = __importStar(require("os"));
// 尝试导入rdkit-js，如果不可用则使用null
let RDKit = null;
try {
    RDKit = require('rdkit-js');
}
catch (e) {
    console.error('警告: rdkit-js 未安装或无法加载。3D结构生成功能将受限。');
}
// 缓存目录
const CACHE_DIR = path.join(os.homedir(), '.pubchem-mcp', 'cache');
// 确保缓存目录存在
try {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
}
catch (error) {
    console.error(`无法创建缓存目录: ${error}`);
}
/**
 * 从PubChem下载SDF格式的3D结构
 */
async function downloadSDFFromPubChem(cid) {
    const url = `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${cid}/record/SDF/?record_type=3d&response_type=display&display_type=sdf`;
    try {
        const response = await axios_1.default.get(url);
        if (response.status === 200) {
            return response.data;
        }
        else {
            console.error(`下载SDF失败，CID: ${cid}。状态码: ${response.status}`);
            return null;
        }
    }
    catch (error) {
        console.error(`下载SDF时出错，CID: ${cid}。错误: ${error.message}`);
        return null;
    }
}
/**
 * 从SMILES生成3D结构
 */
function generate3DFromSMILES(smiles) {
    if (!RDKit) {
        console.error('rdkit-js 未加载，无法从SMILES生成3D结构');
        return null;
    }
    try {
        // 创建分子对象
        const mol = RDKit.Mol.fromSmiles(smiles);
        if (!mol) {
            return null;
        }
        // 添加氢原子
        const molWithH = mol.addHs();
        // 生成3D构象
        const result = molWithH.generate3DCoords();
        if (!result) {
            molWithH.delete();
            return null;
        }
        // 优化结构
        molWithH.MMFFoptimizeMolecule();
        return molWithH;
    }
    catch (error) {
        console.error(`从SMILES生成3D结构时出错: ${error}`);
        return null;
    }
}
/**
 * 从SDF内容创建分子对象
 */
function sdfToMol(sdfContent) {
    if (!sdfContent) {
        return null;
    }
    // 如果RDKit可用，使用RDKit处理SDF
    if (RDKit) {
        try {
            const mol = RDKit.Mol.fromMolBlock(sdfContent);
            if (!mol) {
                return null;
            }
            // 检查是否有氢原子，如果没有则添加
            let molWithH = mol;
            const hasHydrogens = Array.from({ length: mol.getNumAtoms() }, (_, i) => mol.getAtomWithIdx(i).getAtomicNum() === 1).some(Boolean);
            if (!hasHydrogens) {
                molWithH = mol.addHs();
                molWithH.MMFFoptimizeMolecule();
                mol.delete();
            }
            return molWithH;
        }
        catch (error) {
            console.error(`将SDF转换为分子对象时出错: ${error}`);
            return null;
        }
    }
    else {
        // 如果RDKit不可用，使用简单的SDF解析器
        return parseSDF(sdfContent);
    }
}
/**
 * 简单的SDF解析器，不依赖于RDKit
 */
function parseSDF(sdfContent) {
    try {
        const lines = sdfContent.split('\n');
        if (lines.length < 4) {
            return null;
        }
        // 解析原子数和键数
        const countsLine = lines[3].trim();
        const atomCount = parseInt(countsLine.substring(0, 3).trim());
        if (isNaN(atomCount) || atomCount <= 0) {
            return null;
        }
        // 解析原子
        const atoms = [];
        for (let i = 0; i < atomCount; i++) {
            const lineIndex = 4 + i;
            if (lineIndex >= lines.length) {
                break;
            }
            const line = lines[lineIndex];
            if (line.length < 35) {
                continue;
            }
            // 解析SDF格式的原子行
            // 格式: x y z element ...
            // 使用正则表达式匹配坐标和元素符号
            const match = line.match(/\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+([A-Za-z]+)/);
            if (!match) {
                continue;
            }
            const x = parseFloat(match[1]);
            const y = parseFloat(match[2]);
            const z = parseFloat(match[3]);
            const symbol = match[4];
            if (isNaN(x) || isNaN(y) || isNaN(z)) {
                continue;
            }
            atoms.push({ symbol, x, y, z });
        }
        if (atoms.length === 0) {
            return null;
        }
        // 创建一个简单的分子对象
        return {
            atoms,
            getNumAtoms: () => atoms.length,
            getAtomWithIdx: (i) => ({
                getSymbol: () => atoms[i].symbol,
                getAtomicNum: () => getAtomicNumber(atoms[i].symbol)
            }),
            getConformer: () => ({
                getAtomPos: (i) => ({
                    x: atoms[i].x,
                    y: atoms[i].y,
                    z: atoms[i].z
                })
            }),
            delete: () => { } // 空函数，因为我们不需要释放内存
        };
    }
    catch (error) {
        console.error(`解析SDF时出错: ${error}`);
        return null;
    }
}
/**
 * 获取元素的原子序数
 */
function getAtomicNumber(symbol) {
    const elements = {
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
    };
    return elements[symbol] || 0;
}
/**
 * 将分子对象转换为XYZ数据
 */
function molToXYZData(mol, compoundInfo) {
    if (!mol) {
        return null;
    }
    try {
        const numAtoms = mol.getNumAtoms();
        const conf = mol.getConformer();
        // 构建信息行
        let infoLine = '';
        for (const [key, value] of Object.entries(compoundInfo)) {
            if (value) {
                infoLine += `${key}=${value} `;
            }
        }
        // 构建原子数组
        const atoms = [];
        for (let i = 0; i < numAtoms; i++) {
            const atom = mol.getAtomWithIdx(i);
            const pos = conf.getAtomPos(i);
            atoms.push({
                symbol: atom.getSymbol(),
                x: pos.x,
                y: pos.y,
                z: pos.z
            });
        }
        return {
            atomCount: numAtoms,
            info: infoLine.trim(),
            atoms
        };
    }
    catch (error) {
        console.error(`将分子对象转换为XYZ数据时出错: ${error}`);
        return null;
    }
}
/**
 * 将XYZ数据转换为XYZ格式字符串
 */
function xyzDataToString(xyzData) {
    let result = `${xyzData.atomCount}\n${xyzData.info}\n`;
    for (const atom of xyzData.atoms) {
        // 确保元素符号不为空，如果为空则使用默认值"C"
        const symbol = atom.symbol && atom.symbol.trim() !== "" && atom.symbol !== "0" ? atom.symbol : "C";
        result += `${symbol} ${atom.x.toFixed(6)} ${atom.y.toFixed(6)} ${atom.z.toFixed(6)}\n`;
    }
    return result;
}
/**
 * 获取化合物的XYZ格式3D结构
 */
async function getXYZStructure(cid, smiles, compoundInfo) {
    // 检查缓存
    const cacheFile = path.join(CACHE_DIR, `${cid}.xyz`);
    if (fs.existsSync(cacheFile)) {
        try {
            return fs.readFileSync(cacheFile, 'utf-8');
        }
        catch (error) {
            console.error(`读取缓存文件时出错: ${error}`);
        }
    }
    // 尝试从PubChem下载SDF
    const sdfContent = await downloadSDFFromPubChem(cid);
    if (!sdfContent) {
        return null;
    }
    try {
        // 解析SDF文件
        const lines = sdfContent.split('\n');
        if (lines.length < 4) {
            return null;
        }
        // 解析原子数
        const countsLine = lines[3].trim();
        const atomCount = parseInt(countsLine.substring(0, 3).trim());
        if (isNaN(atomCount) || atomCount <= 0) {
            return null;
        }
        // 构建信息行
        let infoLine = '';
        for (const [key, value] of Object.entries(compoundInfo)) {
            if (value) {
                infoLine += `${key}=${value} `;
            }
        }
        // 构建XYZ格式输出
        let xyzString = `${atomCount}\n${infoLine.trim()}\n`;
        // 解析原子坐标和元素符号
        for (let i = 0; i < atomCount; i++) {
            const lineIndex = 4 + i;
            if (lineIndex >= lines.length) {
                break;
            }
            const line = lines[lineIndex];
            if (line.length < 35) {
                continue;
            }
            // 使用正则表达式匹配坐标和元素符号
            const match = line.match(/\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+([A-Za-z]+)/);
            if (!match) {
                continue;
            }
            const x = parseFloat(match[1]);
            const y = parseFloat(match[2]);
            const z = parseFloat(match[3]);
            const symbol = match[4];
            if (isNaN(x) || isNaN(y) || isNaN(z)) {
                continue;
            }
            xyzString += `${symbol} ${x.toFixed(6)} ${y.toFixed(6)} ${z.toFixed(6)}\n`;
        }
        // 保存到缓存
        try {
            fs.writeFileSync(cacheFile, xyzString);
        }
        catch (error) {
            console.error(`写入缓存文件时出错: ${error}`);
        }
        return xyzString;
    }
    catch (error) {
        console.error(`解析SDF文件时出错: ${error}`);
        return null;
    }
}
