import requests
import re
import os
import datetime

# 从环境变量获取 Token
GITHUB_TOKEN = os.environ.get("GH_TOKEN")

def search_github_tg():
    # 搜索包含 Telegram 代理特征码的文件，按最新索引排序
    queries = [
        "tg://proxy?server=",
        "t.me/proxy?server=",
        "MTProxy secret="
    ]
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    all_links = set()

    for q in queries:
        url = f"https://api.github.com/search/code?q={q}&sort=indexed"
        try:
            res = requests.get(url, headers=headers, timeout=10).json()
            for item in res.get('items', []):
                raw_url = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                content = requests.get(raw_url, timeout=5).text
                # 正则匹配两种协议格式
                links = re.findall(r'(tg://proxy\?server=[^\s"\'<>]+|https://t.me/proxy\?server=[^\s"\'<>]+)', content)
                for link in links:
                    # 统一转换为 tg:// 格式以便直接调用
                    all_links.add(link.replace("https://t.me/proxy", "tg://proxy"))
        except Exception as e:
            print(f"搜索 {q} 时出错: {e}")
    
    return sorted(list(all_links))

def save_to_readme(proxies):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# ✈️ Telegram MTProto 自动订阅\n\n")
        f.write(f"最后更新时间: `{now} (UTC)`\n\n")
        f.write(f"### 🔗 实时代理列表 ({len(proxies)}个)\n\n")
        f.write("> **提示**: 点击下方链接可直接在 Telegram 中启用代理。\n\n")
        for p in proxies:
            f.write(f"- {p}\n")

if __name__ == "__main__":
    proxy_list = search_github_tg()
    save_to_readme(proxy_list)
