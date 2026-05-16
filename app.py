import os
import sys

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
    # 强制劫持云平台的动态端口
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 正在点火专属金融云节点，绑定端口：{port}")
    
    # 强制启用 SSE 协议向外广播
    mcp.run(transport="sse", host="0.0.0.0", port=port)
