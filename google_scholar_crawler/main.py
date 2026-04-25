import requests
import json
import os
import re

def get_citations_from_html(user_id):
    url = f"https://scholar.google.com/citations?user={user_id}&hl=en"
    
    # 必须伪装成浏览器，否则 Google 直接拒绝
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        print(f"🔍 正在伪装成浏览器访问 Google Scholar...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ 请求失败！状态码: {response.status_code}")
            print("提示：Google 可能拦截了请求（反爬虫）。")
            return None

        html_content = response.text
        
        # 方法：使用正则表达式查找 "Cited by <b>数字</b>"
        # 这里的逻辑是寻找 "Cited by" 后面紧跟的加粗数字
        match = re.search(r'Cited by.*?<b>(\d+)</b>', html_content)
        
        if match:
            citations = int(match.group(1))
            print(f"✅ 提取成功！引用次数: {citations}")
            return citations
        else:
            print("❌ 未能找到引用次数。可能是网页结构变了，或者被重定向到了验证码页面。")
            # 调试用：打印前500个字符看看网页里到底是啥
            # print(html_content[:500]) 
            return None

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return None

# --- 主程序 ---
scholar_id = os.getenv('GOOGLE_SCHOLAR_ID') # 记得在 GitHub Secrets 设置这个变量

if scholar_id:
    citations = get_citations_from_html(scholar_id)
    
    if citations is not None:
        # 保存数据
        os.makedirs('results', exist_ok=True)
        badge_data = {
            "schemaVersion": 1,
            "label": "Google Scholar Citations",
            "message": str(citations),
            "color": "blue"
        }
        with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
            json.dump(badge_data, f)
        print("🎉 徽章更新完毕！")
    else:
        print("💡 建议：如果一直失败，请换用 Semantic Scholar API 方案。")
