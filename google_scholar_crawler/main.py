from scholarly import scholarly
import json
import os
from datetime import datetime
import time

# 设置超时，防止一直卡住！
scholarly.set_timeout(10)
scholarly.set_retries(2)

# 防止请求过快被封
time.sleep(1)

try:
    # 读取环境变量
    scholar_id = os.getenv('GOOGLE_SCHOLAR_ID')
    if not scholar_id:
        raise Exception("未设置 GOOGLE_SCHOLAR_ID")

    print(f"正在抓取 Scholar ID: {scholar_id}")

    # 核心抓取
    author = scholarly.search_author_id(scholar_id)
    scholarly.fill(author, sections=['basics', 'indices', 'counts'])

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
    print(f"❌ 出错了: {str(e)}")
    raise
