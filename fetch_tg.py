import requests
import re
import datetime
import base64

def fetch_proxies():
    all_links = []
    
    # 🎯 方案：直接抓取已经聚合好的订阅转换源 (这些是 2026 年最稳的“矿场”)
    sources = [
        "https://raw.githubusercontent.com/WilliamStar007/Proxy/main/mtproto.txt",
        "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64",
        "https://raw.githubusercontent.com/LalatinaHub/MTProto-Collector/main/links.txt"
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    for url in sources:
        try:
            res = requests.get(url, headers=headers, timeout=15)
            content = res.text
            
            # 如果是 Base64 加密的源，先解码
            if "tg://proxy" not in content and len(content) > 100:
                try:
                    content = base64.b64decode(content).decode('utf-8')
                except:
                    pass
            
            # 匹配标准的 tg://proxy 格式
            found = re.findall(r'tg://proxy\?server=[^\s"\'<>&\u4e00-\u9fa5]+', content)
            for link in found:
                # 彻底清洗
                clean_link = link.replace("&amp;", "&").strip()
                if clean_link not in all_links:
                    all_links.append(clean_link)
        except:
            continue

    # 排序：取最新的 20 个
    return all_links[:20]

def save_to_readme(proxies):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# ✈️ Telegram MTProto 自动补给站\n\n")
        f.write(f"最后巡检: `{now} (北京时间)`\n\n")
        
        if not proxies:
            f.write("### ⚠️ 状态：节点池正在维护\n")
            f.write("由于 GitHub 网络波动，建议点击右上角 **Actions** 手动触发 `Run workflow`。\n")
        else:
            f.write("### 🚀 今日实时节点 (电脑端若无效请复制原始协议)\n\n")
            f.write("| 序号 | 快速操作 | 原始协议 (复制发送给 TG 里的 Saved Messages) |\n")
            f.write("| :--- | :--- | :--- |\n")
            for i, p in enumerate(proxies, 1):
                # 转换格式
                http_link = p.replace("tg://proxy", "https://t.me/proxy")
                f.write(f"| {i} | [⚡ 点击导入]({http_link}) | `{p}` |\n")

if __name__ == "__main__":
    proxy_list = fetch_proxies()
    save_to_readme(proxy_list)
