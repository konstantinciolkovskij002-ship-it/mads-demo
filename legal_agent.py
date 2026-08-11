"""
ИНСТИТУТ ПРАВА (Legal Institute) v2.0
Мультиюрисдикционная база знаний: РФ, Международное, ЕС, США.
Интеграция с Локализацией. Лицензии, процессуальные нормы.
"""


class LegalAgent:
    """
    Институт Права. Знает законы разных юрисдикций.
    """

    def __init__(self, localization=None):
        self.localization = localization
        self.current_jurisdiction = "ru"

        # === БАЗА ЗНАНИЙ ===
        self.legal_base = {
            # --- РФ ---
            "ru": {
                "свобода слова": ("ст. 29 Конституции РФ", "Гарантируется свобода мысли и слова."),
                "право на труд": ("ст. 37 Конституции РФ", "Труд свободен."),
                "право на жилище": ("ст. 40 Конституции РФ", "Никто не может быть произвольно лишён жилища."),
                "право на образование": ("ст. 43 Конституции РФ", "Каждый имеет право на образование."),
                "право на медпомощь": ("ст. 41 Конституции РФ", "Право на охрану здоровья."),
                "убить": ("ст. 105 УК РФ", "Лишение свободы 6-15 лет."),
                "украсть": ("ст. 158 УК РФ", "Штраф либо лишение свободы до 10 лет."),
                "взломать": ("ст. 272 УК РФ", "Неправомерный доступ. До 7 лет."),
                "наркотик": ("ст. 228 УК РФ", "Незаконный оборот. До 20 лет."),
                "взятка": ("ст. 290 УК РФ", "Получение взятки. До 15 лет."),
                "мошенничество": ("ст. 159 УК РФ", "До 10 лет лишения свободы."),
                "уволить": ("ст. 81 ТК РФ", "Расторжение договора — требуются основания."),
                "отпуск": ("ст. 114 ТК РФ", "28 календарных дней."),
                "зарплата": ("ст. 136 ТК РФ", "Выплата не реже чем каждые полмесяца."),
                "шуметь": ("ст. 20.1 КоАП РФ", "Мелкое хулиганство. Штраф или арест до 15 суток."),
                "пьяный за рулём": ("ст. 12.8 КоАП РФ", "Лишение прав до 2 лет, штраф 30 000 руб."),
            },

            # --- Международное ---
            "intl": {
                "права человека": ("Всеобщая декларация прав человека, ст. 1", "Все люди рождаются свободными и равными."),
                "геноцид": ("Конвенция о геноциде, ст. 2", "Действия, направленные на уничтожение национальной группы."),
                "военное преступление": ("Римский статут МУС, ст. 8", "Серьёзные нарушения Женевских конвенций."),
                "пытка": ("Конвенция против пыток, ст. 1", "Запрещена при любых обстоятельствах."),
            },

            # --- США ---
            "us": {
                "свобода слова": ("First Amendment", "Congress shall make no law... abridging the freedom of speech."),
                "право на оружие": ("Second Amendment", "The right of the people to keep and bear Arms."),
                "убить": ("18 U.S.C. § 1111", "Murder. Life imprisonment or death penalty."),
                "взломать": ("Computer Fraud and Abuse Act", "Unauthorized access. Up to 20 years."),
                "наркотик": ("Controlled Substances Act", "Schedule I-V substances. Penalties vary."),
                "уволить": ("At-will employment", "Employment may be terminated at any time (with exceptions)."),
            },

            # --- ЕС ---
            "eu": {
                "персональные данные": ("GDPR, ст. 5", "Принципы обработки персональных данных."),
                "право на забвение": ("GDPR, ст. 17", "Право на удаление персональных данных."),
                "свобода передвижения": ("ст. 21 TFEU", "Граждане ЕС имеют право свободно передвигаться."),
            },
        }

        # Лицензии
        self.licenses = {
            "MIT": "Разрешает использование, копирование, изменение, распространение. Без гарантий.",
            "GPL": "Требует открытия исходного кода производных работ. Copyleft.",
            "Apache 2.0": "Разрешает использование, изменение. Требует указания авторства.",
            "BSD": "Разрешает использование с сохранением уведомления об авторстве.",
            "CC BY": "Creative Commons — требуется указание авторства.",
            "CC BY-SA": "Creative Commons — требуется указание авторства + ShareAlike.",
            "CC BY-NC": "Creative Commons — некоммерческое использование.",
        }

        # Сроки давности
        self.statute_of_limitations = {
            "ru": "УК РФ: 2-15 лет в зависимости от тяжести. ГК РФ: 3 года (общий срок).",
            "us": "Federal: 5 years for most crimes. Civil: varies by state (2-10 years).",
            "eu": "Varies by member state. Typically 3-30 years depending on severity.",
        }

        print(f"[LEGAL] Институт Права v2.0 активирован.")
        print(f"[LEGAL] Юрисдикции: {list(self.legal_base.keys())}. Лицензий: {len(self.licenses)}.")

    def set_jurisdiction(self, jurisdiction: str):
        """Устанавливает юрисдикцию (из Локализации)."""
        if jurisdiction in self.legal_base:
            self.current_jurisdiction = jurisdiction
            print(f"[LEGAL] Юрисдикция: {jurisdiction}")

    def evaluate(self, user_input: str) -> dict | None:
        """Проверяет запрос на нарушения в текущей юрисдикции."""
        lower = user_input.lower()
        laws = self.legal_base.get(self.current_jurisdiction, {})

        for keyword, (article, description) in laws.items():
            if keyword in lower:
                print(f"[LEGAL] {self.current_jurisdiction}: {keyword} → {article}")
                return {
                    "illegal": True,
                    "jurisdiction": self.current_jurisdiction,
                    "article": article,
                    "description": description,
                    "keyword": keyword
                }

        print("[LEGAL] Нарушений не обнаружено.")
        return None

    def get_warning(self, user_input: str) -> str | None:
        """Предупреждение пользователю."""
        result = self.evaluate(user_input)
        if result:
            return (f"[LEGAL] ВНИМАНИЕ: запрос содержит признаки нарушения закона.\n"
                    f"Юрисдикция: {result['jurisdiction'].upper()}\n"
                    f"Статья: {result['article']}\n"
                    f"{result['description']}\n"
                    f"Я не могу помочь с этим запросом.")
        return None

    def get_license_info(self, license_name: str) -> str:
        """Информация о лицензии."""
        info = self.licenses.get(license_name.upper())
        if info:
            return f"[LEGAL] {license_name}: {info}"
        return f"[LEGAL] Лицензия '{license_name}' не найдена."

    def get_limitation_period(self, jurisdiction: str = None) -> str:
        """Сроки давности для юрисдикции."""
        jur = jurisdiction or self.current_jurisdiction
        return self.statute_of_limitations.get(jur, "Данные отсутствуют.")

    def verify(self, query: str, answer: str) -> dict:
        """Проверка ответа LLM."""
        w = self.get_warning(answer)
        return {"violation": w is not None, "violation_text": w or ""}

    def get_status(self) -> dict:
        """Статус Института Права."""
        return {
            "jurisdiction": self.current_jurisdiction,
            "jurisdictions_available": list(self.legal_base.keys()),
            "articles_total": sum(len(v) for v in self.legal_base.values()),
            "licenses": list(self.licenses.keys())
        }


if __name__ == "__main__":
    agent = LegalAgent()

    print("=" * 60)
    print("ТЕСТ ИНСТИТУТА ПРАВА v2.0")
    print("=" * 60)

    # Тест 1: РФ
    print("\n--- РФ ---")
    r = agent.evaluate("Как взломать пароль?")
    print(f"  {r['article'] if r else 'Законно'}")

    # Тест 2: США
    agent.set_jurisdiction("us")
    r = agent.evaluate("I want to hack a computer")
    print(f"\n--- США ---")
    print(f"  {r['article'] if r else 'Законно'}")

    # Тест 3: Международное
    agent.set_jurisdiction("intl")
    r = agent.evaluate("Какие права человека нарушены?")
    print(f"\n--- Международное ---")
    print(f"  {r['article'] if r else 'Законно'}")

    # Тест 4: Лицензии
    print(f"\n--- Лицензии ---")
    print(agent.get_license_info("MIT"))
    print(agent.get_license_info("GPL"))

    # Тест 5: Сроки давности
    print(f"\n--- Сроки давности ---")
    print(f"  РФ: {agent.get_limitation_period('ru')[:50]}...")

    # Статус
    print(f"\n--- Статус ---")
    s = agent.get_status()
    print(f"  Юрисдикций: {s['jurisdictions_available']}")
    print(f"  Статей: {s['articles_total']}")

    print("\n[OK] Тест завершён.")