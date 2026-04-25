import requests
import json
import os
import time
import random

def get_scholar_citations(user_id):
    url = f"https://scholar.google.com/citations?user={user_id}&hl=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    for attempt in range(3):
        try:
            print(f"🔍 正在连接 Google Scholar... (尝试 {attempt + 1}/3)")
            response = requests.get(url, headers=headers, timeout=10)
            
            if "Cited by" in response.text:
                # 简单的字符串查找提取引用数（Google 页面通常包含 "Cited by <b>123</b>"）
                import re
                match = re.search(r'Cited by</a>.*?<b>(\d+)</b>', response.text)
                if match:
                    return int(match.group(1))
                # 备用匹配模式（针对个人主页概览）
                match = re.search(r'All citations</a>.*?<b>(\d+)</b>', response.text)
                if match:
                    return int(match.group(1))
            print("⚠️ 未能解析数据，可能是反爬虫拦截。")
            
        except Exception as e:
            print(f"⚠️ 连接错误: {e}")
        
        if attempt < 2:
            time.sleep(random.uniform(2, 5))
            
    return 0 # 失败返回0

try:
    scholar_id = os.getenv('GOOGLE_SCHOLAR_ID')
    if not scholar_id:
        raise Exception("未设置 GOOGLE_SCHOLAR_ID")

    citations = get_scholar_citations(scholar_id)
    print(f"✅ 获取成功：{citations}")

    # 保存文件
    os.makedirs('results', exist_ok=True)
    data = {
        "schemaVersion": 1,
        "label": "Google Scholar Citations",
        "message": str(citations)
    }
    with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
        
except Exception as e:
    print(f"❌ 出错: {e}")
    raise
