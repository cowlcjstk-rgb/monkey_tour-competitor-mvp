EXTRACTION_PROMPT = """
다음은 여행/투어 상품 페이지 본문이다.
아래 항목을 JSON으로 추출하라.

항목:
- source_name
- product_name
- price
- currency
- tour_type
- duration
- pickup
- included
- excluded
- highlights
- child_policy
- cancellation_policy
- options
- summary_strength
- summary_weakness

규칙:
- 추정하지 말고 본문에 있는 정보만 사용하라.
- 없으면 null 또는 빈 배열로 둬라.
"""

ANALYSIS_PROMPT = """
다음은 우리 상품 1개와 경쟁사 상품 3개의 데이터다.
다음을 작성하라:
1. 가격 포지션 분석
2. 우리 상품 강점 3개
3. 우리 상품 약점 3개
4. 액션 아이템 5개
"""
