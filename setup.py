"""PubChem MCP服务器安装配置"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pubchem-mcp",
    version="1.0.0",
    author="Roo AI",
    author_email="info@roo.ai",
    description="PubChem MCP服务器，允许大语言模型访问PubChem API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roo-ai/pubchem-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.24.0",
        "mcp-sdk>=0.1.0",
        "typing-extensions>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pubchem-mcp=pubchem_mcp.server:main",
        ],
    },
)