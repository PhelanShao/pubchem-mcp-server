import { AxiosRequestConfig } from 'axios';

export interface PubChemData {
  IUPACName: string;
  MolecularFormula: string;
  MolecularWeight: string;
  CanonicalSMILES: string;
  InChI: string;
  InChIKey: string;
  CID: string;
  XYZ?: string; // XYZ格式的3D结构数据
}

export interface Atom {
  symbol: string;
  x: number;
  y: number;
  z: number;
}

export interface XYZData {
  atomCount: number;
  info: string;
  atoms: Atom[];
}

export interface ToolInput {
  query: string;
  format?: string;
  include_3d?: boolean;
}

export interface AxiosConfig extends AxiosRequestConfig {
  retry?: number;
  retryDelay?: number;
}
