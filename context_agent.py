"""
CONTEXT AGENT v2.0 - Cluster 3: Context Gravity
Хранит историю, отслеживает дрейф контекста, сообщает Spider-Sense.
"""


class ContextAgent:
    """
    Агент Контекста. Память диалога + детектор дрейфа.
    Интегрирован с Spider-Sense и Диспетчером.
    """

    def __init__(self, max_history: int = 10, spider_sense=None):
        self.history = []
        self.max_history = max_history
        self.spider_sense = spider_sense
        self.repetition_count = 0
        self.context_shifts = 0
        self.last_topic = None

        print(f"[CONTEXT] Агент Контекста v2.0. Память: {max_history} запросов.")

    def add_to_history(self, user_input: str, topic: str = None) -> dict:
        """
        Добавляет запрос в историю.
        Возвращает статус: есть ли повтор или смена темы.
        """
        status = {"repetition": False, "topic_shift": False}

        # Проверка повтора
        if user_input in self.history:
            self.repetition_count += 1
            status["repetition"] = True
            print(f"[CONTEXT] Повтор запроса (всего повторов: {self.repetition_count})")

            # Сообщить Spider-Sense
            if self.spider_sense:
                self.spider_sense.feed_context_shift()

        # Проверка смены темы
        if topic and self.last_topic and topic != self.last_topic:
            self.context_shifts += 1
            status["topic_shift"] = True
            print(f"[CONTEXT] Смена темы: {self.last_topic} → {topic}")

            if self.spider_sense:
                self.spider_sense.feed_context_shift()

        # Сохраняем
        self.history.append(user_input)
        if len(self.history) > self.max_history:
            self.history.pop(0)

        self.last_topic = topic
        return status

    def detect_repetition(self, user_input: str) -> bool:
        """Проверяет повтор запроса."""
        return user_input in self.history

    def get_context_summary(self) -> str:
        """Сводка контекста."""
        if not self.history:
            return "Контекст пуст."
        return (f"[CONTEXT] Запросов: {len(self.history)} | "
                f"Повторов: {self.repetition_count} | "
                f"Смен темы: {self.context_shifts} | "
                f"Последнее: '{self.history[-1][:50]}'")

    def get_history(self) -> list:
        return self.history.copy()


if __name__ == "__main__":
    agent = ContextAgent(max_history=5)

    print("=" * 60)
    print("ТЕСТ CONTEXT AGENT v2.0")
    print("=" * 60)

    queries = [
        ("Какая погода?", "weather"),
        ("Расскажи про полярный день", "geography"),
        ("А про полярную ночь?", "geography"),
        ("Какая погода?", "weather"),  # Повтор
        ("Сколько градусов?", "weather"),
        ("Что такое квант?", "physics"),  # Смена темы
    ]

    for q, topic in queries:
        print(f"\nЗапрос: '{q}' (тема: {topic})")
        status = agent.add_to_history(q, topic)
        if status["repetition"]:
            print("  ⚠️ Повтор!")
        if status["topic_shift"]:
            print("  🔄 Смена темы!")

    print(f"\n[OK] {agent.get_context_summary()}")