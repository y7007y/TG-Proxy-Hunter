import requests
import re
import datetime
from urllib.parse import unquote

def fetch_proxies():
    all_links = []
    # 聚焦于最活跃的三个频道 Web 预览版
    targets = [
        "https://t.me/s/ProxyMTProto",
        "https://t.me/s/MTProxy_List",
        "https://t.me/s/Mpro_x"
    ]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    for url in targets:
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                # 提取原始链接
                found = re.findall(r'tg://proxy\?server=[^\s"\'<>&\u4e00-\u9fa5]+&port=[0-9]+&secret=[a-zA-Z0-9]+', res.text)
                for link in found:
                    # 关键：彻底清洗 HTML 转义字符 (如 &amp;)
                    clean_link = unquote(link).replace("&amp;", "&").strip()
                    if clean_link not in all_links:
                        all_links.append(clean_link)
        except:
            pass
    return all_links[-20:]

def save_to_readme(proxies):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# ✈️ Telegram MTProto 极简订阅\n\n")
        f.write(f"最后巡检: `{now} (北京时间)`\n\n")
        
        if not proxies:
            f.write("### 📭 暂无有效节点，正在重新调度...\n")
        else:
            f.write("### ⚡ 方案 A：一键导入 (推荐)\n")
            f.write("> 点击下方按钮，若弹出 Telegram 即可直接启用。\n\n")
            
            for i, p in enumerate(reversed(proxies), 1):
                # 转换成 https 格式以获得更好的浏览器兼容性
                http_link = p.replace("tg://proxy", "https://t.me/proxy")
                f.write(f"[{i}. 点击导入此代理]({http_link}) &nbsp;&nbsp; ")
                if i % 2 == 0: f.write("\n\n") # 每行放两个链接，避免排版过长

            f.write("\n\n---\n\n")
            f.write("### 🛠️ 方案 B：手动复制 (若方案 A 无效)\n")
            f.write("> 复制下方完整代码，直接粘贴发送给任意 Telegram 联系人（或 Saved Messages），然后点击该链接即可。\n\n")
            f.write("```text\n")
            for p in reversed(proxies):
                f.write(f"{p}\n")
            f.write("```\n")

if __name__ == "__main__":
    proxy_list = fetch_proxies()
    save_to_readme(proxy_list)
