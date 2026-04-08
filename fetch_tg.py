import requests
import re
import datetime

def fetch_proxies():
    all_links = []
    # 🎯 2026 年最稳的 3 个实时更新频道（Web 预览模式）
    # 这些页面是公开的，GitHub Actions 访问它们的成功率最高
    channels = [
        "https://t.me/s/ProxyMTProto",
        "https://t.me/s/MTProxy_List",
        "https://t.me/s/Mpro_x"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for url in channels:
        try:
            print(f"正在强力扫描: {url}")
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code == 200:
                # 核心改进：匹配包含 server, port, secret 的完整链接，并忽略转义
                # 这种正则能抓到隐藏在 HTML 属性里的原始链接
                found = re.findall(r'tg://proxy\?server=[a-zA-Z0-9\.-]+&amp;port=[0-9]+&amp;secret=[a-zA-Z0-9]+', res.text)
                
                # 如果上面抓不到，尝试兼容非转义格式
                if not found:
                    found = re.findall(r'tg://proxy\?server=[a-zA-Z0-9\.-]+&port=[0-9]+&secret=[a-zA-Z0-9]+', res.text)
                
                for link in found:
                    # 彻底清洗 &amp; 符号，这是导致“链接无效”的罪魁祸首
                    clean_link = link.replace("&amp;", "&").strip()
                    if clean_link not in all_links:
                        all_links.append(clean_link)
        except Exception as e:
            print(f"扫描 {url} 失败: {e}")

    # 只保留最新的 20 个（通常频道最后发的最新）
    return all_links[-20:]

def save_to_readme(proxies):
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# ✈️ Telegram MTProto 自动补给站\n\n")
        f.write(f"最后巡检: `{now} (北京时间)`\n\n")
        
        if not proxies:
            f.write("### ❌ 状态：全线链路阻断\n")
            f.write("当前 GitHub Actions 节点无法访问 Telegram 镜像，请尝试手动运行一次。\n")
        else:
            f.write(f"### ✅ 今日捕获到 {len(proxies)} 个活跃节点\n\n")
            f.write("| 序号 | 操作 | 链接 (若点击失效请复制下方代码) |\n")
            f.write("| :--- | :--- | :--- |\n")
            for i, p in enumerate(reversed(proxies), 1):
                # 转换 http 链接增强兼容性
                http_link = p.replace("tg://proxy", "https://t.me/proxy")
                f.write(f"| {i} | [⚡ 点击导入]({http_link}) | `{p}` |\n")

if __name__ == "__main__":
    proxy_list = fetch_proxies()
    save_to_readme(proxy_list)
