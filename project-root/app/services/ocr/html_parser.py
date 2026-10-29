from bs4 import BeautifulSoup

def extract_text_from_html(html_path: str) -> str:
    """
    HTML（WEB版検針票）を DOM解析してテキスト抽出する
    """
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    # HTML内のテキストをすべて抽出
    text = soup.get_text(separator="\n")

    return text
