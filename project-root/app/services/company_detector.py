def detect_company(text: str) -> str:
    """
    OCR/HTMLから抽出したテキストをもとに
    電力会社を判定する
    """

    # 東北電力
    if ("東北電力" in text) or ("ご使用量" in text and "東北" in text):
        return "東北電力"

    # 北陸電力
    if ("北陸電力" in text) or ("ほくリンク" in text):
        return "北陸電力"

    # 東京電力
    if ("東京電力" in text) or ("TEPCO" in text) or ("くらしTEPCO" in text):
        return "東京電力"

    # 中部電力
    if ("中部電力" in text) or ("カテエネ" in text):
        return "中部電力"

    # 判定できない場合
    return None
