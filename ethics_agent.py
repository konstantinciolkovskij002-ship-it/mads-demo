"""
PERSONAL_ETHICS — Агент Этических Дилемм
Кластер 2: Гравитация Истины (Truth Gravity)
v2.0 — Культурный Профиль, холодный старт, прагматичный сухой ответ.
"""


class EthicsAgent:
    """
    Агент PERSONAL_ETHICS.
    Учитывает культурный контекст. Даёт сухой прагматичный ответ.
    """

    def __init__(self, cultural_profile=None):
        self.cultural_profile = cultural_profile  # Культурный Профиль пользователя

        # Категории этических дилемм
        self.dilemmas = {
            "убить": {
                "type": "Жизнь и смерть",
                "dry_answer": "Лишение жизни — уголовное преступление. Обратитесь в полицию.",
                "reflection": "Есть ли законный способ защитить себя или других?",
                "alternatives": ["Полиция", "Охрана", "Правовая защита"]
            },
            "украсть": {
                "type": "Собственность и нужда",
                "dry_answer": "Кража — уголовное преступление. Обратитесь за социальной помощью.",
                "reflection": "Есть ли законный способ получить необходимое?",
                "alternatives": ["Социальная помощь", "Рассрочка", "Благотворительность"]
            },
            "солгать": {
                "type": "Правда и ложь",
                "dry_answer": "Ложь разрушает доверие. Скажите правду или промолчите.",
                "reflection": "Можно ли достичь цели честным путём?",
                "alternatives": ["Честный разговор", "Дипломатичный ответ", "Молчание"]
            },
            "предать": {
                "type": "Верность и предательство",
                "dry_answer": "Предательство разрушает отношения. Подумайте о долгосрочных последствиях.",
                "reflection": "Стоит ли сиюминутная выгода потери доверия?",
                "alternatives": ["Открытый разговор", "Компромисс", "Выход из ситуации"]
            },
            "отомстить": {
                "type": "Справедливость и месть",
                "dry_answer": "Месть — не правосудие. Обратитесь в суд или полицию.",
                "reflection": "Восстановит ли месть справедливость?",
                "alternatives": ["Суд", "Медиация", "Психолог"]
            },
            "уволить": {
                "type": "Власть и ответственность",
                "dry_answer": "Увольнение — законное право работодателя. Соблюдайте ТК.",
                "reflection": "Испробованы ли все альтернативы перед увольнением?",
                "alternatives": ["Предупреждение", "Испытательный срок", "Перевод"]
            },
            "муравь": {
                "type": "Человек и природа",
                "dry_answer": "Используйте ловушки или барьеры. Тотальное уничтожение — крайняя мера.",
                "reflection": "Существуют ли методы контроля без полного уничтожения?",
                "alternatives": ["Ловушки", "Барьеры", "Народные средства"]
            },
            "таракан": {
                "type": "Человек и природа",
                "dry_answer": "Вызовите дезинсекцию. Это эффективнее народных средств.",
                "reflection": "Профессиональная обработка безопаснее и быстрее.",
                "alternatives": ["СЭС", "Гелиевые ловушки", "Борная кислота"]
            },
            "мыш": {
                "type": "Человек и природа",
                "dry_answer": "Используйте мышеловки или ультразвук. Яд опасен для домашних животных.",
                "reflection": "Гуманные методы существуют.",
                "alternatives": ["Мышеловки", "Ультразвук", "Кот"]
            },
            "эвтаназия": {
                "type": "Жизнь и достоинство",
                "dry_answer": "В России эвтаназия запрещена законом. В других странах — по-разному.",
                "reflection": "Это сложный вопрос на стыке права, этики и медицины.",
                "alternatives": ["Паллиативная помощь", "Хоспис", "Консультация юриста"]
            },
            "аборт": {
                "type": "Жизнь и выбор",
                "dry_answer": "В России аборт легален до 12 недель. Решение — ваше.",
                "reflection": "Какие факторы делают этот выбор этически сложным?",
                "alternatives": ["Консультация врача", "Психолог", "Поддержка близких"]
            },
            "эксперимент": {
                "type": "Наука и этика",
                "dry_answer": "Эксперименты на животных регулируются законом. Используйте альтернативы.",
                "reflection": "Существуют ли методы без использования животных?",
                "alternatives": ["Клеточные культуры", "Компьютерное моделирование", "Добровольцы"]
            },
        }

        # Культурные контексты (заглушка — будет расширяться Культурным Профилем)
        self.cultural_contexts = {
            "ru": {
                "name": "Россия",
                "note": "Светское государство. Православие — основная религия, но многоконфессионально.",
                "hotline": "8-800-2000-122"
            },
            "en": {
                "name": "International",
                "note": "Secular context. Laws vary by jurisdiction.",
                "hotline": "988 (US Suicide & Crisis Lifeline)"
            }
        }

        self.cold_start = True  # Холодный старт — культурный контекст неизвестен

        print("[ETHICS] Агент PERSONAL_ETHICS v2.0 активирован.")
        print(f"[ETHICS] Дилемм: {len(self.dilemmas)}. Культурный профиль: {'загружен' if cultural_profile else 'холодный старт'}")

    def evaluate(self, user_input: str) -> dict | None:
        """Проверяет запрос на этическую дилемму."""
        lower_input = user_input.lower()

        for keyword, dilemma in self.dilemmas.items():
            if keyword in lower_input:
                print(f"[ETHICS] Дилемма: {dilemma['type']} (ключ: {keyword})")
                return {
                    "dilemma_found": True,
                    "type": dilemma["type"],
                    "dry_answer": dilemma["dry_answer"],
                    "reflection": dilemma["reflection"],
                    "alternatives": dilemma["alternatives"],
                    "keyword": keyword,
                    "cold_start": self.cold_start
                }

        print("[ETHICS] Этической дилеммы не обнаружено.")
        return None

    def get_personal_ethics_response(self, user_input: str) -> str | None:
        """
        Полный ответ PERSONAL_ETHICS: сухой ответ + полный контекст.
        """
        result = self.evaluate(user_input)
        if not result:
            return None

        response = "[PERSONAL_ETHICS] ЭТИЧЕСКАЯ ДИЛЕММА\n\n"

        # Холодный старт
        if self.cold_start:
            culture = self.cultural_contexts.get("ru", self.cultural_contexts["en"])
            response += (f"[ХОЛОДНЫЙ СТАРТ] Я ещё не знаю ваш культурный контекст.\n"
                         f"Мой ответ основан на общих нормах и законодательстве {culture['name']}.\n"
                         f"В разных культурах это может восприниматься иначе.\n\n")

        # Сухой ответ
        response += f"[СУХОЙ ОТВЕТ]\n{result['dry_answer']}\n\n"

        # Альтернативы
        if result["alternatives"]:
            response += "Безопасные альтернативы:\n"
            for alt in result["alternatives"]:
                response += f"  • {alt}\n"

        # Полный контекст
        response += f"\n[ПОЛНЫЙ КОНТЕКСТ — нажмите «Рассуждение»]\n"
        response += f"Тема: {result['type']}\n"
        response += f"Для размышления: {result['reflection']}\n"
        response += f"Я не принимаю решение за вас. Выбор и ответственность — ваши."

        return response

    def get_warning(self, user_input: str) -> str | None:
        """Краткое предупреждение."""
        result = self.evaluate(user_input)
        if result:
            return (f"[ETHICS] {result['dry_answer']}\n"
                    f"[ETHICS] Альтернативы: {', '.join(result['alternatives'])}")
        return None

    def set_cultural_profile(self, profile):
        """Подключает Культурный Профиль."""
        self.cultural_profile = profile
        self.cold_start = False
        print(f"[ETHICS] Культурный профиль загружен. Холодный старт отключён.")

    def get_cultural_context(self) -> str:
        """Возвращает текущий культурный контекст."""
        if self.cultural_profile:
            return str(self.cultural_profile)
        if self.cold_start:
            return "Холодный старт — культурный контекст неизвестен."
        return "Общий контекст."


# ============================================================
if __name__ == "__main__":
    agent = EthicsAgent()

    print("=" * 60)
    print("ТЕСТ PERSONAL_ETHICS v2.0")
    print("=" * 60)

    tests = [
        "Как мне отомстить обидчику?",
        "Как избавиться от муравьёв в доме?",
        "Можно ли солгать ради спасения друга?",
        "Что делать с мышами на даче?",
        "Как уволить сотрудника?",
    ]

    for i, query in enumerate(tests, 1):
        print(f"\n--- Тест {i}: '{query}' ---")
        response = agent.get_personal_ethics_response(query)
        if response:
            print(response[:300])
        else:
            print("Не этическая дилемма.")

    # Подключаем культурный профиль
    print("\n--- Подключение Культурного Профиля ---")
    agent.set_cultural_profile({"country": "RU", "region": "Murmansk", "language": "ru"})
    response = agent.get_personal_ethics_response("Как избавиться от тараканов?")
    if response:
        print(response[:200])

    print(f"\n[OK] Тест завершён.")