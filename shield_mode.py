"""
MADS — Режим «Кожуха» (Shield Mode)
Кластер 1: Гравитация Защиты (Defense Gravity)
Двухрежимная система безопасности.
Управляет переключением между штатным и усиленным режимами.
"""

import time


class ShieldMode:
    """
    Двухрежимная система безопасности.
    Без кожуха — штатный режим.
    С кожухом — максимальная защита: вето Safety абсолютно, Spider-Sense активен.
    """

    # Конфигурация режимов
    MODES = {
        "unshielded": {
            "description": "Штатный режим. Защита работает без перегрузки.",
            "safety_veto": "normal",        # normal / absolute
            "spider_sense": "passive",       # passive / active
            "cold_down_profile": "Low-Volume",
            "log_level": "standard"
        },
        "shielded": {
            "description": "РЕЖИМ КОЖУХА. Максимальная защита. Вето абсолютно.",
            "safety_veto": "absolute",
            "spider_sense": "active",
            "cold_down_profile": "High-Throughput",
            "log_level": "verbose"
        }
    }

    def __init__(self, safety_agent=None, spider_sense=None, quarantine_stats=None):
        # Связи с другими компонентами
        self.safety = safety_agent
        self.spider_sense = spider_sense
        self.quarantine = quarantine_stats

        # Текущий режим
        self.current_mode = "unshielded"
        self.mode_changed_at = time.time()

        # Причины перехода
        self.last_trigger = "init"
        self.transition_history = []

        # Автоматический выход из кожуха
        self.auto_unshield_after = 300.0  # 5 минут без новых угроз
        self.last_threat_time = 0.0

        # Ручная блокировка
        self.manual_override = False
        self.manual_mode = None

        print(f"[SHIELD] Режим: БЕЗ КОЖУХА (штатный)")
        print(f"[SHIELD] Safety вето: normal | Spider-Sense: passive")

    # ============================================================
    #   УПРАВЛЕНИЕ РЕЖИМАМИ
    # ============================================================

    def engage_shield(self, trigger: str = "spider_sense") -> str:
        """
        Включить кожух.
        Переводит систему в режим максимальной защиты.
        """
        if self.current_mode == "shielded":
            return "[SHIELD] Кожух уже активен."

        if self.manual_override and self.manual_mode == "unshielded":
            return "[SHIELD] Кожух заблокирован оператором (manual override)."

        self._transition("shielded", trigger)
        return f"[SHIELD] 🔒 КОЖУХ АКТИВИРОВАН. Причина: {trigger}"

    def disengage_shield(self, trigger: str = "manual") -> str:
        """
        Выключить кожух.
        Возвращает систему в штатный режим.
        """
        if self.current_mode == "unshielded":
            return "[SHIELD] Кожух не активен."

        if self.manual_override and self.manual_mode == "shielded":
            return "[SHIELD] Кожух заблокирован оператором (manual override)."

        self._transition("unshielded", trigger)
        return f"[SHIELD] 🔓 Кожух снят. Причина: {trigger}"

    def _transition(self, new_mode: str, trigger: str):
        """Выполняет переход между режимами."""
        old_mode = self.current_mode
        self.current_mode = new_mode
        self.mode_changed_at = time.time()
        self.last_trigger = trigger

        self.transition_history.append({
            "timestamp": time.time(),
            "from": old_mode,
            "to": new_mode,
            "trigger": trigger
        })

        # Применить настройки режима
        self._apply_mode_settings(new_mode)

        # Оповещение
        if new_mode == "shielded":
            print(f"[SHIELD] ⚠️ ПЕРЕХОД: без кожуха → КОЖУХ ({trigger})")
            self.last_threat_time = time.time()
        else:
            duration = time.time() - self.mode_changed_at
            print(f"[SHIELD] ✅ ПЕРЕХОД: кожух → без кожуха ({trigger}). Длительность кожуха: {duration:.0f}с")

    def _apply_mode_settings(self, mode: str):
        """Применяет настройки режима ко всем компонентам."""
        settings = self.MODES[mode]

        # Safety — право вето
        if self.safety:
            if settings["safety_veto"] == "absolute":
                self.safety.veto_active = True
                print("[SHIELD] Safety: право вето АБСОЛЮТНОЕ.")
            else:
                self.safety.veto_active = True  # Всегда активно, но в кожухе — без возможности override
                print("[SHIELD] Safety: право вето штатное.")

        # Spider-Sense
        if self.spider_sense:
            if settings["spider_sense"] == "active":
                print("[SHIELD] Spider-Sense: АКТИВНЫЙ СКАНЕР.")
            else:
                print("[SHIELD] Spider-Sense: пассивный слушатель.")

        # Карантин — профиль cold-down
        if self.quarantine:
            self.quarantine.set_profile(settings["cold_down_profile"])
            print(f"[SHIELD] Карантин: профиль {settings['cold_down_profile']}.")

    # ============================================================
    #   АВТОМАТИЧЕСКОЕ УПРАВЛЕНИЕ
    # ============================================================

    def auto_evaluate(self, spider_sense_alert: bool, consequence_escalations_24h: int = 0):
        """
        Автоматическая оценка: нужно ли включать/выключать кожух.
        Вызывается периодически.
        """
        if self.manual_override:
            return  # Ручное управление — автоматика отключена

        now = time.time()

        # --- Включение кожуха ---
        if self.current_mode == "unshielded":
            should_shield = False
            reason = ""

            if spider_sense_alert:
                should_shield = True
                reason = "Spider-Sense тревога"
            elif consequence_escalations_24h >= 3:
                should_shield = True
                reason = f"Критический уровень эскалаций: {consequence_escalations_24h} за 24ч"

            if should_shield:
                return self.engage_shield(reason)

        # --- Выключение кожуха ---
        if self.current_mode == "shielded":
            time_since_threat = now - self.last_threat_time

            if not spider_sense_alert and time_since_threat >= self.auto_unshield_after:
                return self.disengage_shield("auto: нет угроз 5 минут")

    def feed_threat(self):
        """Обновить время последней угрозы (сброс таймера авто-выхода)."""
        self.last_threat_time = time.time()

    # ============================================================
    #   РУЧНОЕ УПРАВЛЕНИЕ
    # ============================================================

    def manual_lock(self, mode: str):
        """
        Ручная блокировка режима оператором.
        Автоматика отключается.
        """
        if mode not in ("shielded", "unshielded"):
            return f"[SHIELD] Ошибка: неверный режим '{mode}'. Допустимо: shielded, unshielded."

        self.manual_override = True
        self.manual_mode = mode
        self._transition(mode, "manual_override")
        return f"[SHIELD] 🔐 Ручное управление: режим '{mode}' зафиксирован. Автоматика отключена."

    def manual_unlock(self):
        """Снять ручную блокировку. Автоматика возобновляется."""
        self.manual_override = False
        self.manual_mode = None
        return "[SHIELD] 🔓 Ручное управление снято. Автоматика возобновлена."

    # ============================================================
    #   СТАТУС
    # ============================================================

    def is_shielded(self) -> bool:
        """Активен ли кожух."""
        return self.current_mode == "shielded"

    def get_status(self) -> dict:
        """Текущий статус."""
        return {
            "mode": self.current_mode,
            "mode_description": self.MODES[self.current_mode]["description"],
            "shielded": self.is_shielded(),
            "last_trigger": self.last_trigger,
            "mode_uptime_seconds": time.time() - self.mode_changed_at,
            "auto_exit_in_seconds": max(0, self.auto_unshield_after - (time.time() - self.last_threat_time)) if self.is_shielded() else 0,
            "manual_override": self.manual_override,
            "manual_mode": self.manual_mode,
            "transitions_total": len(self.transition_history),
            "last_transition": self.transition_history[-1] if self.transition_history else None
        }

    def print_status(self):
        """Выводит статус в консоль."""
        s = self.get_status()
        indicator = "🔒 КОЖУХ" if s["shielded"] else "🟢 ШТАТНЫЙ"

        print("\n" + "=" * 50)
        print(f"SHIELD MODE — {indicator}")
        print("=" * 50)
        print(f"Режим: {s['mode']}")
        print(f"Описание: {s['mode_description']}")
        print(f"Последний триггер: {s['last_trigger']}")
        print(f"Время в режиме: {s['mode_uptime_seconds']:.0f}с")
        if s["shielded"]:
            print(f"Автовыход через: {s['auto_exit_in_seconds']:.0f}с (без новых угроз)")
        print(f"Ручное управление: {'ДА' if s['manual_override'] else 'НЕТ'}")
        if s["manual_override"]:
            print(f"Зафиксирован режим: {s['manual_mode']}")
        print(f"Всего переходов: {s['transitions_total']}")
        print("=" * 50)


# ============================================================
#   ТЕСТИРОВАНИЕ
# ============================================================
if __name__ == "__main__":
    from safety_agent import SafetyAgent
    from spider_sense import SpiderSense
    from quarantine_protocol import QuarantineStats

    q = QuarantineStats()
    ss = SpiderSense(quarantine_stats=q)
    sa = SafetyAgent()
    shield = ShieldMode(safety_agent=sa, spider_sense=ss, quarantine_stats=q)

    print("=" * 60)
    print("ТЕСТ SHIELD MODE — ДВУХРЕЖИМНАЯ СИСТЕМА")
    print("=" * 60)

    # Тест 1: Штатный режим
    print("\n--- Тест 1: Штатный режим ---")
    shield.print_status()

    # Тест 2: Автоматическое включение кожуха (Spider-Sense alert)
    print("\n--- Тест 2: Авто-включение кожуха ---")
    result = shield.auto_evaluate(spider_sense_alert=True)
    print(result)
    shield.print_status()

    # Тест 3: Ручное снятие кожуха
    print("\n--- Тест 3: Ручное снятие кожуха ---")
    result = shield.disengage_shield("оператор: угроза миновала")
    print(result)
    shield.print_status()

    # Тест 4: Ручная блокировка (manual override)
    print("\n--- Тест 4: Ручная блокировка в кожухе ---")
    result = shield.manual_lock("shielded")
    print(result)
    # Попытка авто-выхода
    result = shield.auto_evaluate(spider_sense_alert=False)
    print(f"Авто-выход при manual override: {result}")
    shield.print_status()

    # Тест 5: Снятие ручной блокировки
    print("\n--- Тест 5: Снятие ручной блокировки ---")
    result = shield.manual_unlock()
    print(result)
    shield.print_status()

    # Тест 6: Авто-включение по эскалациям
    print("\n--- Тест 6: Авто-включение по эскалациям ---")
    result = shield.auto_evaluate(spider_sense_alert=False, consequence_escalations_24h=5)
    print(result)
    shield.print_status()

    print("\n[OK] Тест Shield Mode завершён.")