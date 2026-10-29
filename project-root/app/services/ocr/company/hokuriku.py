import re

def extract(text: str) -> dict:
    result = {}

    result["company"] = "北陸電力"

    result["usage"] = _find(r"ご使用量[:：]?\s*([0-9]+)\s*kWh", text)
    result["price"] = _find(r"ご請求金額[:：]?\s*([0-9,]+)円", text)
    result["contract"] = _find(r"(従量電灯|業務用電力)", text)
    result["meter_date"] = _find(r"検針日[:：]?\s*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})", text)
    result["supply_point"] = _find(r"供給地点番号[:：]?\s*([0-9]{22})", text)

    result.update(_common_extract(text))

    return result


def _find(pattern: str, text: str):
    m = re.search(pattern, text)
    return m.group(1) if m else None


def _common_extract(text: str) -> dict:
    return {
        "prev_usage": _find(r"前月使用量[:：]?\s*([0-9]+)\s*kWh", text),
        "fuel_cost": _find(r"燃料調整費[:：]?\s*([0-9,]+)円", text),
        "renewable_cost": _find(r"再エネ賦課金[:：]?\s*([0-9,]+)円", text),
        "basic_fee": _find(r"基本料金[:：]?\s*([0-9,]+)円", text),
        "meter_fee": _find(r"従量料金[:：]?\s*([0-9,]+)円", text),
        "power_fee": _find(r"電力量料金[:：]?\s*([0-9,]+)円", text),
        "contract_amp": _find(r"契約容量[:：]?\s*([0-9]+)A", text),
        "customer_id": _find(r"需要家番号[:：]?\s*([0-9]+)", text),
        "billing_month": _find(r"請求月[:：]?\s*([0-9]{4}/[0-9]{1,2})", text),
        "due_date": _find(r"支払期限[:：]?\s*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})", text),
    }
