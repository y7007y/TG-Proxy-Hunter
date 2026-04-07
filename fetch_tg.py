import requests
import re
import os
import datetime

GITHUB_TOKEN = os.environ.get("GH_TOKEN")

def search_github_tg():
    # 增加更强大的搜索词
    queries = ["tg://proxy?server=", "t.me/proxy?server=", "MTProxy secret=ee"]
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    all_links = []

    for q in queries:
        url = f"https://api.github.com/search/code?q={q}&sort=indexed&order=desc"
        try:
            res = requests.get(url, headers=headers, timeout=15).json()
            for item in res.get('items', []):
                raw_url = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                content = requests.get(raw_url, timeout=5).text
                links = re.findall(r'(tg://proxy\?server=[^\s"\'<>]+|https://t.me/proxy\?server=[^\s"\'<>]+)', content)
                for link in links:
                    # 统一标准化
                    clean_link = link.replace("https://t.me/proxy", "tg://proxy")
                    if clean_link not in all_links:
                        all_links.append(clean_link)
        except:
            pass
    return all_links[:20]

def save_to_readme(proxies):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# ✈️ Telegram MTProto 精选订阅\n\n")
        f.write(f"更新时间: `{now} (UTC)`\n\n")
        f.write(f"### 🚀 节点列表 (推荐使用点击导入)\n\n")
        
        if not proxies:
            f.write("⚠️ 暂时没有发现有效代理，等待下次自动抓取。\n")
        else:
            # 使用表格增强兼容性和可读性
            f.write("| 序号 | 快速操作 | 原始协议 (备用) |\n")
            f.write("| :--- | :--- | :--- |\n")
            for i, p in enumerate(proxies, 1):
                # 将 tg:// 转换为 https:// 以解决电脑端点击无效的问题
                http_link = p.replace("tg://proxy", "https://t.me/proxy")
                f.write(f"| {i} | [⚡ 点击一键导入]({http_link}) | `{p}` |\n")

if __name__ == "__main__":
    proxy_list = search_github_tg()
    save_to_readme(proxy_list)
