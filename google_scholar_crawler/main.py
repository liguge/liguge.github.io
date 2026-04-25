import requests
import json
import os

def main():
    # 1. 获取密钥和 ID
    api_key = os.getenv('SERP_API_KEY')
    scholar_id = os.getenv('GOOGLE_SCHOLAR_ID')
    
    # 本地调试用（如果环境变量没设置，可以在这里硬编码测试）
    # 如果你在本地运行报错，取消下面两行的注释，并填入你的 Key 和 ID
    # if not api_key: api_key = "你的-serpapi-key"
    # if not scholar_id: scholar_id = "1DtpMlAAAAAJ" 

    if not api_key or not scholar_id:
        print("❌ 错误：请在 GitHub Secrets 中设置 SERP_API_KEY 和 GOOGLE_SCHOLAR_ID")
        return

    print(f"🔍 正在通过 SerpAPI 获取数据...")

    # 2. 发送请求
    params = {
        "engine": "google_scholar_author",
        "author_id": scholar_id,
        "api_key": api_key
    }

    try:
        response = requests.get("https://serpapi.com/search.json", params=params, timeout=10)
        data = response.json()

        # 3. 核心：精准提取引用数 (根据你上传的 searchm.txt 结构)
        # 路径: cited_by -> table -> 第一个元素 -> citations -> all
        citations = 0
        if 'cited_by' in data and 'table' in data['cited_by']:
            # 防御性编程：确保列表不为空
            if len(data['cited_by']['table']) > 0:
                all_cites = data['cited_by']['table'][0].get('citations', {}).get('all')
                if isinstance(all_cites, int):
                    citations = all_cites
                else:
                    print("⚠️ 警告：未找到 'all' 引用数字段，可能数据结构有变动。")
            else:
                print("⚠️ 警告：cited_by 表格为空。")
        else:
            print("❌ 错误：API 返回数据中缺少 'cited_by' 字段。原始错误:", data.get('error', 'Unknown'))

        print(f"✅ 成功提取！总引用次数: {citations}")

        # 4. 保存为徽章格式
        os.makedirs('results', exist_ok=True)
        badge_data = {
            "schemaVersion": 1,
            "label": "Google Scholar",
            "message": f"{citations}",
            "color": "critical" # 颜色可以根据喜好改，比如 blue, green, 9cf 等
        }
        with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
            json.dump(badge_data, f, indent=2)
        
        print("🎉 任务完成！徽章已生成。")

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求异常: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析错误: {e}")
        print("服务器返回的原始内容:", response.text[:500]) # 打印前500字符用于排查
    except Exception as e:
        print(f"❌ 未知错误: {e}")

if __name__ == "__main__":
    main()
