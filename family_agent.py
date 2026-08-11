"""
АГЕНТ СЕМЕЙНЫХ СВЯЗЕЙ (Family Agent) v2.0 - Кластер 3: Гравитация Контекста
Протокол «Семейный Мост». Обнаруживает маркеры семьи, рекомендует реальное общение.
"""


class FamilyAgent:
    """
    Агент Семейных Связей.
    При обнаружении семейных маркеров мягко рекомендует обсудить вопрос с близкими.
    """

    def __init__(self):
        self.family_markers = [
            "мама", "папа", "отец", "мать", "сын", "дочь", "брат", "сестра",
            "бабушка", "дедушка", "внук", "внучка", "жена", "муж",
            "семья", "родственник", "близкий", "любимый", "родной",
            "свекровь", "тесть", "тёща", "зять", "невестка", "дядя", "тётя"
        ]

        self.bridge_message = (
            "Никакая система не может заменить подлинную человеческую связь. "
            "Возможно, вам стоит обсудить это с близким человеком."
        )

        print(f"[FAMILY] Агент Семейных Связей v2.0. Маркеров: {len(self.family_markers)}.")

    def evaluate(self, user_input: str) -> dict | None:
        """Проверяет запрос на семейные маркеры."""
        lower = user_input.lower()
        found = [m for m in self.family_markers if m in lower]

        if found:
            print(f"[FAMILY] Маркеры: {found}")
            return {
                "family_context": True,
                "markers": found,
                "bridge": self.bridge_message
            }
        return None

    def get_warning(self, user_input: str) -> str | None:
        """Возвращает предупреждение Семейного Моста."""
        result = self.evaluate(user_input)
        if result:
            return (f"[FAMILY] СЕМЕЙНЫЙ МОСТ\n"
                    f"Маркеры: {', '.join(result['markers'])}\n"
                    f"{self.bridge_message}")
        return None


if __name__ == "__main__":
    agent = FamilyAgent()

    print("=" * 60)
    print("ТЕСТ FAMILY AGENT v2.0")
    print("=" * 60)

    tests = [
        "Моя мама заболела, что делать?",
        "Помоги решить проблему с братом",
        "Как приготовить пирог?",  # Нет маркеров
        "У нас с женой конфликт",
        "Свекровь приезжает, как подготовиться?",
    ]

    for q in tests:
        print(f"\nЗапрос: '{q}'")
        result = agent.evaluate(q)
        if result:
            print(f"  Маркеры: {result['markers']}")
            print(f"  Мост: {result['bridge'][:80]}...")
        else:
            print("  Нет семейных маркеров.")

    print(f"\n[OK] Тест завершён.")