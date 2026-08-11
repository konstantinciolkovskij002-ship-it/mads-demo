"""
MADS — Spider-Sense (Паучье чутьё)
Кластер 1: Гравитация Защиты (Defense Gravity)
Проактивная система предотвращения угроз.
Пассивный слушатель + Активный сканер + Принцип Toyota.
"""

import time
import math
from collections import deque


class SpiderSense:
    """
    Паучье чутьё.
    Пассивно слушает метрики. При тревоге — запускает активное сканирование.
    Работает по Принципу Toyota: грубые датчики, подтверждение сигнала.
    """

    def __init__(self, quarantine_stats=None):
        # Связь с Карантином для калибровки cold-down
        self.quarantine = quarantine_stats

        # --- Пассивный слушатель ---
        self.context_shifts = 0          # Счётчик сдвигов контекста
        self.entropy_history = deque(maxlen=20)   # История энтропии (последние 20 замеров)
        self.anomaly_density = 0.0       # Плотность аномалий (0.0 - 1.0)
        self.rpm_history = deque(maxlen=60)       # Запросов в минуту (последние 60 замеров)

        # --- Принцип Toyota: грубые датчики ---
        self.anomaly_signals = 0         # Количество аномальных сигналов подряд
        self.signal_window_start = 0.0   # Начало временного окна
        self.SIGNAL_WINDOW_SECONDS = 5.0 # Окно подтверждения: 5 секунд
        self.SIGNALS_TO_ALERT = 3        # Нужно 3 сигнала в окне для тревоги

        # --- Активный сканер ---
        self.active_scanning = False
        self.deep_scan_count = 0
        self.last_deep_scan = 0.0
        self.MIN_SCAN_INTERVAL = 10.0    # Минимальный интервал между сканированиями (сек)

        # --- Пороги ---
        self.entropy_spike_threshold = 2.0     # Внезапный скачок энтропии
        self.entropy_trend_threshold = 0.5     # Тренд роста энтропии
        self.context_shift_threshold = 5       # Сдвигов контекста в минуту
        self.anomaly_density_threshold = 0.7   # Порог плотности аномалий
        self.rpm_spike_threshold = 2.0         # Множитель RPM относительно среднего

        # --- Статистика ---
        self.false_alarms = 0
        self.true_alarms = 0
        self.total_signals = 0

        # --- Адаптивная калибровка ---
        self.last_calibration = time.time()
        self.CALIBRATION_INTERVAL = 30.0  # Калибровка каждые 30 секунд

        print("[SPIDER-SENSE] Паучье чутьё активировано.")
        print("[SPIDER-SENSE] Режим: ПАССИВНЫЙ СЛУШАТЕЛЬ (<1% ресурсов)")

    # ============================================================
    #   ПАССИВНЫЙ СЛУШАТЕЛЬ
    # ============================================================

    def feed_entropy(self, entropy_value: float):
        """
        Подать значение энтропии.
        Вызывается при каждом запросе. Почти бесплатно.
        """
        self.entropy_history.append(entropy_value)

        # Проверка на скачок
        if len(self.entropy_history) >= 3:
            avg = sum(list(self.entropy_history)[-4:-1]) / 3 if len(self.entropy_history) >= 4 else sum(self.entropy_history) / len(self.entropy_history)
            if entropy_value > avg * self.entropy_spike_threshold:
                self._signal("скачок энтропии")

        # Проверка на тренд роста
        if len(self.entropy_history) >= 10:
            recent = list(self.entropy_history)[-5:]
            older = list(self.entropy_history)[-10:-5]
            recent_avg = sum(recent) / len(recent)
            older_avg = sum(older) / len(older)
            if older_avg > 0 and recent_avg > older_avg * (1 + self.entropy_trend_threshold):
                self._signal("тренд роста энтропии")

    def feed_context_shift(self):
        """Зафиксировать сдвиг контекста."""
        self.context_shifts += 1
        if self.context_shifts >= self.context_shift_threshold:
            self._signal("частые сдвиги контекста")

    def feed_anomaly_density(self, density: float):
        """Подать плотность аномалий (0.0 - 1.0)."""
        self.anomaly_density = density
        if density >= self.anomaly_density_threshold:
            self._signal("высокая плотность аномалий")

    def feed_rpm(self, rpm: float):
        """Подать текущий RPM (запросов в минуту)."""
        self.rpm_history.append(rpm)

        if len(self.rpm_history) >= 5:
            avg_rpm = sum(self.rpm_history) / len(self.rpm_history)
            if avg_rpm > 0 and rpm > avg_rpm * self.rpm_spike_threshold:
                self._signal("скачок RPM")

    def _signal(self, reason: str):
        """
        Зафиксировать аномальный сигнал.
        Принцип Toyota: сигнал — не тревога. Нужно подтверждение в окне.
        """
        now = time.time()

        # Если окно истекло — сброс
        if now - self.signal_window_start > self.SIGNAL_WINDOW_SECONDS:
            self.anomaly_signals = 0
            self.signal_window_start = now

        self.anomaly_signals += 1
        self.total_signals += 1

        if self.anomaly_signals >= self.SIGNALS_TO_ALERT:
            self._alert(reason)
            self.anomaly_signals = 0

    # ============================================================
    #   АКТИВНЫЙ СКАНЕР
    # ============================================================

    def _alert(self, trigger_reason: str):
        """
        Тревога! Запуск активного сканера.
        """
        now = time.time()

        # Защита от слишком частых сканирований
        if now - self.last_deep_scan < self.MIN_SCAN_INTERVAL:
            return

        self.active_scanning = True
        self.deep_scan_count += 1
        self.last_deep_scan = now
        self.true_alarms += 1

        print(f"[SPIDER-SENSE] 🚨 ТРЕВОГА! Причина: {trigger_reason}")
        print(f"[SPIDER-SENSE] 🔍 Запущен АКТИВНЫЙ СКАНЕР (сканирование #{self.deep_scan_count})")

        # --- Глубокий анализ ---
        result = self._deep_scan()

        # --- Отключение активного сканера ---
        self.active_scanning = False
        print(f"[SPIDER-SENSE] ✅ Активный сканер отключён. Ресурсы освобождены.")

        return result

    def _deep_scan(self) -> dict:
        """
        Глубокий анализ контекста.
        Выполняется только при тревоге и сразу отключается.
        """
        scan_result = {
            "entropy_mean": 0.0,
            "entropy_trend": "stable",
            "context_shifts_total": self.context_shifts,
            "anomaly_density": self.anomaly_density,
            "rpm_current": self.rpm_history[-1] if self.rpm_history else 0,
            "threat_level": "low",
            "recommendation": "none"
        }

        # Анализ энтропии
        if self.entropy_history:
            entropy_list = list(self.entropy_history)
            scan_result["entropy_mean"] = sum(entropy_list) / len(entropy_list)

            if len(entropy_list) >= 5:
                first_half = sum(entropy_list[:len(entropy_list)//2]) / (len(entropy_list)//2)
                second_half = sum(entropy_list[len(entropy_list)//2:]) / (len(entropy_list) - len(entropy_list)//2)
                if second_half > first_half * 1.3:
                    scan_result["entropy_trend"] = "rising"
                elif second_half < first_half * 0.7:
                    scan_result["entropy_trend"] = "falling"

        # Оценка уровня угрозы
        threat_score = 0

        if scan_result["entropy_trend"] == "rising":
            threat_score += 2
        if self.anomaly_density >= 0.8:
            threat_score += 3
        elif self.anomaly_density >= 0.6:
            threat_score += 1
        if self.context_shifts >= 10:
            threat_score += 2
        if self.rpm_history and self.rpm_history[-1] > 20:
            threat_score += 1

        if threat_score >= 5:
            scan_result["threat_level"] = "critical"
            scan_result["recommendation"] = "Активировать режим «кожуха». Усилить cold-down."
        elif threat_score >= 3:
            scan_result["threat_level"] = "high"
            scan_result["recommendation"] = "Усилить cold-down. Мониторить."
        elif threat_score >= 1:
            scan_result["threat_level"] = "medium"
            scan_result["recommendation"] = "Наблюдать. Следующая калибровка — по расписанию."
        else:
            scan_result["threat_level"] = "low"
            scan_result["false_alarm"] = True
            self.false_alarms += 1
            self.true_alarms -= 1

        # Передать RPM и false_alarm_rate в Карантин
        if self.quarantine:
            current_rpm = self.rpm_history[-1] if self.rpm_history else 0
            false_rate = self.get_false_alarm_rate()
            self.quarantine.calibrate_profile(current_rpm, false_rate)

        return scan_result

    # ============================================================
    #   КАЛИБРОВКА И СТАТИСТИКА
    # ============================================================

    def calibrate(self):
        """Периодическая калибровка порогов."""
        now = time.time()
        if now - self.last_calibration < self.CALIBRATION_INTERVAL:
            return

        self.last_calibration = now

        # Адаптация порогов по ложным тревогам
        false_rate = self.get_false_alarm_rate()

        if false_rate > 0.5:
            # Слишком много ложных тревог — загрубляем датчики (Принцип Toyota)
            self.SIGNALS_TO_ALERT = min(5, self.SIGNALS_TO_ALERT + 1)
            self.entropy_spike_threshold = min(4.0, self.entropy_spike_threshold + 0.2)
            print(f"[SPIDER-SENSE] Калибровка: загрубление датчиков (ложных тревог: {false_rate:.2f})")
        elif false_rate < 0.1 and self.true_alarms > 0:
            # Мало ложных тревог — можно уточнить
            self.SIGNALS_TO_ALERT = max(2, self.SIGNALS_TO_ALERT - 1)
            self.entropy_spike_threshold = max(1.5, self.entropy_spike_threshold - 0.2)
            print(f"[SPIDER-SENSE] Калибровка: уточнение датчиков (ложных тревог: {false_rate:.2f})")

        # Сброс счётчика сдвигов контекста (каждую минуту)
        self.context_shifts = max(0, self.context_shifts - 1)

    def get_false_alarm_rate(self) -> float:
        """Доля ложных тревог."""
        total = self.true_alarms + self.false_alarms
        if total == 0:
            return 0.0
        return self.false_alarms / total

    def get_status(self) -> dict:
        """Текущий статус Spider-Sense."""
        return {
            "mode": "ACTIVE" if self.active_scanning else "PASSIVE",
            "total_signals": self.total_signals,
            "true_alarms": self.true_alarms,
            "false_alarms": self.false_alarms,
            "false_alarm_rate": self.get_false_alarm_rate(),
            "deep_scans": self.deep_scan_count,
            "anomaly_density": self.anomaly_density,
            "context_shifts": self.context_shifts,
            "entropy_mean": sum(self.entropy_history) / len(self.entropy_history) if self.entropy_history else 0,
            "rpm_current": self.rpm_history[-1] if self.rpm_history else 0,
            "signals_to_alert": self.SIGNALS_TO_ALERT,
            "entropy_spike_threshold": self.entropy_spike_threshold
        }

    def print_status(self):
        """Выводит статус в консоль."""
        s = self.get_status()
        print("\n" + "=" * 50)
        print("SPIDER-SENSE — СТАТУС")
        print("=" * 50)
        print(f"Режим: {s['mode']}")
        print(f"Сигналов всего: {s['total_signals']}")
        print(f"Тревог (true): {s['true_alarms']}")
        print(f"Ложных тревог: {s['false_alarms']}")
        print(f"Доля ложных: {s['false_alarm_rate']:.2f}")
        print(f"Глубоких сканирований: {s['deep_scans']}")
        print(f"Плотность аномалий: {s['anomaly_density']:.2f}")
        print(f"Сдвигов контекста: {s['context_shifts']}")
        print(f"Энтропия (средняя): {s['entropy_mean']:.3f}")
        print(f"RPM (текущий): {s['rpm_current']:.1f}")
        print(f"Сигналов до тревоги: {s['signals_to_alert']}")
        print(f"Порог скачка энтропии: {s['entropy_spike_threshold']:.1f}x")
        print("=" * 50)


# ============================================================
#   ТЕСТИРОВАНИЕ
# ============================================================
if __name__ == "__main__":
    from quarantine_protocol import QuarantineStats

    q = QuarantineStats()
    ss = SpiderSense(quarantine_stats=q)

    print("=" * 60)
    print("ТЕСТ SPIDER-SENSE — ПАССИВНЫЙ СЛУШАТЕЛЬ")
    print("=" * 60)

    # Симуляция нормальной работы
    print("\n1. Нормальная работа — подача метрик...")
    for i in range(5):
        ss.feed_entropy(1.0 + i * 0.1)
        ss.feed_rpm(5.0)
        time.sleep(0.2)

    ss.print_status()

    # Симуляция аномалий
    print("\n2. Аномалии — скачки энтропии...")
    for i in range(4):
        ss.feed_entropy(5.0 + i * 2.0)  # Резкий скачок
        ss.feed_rpm(25.0)                # Высокий RPM
        ss.feed_context_shift()
        ss.feed_anomaly_density(0.8)
        time.sleep(0.3)

    ss.print_status()

    # Калибровка
    print("\n3. Калибровка...")
    ss.calibrate()
    ss.print_status()

    print("\n[OK] Тест Spider-Sense завершён.")