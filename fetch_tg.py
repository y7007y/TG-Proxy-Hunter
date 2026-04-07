import requests
import re
import os
import datetime

# 从环境变量获取 Token
GITHUB_TOKEN = os.environ.get("GH_TOKEN")

def search_github_tg():
    # 增加更精准的搜索词，确保抓到的是最新的
    queries = [
        "tg://proxy?server=",
        "t.me/proxy?server="
    ]
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    all_links = [] # 改用列表以保持原始搜索顺序

    for q in queries:
        # 增加 sort=indexed 确保获取 GitHub 最新收录的代理
        url = f"https://api.github.com/search/code?q={q}&sort=indexed&order=desc"
        try:
            res = requests.get(url, headers=headers, timeout=15).json()
            for item in res.get('items', []):
                raw_url = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                content = requests.get(raw_url, timeout=5).text
                # 匹配链接
                links = re.findall(r'(tg://proxy\?server=[^\s"\'<>]+|https://t.me/proxy\?server=[^\s"\'<>]+)', content)
                for link in links:
                    clean_link = link.replace("https://t.me/proxy", "tg://proxy")
                    if clean_link not in all_links:
                        all_links.append(clean_link)
        except Exception as e:
            print(f"搜索 {q} 时出错: {e}")
    
    # 💥 核心修改：仅保留前 20 个最新抓取到的代理
    return all_links[:20]

def save_to_readme(proxies):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# ✈️ Telegram MTProto 订阅 (精选版)\n\n")
        f.write(f"最后更新: `{now} (UTC)`\n\n")
        f.write(f"### 🚀 今日优选代理 Top 20\n\n")
        f.write("> **注**: Telegram 代理失效快，建议每 2 小时刷新本页获取最新节点。\n\n")
        
        if not proxies:
            f.write("目前未抓取到有效链接，请稍后再试。\n")
        else:
            for i, p in enumerate(proxies, 1):
                f.write(f"{i}. {p}\n")

if __name__ == "__main__":
    proxy_list = search_github_tg()
    save_to_readme(proxy_list)
