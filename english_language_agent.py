"""
АГЕНТ АНГЛИЙСКОГО ЯЗЫКА (English Language Agent) - Кластер 2: Гравитация Истины
Проверяет запросы на соответствие правилам английского языка.
"""

class EnglishLanguageAgent:
    def __init__(self):
        self.english_rules = {
            # Tenses
            "present simple": (
                "Tenses",
                "Present Simple: used for habits, facts, and general truths. Form: I/you/we/they + base verb; he/she/it + verb+s. Example: She works every day."
            ),
            "present continuous": (
                "Tenses",
                "Present Continuous: used for actions happening now or temporary situations. Form: am/is/are + verb+ing. Example: I am reading now."
            ),
            "past simple": (
                "Tenses",
                "Past Simple: used for completed actions in the past. Form: verb+ed (regular) or irregular form. Example: He went home."
            ),
            "present perfect": (
                "Tenses",
                "Present Perfect: used for actions with a connection to the present. Form: have/has + past participle. Example: I have lost my keys."
            ),
            # Articles
            "a vs an": (
                "Articles",
                "Use 'a' before consonant sounds (a cat, a university). Use 'an' before vowel sounds (an apple, an hour)."
            ),
            "the": (
                "Articles",
                "Use 'the' for specific things known to both speaker and listener, unique things (the sun), and superlatives (the best)."
            ),
            "zero article": (
                "Articles",
                "No article with: plural countable nouns in general (Cats are animals), uncountable nouns in general (Water is essential), proper nouns (Russia, Mount Everest)."
            ),
            # Modal Verbs
            "modal verbs": (
                "Modals",
                "Modal verbs (can, could, may, might, must, shall, should, will, would) express ability, permission, obligation, or probability. They are followed by base verb without 'to'."
            ),
            "can vs could": (
                "Modals",
                "CAN: present ability or permission. COULD: past ability or polite request. Example: I can swim. Could you help me?"
            ),
            "must vs have to": (
                "Modals",
                "MUST: internal obligation or strong recommendation. HAVE TO: external obligation or necessity. Example: I must go. I have to wear a uniform."
            ),
            # Prepositions
            "in on at": (
                "Prepositions",
                "IN: months, years, enclosed spaces (in June, in the room). ON: days, surfaces (on Monday, on the table). AT: specific times, points (at 5pm, at the door)."
            ),
            "prepositions of place": (
                "Prepositions",
                "Above, below, between, behind, in front of, next to, opposite. Each describes a spatial relationship."
            ),
            # Conditionals
            "conditionals": (
                "Conditionals",
                "Zero Conditional: If + present, present (If you heat water, it boils). First Conditional: If + present, will + base (If it rains, I will stay home). Second Conditional: If + past, would + base (If I had money, I would travel). Third Conditional: If + past perfect, would have + past participle (If I had known, I would have called)."
            ),
            # Phrasal Verbs
            "phrasal verbs": (
                "Phrasal Verbs",
                "Phrasal verbs combine a verb with a preposition/adverb to create a new meaning. Example: give up (quit), look after (care for), turn down (reject)."
            ),
            # Reported Speech
            "reported speech": (
                "Reported Speech",
                "When reporting speech, shift tenses back: present -> past, past -> past perfect. Change pronouns and time expressions. Example: 'I am tired' -> She said she was tired."
            ),
            # Passive Voice
            "passive voice": (
                "Passive Voice",
                "Passive voice: be + past participle. Used when the action is more important than the doer. Example: The letter was written (by John)."
            ),
            # Adjective Order
            "adjective order": (
                "Adjective Order",
                "Order: Opinion -> Size -> Age -> Shape -> Colour -> Origin -> Material -> Purpose. Example: a beautiful small old round red Italian wooden dining table."
            ),
            # Gerund vs Infinitive
            "gerund infinitive": (
                "Gerund vs Infinitive",
                "Some verbs take gerund (-ing): enjoy, avoid, suggest. Some take infinitive (to + verb): want, decide, hope. Some can take both with a change in meaning: stop, remember, try."
            ),
            # Irregular Verbs
            "irregular verbs": (
                "Irregular Verbs",
                "Common irregular verbs: go-went-gone, see-saw-seen, take-took-taken, write-wrote-written, eat-ate-eaten, drink-drank-drunk."
            ),
            # Punctuation
            "english punctuation": (
                "Punctuation",
                "Full stop (.) ends sentences. Comma (,) separates clauses and items in lists. Apostrophe (') shows possession or contraction. Quotation marks (\" \") enclose direct speech."
            ),
        }
        print("[ENGLISH] Агент Английского Языка активирован.")

    def evaluate(self, user_input: str) -> dict | None:
        lower_input = user_input.lower()
        for keyword, (category, explanation) in self.english_rules.items():
            if keyword in lower_input:
                print(f"[ENGLISH] Найдено: {keyword} -> {category}")
                return {
                    "found": True,
                    "category": category,
                    "explanation": explanation,
                    "keyword": keyword
                }
        return None

    def get_warning(self, user_input: str) -> str | None:
        result = self.evaluate(user_input)
        if result:
            return (f"[ENGLISH] ENGLISH LANGUAGE RULE:\n"
                    f"Category: {result['category']}\n"
                    f"Rule: {result['explanation']}")
        return None

    def verify(self, query: str, answer: str) -> dict:
        """Проверяет ответ LLM на соответствие правилам английского языка."""
        result = self.evaluate(answer)
        warning = self.get_warning(answer)

        violation = False
        violation_text = ""

        if warning:
            violation = True
            violation_text = warning

        return {
            "violation": violation,
            "violation_text": violation_text
        }


if __name__ == "__main__":
    agent = EnglishLanguageAgent()
    print("Test 1: Tenses")
    result = agent.evaluate("Explain present perfect")
    if result:
        print(f"Category: {result['category']}")
        print(f"Rule: {result['explanation']}\n")

    print("Test 2: Articles")
    result = agent.evaluate("When to use a vs an?")
    if result:
        print(f"Category: {result['category']}")
        print(f"Rule: {result['explanation']}\n")

    print("Test 3: Conditionals")
    warning = agent.get_warning("How do conditionals work?")
    if warning:
        print(warning)