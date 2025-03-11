import { getPubchemData } from '../src/index';

describe('PubChem MCP Tests', () => {
  test('查询化合物（JSON格式）', async () => {
    const result = await getPubchemData('aspirin');
    const data = JSON.parse(result);
    expect(data).toHaveProperty('CID');
    expect(data).toHaveProperty('IUPACName');
    expect(data).toHaveProperty('MolecularFormula');
    expect(data.MolecularFormula).toBe('C9H8O4');
  });

  test('查询化合物（CSV格式）', async () => {
    const result = await getPubchemData('aspirin', 'CSV');
    expect(result).toContain('CID');
    expect(result).toContain('2244');
    expect(result).toContain('C9H8O4');
  });

  test('使用CID查询', async () => {
    const result = await getPubchemData('2244');
    const data = JSON.parse(result);
    expect(data.CID).toBe('2244');
    expect(data.MolecularFormula).toBe('C9H8O4');
  });

  test('处理无效查询', async () => {
    const result = await getPubchemData('');
    expect(result).toContain('Error');
  });

  test('处理不存在的化合物', async () => {
    const result = await getPubchemData('nonexistentcompound123');
    expect(result).toContain('Error');
  });
});
