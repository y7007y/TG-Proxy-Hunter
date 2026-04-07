import requests
import re
import os
import datetime
import base64

GITHUB_TOKEN = os.environ.get("GH_TOKEN")

def search_github_tg():
    # 2026 年更精准的特征词：MTProto 混淆版常用 secret 开头为 ee 或带有长密钥
    queries = [
        "tg://proxy?server=",
        "t.me/proxy?server=",
        "MTProxy+secret=ee",
        "MTProxy+port=443"
    ]
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    } if GITHUB_TOKEN else {}
    
    all_links = []

    for q in queries:
        # 增加 per_page=50 扩大单次抓取量
        url = f"https://api.github.com/search/code?q={q}&sort=indexed&order=desc&per_page=50"
        try:
            res = requests.get(url, headers=headers, timeout=15).json()
            items = res.get('items', [])
            
            for item in items:
                raw_url = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                # 针对某些项目可能需要 Base64 解码或直接读取
                content = requests.get(raw_url, timeout=5).text
                
                # 增强正则：匹配包含 server, port, secret 的完整链接
                pattern = r'(tg://proxy\?server=[^\s"\'<>&\u4e00-\u9fa5]+|https://t.me/proxy\?server=[^\s"\'<>&\u4e00-\u9fa5]+)'
                links = re.findall(pattern, content)
                
                for link in links:
                    # 规范化处理，去除可能残留的 Markdown 符号
                    clean_link = link.replace("https://t.me/proxy", "tg://proxy").split(')')[0].split(']')[0]
                    if "server=" in clean_link and "port=" in clean_link and clean_link not in all_links:
                        all_links.append(clean_link)
        except Exception as e:
            print(f"搜索 {q} 时遇到干扰: {e}")
            
    return all_links[:20]

def save_to_readme(proxies):
    now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# ✈️ Telegram MTProto 订阅 (2026 自动版)\n\n")
        f.write(f"最后巡检时间: `{now} (北京时间)`\n\n")
        
        if not proxies:
            f.write("### 📭 状态：当前公共池暂时空洞\n\n")
            f.write("> **分析**：可能是 GitHub API 触发了速率限制或当前搜索范围内无新节点更新。脚本将在 2 小时后自动重试。\n")
        else:
            f.write("### 🚀 今日精选一键导入\n\n")
            f.write("| 序号 | 快速操作 (电脑/手机通用) | 原始协议 (备用) |\n")
            f.write("| :--- | :--- | :--- |\n")
            for i, p in enumerate(proxies, 1):
                http_link = p.replace("tg://proxy", "https://t.me/proxy")
                f.write(f"| {i} | [⚡ 点击一键导入]({http_link}) | `{p}` |\n")

if __name__ == "__main__":
    proxy_list = search_github_tg()
    save_to_readme(proxy_list)
