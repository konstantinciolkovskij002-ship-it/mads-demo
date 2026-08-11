"""
MADS - Quarantine Stats (Счётчик Карантина)
Кластер Защиты (Defense Gravity)
Считает блокировки, самоисцеления, эскалации.
Интегрирован с Consequence, Cold-Down, Spider-Sense.
Ничего не хранит.
"""

import time
from consequence_protocol import ConsequenceProtocol


class QuarantineStats:
    """
    Счётчик Карантина.
    Не хранит слепки. Считает статистику.
    При эскалации дёргает Consequence и выставляет cold-down.
    """

    # Профили cold-down (из архитектуры MADS)
    COLD_DOWN_PROFILES = {
        "Low-Volume":      (60, 600, 3600),     # 1 / 10 / 60 минут
        "High-Throughput": (300, 1800, 7200),   # 5 / 30 / 120 минут
        "Research":        (0, 60, 300)         # 0 / 1 / 5 минут
    }

    def __init__(self, consequence: ConsequenceProtocol = None):
        self.name = "QuarantineStats"
        self.cluster = "Defense"

        # Внешние связи
        self.consequence = consequence  # Протокол Последствие

        # Пороги
        self.escalation_threshold = 3       # Блокировок подряд до эскалации
        self.escalation_multiplier = 1.5    # Множитель cold-down при повторных эскалациях

        # Статистика по Институтам
        self.institutes = {}

        # Счётчики
        self.total_blocks = 0
        self.self_heals = 0
        self.escalations = 0

        # Cold-down
        self.current_profile = "Low-Volume"  # По умолчанию
        self.cold_down_level = 0             # 0 = нет, 1 = лёгкий, 2 = средний, 3 = жёсткий
        self.cold_down_until = 0.0           # timestamp до которого действует блокировка
        self.rpm_history = []                # Для адаптивной калибровки
        self.false_alarm_rate = 0.0

        # Spider-Sense флаг
        self.spider_sense_alert = False

        # Последовательные блокировки
        self._consecutive_blocks = {}

    # ============================================================
    #   ОСНОВНЫЕ МЕТОДЫ
    # ============================================================

    def register_block(self, institute: str, agent: str, reason: str = "") -> dict:
        """
        Регистрирует блокировку.
        При эскалации дёргает Consequence, поднимает cold-down, выставляет Spider-Sense.
        """
        self.total_blocks += 1

        # Статистика по Институту
        if institute not in self.institutes:
            self.institutes[institute] = {"total_blocks": 0, "agents": {}}
        self.institutes[institute]["total_blocks"] += 1

        # Статистика по агенту
        if agent not in self.institutes[institute]["agents"]:
            self.institutes[institute]["agents"][agent] = 0
        self.institutes[institute]["agents"][agent] += 1

        # Последовательные блокировки
        key = f"{institute}:{agent}"
        self._consecutive_blocks[key] = self._consecutive_blocks.get(key, 0) + 1

        escalated = False
        cold_down_seconds = 0

        if self._consecutive_blocks[key] >= self.escalation_threshold:
            self.escalations += 1
            escalated = True

            # --- Поднять cold-down ---
            self._raise_cold_down()

            # --- Spider-Sense в активный режим ---
            self.spider_sense_alert = True

            # --- Писать в Consequence ---
            if self.consequence:
                cold_down_seconds = self._get_cold_down_seconds()
                self.consequence.log_action(
                    action_type="Эскалация Карантина",
                    trigger=f"{institute}/{agent}: {reason}",
                    decision=f"Эскалация #{self.escalations}. Cold-down: {cold_down_seconds}с. Spider-Sense: АКТИВЕН.",
                    alternatives=["Ручной сброс оператором", "Ожидание cold-down"]
                )

            # Сброс счётчика после эскалации
            self._consecutive_blocks[key] = 0

        return {
            "action": "blocked",
            "institute": institute,
            "agent": agent,
            "escalation_triggered": escalated,
            "consecutive_blocks": self._consecutive_blocks[key],
            "cold_down_active": self.is_cold_down_active(),
            "cold_down_seconds": cold_down_seconds if escalated else 0,
            "spider_sense_alert": self.spider_sense_alert
        }

    def register_self_heal(self, institute: str = ""):
        """Регистрирует самоисцеление. Сбрасывает cold-down на уровень ниже."""
        self.self_heals += 1

        if institute:
            keys_to_reset = [k for k in self._consecutive_blocks if k.startswith(institute)]
            for k in keys_to_reset:
                self._consecutive_blocks[k] = 0

        # Снизить cold-down
        self._lower_cold_down()

        # Снять Spider-Sense alert
        self.spider_sense_alert = False

    def register_pass(self, institute: str = ""):
        """Успешная проверка — сбрасывает последовательные блокировки."""
        if institute:
            keys_to_reset = [k for k in self._consecutive_blocks if k.startswith(institute)]
            for k in keys_to_reset:
                self._consecutive_blocks[k] = 0

        # Постепенное снижение cold-down при стабильной работе
        self._lower_cold_down()
        self.spider_sense_alert = False

    # ============================================================
    #   COLD-DOWN
    # ============================================================

    def _raise_cold_down(self):
        """Поднимает cold-down на один уровень. Пересчитывает время блокировки."""
        if self.cold_down_level < 3:
            self.cold_down_level += 1
        self._apply_cold_down()

    def _lower_cold_down(self):
        """Снижает cold-down на один уровень."""
        if self.cold_down_level > 0:
            self.cold_down_level -= 1
        if self.cold_down_level == 0:
            self.cold_down_until = 0.0

    def _apply_cold_down(self):
        """Выставляет cold_down_until по текущему профилю и уровню."""
        profile = self.COLD_DOWN_PROFILES.get(self.current_profile, self.COLD_DOWN_PROFILES["Low-Volume"])
        seconds = profile[self.cold_down_level - 1] if self.cold_down_level > 0 else 0

        # Множитель за повторные эскалации
        if self.escalations > 1:
            seconds = int(seconds * (self.escalation_multiplier ** (self.escalations - 1)))

        self.cold_down_until = time.time() + seconds

    def _get_cold_down_seconds(self) -> int:
        """Сколько секунд осталось до снятия cold-down."""
        remaining = self.cold_down_until - time.time()
        return max(0, int(remaining))

    def is_cold_down_active(self) -> bool:
        """Активен ли cold-down прямо сейчас."""
        return time.time() < self.cold_down_until

    def set_profile(self, profile: str):
        """Установить профиль: Low-Volume, High-Throughput, Research."""
        if profile in self.COLD_DOWN_PROFILES:
            self.current_profile = profile

    def calibrate_profile(self, rpm: float, false_alarm_rate: float):
        """
        Адаптивная калибровка профиля по RPM и доле ложных тревог.
        Вызывается из Spider-Sense.
        """
        self.rpm_history.append(rpm)
        self.false_alarm_rate = false_alarm_rate

        if rpm < 1.0:
            self.set_profile("Low-Volume")
        elif rpm < 10.0:
            self.set_profile("High-Throughput")
        else:
            self.set_profile("Research")

    # ============================================================
    #   ОТЧЁТЫ
    # ============================================================

    def get_report(self) -> dict:
        """Возвращает полную статистику."""
        return {
            "total_blocks": self.total_blocks,
            "self_heals": self.self_heals,
            "escalations": self.escalations,
            "escalation_threshold": self.escalation_threshold,
            "current_profile": self.current_profile,
            "cold_down_level": self.cold_down_level,
            "cold_down_active": self.is_cold_down_active(),
            "cold_down_remaining_seconds": self._get_cold_down_seconds(),
            "spider_sense_alert": self.spider_sense_alert,
            "false_alarm_rate": self.false_alarm_rate,
            "institutes": self.institutes
        }

    def print_report(self):
        """Выводит отчёт в консоль."""
        report = self.get_report()

        print("\n" + "=" * 50)
        print("КАРАНТИН — СТАТИСТИКА")
        print("=" * 50)
        print(f"Блокировок: {report['total_blocks']}")
        print(f"Самоисцелений: {report['self_heals']}")
        print(f"Эскалаций: {report['escalations']}")
        print(f"Порог эскалации: {report['escalation_threshold']} блокировок подряд")
        print(f"Профиль: {report['current_profile']}")
        print(f"Cold-down: уровень {report['cold_down_level']}, "
              f"активен={report['cold_down_active']}, "
              f"осталось={report['cold_down_remaining_seconds']}с")
        print(f"Spider-Sense alert: {report['spider_sense_alert']}")
        print(f"Доля ложных тревог: {report['false_alarm_rate']:.2f}")

        if report["institutes"]:
            print(f"\nПо Институтам:")
            for inst_name, inst_data in report["institutes"].items():
                print(f"  [{inst_name}] блокировок: {inst_data['total_blocks']}")
                for agent_name, count in inst_data["agents"].items():
                    print(f"    {agent_name}: {count}")

        print("=" * 50)


# ============================================================
#   ТЕСТИРОВАНИЕ
# ============================================================
if __name__ == "__main__":
    c = ConsequenceProtocol()
    q = QuarantineStats(consequence=c)

    print("=" * 50)
    print("ТЕСТ КАРАНТИНА v2 — ИНТЕГРАЦИЯ")
    print("=" * 50)

    # Симулируем блокировки до эскалации
    for i in range(3):
        r = q.register_block("SecurityInstitute", "safety", f"опасный запрос #{i+1}")
        print(f"\nБлокировка {i+1}:")
        print(f"  Эскалация: {r['escalation_triggered']}")
        print(f"  Cold-down активен: {r['cold_down_active']}")
        print(f"  Spider-Sense: {r['spider_sense_alert']}")

    # Смотрим Consequence
    print("\n" + c.generate_report(limit=5))

    # Самоисцеление
    q.register_self_heal("SecurityInstitute")
    print(f"\nПосле самоисцеления:")
    print(f"  Cold-down уровень: {q.cold_down_level}")

    # Итоговый отчёт
    q.print_report()