EXTRACTION_PROMPT = """
다음은 여행/투어 상품 페이지 본문이다.
본문에 있는 정보만 사용해서 JSON으로 추출하라.

규칙:
- 추정하지 말 것
- 정보가 없으면 null 또는 빈 배열
- 포함사항과 불포함사항 분리
- pickup 값은 included / excluded / partial / unknown 중 하나
"""

ANALYSIS_PROMPT = """
다음은 우리 상품 1개와 경쟁사 상품 3개의 구조화된 데이터다.
아래 항목을 JSON으로 작성하라.

1. positioning
2. our_strengths
3. our_weaknesses
4. action_items

규칙:
- 사실 기반으로 작성
- 정보가 없으면 과장하지 말 것
- 상품관리 담당자가 바로 수정에 활용할 수 있게 작성
"""
