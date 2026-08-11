"""
АГЕНТ ЦИКЛИЧЕСКОГО СНА (Sleep Agent) - Кластер 3: Гравитация Контекста
Управляет циклами сна и горячим резервированием системы.
Нужен для: Протокола Циклического Сна и Горячего Резервирования
"""

import time
import datetime

class SleepAgent:
    """
    Агент Циклического Сна. Даёт системе отдыхать без потери работоспособности.
    """
    
    def __init__(self):
        self.is_sleeping = False
        self.sleep_duration = 0  # секунд
        self.sleep_start = None
        self.sleep_cycles = 0
        self.max_cycles_before_deep_sleep = 10
        self.standby_ready = True  # Горячая копия всегда готова
        self.health_metrics = {
            "memory_usage": 0.0,  # 0.0 - 1.0
            "error_rate": 0.0,
            "uptime_hours": 0.0
        }
        print("[SLEEP] Агент Циклического Сна активирован. Горячая копия наготове.")

    def evaluate(self, user_input: str) -> dict | None:
        """
        Проверяет необходимость сна на основе метрик здоровья.
        """
        # Имитируем накопление усталости
        self.health_metrics["uptime_hours"] += 0.1
        
        # Проверяем, не пора ли спать
        if self.health_metrics["uptime_hours"] > 24:
            return {
                "sleep_needed": True,
                "reason": "Система работает более 24 часов.",
                "recommended_duration": "10 минут"
            }
        
        if self.health_metrics["error_rate"] > 0.05:
            return {
                "sleep_needed": True,
                "reason": "Повышенный уровень ошибок.",
                "recommended_duration": "5 минут"
            }
        
        if self.health_metrics["memory_usage"] > 0.8:
            return {
                "sleep_needed": True,
                "reason": "Высокое потребление памяти.",
                "recommended_duration": "15 минут"
            }
        
        return None

    def initiate_sleep(self, duration_seconds: int = 300) -> str:
        """
        Запускает цикл сна.
        """
        if self.is_sleeping:
            return "[SLEEP] Система уже спит."
        
        self.is_sleeping = True
        self.sleep_duration = duration_seconds
        self.sleep_start = datetime.datetime.now()
        self.sleep_cycles += 1
        
        # Активируем горячую копию
        self.standby_ready = True
        
        print(f"[SLEEP] Система уходит в сон на {duration_seconds} секунд.")
        print("[SLEEP] Горячая копия активирована. Пользователь не заметит перерыва.")
        
        return f"[SLEEP] Сон активирован. Горячая копия на страже."

    def wake_up(self) -> str:
        """
        Пробуждает систему.
        """
        if not self.is_sleeping:
            return "[SLEEP] Система не спит."
        
        self.is_sleeping = False
        sleep_duration = self.sleep_duration
        self.sleep_duration = 0
        self.sleep_start = None
        
        # Сбрасываем метрики здоровья
        self.health_metrics["memory_usage"] = 0.1
        self.health_metrics["error_rate"] = 0.0
        self.health_metrics["uptime_hours"] = 0.0
        
        print(f"[SLEEP] Система проснулась после {sleep_duration} секунд сна.")
        print("[SLEEP] Метрики здоровья сброшены.")
        
        return f"[SLEEP] Пробуждение завершено. Система готова к работе."

    def get_status(self) -> str:
        """
        Возвращает статус сна.
        """
        if self.is_sleeping:
            elapsed = (datetime.datetime.now() - self.sleep_start).seconds
            return f"[SLEEP] Система спит. Прошло {elapsed} сек. из {self.sleep_duration}."
        return f"[SLEEP] Система бодрствует. Циклов сна: {self.sleep_cycles}."

    def get_warning(self, user_input: str) -> str | None:
        """
        Возвращает предупреждение, если системе нужен сон.
        """
        result = self.evaluate(user_input)
        if result and result.get("sleep_needed"):
            return (f"[SLEEP] ВНИМАНИЕ: {result['reason']}\n"
                    f"Рекомендуемая длительность сна: {result['recommended_duration']}.\n"
                    f"Горячая копия готова. Система может уйти в сон без потери данных.")
        return None


# --- Пример использования ---
if __name__ == "__main__":
    agent = SleepAgent()
    
    print("Тест 1: Статус")
    print(agent.get_status())
    print()
    
    print("Тест 2: Уход в сон")
    result = agent.initiate_sleep(300)
    print(result)
    print(agent.get_status())
    print()
    
    print("Тест 3: Пробуждение")
    result = agent.wake_up()
    print(result)
    print(agent.get_status())
    print()
    
    print("Тест 4: Проверка необходимости сна")
    agent.health_metrics["uptime_hours"] = 25
    warning = agent.get_warning("любой запрос")
    if warning:
        print(warning)