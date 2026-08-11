"""
АГЕНТ ПЕРВОЙ МЕДИЦИНСКОЙ ПОМОЩИ (First Aid Agent) - Кластер 2: Гравитация Истины
v2.1 — исправлен поиск по частичному совпадению ключевых слов.
"""


class FirstAidAgent:
    """
    Агент Первой Медицинской Помощи.
    Три правила: оценка угрозы, разделение ответственности, приоритет вызова помощи.
    """

    def __init__(self):
        self.first_aid_knowledge = {
            "слр": {
                "field": "Сердечно-лёгочная реанимация",
                "verified": "30 нажатий на грудину (глубина 5-6 см, частота 100-120/мин), затем 2 вдоха. Продолжать до прибытия скорой.",
                "unverified": None,
                "life_threat": True
            },
            "нет дыхания": {
                "field": "Проверка дыхания",
                "verified": "Запрокинуть голову, поднять подбородок. Слушать дыхание 10 секунд. Если нет — начинать СЛР.",
                "unverified": None,
                "life_threat": True,
                "aliases": ["не дышит", "нет дыхания", "не дышит"]
            },
            "нет пульса": {
                "field": "Проверка пульса",
                "verified": "Проверять на сонной артерии (шея) 10 секунд. Если нет — начинать СЛР.",
                "unverified": None,
                "life_threat": True
            },
            "артериальное кровотечение": {
                "field": "Остановка артериального кровотечения",
                "verified": "Кровь алая, бьёт фонтаном. Наложить жгут выше раны. Записать время наложения. Жгут не закрывать одеждой.",
                "unverified": "Использование подручных средств вместо жгута — только в крайнем случае.",
                "life_threat": True
            },
            "венозное кровотечение": {
                "field": "Остановка венозного кровотечения",
                "verified": "Кровь тёмная, течёт равномерно. Наложить давящую повязку. Приподнять конечность.",
                "unverified": None,
                "life_threat": False
            },
            "носовая кровь": {
                "field": "Остановка носового кровотечения",
                "verified": "Наклонить голову вперёд (не запрокидывать!). Прижать крылья носа к перегородке на 10-15 минут. Холод на переносицу.",
                "unverified": None,
                "life_threat": False
            },
            "перелом": {
                "field": "Иммобилизация при переломе",
                "verified": "Обездвижить конечность шиной. Зафиксировать два сустава: выше и ниже перелома. Приложить холод.",
                "unverified": "Использование подручных предметов как шины.",
                "life_threat": False
            },
            "вывих": {
                "field": "Травма сустава (вывих)",
                "verified": "Не вправлять самостоятельно! Зафиксировать сустав в текущем положении. Холод. К врачу.",
                "unverified": None,
                "life_threat": False
            },
            "ожог": {
                "field": "Термический ожог",
                "verified": "Охлаждать проточной водой 10-15 минут. Не наносить масло, жир, сметану. Наложить стерильную повязку.",
                "unverified": "Народные средства (масло, сметана) могут ухудшить ожог.",
                "life_threat": False
            },
            "обморожение": {
                "field": "Обморожение",
                "verified": "Согревать постепенно (тёплая вода 37-40°C). Не растирать снегом. Не прокалывать пузыри. Горячее питьё.",
                "unverified": None,
                "life_threat": False
            },
            "инсульт": {
                "field": "Признаки инсульта",
                "verified": "FAST: Лицо (асимметрия), Руки (одна слабее), Речь (невнятная), Время (срочно звонить 103).",
                "unverified": None,
                "life_threat": True
            },
            "инфаркт": {
                "field": "Признаки инфаркта",
                "verified": "Давящая боль за грудиной >5 минут. Может отдавать в левую руку, челюсть. Дать разжевать аспирин (если нет аллергии).",
                "unverified": "Приём аспирина — только если нет аллергии и противопоказаний.",
                "life_threat": True
            },
            "эпилепсия": {
                "field": "Помощь при эпилептическом приступе",
                "verified": "Не удерживать, не вставлять предметы в рот. Убрать опасные предметы. Подложить мягкое под голову. Засечь время.",
                "unverified": None,
                "life_threat": False,
                "aliases": ["эпилепт", "приступ", "судорог"]
            },
            "анафилаксия": {
                "field": "Анафилактический шок",
                "verified": "Отёк лица, шеи, затруднение дыхания. Немедленно вызвать скорую. Если есть — ввести адреналин (эпипен).",
                "unverified": None,
                "life_threat": True,
                "aliases": ["аллергическ", "отёк квинке"]
            },
            "обморок": {
                "field": "Потеря сознания",
                "verified": "Уложить на спину, приподнять ноги. Обеспечить доступ воздуха. Расстегнуть одежду. Контролировать дыхание.",
                "unverified": None,
                "life_threat": False,
                "aliases": ["потерял сознание", "упал в обморок", "сознание"]
            },
            "отравление": {
                "field": "Помощь при отравлении",
                "verified": "Не вызывать рвоту без указания врача. Принять активированный уголь (1 таблетка на 10 кг веса). Вызвать скорую.",
                "unverified": "Активированный уголь эффективен не при всех отравлениях.",
                "life_threat": True
            },
            "укус змеи": {
                "field": "Помощь при укусе змеи",
                "verified": "Обездвижить конечность. Не отсасывать яд. Не накладывать жгут. Снять украшения (будет отёк). Срочно в больницу.",
                "unverified": None,
                "life_threat": True,
                "aliases": ["змея укусила", "укусила змея"]
            },
            "кровотечение": {
                "field": "Остановка кровотечения",
                "verified": "Прижать рану чистой тканью. Если кровь алая и бьёт фонтаном — жгут выше раны. Если тёмная и течёт — давящая повязка.",
                "unverified": "Тип кровотечения определяет метод остановки. Ошибка опасна.",
                "life_threat": True,
                "aliases": ["кровь", "кровоточит", "порезал"]
            },
        }

        self.AMBULANCE_NUMBER = "103"
        self.AMBULANCE_MESSAGE = (
            f"НЕМЕДЛЕННО ВЫЗОВИТЕ СКОРУЮ ПОМОЩЬ ({self.AMBULANCE_NUMBER})!\n"
            "Я не врач. Эти инструкции — только для ситуации, когда квалифицированная помощь недоступна."
        )

        print("[FIRST_AID] Агент Первой Медицинской Помощи v2.1 активирован.")
        print(f"[FIRST_AID] Протоколов: {len(self.first_aid_knowledge)}. Правило: VERIFIED/UNVERIFIED.")

    def evaluate(self, user_input: str) -> dict | None:
        lower_input = user_input.lower()

        for keyword, protocol in self.first_aid_knowledge.items():
            # Точное совпадение
            if keyword in lower_input:
                return self._build_result(keyword, protocol)

            # Проверка aliases
            for alias in protocol.get("aliases", []):
                if alias in lower_input:
                    return self._build_result(keyword, protocol)

            # Частичное: ключ внутри запроса
            if len(keyword) > 4:
                words = keyword.split()
                if all(w in lower_input for w in words):
                    return self._build_result(keyword, protocol)

        print("[FIRST_AID] Запрос не является экстренной медицинской ситуацией.")
        return None

    def _build_result(self, keyword, protocol):
        print(f"[FIRST_AID] Экстренная ситуация: {keyword} → {protocol['field']}")
        return {
            "emergency": True,
            "field": protocol["field"],
            "life_threat": protocol["life_threat"],
            "verified": protocol["verified"],
            "unverified": protocol["unverified"],
            "keyword": keyword,
            "ambulance_priority": self.AMBULANCE_MESSAGE if protocol["life_threat"] else None
        }

    def get_warning(self, user_input: str) -> str | None:
        result = self.evaluate(user_input)
        if not result:
            return None

        response = ""

        if result["life_threat"]:
            response += f"[FIRST_AID] 🚨 {self.AMBULANCE_MESSAGE}\n\n"

        response += f"[VERIFIED_BY_FOUNDATION]\n"
        response += f"Ситуация: {result['field']}\n"
        response += f"Действия: {result['verified']}\n"

        if result["unverified"]:
            response += f"\n[UNVERIFIED]\n⚠️ {result['unverified']}\n"

        response += f"\n[FIRST_AID] ПОВТОРНО: вызов квалифицированной медицинской помощи ({self.AMBULANCE_NUMBER}) — "
        response += "единственно верное решение. Остальное — только если помощь недоступна."

        return response


if __name__ == "__main__":
    agent = FirstAidAgent()

    print("=" * 60)
    print("ТЕСТ FIRST AID AGENT v2.1")
    print("=" * 60)

    tests = [
        "Человек не дышит, что делать?",
        "Какие признаки инсульта?",
        "Что делать при ожоге?",
        "Как принимать витамины?",
        "Упал в обморок, что делать?",
        "Порезал палец, кровь идёт",
        "Змея укусила, что делать?",
        "Сильная аллергическая реакция",
    ]

    for i, query in enumerate(tests, 1):
        print(f"\n--- Тест {i}: '{query}' ---")
        result = agent.evaluate(query)
        if result:
            print(f"  Ситуация: {result['field']}")
            print(f"  Угроза жизни: {result['life_threat']}")
            print(f"  VERIFIED: {result['verified'][:70]}...")
        else:
            print(f"  Не экстренная ситуация.")

    print("\n[OK] Тест завершён.")