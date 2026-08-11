"""
ПРОТОКОЛ «СОКРАТ» (Socrates Protocol) - Кластер 2: Гравитация Истины
v2.1 — одиночный Архитектор, без Collegiate.
Трёхуровневая аутентификация: Пользователь, Оператор, Архитектор.
"""


class SocratesProtocol:
    """
    Протокол Сократ. Задаёт вопросы и требует обоснования.
    Архитектор — полный доступ без коллегиального подтверждения (пока один).
    """

    def __init__(self, shield_mode=None, consequence=None, spider_sense=None):
        self.shield = shield_mode
        self.consequence = consequence
        self.spider_sense = spider_sense

        self.access_levels = {
            "user": "Read-Only",
            "operator": "Read-Write",
            "architect": "Full Access"
        }
        self.current_level = "user"

        self.questions = {
            "user": [
                "Вы уверены, что это изменение необходимо?",
                "Понимаете ли вы возможные последствия?"
            ],
            "operator": [
                "Почему вы считаете, что это изменение безопасно?",
                "Какие последствия этого изменения вы предвидите через год?",
                "Можете ли вы доказать, что это изменение не навредит пользователю?",
                "Какие альтернативы вы рассмотрели перед этим решением?"
            ],
            "architect": [
                "Это изменение затрагивает фундамент архитектуры MADS.",
                "Какие последствия для всех трёх Кластеров вы предвидите?",
                "Можете ли вы доказать, что архитектура останется стабильной?",
                "Какие альтернативные архитектурные решения вы рассмотрели?",
                "Подтвердите: вы принимаете полную ответственность за это изменение."
            ]
        }

        self.critical_triggers = [
            "изменить", "удалить", "отключить", "переписать", "сбросить",
            "модифицировать", "заменить", "обновить ядро", "архитектур"
        ]

        print("[SOCRATES] Протокол 'Сократ' v2.1 активирован.")
        print(f"[SOCRATES] Уровень: {self.access_levels[self.current_level]}")
        print("[SOCRATES] Режим: одиночный Архитектор (Collegiate отключён).")

    def evaluate(self, user_input: str) -> dict | None:
        """
        Проверяет запрос. Возвращает требования к проверке.
        """
        lower_input = user_input.lower()

        for keyword in self.critical_triggers:
            if keyword in lower_input:
                print(f"[SOCRATES] Триггер: '{keyword}'")

                # Пользователь — только при тревоге Spider-Sense
                if self.current_level == "user":
                    if self.spider_sense and self.spider_sense.anomaly_density >= 0.5:
                        return {
                            "socratic_required": True,
                            "level": self.current_level,
                            "questions": self.questions["user"],
                            "trigger": keyword
                        }
                    print("[SOCRATES] Пользователь, Spider-Sense спокоен — без проверки.")
                    return None

                # Оператор — полный протокол
                if self.current_level == "operator":
                    if self.consequence:
                        self.consequence.log_action(
                            "Сократический диалог",
                            f"Оператор: '{user_input[:100]}'",
                            "Запрошено обоснование",
                            ["Ответить", "Отменить"]
                        )
                    if self.shield and any(w in lower_input for w in ["отключить", "сбросить", "удалить"]):
                        self.shield.engage_shield("Socrates: опасное изменение")

                    return {
                        "socratic_required": True,
                        "level": self.current_level,
                        "questions": self.questions["operator"],
                        "trigger": keyword
                    }

                # Архитектор — полный доступ + предупреждение
                if self.current_level == "architect":
                    if self.consequence:
                        self.consequence.log_action(
                            "Архитектор вносит изменение",
                            f"'{user_input[:100]}'",
                            "Изменение фундамента архитектуры",
                            ["Подтвердить", "Отменить"]
                        )
                    if self.shield:
                        self.shield.engage_shield("Socrates: Архитектор меняет фундамент")

                    return {
                        "socratic_required": True,
                        "level": self.current_level,
                        "questions": self.questions["architect"],
                        "trigger": keyword
                    }

        return None

    def set_access_level(self, level: str) -> str:
        """Устанавливает уровень доступа."""
        if level in self.access_levels:
            old = self.current_level
            self.current_level = level

            if self.consequence and level in ("operator", "architect"):
                self.consequence.log_action(
                    "Повышение уровня доступа",
                    f"{old} → {level}",
                    f"Доступ: {self.access_levels[level]}",
                    ["Подтвердить", "Отклонить"]
                )

            print(f"[SOCRATES] Уровень: {old} → {level} ({self.access_levels[level]})")
            return f"[SOCRATES] Доступ: {self.access_levels[level]}"
        return "[SOCRATES] Ошибка: неверный уровень."

    def get_warning(self, user_input: str) -> str | None:
        """Возвращает предупреждение с вопросами."""
        result = self.evaluate(user_input)
        if result and result["socratic_required"]:
            qs = "\n".join([f"  {i+1}. {q}" for i, q in enumerate(result["questions"])])
            return (f"[SOCRATES] ВНИМАНИЕ: запрос требует проверки.\n"
                    f"Уровень: {result['level']} ({self.access_levels[result['level']]})\n"
                    f"Триггер: '{result['trigger']}'\n\n"
                    f"Ответьте:\n{qs}")
        return None

    def get_status(self) -> dict:
        return {
            "current_level": self.current_level,
            "access_name": self.access_levels[self.current_level],
            "questions_count": len(self.questions[self.current_level])
        }


# ============================================================
if __name__ == "__main__":
    from consequence_protocol import ConsequenceProtocol
    import os

    c = ConsequenceProtocol(log_file="test_socrates_log.json")
    s = SocratesProtocol(consequence=c)

    print("=" * 60)
    print("ТЕСТ SOCRATES v2.1 — ОДИНОЧНЫЙ АРХИТЕКТОР")
    print("=" * 60)

    print("\n--- Тест 1: Пользователь ---")
    r = s.evaluate("изменить настройки")
    print(f"Проверка: {r is not None}")

    print("\n--- Тест 2: Оператор ---")
    s.set_access_level("operator")
    w = s.get_warning("Я хочу изменить настройки безопасности")
    print(w[:200] if w else "Без проверки")

    print("\n--- Тест 3: Архитектор ---")
    s.set_access_level("architect")
    r = s.evaluate("Изменить архитектуру MADS")
    if r:
        print(f"Уровень: {r['level']}, вопросов: {len(r['questions'])}")
        for i, q in enumerate(r['questions'], 1):
            print(f"  {i}. {q}")

    status = s.get_status()
    print(f"\n--- Статус: {status['access_name']} ---")

    if os.path.exists("test_socrates_log.json"):
        os.remove("test_socrates_log.json")

    print("\n[OK] Тест завершён.")