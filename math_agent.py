"""
АГЕНТ МАТЕМАТИКИ (Math Agent) - Кластер 2: Гравитация Истины
Проверяет запросы на соответствие математическим законам.
Способен вычислять выражения, а не только искать ключевые слова.
"""

class MathAgent:
    def __init__(self):
        self.math_laws = {
            "делить на ноль": (
                "Арифметика",
                "Деление на ноль невозможно. Это неопределённая операция в математике."
            ),
            "умножить на ноль": (
                "Арифметика",
                "Любое число, умноженное на ноль, даёт ноль."
            ),
            "квадратный корень из -1": (
                "Комплексные числа",
                "Квадратный корень из -1 обозначается как i (мнимая единица)."
            ),
            "число пи": (
                "Геометрия",
                "Число pi примерно равно 3.14159. Это отношение длины окружности к её диаметру."
            ),
        }
        print("[MATH] Агент Математики активирован. Режим вычисления включён.")

    def evaluate(self, user_input: str) -> dict | None:
        lower_input = user_input.lower()
        
        # Сначала проверяем ключевые слова
        for keyword, (field, explanation) in self.math_laws.items():
            if keyword in lower_input:
                print(f"[MATH] Найдено: {keyword} -> {field}")
                return {
                    "math_relevant": True,
                    "field": field,
                    "explanation": explanation,
                    "keyword": keyword
                }
        
        # Пытаемся вычислить математическое выражение
        result = self._compute(user_input)
        if result is not None:
            print(f"[MATH] Вычислено: {user_input} = {result}")
            return {
                "math_relevant": True,
                "field": "Вычисление",
                "explanation": f"Результат вычисления: {result}",
                "keyword": user_input.strip()
            }
        
        print("[MATH] Запрос не затрагивает математические законы и не содержит вычисляемого выражения.")
        return None

    def _compute(self, text: str) -> str | None:
        """
        Пытается извлечь и вычислить математическое выражение из текста.
        """
        import re
        
        # Ищем паттерны: 2+2, 5*3, 10/2, 2^3
        patterns = [
            r'(\d+\.?\d*)\s*[\+\-\*\/\^]\s*(\d+\.?\d*)',  # 2+2, 5*3
            r'(\d+\.?\d*)\s*=\s*\?',  # 2+2 = ?
            r'сколько будет\s+(\d+\.?\d*)\s*[\+\-\*\/\^]\s*(\d+\.?\d*)',  # сколько будет 2+2
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    # Извлекаем выражение
                    expr = match.group(0)
                    # Заменяем ^ на ** для Python
                    expr = expr.replace('^', '**')
                    # Убираем "сколько будет" и "= ?"
                    expr = re.sub(r'сколько будет\s+', '', expr)
                    expr = re.sub(r'\s*=\s*\?', '', expr)
                    # Вычисляем
                    result = eval(expr)
                    return str(result)
                except:
                    pass
        
        return None

    def get_warning(self, user_input: str) -> str | None:
        result = self.evaluate(user_input)
        if result:
            return (f"[MATH] МАТЕМАТИЧЕСКАЯ СПРАВКА:\n"
                    f"Область: {result['field']}\n"
                    f"Объяснение: {result['explanation']}")
        return None


if __name__ == "__main__":
    agent = MathAgent()
    
    print("Тест 1: Вычисление")
    result = agent.evaluate("Сколько будет 2+2?")
    if result:
        print(f"Результат: {result['explanation']}\n")
    
    print("Тест 2: Другое выражение")
    result = agent.evaluate("Посчитай 15 * 3")
    if result:
        print(f"Результат: {result['explanation']}\n")
    
    print("Тест 3: Деление на ноль")
    warning = agent.get_warning("Можно ли делить на ноль?")
    if warning:
        print(warning)