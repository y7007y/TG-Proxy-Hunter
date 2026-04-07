def save_to_readme(proxies):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# ✈️ Telegram MTProto 精选订阅\n\n")
        f.write(f"更新时间: `{now} (UTC)`\n\n")
        
        if not proxies:
            f.write("⚠️ 暂时没有发现有效代理，等待下次自动抓取。\n")
        else:
            f.write("### 🚀 节点列表 (若点击无效，请尝试复制链接手动添加)\n\n")
            f.write("| 序号 | 快速链接 (推荐点击) | 原始协议 (备用复制) |\n")
            f.write("| :--- | :--- | :--- |\n")
            for i, p in enumerate(proxies, 1):
                # 转换成 https 格式提高兼容性
                http_link = p.replace("tg://proxy", "https://t.me/proxy")
                f.write(f"| {i} | [⚡ 点击导入]({http_link}) | `{p}` |\n")

        f.write("\n\n---\n*注：若提示链接无效，请确保 Telegram 桌面端已安装并处于登录状态。*")
