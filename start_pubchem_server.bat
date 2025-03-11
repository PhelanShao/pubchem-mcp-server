@echo off
rem 启动PubChem MCP服务器的脚本 (Windows)

echo 启动PubChem MCP服务器...

rem 检查Python是否可用
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo 错误: 找不到Python。请确保Python已安装且在PATH中。
    goto :end
)

rem 检查版本
for /f "tokens=*" %%a in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set PY_VERSION=%%a
for /f "tokens=*" %%a in ('python -c "import sys; print(1 if sys.version_info.major>=3 and sys.version_info.minor>=8 else 0)"') do set VERSION_OK=%%a

if %VERSION_OK% equ 0 (
    echo 错误: 需要Python 3.8或更高版本。当前版本: %PY_VERSION%
    goto :end
)

rem 检查httpx库
python -c "import httpx" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo 警告: 未找到httpx库。尝试安装...
    python -m pip install httpx
    if %ERRORLEVEL% neq 0 (
        echo 错误: 无法安装httpx库。请手动安装: pip install httpx
        goto :end
    )
)

rem 启动服务器
echo 启动PubChem MCP服务器...
python pubchem_server.py

:end
echo.
echo 服务器已退出。按任意键继续...
pause >nul