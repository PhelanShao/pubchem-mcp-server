import { AxiosRequestConfig } from 'axios';

export interface PubChemData {
  IUPACName: string;
  MolecularFormula: string;
  MolecularWeight: string;
  CanonicalSMILES: string;
  InChI: string;
  InChIKey: string;
  CID: string;
}

export interface ToolInput {
  query: string;
  format?: string;
}

export interface AxiosConfig extends AxiosRequestConfig {
  retry?: number;
  retryDelay?: number;
}
