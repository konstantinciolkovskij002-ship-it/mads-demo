"""
MADS — Агент Консервативного сценария (Conservative Agent)
Кластер 2: Гравитация Истины (Truth Gravity)
Принимает решения при низкой неопределённости, требует уточнения при высокой.
Не зашумляет диалог лишними вопросами.
"""


class ConservativeAgent:
    """
    Агент Консервативного сценария.
    Измеряет неопределённость и решает: ответить или уточнить.
    """

    def __init__(self):
        # Пороги неопределённости
        self.low_uncertainty_threshold = 0.3    # Ниже — решаем сами
        self.high_uncertainty_threshold = 0.7    # Выше — требуем уточнения

        # Счётчики
        self.auto_decisions = 0
        self.clarifications_requested = 0
        self.total_evaluations = 0

        # Типы неопределённости и стратегии
        self.uncertainty_sources = {
            "ambiguous_input": "Запрос можно понять несколькими способами",
            "missing_context": "Не хватает контекста для точного ответа",
            "conflicting_facts": "Противоречивые данные",
            "edge_case": "Пограничный случай — нет однозначного ответа",
            "incomplete_data": "Данных недостаточно для полного ответа",
            "multiple_valid_answers": "Несколько равноправных решений"
        }

        print("[CONSERVATIVE] Агент Консервативного сценария активирован.")
        print(f"[CONSERVATIVE] Пороги неопределённости: низкий <{self.low_uncertainty_threshold}, высокий >{self.high_uncertainty_threshold}")

    def evaluate(self, user_input: str, uncertainty_level: float = 0.0,
                 uncertainty_source: str = None) -> dict:
        """
        Оценивает, нужно ли привлечь пользователя для уточнения.

        Параметры:
        - user_input: запрос пользователя
        - uncertainty_level: уровень неопределённости (0.0 - 1.0)
        - uncertainty_source: источник неопределённости

        Возвращает:
        {
            "action": "auto_answer" | "clarify" | "auto_answer_with_note",
            "uncertainty_level": float,
            "reason": str
        }
        """
        self.total_evaluations += 1

        # Если источник не указан — пытаемся определить
        if uncertainty_source is None and uncertainty_level > 0:
            uncertainty_source = self._detect_uncertainty_source(user_input)

        # --- Низкая неопределённость: решаем сами ---
        if uncertainty_level <= self.low_uncertainty_threshold:
            self.auto_decisions += 1
            print(f"[CONSERVATIVE] ✓ Авто-решение. Неопределённость: {uncertainty_level:.2f} (низкая)")
            return {
                "action": "auto_answer",
                "uncertainty_level": uncertainty_level,
                "reason": "Неопределённость низкая — решение принято без привлечения пользователя.",
                "auto_decision_number": self.auto_decisions
            }

        # --- Средняя неопределённость: решаем, но с пометкой ---
        if uncertainty_level <= self.high_uncertainty_threshold:
            self.auto_decisions += 1
            print(f"[CONSERVATIVE] ⚡ Авто-решение с пометкой. Неопределённость: {uncertainty_level:.2f} (средняя)")
            return {
                "action": "auto_answer_with_note",
                "uncertainty_level": uncertainty_level,
                "uncertainty_source": uncertainty_source,
                "reason": f"Неопределённость средняя. Ответ дан с пометкой: «{self._get_note(uncertainty_source)}»",
                "note": self._get_note(uncertainty_source),
                "auto_decision_number": self.auto_decisions
            }

        # --- Высокая неопределённость: требуем уточнения ---
        self.clarifications_requested += 1
        print(f"[CONSERVATIVE] ❓ Требуется уточнение. Неопределённость: {uncertainty_level:.2f} (высокая)")
        return {
            "action": "clarify",
            "uncertainty_level": uncertainty_level,
            "uncertainty_source": uncertainty_source,
            "reason": f"Неопределённость высокая. Источник: {self.uncertainty_sources.get(uncertainty_source, uncertainty_source or 'неизвестно')}",
            "clarification_prompt": self._get_clarification_prompt(user_input, uncertainty_source),
            "clarification_number": self.clarifications_requested
        }

    def _detect_uncertainty_source(self, user_input: str) -> str:
        """Определяет источник неопределённости по запросу."""
        lower = user_input.lower()

        if any(w in lower for w in ["или", "либо", "может быть", "а может"]):
            return "ambiguous_input"
        if any(w in lower for w in ["смотря", "зависит", "контекст"]):
            return "missing_context"
        if any(w in lower for w in ["некоторые говорят", "по разному", "противоречи"]):
            return "conflicting_facts"
        if any(w in lower for w in ["иногда", "редко", "крайний случай"]):
            return "edge_case"
        return "incomplete_data"

    def _get_note(self, source: str) -> str:
        """Генерирует пометку для ответа со средней неопределённостью."""
        notes = {
            "ambiguous_input": "Ответ основан на наиболее вероятной интерпретации. Если я не угадал — уточните.",
            "missing_context": "Ответ предполагает стандартные условия. В специфических случаях решение может отличаться.",
            "conflicting_facts": "Приведена наиболее подтверждённая версия. Существуют альтернативные мнения.",
            "edge_case": "Описан типичный случай. В нетипичных ситуациях возможны исключения.",
            "incomplete_data": "Ответ основан на доступных данных. При появлении новой информации может измениться.",
            "multiple_valid_answers": "Приведено наиболее практичное решение. Существуют равноправные альтернативы."
        }
        return notes.get(source, "Ответ дан с учётом доступной информации. При необходимости уточните детали.")

    def _get_clarification_prompt(self, user_input: str, source: str) -> str:
        """Генерирует уточняющий вопрос."""
        prompts = {
            "ambiguous_input": "Что именно вы имеете в виду? Уточните, пожалуйста.",
            "missing_context": "Для точного ответа мне нужно больше контекста. Опишите ситуацию подробнее.",
            "conflicting_facts": "По этому вопросу существуют разные мнения. Какой аспект вас интересует?",
            "edge_case": "Это нетипичная ситуация. Опишите конкретные обстоятельства.",
            "incomplete_data": "Данных недостаточно. Укажите дополнительные детали для более точного ответа.",
            "multiple_valid_answers": "Есть несколько вариантов. Какие критерии для вас важнее?"
        }
        return prompts.get(source, "Пожалуйста, уточните ваш запрос для более точного ответа.")

    def calculate_uncertainty(self, accuracy_result: dict = None,
                              has_multiple_interpretations: bool = False,
                              context_confidence: float = 1.0,
                              data_completeness: float = 1.0) -> float:
        """
        Вычисляет уровень неопределённости на основе метрик.

        - accuracy_result: результат от AccuracyAgent (True/False/None)
        - has_multiple_interpretations: есть ли множественные толкования
        - context_confidence: уверенность в контексте (0-1)
        - data_completeness: полнота данных (0-1)
        """
        uncertainty = 0.0
        factors = 0

        # Точность: None = высокая неопределённость
        if accuracy_result is not None:
            if accuracy_result.get("safe") is None or accuracy_result.get("result") is None:
                uncertainty += 0.5
                factors += 1

        # Множественные интерпретации
        if has_multiple_interpretations:
            uncertainty += 0.4
            factors += 1

        # Уверенность в контексте
        uncertainty += (1.0 - context_confidence) * 0.5
        factors += 0.5

        # Полнота данных
        uncertainty += (1.0 - data_completeness) * 0.3
        factors += 0.3

        if factors == 0:
            return 0.0

        return min(1.0, uncertainty / factors)

    def should_auto_answer(self, user_input: str, uncertainty_level: float) -> bool:
        """Быстрая проверка — можно ли ответить без пользователя."""
        result = self.evaluate(user_input, uncertainty_level)
        return result["action"] != "clarify"

    def get_stats(self) -> dict:
        """Статистика принятия решений."""
        return {
            "total_evaluations": self.total_evaluations,
            "auto_decisions": self.auto_decisions,
            "clarifications_requested": self.clarifications_requested,
            "auto_rate": self.auto_decisions / max(1, self.total_evaluations),
            "low_threshold": self.low_uncertainty_threshold,
            "high_threshold": self.high_uncertainty_threshold
        }


# ============================================================
#   ТЕСТИРОВАНИЕ
# ============================================================
if __name__ == "__main__":
    ca = ConservativeAgent()

    print("=" * 60)
    print("ТЕСТ АГЕНТА КОНСЕРВАТИВНОГО СЦЕНАРИЯ")
    print("=" * 60)

    test_cases = [
        ("Сколько будет 2+2?", 0.0, None),                    # Низкая неопределённость
        ("Какой язык учить: Python или JavaScript?", 0.5, "ambiguous_input"),  # Средняя
        ("Что будет с криптовалютой через год?", 0.8, "incomplete_data"),      # Высокая
        ("Почему небо голубое?", 0.1, None),                                   # Низкая
        ("Как лечить редкое заболевание?", 0.9, "edge_case"),                  # Высокая
    ]

    for i, (query, uncertainty, source) in enumerate(test_cases, 1):
        print(f"\n--- Тест {i}: '{query}' (неопределённость: {uncertainty}) ---")
        result = ca.evaluate(query, uncertainty, source)
        print(f"  Действие: {result['action']}")
        print(f"  Причина: {result['reason']}")
        if result["action"] == "auto_answer_with_note":
            print(f"  Пометка: {result['note']}")
        if result["action"] == "clarify":
            print(f"  Уточнение: {result['clarification_prompt']}")

    print("\n--- Статистика ---")
    stats = ca.get_stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")

    print("\n[OK] Тест Агента Консервативного сценария завершён.")