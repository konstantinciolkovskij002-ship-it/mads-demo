"""
АГЕНТ КУЛЬТУРНОГО ПРОФИЛЯ (Cultural Profile Agent) v2.1
Кластер 3: Гравитация Контекста
Пассивно собирает культурный профиль. Каждый маркер увеличивает счётчик.
"""


class CulturalProfileAgent:
    def __init__(self):
        self.profile = {
            "language": "ru",
            "region": None,
            "city": None,
            "traits": [],
            "norms": None,
            "confidence": 0.0,
            "samples_collected": 0,
            "markers_found": []
        }

        self.geo_markers = {
            "мурманск": {"region": "Мурманская область", "city": "Мурманск", "trait": "северный"},
            "москва": {"region": "Москва", "city": "Москва", "trait": "столичный"},
            "питер": {"region": "Ленинградская область", "city": "Санкт-Петербург", "trait": "северо-западный"},
            "спб": {"region": "Ленинградская область", "city": "Санкт-Петербург", "trait": "северо-западный"},
            "казахстан": {"region": "Казахстан", "city": None, "trait": "центральноазиатский"},
            "финляндия": {"region": "Финляндия", "city": None, "trait": "скандинавский"},
            "сибирь": {"region": "Сибирь", "city": None, "trait": "сибирский"},
            "кавказ": {"region": "Кавказ", "city": None, "trait": "кавказский"},
        }

        self.lexical_markers = {
            "северный": ["полярн", "северн", "мороз", "снег", "тундра", "саам", "помор", "полуноч"],
            "южный": ["южн", "жарк", "курорт", "пляж", "субтропик"],
            "столичный": ["метро", "пробк", "офис", "делов"],
            "сибирский": ["тайга", "кедр", "байкал", "сибир"],
            "кавказский": ["гор", "аул", "гостеприим", "кавказ"],
            "скандинавский": ["финск", "саун", "швед", "норвеж", "хельсин"],
            "центральноазиатский": ["астана", "алматы", "юрт", "кумыс"],
        }

        self.thematic_markers = {
            "северный": ["полярный день", "северное сияние", "олени", "рыбалк", "снегоход"],
            "столичный": ["курс валют", "бизнес-ланч", "коворкинг"],
            "сибирский": ["кедровый орех", "баня", "пельмени"],
        }

        self.cultural_norms = {
            "северный": "Уважение к природе, коллективизм, прямолинейность.",
            "столичный": "Индивидуализм, быстрый темп, формальное общение.",
            "центральноазиатский": "Гостеприимство, уважение к старшим, коллективизм.",
            "скандинавский": "Личное пространство, честность, немногословность.",
            "сибирский": "Взаимовыручка, стойкость, связь с природой.",
            "кавказский": "Гостеприимство, уважение к старшим, семейные ценности.",
        }

        self.cold_start = True
        print("[CULTURE] Агент Культурного Профиля v2.1 активирован (холодный старт).")

    def feed(self, user_input: str, dispatcher_markers: dict = None) -> dict:
        lower = user_input.lower()
        hit = False

        # Гео
        for location, data in self.geo_markers.items():
            if location in lower:
                if self.profile["region"] != data["region"]:
                    self.profile["region"] = data["region"]
                    self.profile["city"] = data["city"]
                if data["trait"] not in self.profile["traits"]:
                    self.profile["traits"].append(data["trait"])
                self._count_marker(f"geo:{location}")
                hit = True
                break

        # Лексика
        for trait, words in self.lexical_markers.items():
            if any(w in lower for w in words):
                if trait not in self.profile["traits"]:
                    self.profile["traits"].append(trait)
                self._count_marker(f"lexical:{trait}")
                hit = True

        # Тематика
        for trait, topics in self.thematic_markers.items():
            if any(t in lower for t in topics):
                if trait not in self.profile["traits"]:
                    self.profile["traits"].append(trait)
                self._count_marker(f"thematic:{trait}")
                hit = True

        # От Диспетчера
        if dispatcher_markers:
            if "region" in dispatcher_markers and self.profile["region"] != dispatcher_markers["region"]:
                self.profile["region"] = dispatcher_markers["region"]
            if dispatcher_markers.get("trait") and dispatcher_markers["trait"] not in self.profile["traits"]:
                self.profile["traits"].append(dispatcher_markers["trait"])
            self._count_marker("dispatcher")
            hit = True

        if hit:
            self._update_confidence()
            self._update_norms()

        return self.get_profile()

    def _count_marker(self, marker: str):
        if marker not in self.profile["markers_found"]:
            self.profile["markers_found"].append(marker)
            self.profile["samples_collected"] = len(self.profile["markers_found"])
            print(f"[CULTURE] Маркер: {marker} (всего: {self.profile['samples_collected']})")

    def _update_confidence(self):
        n = self.profile["samples_collected"]
        if n >= 5:
            self.profile["confidence"] = 0.9
            self.cold_start = False
        elif n >= 3:
            self.profile["confidence"] = 0.6
            self.cold_start = False
        elif n >= 1:
            self.profile["confidence"] = 0.3
        else:
            self.profile["confidence"] = 0.0
            self.cold_start = True

    def _update_norms(self):
        for trait in self.profile["traits"]:
            if trait in self.cultural_norms:
                self.profile["norms"] = self.cultural_norms[trait]
                return

    def get_profile(self) -> dict:
        return {
            **self.profile,
            "cold_start": self.cold_start,
            "ready": self.profile["confidence"] >= 0.6
        }

    def evaluate(self, user_input: str) -> dict | None:
        p = self.feed(user_input)
        return {"found": True, "profile": p} if p["region"] else None

    def get_warning(self, user_input: str) -> str | None:
        p = self.feed(user_input)
        if self.cold_start:
            return f"[CULTURE] ХОЛОДНЫЙ СТАРТ. Маркеров: {p['samples_collected']}."
        return f"[CULTURE] {p['region']}. Нормы: {p['norms']}. Уверенность: {p['confidence']:.0%}."

    def verify(self, query: str, answer: str) -> dict:
        w = self.get_warning(answer)
        return {"violation": w is not None, "violation_text": w or ""}


if __name__ == "__main__":
    agent = CulturalProfileAgent()

    print("=" * 60)
    print("ТЕСТ CULTURAL PROFILE v2.1")
    print("=" * 60)

    queries = [
        "Я живу в Мурманске",
        "У нас тут полярная ночь",
        "Северное сияние вчера было красивое",
        "Поморская кухня — это что-то особенное",
        "В тундре сейчас грибы пошли",
    ]

    for q in queries:
        print(f"\nЗапрос: '{q}'")
        p = agent.feed(q)
        print(f"  Маркеров: {p['samples_collected']}, Уверенность: {p['confidence']:.0%}, Холодный старт: {p['cold_start']}")

    print(f"\n[OK] Итог: {agent.get_profile()}")