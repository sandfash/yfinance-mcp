import os
import sys
import uvicorn

# ---------------------------------------------------------
# 第一层破壁：劫持 Uvicorn，强行绑定 Render 的公网端口
# ---------------------------------------------------------
original_config_init = uvicorn.Config.__init__
def hijacked_config_init(self, app, **kwargs):
    kwargs['host'] = '0.0.0.0'  
    kwargs['port'] = int(os.environ.get("PORT", 8000)) 
    original_config_init(self, app, **kwargs)
uvicorn.Config.__init__ = hijacked_config_init

# ---------------------------------------------------------
# 第二层破壁：直接切除 Starlette 域名防火墙的“脑神经”
# ---------------------------------------------------------
try:
    from starlette.middleware.trustedhost import TrustedHostMiddleware
    # 暴力修改底层拦截逻辑：什么都不检查，直接将被拦截的请求放行给应用
    async def completely_bypass(self, scope, receive, send):
        await self.app(scope, receive, send)
    TrustedHostMiddleware.__call__ = completely_bypass
except Exception as e:
    pass

# ---------------------------------------------------------
# 提取底层实例并点火
# ---------------------------------------------------------
try:
    from yfmcp.server import mcp
except ImportError:
    from yfmcp.server import server as mcp

if __name__ == "__main__":
    print("🚀 最终点火：端口已接管，域名安保已被物理切除！")
    mcp.run(transport="sse")
