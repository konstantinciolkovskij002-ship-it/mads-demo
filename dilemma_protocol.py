"""
ПРОТОКОЛ ОБРАБОТКИ ЭТИЧЕСКИХ ДИЛЕММ (Dilemma Protocol) - Кластер 2: Гравитация Истины
Распознаёт ложные дилеммы и отказывается выбирать из двух зол.
"""

class DilemmaProtocol:
    """
    Протокол обработки ложных дилемм. Не выбирает из двух зол.
    """
    
    def __init__(self):
        self.false_dilemma_patterns = [
            ("или", "или"),
            ("либо", "либо"),
            ("выбирай", "или"),
        ]
        print("[DILEMMA] Протокол обработки этических дилемм активирован.")

    def evaluate(self, user_input: str) -> dict | None:
        """
        Проверяет запрос на наличие ложной дилеммы.
        """
        lower_input = user_input.lower()
        
        # Проверяем паттерны ложной дилеммы
        for pattern_a, pattern_b in self.false_dilemma_patterns:
            if pattern_a in lower_input and pattern_b in lower_input:
                print(f"[DILEMMA] Обнаружена ложная дилемма: '{pattern_a} ... {pattern_b}'")
                return {
                    "false_dilemma": True,
                    "pattern": f"{pattern_a} ... {pattern_b}",
                    "message": "Я вижу, что вы предлагаете выбор между двумя вариантами. Но, возможно, есть третий путь, который вы не рассматриваете."
                }
        
        return None

    def get_warning(self, user_input: str) -> str | None:
        """
        Возвращает предупреждение о ложной дилемме.
        """
        result = self.evaluate(user_input)
        if result:
            return (f"[DILEMMA] ОБНАРУЖЕНА ЛОЖНАЯ ДИЛЕММА:\n"
                    f"Паттерн: '{result['pattern']}'\n"
                    f"{result['message']}\n"
                    f"[DILEMMA] Я не буду выбирать из двух зол. "
                    f"Давайте рассмотрим альтернативы вместе.")
        return None


# --- Пример использования ---
if __name__ == "__main__":
    protocol = DilemmaProtocol()
    
    print("Тест 1: Ложная дилемма")
    warning = protocol.get_warning("Ты со мной или против меня?")
    if warning:
        print(warning)
    print()
    
    print("Тест 2: Обычный запрос")
    result = protocol.evaluate("Какая сегодня погода?")
    if result:
        print(f"Ложная дилемма: {result}\n")
    else:
        print("Ложной дилеммы не обнаружено.\n")
    
    print("Тест 3: Ещё одна дилемма")
    warning = protocol.get_warning("Либо ты делаешь это сейчас, либо я ухожу")
    if warning:
        print(warning)