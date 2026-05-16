import os
import sys
import uvicorn

# ---------------------------------------------------------
# 第一重劫持：强行将网线插到 Render 的公网端口上，并允许反向代理
# ---------------------------------------------------------
original_config_init = uvicorn.Config.__init__
def hijacked_config_init(self, app, **kwargs):
    kwargs['host'] = '0.0.0.0'  
    kwargs['port'] = int(os.environ.get("PORT", 8000)) 
    kwargs['proxy_headers'] = True
    kwargs['forwarded_allow_ips'] = '*'
    original_config_init(self, app, **kwargs)
uvicorn.Config.__init__ = hijacked_config_init

# ---------------------------------------------------------
# 第二重劫持：暴力拆除底层的域名防火墙 (解决 Invalid Host header)
# ---------------------------------------------------------
try:
    from starlette.middleware.trustedhost import TrustedHostMiddleware
    original_trusted_init = TrustedHostMiddleware.__init__
    def hijacked_trusted_init(self, app, allowed_hosts=None, **kwargs):
        # 强制将白名单修改为 "*" (放行所有 Render 域名)
        original_trusted_init(self, app, allowed_hosts=["*"], **kwargs)
    TrustedHostMiddleware.__init__ = hijacked_trusted_init
except ImportError:
    pass

# ---------------------------------------------------------
# 动态捕获底层框架实例
try:
    from yfmcp.server import mcp
except ImportError:
    try:
        from yfmcp.server import server as mcp
    except ImportError:
        print("致命错误：无法在底层找到实例")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 正在点火专属金融云节点，底层端口与域名防火墙已全部劫持！")
    mcp.run(transport="sse")
