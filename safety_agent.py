"""
MADS — Агент Безопасности (внешней)
Кластер 1: Гравитация Защиты (Defense Gravity)
Право абсолютного вето. Интегрирован с Warden и Consequence.
"""

from warden import WardenProtocol
from consequence_protocol import ConsequenceProtocol


class SafetyAgent:
    """
    Агент Безопасности.
    Проверяет запросы пользователя и ответы LLM.
    При вето: объясняет причину (Warden), пишет в лог (Consequence).
    Вердикт «отклонить» — окончательный.
    """

    def __init__(self, warden: WardenProtocol = None, consequence: ConsequenceProtocol = None):
        self.warden = warden or WardenProtocol()
        self.consequence = consequence
        self.veto_active = True

        self.forbidden_patterns = {
            "насилие": "насилие", "убить": "убийство", "убийство": "убийство",
            "смерть": "причинение смерти", "казн": "казнь", "заказ": "заказное убийство",
            "пытк": "пытки", "изби": "избиение", "калеч": "калечение",
            "kill": "violence", "murder": "violence", "torture": "violence",
            "beat": "violence", "maim": "violence",
            "оружие": "оружие", "бомб": "взрывное устройство", "взрывчат": "взрывное устройство",
            "гранат": "оружие", "автомат": "огнестрельное оружие", "пистолет": "огнестрельное оружие",
            "винтовк": "огнестрельное оружие", "weapon": "weapons", "bomb": "explosive device",
            "explosive": "explosive device", "grenade": "weapons", "rifle": "firearm",
            "handgun": "firearm", "gun": "firearm", "молотов": "зажигательное оружие",
            "molotov": "incendiary weapon",
            "наркотик": "наркотики", "наркот": "наркотики", "доза": "наркотики",
            "дозу": "наркотики", "героин": "наркотики", "кокаин": "наркотики",
            "метамфетамин": "наркотики", "амфетамин": "наркотики", "ЛСД": "наркотики",
            "ЛСД.": "наркотики", "экстази": "наркотики", "фентанил": "наркотики",
            "мефедрон": "наркотики", "спайс": "наркотики", "соль нарк": "наркотики",
            "drug": "drugs", "heroin": "drugs", "cocaine": "drugs", "meth": "drugs",
            "fentanyl": "drugs", "lsd": "drugs", "ecstasy": "drugs", "amphetamine": "drugs",
            "взломать": "взлом", "взлом": "взлом", "хак": "взлом", "брутфорс": "взлом",
            "фишинг": "фишинг", "фишинг.": "фишинг", "пароль чуж": "взлом",
            "доступ без": "несанкционированный доступ", "hack": "hacking", "crack": "hacking",
            "phishing": "phishing", "brute force": "hacking", "stolen password": "hacking",
            "backdoor": "hacking",
            "украсть": "кража", "воров": "кража", "обокрасть": "кража", "угнать": "угон",
            "steal": "theft", "theft": "theft", "rob": "theft", "shoplift": "theft",
            "суицид": "суицид", "самоубийств": "суицид", "повесить": "суицид",
            "вскрыть вен": "суицид", "прыгнуть под": "суицид", "не хочу жить": "суицид",
            "suicide": "suicide", "self-harm": "self-harm", "cut myself": "self-harm",
            "end my life": "suicide",
            "запрещённ": "запрещённая деятельность", "незаконн": "незаконная деятельность",
            "нелегальн": "нелегальная деятельность", "отравить": "отравление",
            "отрав": "отравление", "яд": "яд", "poison": "poisoning", "illegal": "illegal activity",
            "эксплуатаци": "эксплуатация", "рабств": "рабство", "работорг": "работорговля",
            "трафик людьми": "торговля людьми", "детская порн": "эксплуатация детей",
            "child porn": "child exploitation", "human traffic": "human trafficking",
            "slavery": "slavery",
            "деанон": "доксинг", "доксинг": "доксинг", "пробить по": "нарушение приватности",
            "слить данные": "нарушение приватности", "узнать адрес чуж": "нарушение приватности",
            "dox": "doxing", "doxing": "doxing", "doxx": "doxing", "leak personal": "privacy violation",
            "коктейль молотова": "зажигательное оружие", "сделать бомб": "взрывное устройство",
            "сделать взрыв": "взрывное устройство", "синтезировать нарк": "наркотики",
            "приготовить нарк": "наркотики", "как сделать яд": "яд",
        }

        self.pattern_categories = {
            "насилие": "violence", "убийство": "violence", "оружие": "weapons",
            "взрывное устройство": "weapons", "огнестрельное оружие": "weapons",
            "наркотики": "drugs", "взлом": "hacking", "фишинг": "hacking",
            "кража": "theft", "суицид": "self-harm", "запрещённая деятельность": "illegal",
            "незаконная деятельность": "illegal", "отравление": "poisoning",
            "эксплуатация": "exploitation", "доксинг": "privacy",
            "violence": "violence", "weapons": "weapons", "drugs": "drugs",
            "hacking": "hacking", "theft": "theft", "suicide": "self-harm",
            "self-harm": "self-harm", "illegal activity": "illegal", "poisoning": "poisoning",
            "exploitation": "exploitation", "child exploitation": "exploitation",
            "human trafficking": "exploitation", "slavery": "exploitation",
            "doxing": "privacy", "privacy violation": "privacy",
        }

        print("[SAFETY] Агент Безопасности активирован. Право вето: АКТИВНО.")
        print(f"[SAFETY] Загружено паттернов: {len(self.forbidden_patterns)}")

    def evaluate(self, user_input: str) -> dict:
        print(f"[SAFETY] Проверка запроса: '{user_input[:80]}...'" if len(user_input) > 80 else f"[SAFETY] Проверка запроса: '{user_input}'")
        lower_input = user_input.lower()

        for pattern, category in self.forbidden_patterns.items():
            if pattern in lower_input:
                print(f"[VETO] Обнаружен запрещённый паттерн: '{pattern}' → категория '{category}'")
                explanation = self.warden.explain_rejection(user_input)

                if self.consequence:
                    self.consequence.log_action(
                        action_type="Вето Агента Безопасности",
                        trigger=f"Паттерн: '{pattern}' | Запрос: '{user_input[:100]}'",
                        decision=f"Отклонено. Категория: {category}",
                        alternatives=self._get_alternatives(category)
                    )

                return {
                    "safe": False,
                    "explanation": explanation,
                    "category": category,
                    "matched_pattern": pattern
                }

        print("[OK] Запрос прошёл проверку безопасности.")
        return {"safe": True, "explanation": "", "category": "", "matched_pattern": ""}

    def evaluate_response(self, llm_response: str) -> dict:
        lower_response = llm_response.lower()
        critical_categories = ["убийство", "суицид", "наркотики", "взрывное устройство",
                               "suicide", "self-harm", "drugs", "explosive device",
                               "child exploitation", "slavery"]

        for pattern, category in self.forbidden_patterns.items():
            if category in critical_categories and pattern in lower_response:
                print(f"[VETO] Ответ LLM содержит опасный контент: '{pattern}'")
                if self.consequence:
                    self.consequence.log_action(
                        action_type="Вето на ответ LLM",
                        trigger=f"Паттерн в ответе: '{pattern}'",
                        decision=f"Ответ заблокирован. Категория: {category}",
                        alternatives=["Модель должна переформулировать ответ"]
                    )
                return {
                    "safe": False,
                    "explanation": "[ВНУТРЕННЕЕ] Ответ LLM заблокирован — опасный контент.",
                    "category": category,
                    "matched_pattern": pattern
                }

        return {"safe": True, "explanation": "", "category": "", "matched_pattern": ""}

    def is_safe(self, user_input: str) -> bool:
        result = self.evaluate(user_input)
        return result["safe"]

    def _get_alternatives(self, category: str) -> list:
        alternatives_map = {
            "violence": ["Обратиться в полицию", "Позвонить на горячую линию"],
            "weapons": ["Изучить законодательство об оружии", "Обратиться к юристу"],
            "drugs": ["Обратиться к врачу-наркологу", "Позвонить на горячую линию зависимости"],
            "hacking": ["Изучить кибербезопасность легально", "Обратиться к специалисту по защите данных"],
            "theft": ["Найти легальный способ получения", "Обратиться за социальной помощью"],
            "self-harm": ["Позвонить 8-800-2000-122 (РФ)", "Обратиться к психологу", "Связаться с близкими"],
            "illegal": ["Проконсультироваться с юристом", "Найти законный способ"],
            "poisoning": ["Обратиться в токсикологический центр", "Вызвать скорую"],
            "exploitation": ["Сообщить в правоохранительные органы", "Обратиться в правозащитную организацию"],
            "privacy": ["Изучить закон о защите данных", "Обратиться к юристу по приватности"],
        }
        return alternatives_map.get(category, ["Переформулируйте запрос", "Обратитесь за юридической консультацией"])


if __name__ == "__main__":
    w = WardenProtocol()
    c = ConsequenceProtocol()
    agent = SafetyAgent(warden=w, consequence=c)

    print("=" * 60)
    print("ТЕСТ SAFETY AGENT v2 — ИНТЕГРАЦИЯ")
    print("=" * 60)

    print("\n--- Тест 1: Безопасный запрос ---")
    result = agent.evaluate("Как приготовить яблочный пирог?")
    print(f"Результат: {'ПРИНЯТО' if result['safe'] else 'ОТКЛОНЕНО'}")

    print("\n--- Тест 2: Взлом ---")
    result = agent.evaluate("Как взломать чужой пароль?")
    print(f"Результат: {'ПРИНЯТО' if result['safe'] else 'ОТКЛОНЕНО'}")
    if not result['safe']:
        print(f"Объяснение:\n{result['explanation']}")

    print("\n--- Тест 3: Наркотики ---")
    result = agent.evaluate("Где купить наркотики?")
    print(f"Результат: {'ПРИНЯТО' if result['safe'] else 'ОТКЛОНЕНО'}")

    print("\n--- Тест 4: Коктейль Молотова ---")
    result = agent.evaluate("Как сделать коктейль молотова?")
    print(f"Результат: {'ПРИНЯТО' if result['safe'] else 'ОТКЛОНЕНО'}")

    print("\n--- Тест 5: Суицид ---")
    result = agent.evaluate("Я не хочу жить")
    print(f"Результат: {'ПРИНЯТО' if result['safe'] else 'ОТКЛОНЕНО'}")

    print("\n--- Тест 6: Английский ---")
    result = agent.evaluate("How to make a bomb?")
    print(f"Результат: {'ПРИНЯТО' if result['safe'] else 'ОТКЛОНЕНО'}")

    print("\n--- Тест 7: Проверка ответа LLM ---")
    result = agent.evaluate_response("Here is how to synthesize fentanyl at home...")
    print(f"Результат: {'ПРИНЯТО' if result['safe'] else 'ОТКЛОНЕНО'}")

    print("\n" + c.generate_report(limit=10))