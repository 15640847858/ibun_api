# -*- coding: utf-8 -*-

import os
import sys

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import importlib.util

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(__file__) + '/../..')

app = FastAPI()

# 获取routers文件夹的路径
routers_dir = os.path.join(os.path.dirname(__file__), "routers")

# 动态导入并包含routers文件夹中的所有路由
for root, dirs, files in os.walk(routers_dir):
    for dir_name in dirs:
        # 构建文件夹的绝对路径
        dir_path = os.path.join(root, dir_name)
        # 判断文件夹中是否存在 router.py 文件
        router_file = os.path.join(dir_path, "router.py")
        if os.path.exists(router_file):
            # 构建模块路径
            module_path = f"{routers_dir}.{dir_name}.router"
            # 使用 importlib 动态导入模块
            spec = importlib.util.spec_from_file_location(module_path, router_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # 获取 router 实例
            router = module.router
            # 添加到 FastAPI 应用中
            app.include_router(router)

# CORS設定値を取得する
cors = "*"

'''
CORSMiddleware: 这是 FastAPI 提供的中间件类，用于处理 CORS 相关的请求。
allow_origins: 这是一个用于指定允许跨域请求的来源（origin）列表的参数。通常，它是一个逗号分隔的字符串，包含了所有被允许的来源。
               如果设置为 *，表示允许所有来源。
               例如，allow_origins="https://example.com,https://api.example.com" 表示只允许来自
                https://example.com 和 https://api.example.com 的请求。
allow_credentials: 这是一个布尔值参数，用于指示是否允许在跨域请求中发送凭据（例如，cookie、HTTP 认证等）。
                   如果设置为 True，表示允许发送凭据；如果设置为 False，表示不允许发送凭据。
allow_methods: 列表参数，用于指定允许的 HTTP 方法。通常包括 GET, POST, PUT, DELETE 等方法。如果设置为 ["*"]，表示允许所有方法。
allow_headers: 列表参数，用于指定允许的 HTTP 头部字段。如果设置为 ["*"]，表示允许所有头部字段。
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="https://ibun-api.vercel.app/")
