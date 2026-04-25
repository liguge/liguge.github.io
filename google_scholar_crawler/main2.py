import os
import re
import json
from tavily import TavilyClient

# ================= 配置区域 =================
# 推荐方式：在环境变量中设置
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SCHOLAR_ID = "1DtpMlAAAAAJ"
# ===========================================


def extract_citations_from_content(content: str) -> int:
    if not content:
        return 0

    pattern = re.compile(
        r"(?:Cited\s*by|Citations).*?\|\s*(\d+)",
        re.IGNORECASE | re.DOTALL
    )

    match = pattern.search(content)
    if match:
        return int(match.group(1))

    return 0


def get_citations() -> int:
    if not TAVILY_API_KEY:
        print("❌ 错误：未设置 TAVILY_API_KEY")
        return 0

    client = TavilyClient(api_key=TAVILY_API_KEY)

    query = f'site:scholar.google.com "{SCHOLAR_ID}" "Cited by"'

    print("🔍 正在通过 Tavily 搜索 Google Scholar...")

    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_domains=["scholar.google.com"]
        )

        results = response.get("results", [])
        print(f"✅ 搜索到 {len(results)} 条结果")

        all_numbers = []

        for item in results:
            content = item.get("content", "")
            citations = extract_citations_from_content(content)
            if citations > 0:
                all_numbers.append(citations)

        if not all_numbers:
            print("❌ 未能解析到任何引用数")
            return 0

        # 取最大值，避免被单篇文章引用数干扰
        final_count = max(all_numbers)
        print(f"✅ 最终引用数: {final_count}")
        return final_count

    except Exception as e:
        print(f"❌ Tavily 请求失败: {e}")
        return 0


def main():
    cited_by = get_citations()

    shield_data = {
        "schemaVersion": 1,
        "label": "Google Scholar Citations",
        "message": str(cited_by),
        "color": "blue" if cited_by > 0 else "lightgrey"
    }

    os.makedirs("results", exist_ok=True)
    output_path = "results/gs_data_shieldsio.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(shield_data, f, indent=2)

    print(f"✅ 徽章文件已生成: {output_path}")


if __name__ == "__main__":
    main()
