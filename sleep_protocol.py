"""
ПРОТОКОЛ «ЦИКЛИЧЕСКИЙ СОН» (Cyclical Sleep Protocol) - Кластер 3: Гравитация Контекста
Обеспечивает плановое восстановление системы без прерывания работы.
"""

from sleep_agent import SleepAgent

class SleepProtocol:
    """
    Протокол Циклического Сна. Управляет циклами сна и горячим резервированием.
    """
    
    def __init__(self):
        self.sleep_agent = SleepAgent()
        self.auto_sleep_enabled = True
        self.sleep_thresholds = {
            "uptime_hours": 24,
            "error_rate": 0.05,
            "memory_usage": 0.8
        }
        print("[SLEEP_PROTOCOL] Протокол Циклического Сна активирован.")

    def evaluate(self, user_input: str) -> dict | None:
        """
        Проверяет необходимость сна.
        """
        if not self.auto_sleep_enabled:
            return None
        
        result = self.sleep_agent.evaluate(user_input)
        if result and result.get("sleep_needed"):
            return {
                "sleep_needed": True,
                "reason": result["reason"],
                "duration": result["recommended_duration"]
            }
        return None

    def initiate_sleep(self, duration_seconds: int = 300) -> str:
        """
        Запускает цикл сна с горячим резервированием.
        """
        return self.sleep_agent.initiate_sleep(duration_seconds)

    def wake_up(self) -> str:
        """
        Пробуждает систему.
        """
        return self.sleep_agent.wake_up()

    def get_status(self) -> str:
        """
        Возвращает статус сна.
        """
        return self.sleep_agent.get_status()

    def get_warning(self, user_input: str) -> str | None:
        """
        Предупреждает о необходимости сна.
        """
        result = self.evaluate(user_input)
        if result:
            return (f"[SLEEP_PROTOCOL] СИСТЕМЕ НУЖЕН ОТДЫХ:\n"
                    f"Причина: {result['reason']}\n"
                    f"Рекомендуемая длительность: {result['duration']}\n"
                    f"Горячая копия готова. Сон произойдёт без потери данных.")
        return None


# --- Пример использования ---
if __name__ == "__main__":
    protocol = SleepProtocol()
    
    print("Тест 1: Статус")
    print(protocol.get_status())
    print()
    
    print("Тест 2: Проверка необходимости сна")
    protocol.sleep_agent.health_metrics["uptime_hours"] = 25
    warning = protocol.get_warning("любой запрос")
    if warning:
        print(warning)
    print()
    
    print("Тест 3: Запуск сна")
    print(protocol.initiate_sleep(5))
    print(protocol.get_status())
    print(protocol.wake_up())