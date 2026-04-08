import requests
import re
import datetime

def fetch_proxies():
    all_links = []
    
    # 1. 采集目标：包含知名代理频道和稳定 Raw 源
    # 采用 t.me/s/ 这种 Web 预览模式，不需要 Telegram 账号就能爬取
    targets = [
        "https://t.me/s/ProxyMTProto",
        "https://t.me/s/MTProxy_List",
        "https://t.me/s/Mpro_x",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg_proxies.txt"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for url in targets:
        try:
            print(f"正在扫描源: {url}")
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                # 增强型正则：匹配 tg:// 和 t.me/ 格式，并过滤掉重复和多余字符
                # 专门针对 Telegram 网页版混淆的链接进行提取
                found = re.findall(r'(tg://proxy\?server=[^\s"\'<>&\u4e00-\u9fa5]+|https://t.me/proxy\?server=[^\s"\'<>&\u4e00-\u9fa5]+)', res.text)
                for link in found:
                    # 统一标准化
                    clean_link = link.replace("https://t.me/proxy", "tg://proxy").replace("&amp;", "&")
                    if "server=" in clean_link and clean_link not in all_links:
                        all_links.append(clean_link)
        except Exception as e:
            print(f"扫描 {url} 出错: {e}")

    # 2. 排序并去重（最新的通常在后面，我们取最后发现的 20 个）
    return all_links[-20:]

def save_to_readme(proxies):
    # 北京时间
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# ✈️ Telegram MTProto 订阅 (2026 聚合版)\n\n")
        f.write(f"最后更新时间: `{now} (北京时间)`\n\n")
        
        if not proxies:
            f.write("### 📭 状态：暂时未发现活跃节点\n\n")
            f.write("> **排查建议**：如果此状态持续，请检查 GitHub Actions 的服务器是否能访问 t.me 地址。\n")
        else:
            f.write(f"### 🚀 最新优选节点 ({len(proxies)}个)\n\n")
            f.write("| 序号 | 快速操作 (推荐) | 备用协议 |\n")
            f.write("| :--- | :--- | :--- |\n")
            # 倒序排列，让最新的在最上面
            for i, p in enumerate(reversed(proxies), 1):
                http_link = p.replace("tg://proxy", "https://t.me/proxy")
                f.write(f"| {i} | [⚡ 点击一键导入]({http_link}) | `{p}` |\n")

if __name__ == "__main__":
    proxy_list = fetch_proxies()
    save_to_readme(proxy_list)
