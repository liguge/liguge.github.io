from scholarly import scholarly
import json
import os
import time
import random

# --- 配置 ---
# 设置超时时间，防止卡死
scholarly.set_timeout(10)
scholarly.set_retries(2)

def fetch_citations_with_retry(scholar_id, max_retries=3):
    """
    专门用于获取总引用次数的函数，带重试机制
    """
    for attempt in range(max_retries):
        try:
            print(f"🔍 正在尝试获取数据 (第 {attempt + 1}/{max_retries} 次)...")
            
            # 1. 搜索作者
            author = scholarly.search_author_id(scholar_id)
            
            # 2. 填充数据 - 关键修改：只填充 'indices' (包含引用次数)，不填充 'publications'
            # 这样能极大减少请求量和超时概率
            scholarly.fill(author, sections=['indices'])
            
            # 3. 提取引用次数
            citations = author['citedby']
            print(f"✅ 抓取成功！总被引次数: {citations}")
            return citations
            
        except Exception as e:
            print(f"⚠️ 尝试失败: {str(e)}")
            if attempt < max_retries - 1:
                # 随机等待 3-8 秒，模拟真人
                wait_time = random.uniform(3, 8)
                print(f"⏳ 等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
            else:
                raise Exception(f"经过 {max_retries} 次尝试后仍然失败。")

try:
    # 读取环境变量
    scholar_id = os.getenv('GOOGLE_SCHOLAR_ID')
    if not scholar_id:
        raise Exception("❌ 错误：未设置 GOOGLE_SCHOLAR_ID 环境变量")

    # 执行抓取
    total_citations = fetch_citations_with_retry(scholar_id)

    # --- 生成徽章所需的 JSON 文件 ---
    os.makedirs('results', exist_ok=True)
    
    shieldio_data = {
        "schemaVersion": 1,
        "label": "Google Scholar Citations",
        "message": str(total_citations)
    }
    
    with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
        json.dump(shieldio_data, f, ensure_ascii=False)

    print("🎉 任务完成！徽章数据已更新。")

except Exception as e:
    print(f"❌ 最终出错: {str(e)}")
    raise
