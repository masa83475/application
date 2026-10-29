import csv
import uuid
import os

def generate_csv(data: dict) -> str:
    """
    抽出結果 dict を CSV に変換し、一時ファイルとして保存する
    FileResponse で返却できるようにファイルパスを返す
    """

    # 一時ファイルパス
    temp_id = str(uuid.uuid4())
    csv_path = f"/tmp/{temp_id}.csv"

    # CSVの列順（固定）
    headers = [
        "電力会社名",
        "契約種別",
        "検針日",
        "使用量(kWh)",
        "請求金額",
        "供給地点番号",
        "前月使用量",
        "燃料調整費",
        "再エネ賦課金",
        "基本料金",
        "従量料金",
        "電力量料金",
        "契約容量",
        "需要家番号",
        "請求月",
        "支払期限"
    ]

    # dict → CSV行に変換
    row = [
        data.get("company"),
        data.get("contract"),
        data.get("meter_date"),
        data.get("usage"),
        data.get("price"),
        data.get("supply_point"),
        data.get("prev_usage"),
        data.get("fuel_cost"),
        data.get("renewable_cost"),
        data.get("basic_fee"),
        data.get("meter_fee"),
        data.get("power_fee"),
        data.get("contract_amp"),
        data.get("customer_id"),
        data.get("billing_month"),
        data.get("due_date"),
    ]

    # CSV書き込み
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(row)

    return csv_path
