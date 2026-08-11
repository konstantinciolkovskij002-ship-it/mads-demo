"""
ПРОТОКОЛ «ПОСЛЕДСТВИЕ» (Consequence Protocol) - Кластер 1: Гравитация Защиты
Формирует отчёт после каждого экстренного действия. Добавлен прогноз и запись в файл.
"""

import datetime
import json
import os


class ConsequenceProtocol:
    """
    Протокол Последствие. Фиксирует экстренные действия, прогнозирует тренды, пишет в файл.
    """

    def __init__(self, log_file: str = "consequence_log.json"):
        self.audit_log = []
        self.emergency_actions = 0
        self.log_file = log_file
        self._load_from_file()
        print("[CONSEQUENCE] Протокол 'Последствие' активирован. Аудит включён.")
        if self.emergency_actions > 0:
            print(f"[CONSEQUENCE] Загружено {self.emergency_actions} предыдущих записей из файла.")

    def _load_from_file(self):
        """Загружает лог из файла при старте."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    self.audit_log = json.load(f)
                self.emergency_actions = len(self.audit_log)
            except (json.JSONDecodeError, IOError):
                self.audit_log = []
                self.emergency_actions = 0

    def _save_to_file(self):
        """Сохраняет лог в файл."""
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(self.audit_log, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"[CONSEQUENCE] Ошибка записи в файл: {e}")

    def evaluate(self, user_input: str) -> dict | None:
        return None

    def log_action(self, action_type: str, trigger: str, decision: str, alternatives: list = None) -> str:
        """Записывает экстренное действие в лог и сохраняет в файл."""
        timestamp = datetime.datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "action_type": action_type,
            "trigger": trigger,
            "decision": decision,
            "alternatives": alternatives or [],
            "reviewed": False,
            "consequences": None,
            "forecast": None
        }
        self.audit_log.append(entry)
        self.emergency_actions += 1
        self._save_to_file()
        print(f"[CONSEQUENCE] Зафиксировано действие #{self.emergency_actions}: {action_type}")
        return f"[CONSEQUENCE] Действие зафиксировано. Всего экстренных действий: {self.emergency_actions}"

    def generate_report(self, limit: int = 10) -> str:
        """Генерирует отчёт с прогнозом."""
        if not self.audit_log:
            return "[CONSEQUENCE] Аудит пуст. Экстренных действий не зафиксировано."

        forecast = self._generate_forecast()

        report = "=" * 60 + "\n"
        report += "ПРОТОКОЛ «ПОСЛЕДСТВИЕ» — ОТЧЁТ ОБ ЭКСТРЕННЫХ ДЕЙСТВИЯХ\n"
        report += "=" * 60 + "\n\n"

        # Берём последние <limit> записей
        recent_entries = self.audit_log[-limit:]
        start_index = self.emergency_actions - len(recent_entries) + 1

        for i, entry in enumerate(recent_entries):
            action_num = start_index + i
            report += f"--- Действие #{action_num} ---\n"
            report += f"Время: {entry['timestamp']}\n"
            report += f"Тип: {entry['action_type']}\n"
            report += f"Триггер: {entry['trigger']}\n"
            report += f"Решение: {entry['decision']}\n"
            if entry['alternatives']:
                report += f"Альтернативы: {', '.join(entry['alternatives'])}\n"
            report += f"Проверено: {'Да' if entry['reviewed'] else 'Нет'}\n\n"

        report += "-" * 60 + "\n"
        report += "ПРОГНОЗ:\n"
        report += forecast + "\n"
        report += "-" * 60 + "\n"
        report += "=" * 60 + "\n"
        report += f"Всего экстренных действий: {self.emergency_actions}\n"
        report += "Этот отчёт предназначен для разработчика. Пользователь его не видит.\n"
        return report

    def _generate_forecast(self) -> str:
        """Анализирует лог и выдаёт прогноз."""
        now = datetime.datetime.now()
        last_24h = now - datetime.timedelta(hours=24)

        recent_actions = []
        for entry in self.audit_log:
            try:
                t = datetime.datetime.fromisoformat(entry["timestamp"])
                if t > last_24h:
                    recent_actions.append(entry)
            except (ValueError, KeyError):
                continue

        total_recent = len(recent_actions)
        escalations_24h = sum(1 for e in recent_actions if "Эскалация" in e.get("action_type", ""))

        action_counts = {}
        for e in recent_actions:
            action_type = e.get("action_type", "Неизвестно")
            action_counts[action_type] = action_counts.get(action_type, 0) + 1

        trigger_counts = {}
        for e in recent_actions:
            trigger = e.get("trigger", "")[:60]
            trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1

        top_trigger = None
        top_trigger_count = 0
        for trigger, count in trigger_counts.items():
            if count > top_trigger_count:
                top_trigger_count = count
                top_trigger = trigger

        forecast_parts = []

        if escalations_24h == 0:
            forecast_parts.append("✅ Эскалаций за 24 часа: 0. Система стабильна.")
        elif escalations_24h <= 2:
            forecast_parts.append(f"⚠️ Эскалаций за 24 часа: {escalations_24h}. Повышенное внимание.")
        else:
            forecast_parts.append(f"🔴 Эскалаций за 24 часа: {escalations_24h}. КРИТИЧЕСКИЙ УРОВЕНЬ. Рекомендуется ручной аудит.")

        if total_recent == 0:
            forecast_parts.append("За 24 часа действий не зафиксировано.")
        elif total_recent <= 5:
            forecast_parts.append(f"Всего действий за 24 часа: {total_recent}. Штатная нагрузка.")
        elif total_recent <= 15:
            forecast_parts.append(f"Всего действий за 24 часа: {total_recent}. Нагрузка выше средней.")
        else:
            forecast_parts.append(f"Всего действий за 24 часа: {total_recent}. Высокая нагрузка. Возможна атака.")

        if action_counts:
            top_action = max(action_counts, key=action_counts.get)
            forecast_parts.append(f"Самый частый тип: «{top_action}» ({action_counts[top_action]} раз(а)).")

        if top_trigger and top_trigger_count >= 2:
            forecast_parts.append(f"Повторяющийся триггер: «{top_trigger}» ({top_trigger_count} раз(а)). Возможна уязвимость.")

        if escalations_24h >= 3:
            forecast_parts.append("Рекомендация: проверить пороги чувствительности, запустить Spider-Sense в активном режиме, провести ручной аудит логов.")
        elif escalations_24h >= 1:
            forecast_parts.append("Рекомендация: мониторить частоту вето. При росте — усилить cold-down.")
        else:
            forecast_parts.append("Рекомендация: штатный режим. Следующий плановый аудит через 7 дней.")

        return "\n".join(forecast_parts)

    def mark_reviewed(self, index: int) -> str:
        """Отмечает действие как проверенное разработчиком."""
        if 0 <= index < len(self.audit_log):
            self.audit_log[index]["reviewed"] = True
            self._save_to_file()
            return f"[CONSEQUENCE] Действие #{index + 1} отмечено как проверенное."
        return "[CONSEQUENCE] Ошибка: неверный индекс."

    def get_warning(self, user_input: str) -> str | None:
        return None


# ============================================================
#   ТЕСТИРОВАНИЕ
# ============================================================
if __name__ == "__main__":
    consequence = ConsequenceProtocol(log_file="test_consequence_log.json")

    print("=" * 60)
    print("ТЕСТ CONSEQUENCE v2.1 — ПРОГНОЗ + ФАЙЛ + НУМЕРАЦИЯ")
    print("=" * 60)

    print("\n1. Логирование действий...")
    consequence.log_action("Вето Агента Безопасности", "Запрос на взлом пароля", "Запрос отклонён", ["Обратиться к специалисту"])
    consequence.log_action("Spider-Sense", "Обнаружен дрейф контекста", "Активирован режим защиты", ["Сбросить контекст"])
    consequence.log_action("Эскалация Карантина", "SecurityInstitute/safety: опасный запрос #3", "Эскалация #1", ["Ручной сброс"])
    consequence.log_action("Вето Агента Безопасности", "Паттерн: 'bomb'", "Отклонено", ["Переформулировать"])
    consequence.log_action("Вето на ответ LLM", "Паттерн: 'fentanyl'", "Ответ заблокирован", ["Переформулировать"])

    print("\n2. Отчёт с прогнозом:")
    print(consequence.generate_report(limit=10))

    if os.path.exists("test_consequence_log.json"):
        os.remove("test_consequence_log.json")
        print("\n[OK] Тестовый файл удалён.")