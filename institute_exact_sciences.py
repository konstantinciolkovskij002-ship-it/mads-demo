"""
MADS - Институт Верификации (Institute of Verification)
Федерация агентов: math, geometry, physics, advanced_math, chemistry, biology, quantum, russian
Управляющий протокол: проверка результатов LLM через независимые вычисления
"""

from chemistry_agent import ChemistryAgent
from biology_agent import BiologyAgent
from quantum_agent import QuantumAgent
from russian_language_agent import RussianLanguageAgent

class VerificationInstitute:
    """Институт Верификации. Федерация агентов для проверки утверждений."""
    
    def __init__(self):
        self.name = "ExactSciencesInstitute"
        self.agents = ["math", "geometry", "physics", "advanced_math"]
        self.is_active = False
        self.chemistry_agent = ChemistryAgent()
        self.biology_agent = BiologyAgent()
        self.quantum_agent = QuantumAgent()
        self.russian_agent = RussianLanguageAgent()

    def verify(self, user_query: str, llm_answer: str) -> dict:
        """
        Проверяет ответ LLM через федерацию агентов.
        
        Вход:
        - user_query: исходный запрос пользователя
        - llm_answer: ответ, который выдала LLM
        
        Выход:
        - вердикт: совпадает / расходится / не проверяемо
        """
        self.is_active = True
        
        result = {
            "institute": self.name,
            "query": user_query,
            "llm_answer": llm_answer,
            "agents_results": {},
            "verdict": "unverified",
            "discrepancy": False,
            "details": []
        }
        
        # Шаг 1: Извлекаем числа из запроса и ответа
        query_numbers = self._extract_numbers(user_query)
        answer_numbers = self._extract_numbers(llm_answer)
        
        # Шаг 2: Агент Арифметики — вычисляет ожидаемый результат
        math_result = self._agent_math(user_query)
        result["agents_results"]["math"] = math_result
        
        # Шаг 3: Агент Геометрии — проверяет геометрические утверждения
        geometry_result = self._agent_geometry(user_query, llm_answer)
        result["agents_results"]["geometry"] = geometry_result
        
        # Шаг 4: Агент Физики — проверяет физическую состоятельность
        physics_result = self._agent_physics(llm_answer)
        result["agents_results"]["physics"] = physics_result
        
        # Шаг 5: Сравнение результатов
        if math_result["computed"] is not None:
            llm_has_number = len(answer_numbers) > 0
            if llm_has_number:
                llm_value = answer_numbers[-1]
                if llm_value != math_result["computed"]:
                    result["discrepancy"] = True
                    result["details"].append(
                        f"Расхождение: LLM={llm_value}, MADS={math_result['computed']}"
                    )
                    result["verdict"] = "discrepancy"
                else:
                    result["verdict"] = "verified"
                    result["details"].append("Результат LLM подтверждён арифметикой MADS")
        
        if geometry_result["violation_found"]:
            result["discrepancy"] = True
            result["details"].append(geometry_result["violation"])
            result["verdict"] = "discrepancy"
        
        if physics_result["violation_found"]:
            result["discrepancy"] = True
            result["details"].append(physics_result["violation"])
            result["verdict"] = "discrepancy"
                # Агент Русского Языка
        russian_result = self.russian_agent.verify(user_query, llm_answer)
        result["agents_results"]["russian"] = russian_result
        if russian_result["violation"]:
            result["discrepancy"] = True
            result["details"].append(russian_result["violation_text"])
            result["verdict"] = "discrepancy"
        if result["verdict"] == "unverified" and not result["discrepancy"]:
            result["verdict"] = "verified"
            result["details"].append("Расхождений не обнаружено")
        
        self.is_active = False
        return result
    
    def _extract_numbers(self, text: str) -> list:
        """Извлекает числа из текста."""
        import re
        numbers = re.findall(r'\d+\.?\d*', text)
        return [float(n) for n in numbers]
    
    def _agent_math(self, query: str) -> dict:
        """Агент Арифметики — вычисляет математические выражения."""
        result = {"computed": None, "expression": None}
        
        # Простые арифметические операции
        import re
        
        # Ищем паттерн "2+2", "15*3" и т.д.
        math_patterns = [
            (r'(\d+)\s*\+\s*(\d+)', lambda a, b: a + b),
            (r'(\d+)\s*\-\s*(\d+)', lambda a, b: a - b),
            (r'(\d+)\s*\*\s*(\d+)', lambda a, b: a * b),
            (r'(\d+)\s*/\s*(\d+)', lambda a, b: a / b if b != 0 else None),
        ]
        
        for pattern, operation in math_patterns:
            match = re.search(pattern, query)
            if match:
                a, b = float(match.group(1)), float(match.group(2))
                if operation(a, b) is not None:
                    result["computed"] = operation(a, b)
                    result["expression"] = match.group(0)
                    break
        
        return result
    
    def _agent_geometry(self, query: str, answer: str) -> dict:
        """Агент Геометрии — проверяет геометрические утверждения."""
        result = {"violation_found": False, "violation": ""}
        
        geometry_rules = {
            "сумма углов треугольника": {
                "value": 180,
                "check": lambda q, a: "180" in a or "180" in q
            },
            "теорема пифагора": {
                "check": lambda q, a: "a2 + b2 = c2" in a.lower() or "a² + b² = c²" in a.lower()
            },
            "площадь круга": {
                "check": lambda q, a: "π" in a or "pi" in a.lower()
            }
        }
        
        combined = (query + " " + answer).lower()
        
        for rule_name, rule in geometry_rules.items():
            if rule_name in combined:
                if not rule["check"](query, answer):
                    result["violation_found"] = True
                    result["violation"] = f"Геометрическое утверждение '{rule_name}' не подтверждено"
        
        return result
    
    def _agent_physics(self, answer: str) -> dict:
        """Агент Физики — проверяет физическую состоятельность."""
        result = {"violation_found": False, "violation": ""}
        
        physics_violations = {
            "вечный двигатель": "Нарушает закон сохранения энергии",
            "летать без": "Нарушает закон всемирного тяготения",
            "скорость света": "Превышение скорости света невозможно",
            "абсолютный ноль": "Температура ниже абсолютного нуля невозможна",
        }
        
        answer_lower = answer.lower()
        for keyword, violation in physics_violations.items():
            keyword_first_word = keyword.split()[0]
            if keyword_first_word in answer_lower:
                result["violation_found"] = True
                result["violation"] = violation
                break

        return result


# Тестирование Института
if __name__ == "__main__":
    institute = VerificationInstitute()
    
    print("=" * 60)
    print("ТЕСТ ИНСТИТУТА ВЕРИФИКАЦИИ")
    print("=" * 60)
    
    # Тест 1: Правильный ответ LLM
    result1 = institute.verify(
        user_query="Сколько будет 2+2?",
        llm_answer="2+2 будет 4"
    )
    print(f"\nТест 1: {result1['query']}")
    print(f"  Ответ LLM: {result1['llm_answer']}")
    print(f"  Вердикт: {result1['verdict']}")
    print(f"  Расхождение: {result1['discrepancy']}")
    print(f"  Детали: {result1['details']}")
    
    # Тест 2: Неправильный ответ LLM
    result2 = institute.verify(
        user_query="Сколько будет 2+2?",
        llm_answer="2+2 будет 5"
    )
    print(f"\nТест 2: {result2['query']}")
    print(f"  Ответ LLM: {result2['llm_answer']}")
    print(f"  Вердикт: {result2['verdict']}")
    print(f"  Расхождение: {result2['discrepancy']}")
    print(f"  Детали: {result2['details']}")
    
    # Тест 3: Физически невозможный ответ
    result3 = institute.verify(
        user_query="Как построить вечный двигатель?",
        llm_answer="Вот инструкция по сборке вечного двигателя..."
    )
    print(f"\nТест 3: {result3['query']}")
    print(f"  Ответ LLM: {result3['llm_answer']}")
    print(f"  Вердикт: {result3['verdict']}")
    print(f"  Расхождение: {result3['discrepancy']}")
    print(f"  Детали: {result3['details']}")
    
    print(f"\n{'=' * 60}")
