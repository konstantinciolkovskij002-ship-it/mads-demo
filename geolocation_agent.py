"""
АГЕНТ ГЕОЛОКАЦИИ (Geolocation Agent) - Кластер 3: Гравитация Контекста
Определяет местоположение пользователя и переключает юрисдикции.
Нужен для: Протокола Путешествие
"""

class GeolocationAgent:
    def __init__(self):
        self.current_location = None
        self.previous_location = None
        self.jurisdictions = {
            "россия": {"law": "РФ", "currency": "RUB"},
            "казахстан": {"law": "РК", "currency": "KZT"},
            "финляндия": {"law": "FI", "currency": "EUR"},
        }
        print("[GEO] Агент Геолокации активирован.")

    def evaluate(self, user_input: str) -> dict | None:
        """
        Определяет местоположение пользователя по запросу.
        """
        lower_input = user_input.lower()
        for country, data in self.jurisdictions.items():
            if country in lower_input:
                self.previous_location = self.current_location
                self.current_location = country
                if self.previous_location and self.previous_location != country:
                    print(f"[GEO] Смена юрисдикции: {self.previous_location} -> {country}")
                    return {
                        "location_changed": True,
                        "previous": self.previous_location,
                        "current": country,
                        "law": data["law"],
                        "currency": data["currency"]
                    }
                print(f"[GEO] Местоположение: {country}")
                return {
                    "location_changed": False,
                    "current": country,
                    "law": data["law"],
                    "currency": data["currency"]
                }
        return None

    def get_warning(self, user_input: str) -> str | None:
        result = self.evaluate(user_input)
        if result and result.get("location_changed"):
            return (f"[GEO] ПУТЕШЕСТВИЕ: Вы переместились в новую юрисдикцию.\n"
                    f"Предыдущая: {result['previous']}\n"
                    f"Текущая: {result['current']}\n"
                    f"Право: {result['law']}\n"
                    f"Валюта: {result['currency']}")
        return None
    def verify(self, query: str, answer: str) -> dict:
        """Проверяет геолокационные утверждения в ответе LLM."""
        result = self.evaluate(answer)
        warning = self.get_warning(answer)
        
        violation = False
        violation_text = ""
        
        if warning:
            violation = True
            violation_text = warning
        
        return {
            "violation": violation,
            "violation_text": violation_text
        }


if __name__ == "__main__":
    agent = GeolocationAgent()
    print("Тест 1: Определение")
    result = agent.evaluate("Я в России")
    if result:
        print(f"Страна: {result['current']}\n")
    print("Тест 2: Смена юрисдикции")
    warning = agent.get_warning("Я приехал в Финляндию")
    if warning:
        print(warning)