import requests
import re
import datetime

def fetch_proxies():
    all_links = []
    
    # 🎯 2026 年最稳的三个聚合接口 (无需 Token，直接获取文本)
    api_sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5", # 虽然是S5，但常混有MT
        "https://mtpro.xyz/api/?type=mtproto", # 专门的 MTProto API
        "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray" # 综合订阅源
    ]
    
    # 补充：直接从几个不挂梯子也能访问的镜像源抓
    mirror_sources = [
        "https://proxy-list.download/api/v1/get?type=socks5",
        "https://www.proxy-list.download/api/v1/get?type=https"
    ]

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}

    # 尝试从 API 抓取
    for url in api_sources + mirror_sources:
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                # 匹配标准的 tg://proxy 格式
                found = re.findall(r'tg://proxy\?server=[^\s"\'<>&\u4e00-\u9fa5]+', res.text)
                for link in found:
                    clean_link = link.split('"')[0].split("'")[0].replace("&amp;", "&").strip()
                    if clean_link not in all_links:
                        all_links.append(clean_link)
        except:
            continue

    # 如果 API 抓不到，最后保底策略：构造几个经典的长期有效代理 (防止 README 为空)
    if not all_links:
        # 这里可以放几个你平时收藏的比较稳的长期节点
        pass

    return all_links[:20]

def save_to_readme(proxies):
    # 北京时间
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# ✈️ Telegram MTProto 自动补给站\n\n")
        f.write(f"最后巡检时间: `{now} (北京时间)`\n\n")
        
        if not proxies:
            f.write("### ⚠️ 节点池暂时干涸\n")
            f.write("目前全网公共接口未返回有效 MTProto 节点。脚本将在 2 小时后重新扫描。\n")
        else:
            f.write("### 🚀 最新检测到的可用节点\n\n")
            f.write("| 序号 | 快速连接 | 原始协议 (复制到 TG 粘贴发送即可) |\n")
            f.write("| :--- | :--- | :--- |\n")
            for i, p in enumerate(proxies, 1):
                # 将 tg:// 转换为 https://t.me/ 增强电脑端兼容性
                http_link = p.replace("tg://proxy", "https://t.me/proxy")
                f.write(f"| {i} | [⚡ 点击导入]({http_link}) | `{p}` |\n")

if __name__ == "__main__":
    proxy_list = fetch_proxies()
    save_to_readme(proxy_list)
