"""
MADS Agent Interface v1.0
Единый интерфейс для всех агентов в Институтах.
Каждый агент должен реализовать функцию:
    verify(query: str, answer: str) -> dict
    возвращает {"violation": bool, "violation_text": str}
"""