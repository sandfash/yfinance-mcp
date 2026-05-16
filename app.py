import os
import sys
import uvicorn

# ---------------------------------------------------------
# 终极防线：在底层强行劫持并篡改 Uvicorn 的网络配置
# ---------------------------------------------------------
original_config_init = uvicorn.Config.__init__

def hijacked_config_init(self, app, **kwargs):
    # 强行将它的网线拔下，插到 Render 要求的公网端口上
    kwargs['host'] = '0.0.0.0'  
    kwargs['port'] = int(os.environ.get("PORT", 8000)) 
    original_config_init(self, app, **kwargs)

uvicorn.Config.__init__ = hijacked_config_init
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
    print("🚀 正在点火专属金融云节点，底层网络协议已劫持！")
    mcp.run(transport="sse")
