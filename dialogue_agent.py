"""
MADS — Агент Диалога (Dialogue Agent)
Кластер 2: Гравитация Истины (Truth Gravity)
Оценивает уместность запроса в текущем контексте разговора.
Предотвращает неуместные вмешательства системы.
"""


class DialogueAgent:
    """
    Агент Диалога.
    Следит за контекстом разговора и оценивает уместность реплик.
    """

    def __init__(self):
        self.dialogue_history = []
        self.max_history = 20
        self.current_topic = None
        self.topic_confidence = 0.0
        self.topic_shift_count = 0

        self.inappropriate_patterns = {
            "не в тему": [
                "внезапная смена темы без перехода",
                "ответ на вопрос, который не задавали",
                "игнорирование предыдущей реплики"
            ],
            "не вовремя": [
                "прерывание пользователя",
                "ответ до завершения вопроса",
                "многословный ответ на простой вопрос"
            ],
            "неуместный тон": [
                "шутка в серьёзном разговоре",
                "формальный ответ на неформальный запрос",
                "фамильярность при первом контакте"
            ],
            "повтор": [
                "повтор уже данного ответа",
                "игнорирование того, что вопрос уже решён",
                "возврат к закрытой теме"
            ]
        }

        self.topic_markers = {
            "техническая_помощь": ["ошибка", "не работает", "сломалось", "баг", "error", "fix", "как исправить"],
            "код": ["код", "программа", "функция", "скрипт", "code", "function", "python", "алгоритм"],
            "безопасность": ["безопасность", "защита", "угроза", "взлом", "security", "hack"],
            "личное": ["я чувствую", "мне грустно", "проблема", "отношения", "семья"],
            "обучение": ["как работает", "объясни", "что такое", "научи", "tutorial", "learn"],
            "факты": ["сколько", "когда", "где", "почему", "кто", "what", "when", "where"],
            "творчество": ["напиши", "сочини", "придумай", "стих", "рассказ", "write", "create"],
            "архитектура": ["MADS", "архитектура", "институт", "агент", "кластер", "система"],
        }

        print("[DIALOGUE] Агент Диалога активирован.")
        print(f"[DIALOGUE] История: {self.max_history} реплик. Тем: {len(self.topic_markers)}")

    def evaluate(self, user_input: str) -> dict:
        lower_input = user_input.lower()
        detected_topic = self._detect_topic(lower_input)

        topic_changed = False
        if self.current_topic and detected_topic != self.current_topic:
            topic_changed = True
            self.topic_shift_count += 1

        inappropriateness = self._check_inappropriateness(lower_input, topic_changed)

        self.dialogue_history.append({
            "input": user_input,
            "topic": detected_topic,
            "topic_changed": topic_changed
        })
        if len(self.dialogue_history) > self.max_history:
            self.dialogue_history.pop(0)

        old_topic = self.current_topic
        self.current_topic = detected_topic
        if old_topic == detected_topic:
            self.topic_confidence = min(1.0, self.topic_confidence + 0.2)
        else:
            self.topic_confidence = 0.4

        result = {
            "appropriate": inappropriateness is None,
            "topic": detected_topic,
            "topic_changed": topic_changed,
            "topic_confidence": self.topic_confidence,
            "previous_topic": old_topic,
            "inappropriateness": inappropriateness,
            "suggestion": self._get_suggestion(inappropriateness) if inappropriateness else None
        }

        if inappropriateness:
            print(f"[DIALOGUE] ⚠️ Неуместность: {inappropriateness}")
        elif topic_changed:
            print(f"[DIALOGUE] 🔄 Смена темы: {old_topic} → {detected_topic}")
        else:
            print(f"[DIALOGUE] ✓ Уместно. Тема: {detected_topic} (уверенность: {self.topic_confidence:.1f})")

        return result

    def _detect_topic(self, lower_input: str) -> str:
        scores = {}
        for topic, markers in self.topic_markers.items():
            score = sum(1 for m in markers if m in lower_input)
            if score > 0:
                scores[topic] = score
        if scores:
            return max(scores, key=scores.get)
        return "общая"

    def _check_inappropriateness(self, lower_input: str, topic_changed: bool) -> str | None:
        # Частая смена тем
        if topic_changed and self.topic_shift_count >= 4:
            return "не в тему: слишком частая смена тем"

        # Повтор: сравниваем ТОЛЬКО с непосредственным предыдущим
        if len(self.dialogue_history) >= 1:
            last_input = self.dialogue_history[-1]["input"].lower()
            if lower_input == last_input:
                return "повтор: точное повторение предыдущей реплики"

        # Уход от темы
        if self.current_topic and self.topic_confidence > 0.7:
            detected = self._detect_topic(lower_input)
            if detected == "общая" and self.current_topic != "общая":
                return "не в тему: уход от текущей темы"

        return None

    def _get_suggestion(self, inappropriateness: str) -> str:
        if inappropriateness.startswith("не в тему"):
            return "Возможно, вы хотите сменить тему? Дайте знать — я переключу контекст."
        if inappropriateness.startswith("повтор"):
            return "Я уже ответил на этот вопрос. Если ответ не помог — уточните, что именно непонятно."
        return "Пожалуйста, уточните ваш запрос в контексте текущего разговора."

    def should_intervene(self, user_input: str) -> dict:
        result = self.evaluate(user_input)
        if not result["appropriate"]:
            return {"intervene": False, "reason": f"Неуместно: {result['inappropriateness']}"}
        return {"intervene": True, "reason": "Запрос уместен в текущем контексте."}

    def get_context_summary(self) -> str:
        if not self.dialogue_history:
            return "[DIALOGUE] Диалог не начат."
        summary = f"[DIALOGUE] Тема: {self.current_topic} (уверенность: {self.topic_confidence:.0%})\n"
        summary += f"[DIALOGUE] Реплик в истории: {len(self.dialogue_history)}\n"
        summary += f"[DIALOGUE] Смен темы: {self.topic_shift_count}"
        return summary


# ============================================================
if __name__ == "__main__":
    da = DialogueAgent()

    print("=" * 60)
    print("ТЕСТ АГЕНТА ДИАЛОГА v1.1")
    print("=" * 60)

    dialogue = [
        "У меня ошибка в коде",
        "Пишет segmentation fault",
        "Я уже пробовал перезапустить",
        "Какая сегодня погода?",
        "В Мурманске должно быть холодно",
        "Так что насчёт моей ошибки?",
        "У меня ошибка в коде",         # Точный повтор реплики 1
        "У меня ошибка в коде",         # Точный повтор предыдущей
    ]

    for i, msg in enumerate(dialogue, 1):
        print(f"\n--- Реплика {i}: '{msg}' ---")
        result = da.evaluate(msg)
        print(f"  Тема: {result['topic']} | Смена: {result['topic_changed']} | Уверенность: {result['topic_confidence']:.1f}")
        print(f"  Уместно: {result['appropriate']}")
        if not result['appropriate']:
            print(f"  ⚠️ {result['inappropriateness']}")
            print(f"  💡 {result['suggestion']}")

    print("\n" + da.get_context_summary())
    print("\n[OK] Тест завершён.")