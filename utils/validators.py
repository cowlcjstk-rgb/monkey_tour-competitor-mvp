from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def validate_urls(urls: list[str]):
    if not all(urls):
        return False, "모든 URL을 입력해주세요."

    if len(set(urls)) != len(urls):
        return False, "중복 URL이 있습니다."

    for url in urls:
        if not is_valid_url(url):
            return False, f"유효하지 않은 URL입니다: {url}"

    return True, "OK"
