# -*- coding: utf-8 -*-
import os
import re
import io
from setuptools import setup, find_packages

def get_version():
    fp = os.path.join('rc_openapi_sdk', '__init__.py')
    with io.open(fp, 'r', encoding='utf-8') as f:
        init = f.read()
    return re.search("__version__ = '[^']+'", init).group(0).split("'")[1]

setup(
    name="rc-openapi-sdk",  # 修改包名，添加前缀 rc (融创)
    version=get_version(),     # 从 __init__.py 中获取版本号
    author="Sadam·Sadik",  # 作者
    author_email="Haoke98@outlook.com",  # 作者邮箱
    description="OpenAPI SDK for Python ~ 融创API开放平台所用",    # 简短描述
    long_description=io.open("README.md", 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Haoke98/openapi-sdk",  # 更新为你的实际仓库地址
    packages=find_packages(exclude=["tests*"]),  # 自动发现包，并排除 tests 目录
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",  # HTTP 请求库
        "pycryptodome>=3.9.0",  # 加密相关
        "python-dateutil>=2.8.1",  # 日期时间处理
        "urllib3>=1.26.0",  # HTTP 客户端
        "certifi>=2020.12.5",  # SSL/TLS 证书
    ],
) 