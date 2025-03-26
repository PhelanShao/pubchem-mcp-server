import { XYZData } from './types';
/**
 * 从PubChem下载SDF格式的3D结构
 */
export declare function downloadSDFFromPubChem(cid: string): Promise<string | null>;
/**
 * 从SMILES生成3D结构
 */
export declare function generate3DFromSMILES(smiles: string): any;
/**
 * 从SDF内容创建分子对象
 */
export declare function sdfToMol(sdfContent: string): any;
/**
 * 简单的SDF解析器，不依赖于RDKit
 * @param sdfContent SDF文件内容
 */
export declare function parseSDF(sdfContent: string): any;
/**
 * 将分子对象转换为XYZ数据
 */
export declare function molToXYZData(mol: any, compoundInfo: Record<string, string>): XYZData | null;
/**
 * 将XYZ数据转换为XYZ格式字符串
 */
export declare function xyzDataToString(xyzData: XYZData): string;
/**
 * 获取化合物的XYZ格式3D结构
 */
export declare function getXYZStructure(cid: string, smiles: string, compoundInfo: Record<string, string>): Promise<string | null>;
