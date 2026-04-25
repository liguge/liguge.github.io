from scholarly import scholarly
import json
import os
from datetime import datetime
import time
import random

# --- 新增：带重试和随机延迟的抓取函数 ---
def fetch_with_retry(func, max_retries=3):
    """
    执行一个函数，如果被反爬虫机制拦截，则进行重试。
    """
    for attempt in range(max_retries):
        try:
            print(f"  尝试抓取 (第 {attempt + 1}/{max_retries} 次)...")
            result = func()
            print("  ✅ 抓取成功！")
            return result
        except Exception as e:
            print(f"  ⚠️ 尝试失败: {str(e)}")
            if attempt < max_retries - 1: # 如果不是最后一次尝试
                # 随机等待 5 到 15 秒，模拟真人行为
                wait_time = random.uniform(5, 15)
                print(f"  ⏳ 等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
            else:
                # 所有尝试都失败，抛出异常
                raise Exception(f"经过 {max_retries} 次尝试后仍然失败。")

# 设置超时和重试（这是 scholarly 库本身的重试，与我们的不同）
scholarly.set_timeout(10)
scholarly.set_retries(1)

try:
    # 读取环境变量
    scholar_id = os.getenv('GOOGLE_SCHOLAR_ID')
    if not scholar_id:
        raise Exception("未设置 GOOGLE_SCHOLAR_ID")

    print(f"正在抓取 Scholar ID: {scholar_id}")

    # --- 修改：使用带重试的函数来执行抓取 ---
    print("开始执行抓取...")
    author = fetch_with_retry(lambda: scholarly.search_author_id(scholar_id))
    # 填充详细信息也可能失败，所以也加上重试
    fetch_with_retry(lambda: scholarly.fill(author, sections=['basics', 'indices', 'counts']))

    # 输出信息
    citedby = author.get('citedby', 0)
    print(f"抓取成功！引用数: {citedby}")

    # 生成结果目录
    os.makedirs('results', exist_ok=True)

    # 写入完整数据
    author['updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('results/gs_data.json', 'w', encoding='utf-8') as f:
        json.dump(author, f, ensure_ascii=False, indent=2)

    # 写入徽章用的数据
    shieldio_data = {
        "schemaVersion": 1,
        "label": "Google Scholar Citations",
        "message": str(citedby)
    }
    with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
        json.dump(shieldio_data, f, ensure_ascii=False)

    print("✅ 全部完成！文件已保存到 results/")

except Exception as e:
    print(f"❌ 最终出错了: {str(e)}")
    # 抛出异常，让 GitHub Actions 知道任务失败了
    raise
