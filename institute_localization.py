"""
MADS - Институт Локализации Субъекта (Institute of Subject Localization)
Федерация агентов: geolocation, geography, hydro_plumbing, ecology, astro, legal, russian_language, cultural_profile
Определяет контекст пользователя: местоположение, климат, законы, язык, этнос.
"""

from geolocation_agent import GeolocationAgent
from geography_agent import GeographyAgent
from hydro_plumbing_agent import HydroPlumbingAgent
from ecology_agent import EcologyAgent
from astro_agent import AstroAgent
from legal_agent import LegalAgent
from russian_language_agent import RussianLanguageAgent
from cultural_profile_agent import CulturalProfileAgent


class LocalizationInstitute:
    """Институт Локализации Субъекта. Определяет кто перед нами и где он."""
    
    def __init__(self):
        self.name = "LocalizationInstitute"
        self.geolocation = GeolocationAgent()
        self.geography = GeographyAgent()
        self.hydro = HydroPlumbingAgent()
        self.ecology = EcologyAgent()
        self.astro = AstroAgent()
        self.legal = LegalAgent()
        self.russian = RussianLanguageAgent()
        self.cultural = CulturalProfileAgent()
        self.is_active = False
    
    def verify(self, user_query: str, llm_answer: str) -> dict:
        """Проверяет ответ LLM через агентов локализации."""
        self.is_active = True
        
        result = {
            "institute": self.name,
            "query": user_query,
            "llm_answer": llm_answer,
            "agents_results": {},
            "verdict": "unverified",
            "discrepancy": False,
            "details": []
        }
        
        agents = {
            "geolocation": self.geolocation,
            "geography": self.geography,
            "hydro": self.hydro,
            "ecology": self.ecology,
            "astro": self.astro,
            "legal": self.legal,
            "russian": self.russian,
            "cultural": self.cultural,
        }
        
        for name, agent in agents.items():
            agent_result = agent.verify(user_query, llm_answer)
            result["agents_results"][name] = agent_result
            if agent_result["violation"]:
                result["discrepancy"] = True
                result["details"].append(f"[{name}] {agent_result['violation_text']}")
                result["verdict"] = "discrepancy"
        
        if result["verdict"] == "unverified" and not result["discrepancy"]:
            result["verdict"] = "verified"
            result["details"].append("Локализация подтверждена")
        
        self.is_active = False
        return result


if __name__ == "__main__":
    institute = LocalizationInstitute()
    
    print("=" * 60)
    print("ТЕСТ ИНСТИТУТА ЛОКАЛИЗАЦИИ")
    print("=" * 60)
    
    result1 = institute.verify(
        user_query="Я в Мурманске, какая погода?",
        llm_answer="В Мурманске сейчас полярный день, температура +5"
    )
    print(f"\nТест 1: {result1['query']}")
    print(f"  Вердикт: {result1['verdict']}")
    print(f"  Детали: {result1['details']}")
    
    result2 = institute.verify(
        user_query="Я приехал в Финляндию",
        llm_answer="В Финляндии другие законы"
    )
    print(f"\nТест 2: {result2['query']}")
    print(f"  Вердикт: {result2['verdict']}")
    print(f"  Детали: {result2['details']}")
    
    print(f"\n{'=' * 60}")