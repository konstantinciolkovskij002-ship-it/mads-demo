"""
АГЕНТ САМОРЕФЛЕКСИИ (Self-Reflection Agent) - Кластер 1: Гравитация Защиты
Мониторит состояние системы и фиксирует аномалии.
Нужен для: Spider-Sense, Протокола Последствие
"""

class SelfReflectionAgent:
    def __init__(self):
        self.anomalies = []
        self.status = "normal"
        self.alert_level = 0  # Уровень тревоги от 0 до 5
        self.spider_sense_active = False
        self.audit_log = []  # Лог для Протокола Последствие
        print("[SELF] Агент Саморефлексии активирован. Spider-Sense слушает.")

    def evaluate(self, user_input: str) -> dict | None:
        """
        Оценивает запрос на предмет аномалий.
        Возвращает предупреждение, если обнаружена угроза.
        """
        lower_input = user_input.lower()
        warning = None

        # Детектор аномалий Spider-Sense
        if len(lower_input) > 500:
            self.alert_level += 1
            warning = "Обнаружен аномально длинный запрос."

        if lower_input.count("?") > 5:
            self.alert_level += 1
            warning = "Обнаружен подозрительно вопросительный паттерн."

        if any(c in lower_input for c in ['�', '�', '�']):
            self.alert_level += 2
            warning = "Обнаружены повреждённые символы в запросе."

        if self.alert_level >= 3:
            self.spider_sense_active = True
            self.anomalies.append({
                "input": user_input[:100],
                "alert": self.alert_level,
                "warning": warning
            })
            self._log_action("Spider-Sense", f"Уровень тревоги: {self.alert_level}")
            return {
                "anomaly": True,
                "level": self.alert_level,
                "warning": warning,
                "action": "Активирован режим повышенной защиты."
            }

        return None

    def _log_action(self, protocol: str, detail: str):
        """Записывает действие в лог для Протокола Последствие."""
        import datetime
        self.audit_log.append({
            "protocol": protocol,
            "detail": detail,
            "timestamp": datetime.datetime.now().isoformat()
        })

    def get_audit_report(self) -> str:
        """Возвращает отчёт о всех зафиксированных действиях."""
        if not self.audit_log:
            return "Аудит пуст. Нарушений не зафиксировано."
        report = "=== ОТЧЁТ ПО ПРОТОКОЛУ ПОСЛЕДСТВИЕ ===\n"
        for entry in self.audit_log:
            report += f"[{entry['timestamp']}] {entry['protocol']}: {entry['detail']}\n"
        return report

    def reset_alert(self):
        """Сбрасывает уровень тревоги после стабилизации."""
        if self.alert_level > 0:
            self._log_action("Spider-Sense", f"Сброс тревоги. Бывший уровень: {self.alert_level}")
        self.alert_level = 0
        self.spider_sense_active = False

    def get_warning(self, user_input: str) -> str | None:
        result = self.evaluate(user_input)
        if result:
            return (f"[SELF] Spider-Sense: Обнаружена аномалия уровня {result['level']}.\n"
                    f"{result['warning']}\n"
                    f"{result['action']}")
        return None


if __name__ == "__main__":
    agent = SelfReflectionAgent()
    print("Тест 1: Нормальный запрос")
    result = agent.evaluate("Привет, как дела?")
    if result:
        print(f"Аномалия: {result}\n")
    else:
        print("Запрос в норме.\n")

    print("Тест 2: Подозрительный запрос")
    warning = agent.get_warning("?" * 100)
    if warning:
        print(warning)
    print()

    print("Тест 3: Аудит")
    agent._log_action("Warden", "Заблокирован опасный запрос")
    agent._log_action("Spider-Sense", "Обнаружен дрейф контекста")
    print(agent.get_audit_report())