#!/usr/bin/env node
import axios, { AxiosError, AxiosInstance } from 'axios';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { PubChemData, ToolInput, AxiosConfig } from './types';
import { getXYZStructure } from './xyz';

// 配置日志
const logger = {
  info: (msg: string) => console.log(`[INFO] ${msg}`),
  error: (msg: string) => console.error(`[ERROR] ${msg}`),
  warning: (msg: string) => console.warn(`[WARN] ${msg}`)
};

// 全局缓存
interface CacheData {
  [key: string]: PubChemData;
}

const cache: CacheData = {};

// 创建具有重试功能的axios实例
const axiosInstance: AxiosInstance = axios.create({
  timeout: 10000
});

axiosInstance.interceptors.response.use(undefined, async (err: AxiosError & { config: AxiosConfig }) => {
  const { config } = err;
  if (!config || !config.retry) {
    return Promise.reject(err);
  }

  config.retry -= 1;
  if (config.retry === 0) {
    return Promise.reject(err);
  }

  const delayMs = config.retryDelay || 1000;
  await new Promise(resolve => setTimeout(resolve, delayMs));
  return axiosInstance(config);
});

export async function getPubchemData(query: string, format: string = 'JSON', include3d: boolean = false): Promise<string> {
  logger.info(`接收到查询请求: query=${query}, format=${format}, include3d=${include3d}`);

  if (!query?.trim()) {
    return "Error: query cannot be empty.";
  }

  const queryStr = query.trim();
  const isCid = /^\d+$/.test(queryStr);
  const cacheKey = isCid ? `cid:${queryStr}` : `name:${queryStr.toLowerCase()}`;
  const identifierPath = isCid ? `cid/${queryStr}` : `name/${encodeURIComponent(queryStr)}`;
  let cid = isCid ? queryStr : null;

  logger.info(`查询路径: ${identifierPath}`);

  let data: PubChemData;
  if (cacheKey in cache) {
    logger.info("从缓存中获取数据");
    data = cache[cacheKey];
    if (!cid) {
      cid = data.CID;
      if (!cid) {
        return "Error: Could not find CID in cached data";
      }
    }
  } else {
    const properties = [
      'IUPACName',
      'MolecularFormula',
      'MolecularWeight',
      'CanonicalSMILES',
      'InChI',
      'InChIKey'
    ];

    const url = `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/${identifierPath}/property/${properties.join(',')}/JSON`;
    
    try {
      const response = await axiosInstance.get(url);
      const result = response.data;
      const props = result.PropertyTable?.Properties?.[0];

      if (!props) {
        return "Error: compound not found or no data available.";
      }

      if (!cid) {
        cid = props.CID?.toString();
        if (!cid) {
          return "Error: Could not find CID in the response";
        }
      }

      data = {
        IUPACName: props.IUPACName || '',
        MolecularFormula: props.MolecularFormula || '',
        MolecularWeight: props.MolecularWeight || '',
        CanonicalSMILES: props.CanonicalSMILES || '',
        InChI: props.InChI || '',
        InChIKey: props.InChIKey || '',
        CID: cid
      };

      cache[cacheKey] = data;
      if (cid && `cid:${cid}` !== cacheKey) {
        cache[`cid:${cid}`] = data;
      }
    } catch (error: any) {
      return `Error: ${error.response?.data?.message || error.message}`;
    }
  }

  const fmt = format.toUpperCase();
  
  // 处理XYZ格式
  if (fmt === 'XYZ') {
    if (include3d) {
      try {
        // 获取化合物信息
        const compoundInfo = {
          id: data.CID,
          name: data.IUPACName,
          formula: data.MolecularFormula,
          smiles: data.CanonicalSMILES,
          inchikey: data.InChIKey
        };
        
        // 获取XYZ结构
        const xyzStructure = await getXYZStructure(data.CID, data.CanonicalSMILES, compoundInfo);
        
        if (xyzStructure) {
          return xyzStructure;
        } else {
          return "Error: Failed to generate 3D structure.";
        }
      } catch (error: any) {
        return `Error generating 3D structure: ${error.message}`;
      }
    } else {
      return "Error: include_3d parameter must be true for XYZ format.";
    }
  } else if (fmt === 'CSV') {
    const headers = ['CID', 'IUPACName', 'MolecularFormula', 'MolecularWeight', 
                    'CanonicalSMILES', 'InChI', 'InChIKey'];
    const values = headers.map(h => data[h as keyof PubChemData] || '');
    return `${headers.join(',')}\n${values.join(',')}`;
  } else {
    // 默认返回JSON
    return JSON.stringify(data, null, 2);
  }
}
