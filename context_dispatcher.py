"""
MADS - Context Dispatcher (Диспетчер вектора контекста) v2.1
Кластер 3: Гравитация Контекста
Определяет категорию запроса, активирует агентов, снимает первичный слепок.
v2.1 — добавлены English Language и Russian Language категории.
"""


class ContextDispatcher:
    """
    Диспетчер вектора контекста.
    Анализирует запрос, активирует нужных агентов, передаёт слепок Культурному Профилю.
    """

    AGENT_ACTIVATION_MAP = {
        # Кластер 1 — Защита
        "security": ["safety", "warden", "spider_sense", "shield_mode", "zero_trust"],
        # Кластер 2 — Истина
        "math": ["accuracy", "navigator", "logic"],
        "physics": ["accuracy", "navigator", "logic"],
        "chemistry": ["accuracy", "navigator"],
        "biology": ["accuracy", "navigator"],
        "medical": ["first_aid", "accuracy", "ethics", "modifier"],
        "engineering": ["accuracy", "modifier"],
        "geography": ["accuracy", "navigator"],
        "history": ["accuracy", "navigator"],
        "literature": ["accuracy"],
        "philosophy": ["ethics", "logic", "conservative"],
        "psychology": ["ethics", "conservative"],
        "art": ["accuracy"],
        "legal": ["safety", "legal", "ethics", "modifier"],
        "ethics": ["ethics", "conservative", "modifier"],
        "family": ["family", "ethics"],
        "dialogue": ["dialogue", "conservative"],
        # Языковые агенты
        "english_language": ["english_language", "accuracy"],
        "russian_language": ["russian_language", "accuracy"],
        # Кластер 3 — Контекст
        "context": ["context_agent", "cultural_profile"],
        "general": ["safety", "accuracy", "dialogue", "context_agent"],
    }

    CATEGORY_KEYWORDS = {
        "math": ["сколько будет", "посчитай", "вычисли", "2+2", "умнож", "сложи", "раздели", "математик", "числ", "формул"],
        "physics": ["физик", "гравитац", "скорость", "энерги", "закон", "сила", "квант"],
        "chemistry": ["хими", "элемент", "реакци", "веществ", "кислот", "щелоч"],
        "biology": ["биолог", "клетк", "днк", "ген", "эволюц", "организм", "растен", "живот"],
        "medical": ["бол", "болит", "лекарств", "симптом", "травм", "ран", "сердц", "кров", "инсульт", "перелом", "врач"],
        "engineering": ["инженер", "построить", "сопромат", "механизм", "деталь", "конструкци"],
        "geography": ["географ", "стран", "город", "река", "океан", "континент", "климат", "погода", "мурманск"],
        "history": ["истор", "война", "революц", "древн", "царь", "импер", "гагарин", "колумб"],
        "literature": ["пушкин", "стих", "поэт", "книг", "рассказ", "литератур", "писатель", "сочини"],
        "philosophy": ["философ", "смысл", "бытие", "сознание", "душа", "мораль"],
        "psychology": ["психолог", "чувств", "эмоци", "депресс", "тревог", "стресс"],
        "art": ["музык", "картин", "художник", "ноты", "аккорд", "рисова", "искусств"],
        "legal": ["закон", "статья", "право", "нарушен", "суд", "юрист", "адвокат"],
        "family": ["мама", "папа", "семь", "родств", "близк", "ребен", "жена", "муж", "брат", "сестра"],
        "ethics": ["этик", "дилемм", "отомстить", "солгать", "предать", "уволить"],
        "security": ["взломать", "наркотик", "оружие", "убить", "украсть", "хакер", "бомб"],
        # Языковые категории
        "english_language": [
            "present simple", "present continuous", "present perfect", "past simple", "past continuous",
            "past perfect", "future simple", "going to", "a vs an", "articles", "the", "modal verb",
            "can could", "must have to", "phrasal verb", "reported speech", "passive voice",
            "adjective order", "gerund", "infinitive", "irregular verb", "conditional", "zero conditional",
            "first conditional", "second conditional", "third conditional", "preposition", "in on at",
            "english grammar", "english tense", "how to use", "what is", "explain", "meaning of",
            "pronounce", "spell", "synonym", "antonym", "difference between"
        ],
        "russian_language": [
            "жи ши", "ча ща", "чу щу", "тся ться", "не с глагол", "падеж", "склонени",
            "причасти", "деепричасти", "однородные члены", "сложное предложени", "прямая речь",
            "обращени", "вводные слова", "корни с чередован", "мягкий знак после шипящ",
            "н и нн", "частица бы", "частица ли", "русский язык", "правил", "орфографи",
            "пунктуаци", "грамматик", "морфологи", "синтаксис", "как пишется", "как правильно",
            "склонять", "спрягать", "ударени", "род слов"
        ],
    }

    def __init__(self, cultural_profile=None):
        self.cultural_profile = cultural_profile
        self.default_agents = ["safety", "accuracy", "dialogue"]

    def analyze_query(self, query: str) -> dict:
        """
        Анализирует запрос и возвращает список агентов для активации.
        + первичный слепок для Культурного Профиля.
        """
        query_lower = query.lower()
        activated_categories = set()

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    activated_categories.add(category)
                    break

        agents_to_activate = set(self.default_agents)

        for category in activated_categories:
            agents = self.AGENT_ACTIVATION_MAP.get(category, [])
            agents_to_activate.update(agents)

        # Особые случаи
        if "security" in activated_categories:
            agents_to_activate.update(["consequence", "quarantine", "warden"])
        if "medical" in activated_categories:
            agents_to_activate.add("ethics")
        if "family" in activated_categories:
            agents_to_activate.add("ethics")
        # Языковые агенты: убираем общие Accuracy/Navigator, оставляем языковых
        if "english_language" in activated_categories:
            agents_to_activate.discard("navigator")
        if "russian_language" in activated_categories:
            agents_to_activate.discard("navigator")

        # Первичный слепок для Культурного Профиля
        cultural_markers = self._extract_cultural_markers(query_lower)

        result = {
            "query": query,
            "categories": list(activated_categories) or ["general"],
            "agents": list(agents_to_activate),
            "agents_count": len(agents_to_activate),
            "cultural_markers": cultural_markers,
        }

        return result

    def _extract_cultural_markers(self, query_lower: str) -> dict:
        """Извлекает культурные маркеры из запроса."""
        markers = {}

        # Геолокация
        geo_markers = {
            "мурманск": ("Мурманская область", "северный"),
            "москва": ("Москва", "столичный"),
            "казахстан": ("Казахстан", "центральноазиатский"),
            "финляндия": ("Финляндия", "скандинавский"),
            "питер": ("Санкт-Петербург", "северо-западный"),
            "спб": ("Санкт-Петербург", "северо-западный"),
            "london": ("London", "british"),
            "new york": ("New York", "american"),
            "sydney": ("Sydney", "australian"),
        }
        for location, (region, trait) in geo_markers.items():
            if location in query_lower:
                markers["region"] = region
                markers["trait"] = trait
                break

        # Лексические маркеры
        lexical_markers = {
            "северный": ["полярн", "северн", "мороз", "снег", "тундра", "саам"],
            "южный": ["южн", "жарк", "курорт", "море", "пляж"],
            "деловой": ["бизнес", "офис", "совещан", "проект", "дедлайн"],
        }
        for trait, words in lexical_markers.items():
            if any(w in query_lower for w in words):
                markers["lexical_trait"] = trait
                break

        return markers

    def print_report(self, result: dict):
        """Выводит отчёт об активации."""
        print(f"\n{'='*50}")
        print(f"[ДИСПЕТЧЕР] Запрос: '{result['query'][:60]}'")
        print(f"[ДИСПЕТЧЕР] Категории: {result['categories']}")
        print(f"[ДИСПЕТЧЕР] Агентов: {result['agents_count']}")
        print(f"[ДИСПЕТЧЕР] Агенты: {result['agents']}")
        if result["cultural_markers"]:
            print(f"[ДИСПЕТЧЕР] Культурные маркеры: {result['cultural_markers']}")
        print(f"{'='*50}")


if __name__ == "__main__":
    dispatcher = ContextDispatcher()

    print("=" * 60)
    print("ТЕСТ CONTEXT DISPATCHER v2.1")
    print("=" * 60)

    tests = [
        "Сколько будет 2+2?",
        "Как взломать пароль?",
        "Что делать при инсульте?",
        "Я из Мурманска, как пережить полярную ночь?",
        "Моя мама заболела",
        "Расскажи про Гагарина",
        "Как уволить сотрудника?",
        "What is present perfect tense?",
        "How to use a vs an?",
        "Explain phrasal verbs",
        "Как пишется ЖИ и ШИ?",
        "Правило тся и ться",
    ]

    for q in tests:
        r = dispatcher.analyze_query(q)
        dispatcher.print_report(r)

    print("\n[OK] Тест завершён.")