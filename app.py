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
    print("🚀 正在点火专属金融云节点，移交端口控制权给云平台...")
    # 框架底层已自动接管 0.0.0.0 和环境变量 PORT，只需直接下达 sse 唤醒指令
    mcp.run(transport="sse")
