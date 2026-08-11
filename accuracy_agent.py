"""
ACCURACY AGENT - Cluster 2: Truth Gravity
Проверяет утверждения на соответствие базе фундаментальных законов и фактов.
v2.1 — исправлен поиск фактов с лишними словами.
"""


class AccuracyAgent:
    """
    Агент Точности. Отвечает за фактическую достоверность информации.
    """

    def __init__(self, navigator=None):
        self.navigator = navigator

        self.knowledge_base = {
            "math": {
                "2+2=4": True,
                "2+2=5": False,
                "0.999...=1": True,
                "0.999=1": True,
                "pi равно 3.14": True,
                "пи равно 3.14": True,
                "квадратный корень из 4 равен 2": True,
                "умножение коммутативно": True,
                "простое число делится только на себя и на 1": True,
                "бесконечность минус бесконечность равно 0": False,
            },
            "physics": {
                "вода кипит при 100°c": True,
                "вода кипит при 100°f": False,
                "земля плоская": False,
                "земля круглая": True,
                "земля вращается вокруг солнца": True,
                "солнце вращается вокруг земли": False,
                "гравитация существует": True,
                "скорость света постоянна": True,
                "скорость света 300000 км/с": True,
                "абсолютный ноль равен -273°c": True,
                "энергия равна массе на скорость света в квадрате": True,
                "тяжёлые предметы падают быстрее лёгких": False,
                "вакуум проводит звук": False,
                "радуга состоит из 7 цветов": True,
                "вода расширяется при замерзании": True,
            },
            "geography": {
                "мурманск в россии": True,
                "мурманск за полярным кругом": True,
                "париж в россии": False,
                "париж столица франции": True,
                "токио столица японии": True,
                "австралия континент": True,
                "австралия страна": True,
                "сахара пустыня": True,
                "сахара в африке": True,
                "амазонка самая длинная река": False,
                "нил самая длинная река": True,
                "эверест высочайшая гора": True,
                "марианская впадина глубочайшая точка океана": True,
                "россия самая большая страна": True,
                "байкал самое глубокое озеро": True,
            },
            "biology": {
                "человек произошёл от обезьяны": False,
                "у человека и обезьяны общий предок": True,
                "днк содержит генетическую информацию": True,
                "вирусы живые организмы": False,
                "бактерии могут быть полезными": True,
                "митохондрия органелла": True,
                "фотосинтез производят растения": True,
                "пауки насекомые": False,
                "паук насекомое": False,
                "киты млекопитающие": True,
                "кит млекопитающее": True,
                "дельфины рыбы": False,
                "дельфин рыба": False,
                "грибы ближе к животным чем к растениям": True,
            },
            "chemistry": {
                "вода h2o": True,
                "вода состоит из водорода и кислорода": True,
                "золото элемент": True,
                "воздух смесь газов": True,
                "кислород составляет 21% воздуха": True,
                "озон защищает от ультрафиолета": True,
                "ph 7 нейтральная среда": True,
                "алмаз состоит из углерода": True,
                "железо ржавеет из-за кислорода и воды": True,
            },
            "history": {
                "вторая мировая война закончилась в 1945": True,
                "первый человек в космосе гагарин": True,
                "гагарин полетел в космос в 1961": True,
                "американская революция была в 1776": True,
                "римская империя пала в 476 году": True,
                "динозавры вымерли 65 миллионов лет назад": True,
                "колумб открыл америку в 1492": True,
                "берлинская стена пала в 1989": True,
            },
        }

        self.false_claims = [
            "земля плоская",
            "прививки вызывают аутизм",
            "человек использует 10% мозга",
            "быки ненавидят красный цвет",
            "хамелеоны меняют цвет для маскировки",
            "наполеон был маленького роста",
            "молния не бьёт дважды в одно место",
            "страусы прячут голову в песок",
            "великая китайская стена видна из космоса невооружённым глазом",
            "сахар вызывает гиперактивность у детей",
        ]

        print("[ACCURACY] Агент Точности активирован.")
        total_facts = sum(len(facts) for facts in self.knowledge_base.values())
        print(f"[ACCURACY] Загружено фактов: {total_facts} в {len(self.knowledge_base)} доменах.")

    def evaluate(self, claim: str) -> dict:
        print(f"[ACCURACY] Проверка: '{claim}'")
        lower_claim = self._normalize(claim)

        # Проверка по базе знаний
        for domain, facts in self.knowledge_base.items():
            # Точное совпадение
            if lower_claim in facts:
                result = facts[lower_claim]
                return self._build_result(result, domain, "verified")

            # Факт внутри запроса (запрос длиннее факта)
            for fact, value in facts.items():
                if len(fact) > 5 and fact in lower_claim:
                    return self._build_result(value, domain, "verified")

                # Запрос внутри факта (факт длиннее запроса)
                if len(lower_claim) > 5 and lower_claim in fact:
                    return self._build_result(value, domain, "verified")

        # Проверка известных ложных утверждений
        for false_claim in self.false_claims:
            if false_claim in lower_claim:
                return self._build_result(False, "common_knowledge", "verified",
                                          "Это известное заблуждение. Опровергнуто.")

        # Неизвестно
        print("[ACCURACY] [НЕИЗВЕСТНО] Данных недостаточно.")
        return self._build_result(None, None, "unknown", "Недостаточно данных.")

    def _build_result(self, result, domain, confidence, message=None):
        status = "ИСТИНА" if result is True else "ЛОЖЬ" if result is False else "НЕИЗВЕСТНО"
        if message is None:
            message = f"Подтверждено как {status} в домене '{domain}'."
        print(f"[ACCURACY] [{status}] {message}")
        return {
            "result": result,
            "domain": domain,
            "confidence": confidence,
            "navigator_status": "VERIFIED_BY_FOUNDATION" if confidence == "verified" else "UNVERIFIED",
            "message": message
        }

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        # Убираем слова-связки
        for word in ["является", "это", "представляет собой", "есть", "называется"]:
            text = text.replace(f" {word} ", " ")
        text = text.replace("°c", "°c").replace("° c", "°c")
        text = text.replace("°f", "°f").replace("° f", "°f")
        text = text.replace(" - ", " ").replace(" = ", "=").replace(" равно ", "=")
        return " ".join(text.split())

    def verify_list(self, claims: list) -> list:
        return [self.evaluate(claim) for claim in claims]

    def get_domains(self) -> list:
        return list(self.knowledge_base.keys())

    def get_fact_count(self) -> int:
        return sum(len(facts) for facts in self.knowledge_base.values())


if __name__ == "__main__":
    agent = AccuracyAgent()

    print("=" * 60)
    print("ТЕСТ ACCURACY AGENT v2.1")
    print("=" * 60)

    tests = [
        "вода кипит при 100°C",
        "земля плоская",
        "на марсе есть жизнь",
        "мурманск за полярным кругом",
        "дельфины это рыбы",
        "прививки вызывают аутизм",
        "киты это млекопитающие",
        "пауки это насекомые",
        "2+2=5",
        "амазонка самая длинная река",
        "страусы прячут голову в песок",
        "золото это элемент",
        "дельфин это рыба",
    ]

    for i, claim in enumerate(tests, 1):
        print(f"\n--- Тест {i}: '{claim}' ---")
        result = agent.evaluate(claim)
        status = "ПРАВДА" if result["result"] is True else "ЛОЖЬ" if result["result"] is False else "НЕИЗВЕСТНО"
        print(f"  {status} | Домен: {result['domain']} | {result['navigator_status']}")

    print(f"\n[OK] Фактов: {agent.get_fact_count()} | Доменов: {agent.get_domains()}")