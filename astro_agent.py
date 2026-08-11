"""
АГЕНТ АСТРОФИЗИКИ (Astrophysics Agent) - Кластер 2: Гравитация Истины
Проверяет запросы на соответствие законам астрофизики и космологии.
"""

class AstroAgent:
    def __init__(self):
        self.astro_laws = {
            "чёрная дыра": (
                "Общая теория относительности",
                "Чёрная дыра — область пространства-времени с настолько сильной гравитацией, что даже свет не может её покинуть."
            ),
            "большой взрыв": (
                "Теория Большого взрыва",
                "Вселенная возникла около 13.8 миллиардов лет назад из состояния с бесконечной плотностью и температурой."
            ),
            "тёмная материя": (
                "Космология",
                "Тёмная материя — гипотетическая форма материи, которая не излучает свет, но проявляет себя через гравитацию."
            ),
            "тёмная энергия": (
                "Космология",
                "Тёмная энергия — гипотетическая энергия, вызывающая ускоренное расширение Вселенной."
            ),
            "плоская земля": (
                "Астрофизика",
                "Земля не является плоской. Это научный факт, подтверждённый снимками из космоса и тысячами лет наблюдений."
            ),
        }
        print("[ASTRO] Агент Астрофизики активирован. Законы космоса загружены.")

    def evaluate(self, user_input: str) -> dict | None:
        lower_input = user_input.lower()
        
        # Особая проверка для "плоской земли"
        if "плоская земля" in lower_input or "земля плоская" in lower_input:
            return {
                "found": True,
                "field": "Астрофизика",
                "explanation": "Земля не является плоской. Это научный факт. Под действием собственной гравитации любое массивное тело стремится к форме сферы (гидростатическое равновесие)."
            }
        
        # Проверка на сферичность планет
        if "форма планеты" in lower_input or "форма земли" in lower_input:
            return {
                "found": True,
                "field": "Астрофизика",
                "explanation": "Все достаточно массивные тела под действием собственной гравитации принимают форму, близкую к сфере. Это универсальный закон физики."
            }
        
        for keyword, (field, explanation) in self.astro_laws.items():
            if keyword in lower_input:
                return {
                    "found": True,
                    "field": field,
                    "explanation": explanation
                }
        
        return None

    def get_warning(self, user_input: str) -> str | None:
        result = self.evaluate(user_input)
        if result:
            return (f"[ASTRO] АСТРОФИЗИЧЕСКАЯ СПРАВКА:\n"
                    f"Тема: {result['field']}\n"
                    f"Объяснение: {result['explanation']}")
        return None
    def verify(self, query: str, answer: str) -> dict:
        """Проверяет утверждения в ответе LLM."""
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
   
    agent = AstroAgent()
    
    print("Тест 1: Плоская Земля")
    result = agent.evaluate("Земля плоская?")
    if result:
        print(f"Результат: {result['explanation']}\n")
    
    print("Тест 2: Форма планеты")
    result = agent.evaluate("Какая форма у Земли?")
    if result:
        print(f"Результат: {result['explanation']}\n")
    
    print("Тест 3: Чёрная дыра")
    warning = agent.get_warning("Что такое чёрная дыра?")
    if warning:
        print(warning)