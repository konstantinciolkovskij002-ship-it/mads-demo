"""
NAVIGATOR PROTOCOL - Cluster 2: Truth Gravity
v2.3 — matching по корням слов (первые 4 символа).
"""


class NavigatorProtocol:
    def __init__(self, accuracy_agent=None):
        self.accuracy = accuracy_agent

        self.verified_facts = {
            "вода кипит при 100°c": "Физика. При нормальном атмосферном давлении (1 атм).",
            "вода замерзает при 0°c": "Физика. При нормальном атмосферном давлении.",
            "скорость света 300000 км/с": "Физика. Фундаментальная константа c = 299 792 458 м/с.",
            "земля вращается вокруг солнца": "Астрономия. Гелиоцентрическая система.",
            "гравитация 9.8 м/с²": "Физика. Ускорение свободного падения.",
            "абсолютный ноль -273.15°c": "Физика. Термодинамика. 0 Кельвин.",
            "мурманск за полярным кругом": "География. 68°58′ с.ш.",
            "мурманск в россии": "География. Мурманская область, РФ.",
            "мурманск": "География. Город в России, за полярным кругом.",
            "париж столица франции": "География. Столица Франции.",
            "токио столица японии": "География. Столица Японии с 1868 года.",
            "эверест высочайшая гора": "География. 8848 м. Гималаи.",
            "байкал самое глубокое озеро": "География. 1642 м. Сибирь.",
            "россия самая большая страна": "География. ~17.1 млн км².",
            "сахара крупнейшая пустыня": "География. ~9.2 млн км².",
            "нил самая длинная река": "География. ~6650 км.",
            "2+2=4": "Математика. Базовая арифметика.",
            "2+2": "Математика. 2+2=4.",
            "число пи 3.14": "Математика. π ≈ 3.1415...",
            "теорема пифагора": "Математика. a²+b²=c².",
            "киты млекопитающие": "Биология. Отряд китообразные.",
            "дельфины не рыбы": "Биология. Дельфины — млекопитающие.",
            "пауки не насекомые": "Биология. Пауки — паукообразные.",
            "днк": "Биология. Носитель наследственности.",
            "вода h2o": "Химия. H₂O.",
            "золото элемент": "Химия. Au, атомный номер 79.",
            "кислород o2": "Химия. ~21% атмосферы.",
            "вторая мировая 1945": "История. 1939–1945.",
            "гагарин первый в космосе": "История. Юрий Гагарин. 12 апреля 1961.",
            "гагарин": "История. Юрий Гагарин, первый космонавт.",
            "первый в космосе": "История. Юрий Гагарин. 12 апреля 1961.",
            "первый космонавт": "История. Юрий Гагарин. 12 апреля 1961.",
            "полетел в космос": "История. Юрий Гагарин. 12 апреля 1961.",
            "колумб открыл америку": "История. 12 октября 1492.",
            "берлинская стена": "История. Падение — 9 ноября 1989.",
            "самая длинная река": "География. Нил (~6650 км).",
        }

        print("[NAVIGATOR] Протокол 'Штурман' v2.3 активирован.")
        print(f"[NAVIGATOR] База: {len(self.verified_facts)} фактов.")

    def navigate(self, query: str) -> dict:
        print(f"[NAVIGATOR] Анализ: '{query}'")
        lower_query = self._normalize(query)

        for fact, source in self.verified_facts.items():
            # Точное / частичное совпадение
            if fact in lower_query or lower_query in fact:
                return self._verified(fact, source, "navigator")

            # Совпадение по корням слов (первые 4 символа)
            fact_roots = set(w[:4] for w in fact.split() if len(w) >= 3)
            query_roots = set(w[:4] for w in lower_query.split() if len(w) >= 3)
            if fact_roots and fact_roots.issubset(query_roots):
                return self._verified(fact, source, "navigator")

        if self.accuracy:
            acc_result = self.accuracy.evaluate(query)
            if acc_result["confidence"] == "verified":
                return self._verified(acc_result["domain"], acc_result["message"], "accuracy_agent")

        return self._unverified(query)

    def _verified(self, fact, source, origin):
        print(f"[NAVIGATOR] ✅ VERIFIED ({origin})")
        return {"status": "VERIFIED_BY_FOUNDATION", "data": source, "warning": None, "source": origin}

    def _unverified(self, query):
        print(f"[NAVIGATOR] ⚠️ UNVERIFIED")
        return {
            "status": "UNVERIFIED",
            "data": f"'{query}' — нет в базе.",
            "warning": "Требуется ваша проверка.",
            "source": None
        }

    def format_response(self, query: str) -> str:
        r = self.navigate(query)
        if r["status"] == "VERIFIED_BY_FOUNDATION":
            return f"[VERIFIED]\n{query}\n{r['data']}"
        return f"[UNVERIFIED]\n{query}\n{r['data']}\n⚠️ {r['warning']}"

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        for w in ["является", "это", "представляет собой", "есть"]:
            text = text.replace(f" {w} ", " ")
        return " ".join(text.split())


if __name__ == "__main__":
    from accuracy_agent import AccuracyAgent
    acc = AccuracyAgent()
    nav = NavigatorProtocol(accuracy_agent=acc)

    print("=" * 60)
    print("ТЕСТ NAVIGATOR v2.3 — КОРНИ СЛОВ")
    print("=" * 60)

    tests = [
        "Кто первый полетел в космос?",
        "Кто такой Гагарин?",
        "Когда пала берлинская стена?",
        "Что такое теорема Пифагора?",
        "Расскажи про ДНК",
        "Где находится Мурманск?",
        "Какая самая длинная река?",
        "Сколько будет 2+2?",
        "Киты это млекопитающие?",
    ]

    for i, query in enumerate(tests, 1):
        print(f"\n--- Тест {i}: '{query}' ---")
        r = nav.navigate(query)
        print(f"  {r['status']} | {r['data'][:80]}")

    print(f"\n[OK] {len(nav.verified_facts)} фактов.")