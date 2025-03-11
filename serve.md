flowchart TB
    subgraph Client["客户端层"]
        Claude["Claude AI"]
        OtherClient["其他MCP客户端"]
    end

    subgraph MCPServer["PubChem MCP服务器"]
        API["MCP API接口"]
        
        subgraph Core["核心服务"]
            QueryParser["查询解析器"]
            DataFetcher["数据获取模块"]
            StructureConverter["结构转换模块"]
            ResponseFormatter["响应格式化模块"]
        end
        
        subgraph Cache["缓存系统"]
            ResultCache["结果缓存"]
            LocalDB["本地化学数据库"]
        end
        
        subgraph Utils["工具与辅助服务"]
            RateLimiter["请求速率限制器"]
            ErrorHandler["错误处理"]
            Logging["日志记录"]
        end
    end
    
    subgraph ExternalAPI["外部API"]
        PubChem["PubChem API"]
        ChemSpider["ChemSpider API (可选)"]
        ChEMBL["ChEMBL API (可选)"]
        CSD["剑桥结构数据库 (可选)"]
    end
    
    %% 连接关系
    Claude -->|发送查询请求| API
    OtherClient -->|发送查询请求| API
    
    API -->|解析请求| QueryParser
    
    QueryParser -->|检查缓存| ResultCache
    ResultCache -->|缓存命中| ResponseFormatter
    ResultCache -->|缓存未命中| DataFetcher
    
    QueryParser -->|检索本地数据| LocalDB
    LocalDB -->|本地数据| ResponseFormatter
    
    DataFetcher -->|控制请求频率| RateLimiter
    RateLimiter -->|限制API请求速率| ExternalAPI
    
    DataFetcher -->|请求化学数据| PubChem
    DataFetcher -.->|扩展数据源| ChemSpider
    DataFetcher -.->|扩展数据源| ChEMBL
    DataFetcher -.->|扩展数据源| CSD
    
    PubChem -->|返回化学数据| DataFetcher
    ChemSpider -.->|返回化学数据| DataFetcher
    ChEMBL -.->|返回化学数据| DataFetcher
    CSD -.->|返回化学数据| DataFetcher
    
    DataFetcher -->|原始数据| StructureConverter
    StructureConverter -->|转换结构格式| ResponseFormatter
    
    DataFetcher -->|存储结果| ResultCache
    
    ResponseFormatter -->|格式化响应| API
    API -->|返回结果| Claude
    API -->|返回结果| OtherClient
    
    %% 错误处理
    DataFetcher -->|错误上报| ErrorHandler
    ErrorHandler -->|格式化错误| ResponseFormatter
    ErrorHandler -->|记录错误| Logging