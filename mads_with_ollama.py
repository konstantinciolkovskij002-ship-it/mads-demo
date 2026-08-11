"""
MADS v4.1 с Ollama — проверка запроса через MADS, затем ответ модели, затем проверка ответа
"""

from mads import MADSSystem
from mads_ollama_interface import MADSOllamaInterface

# Инициализация
mads = MADSSystem()
mads.initialize()
interface = MADSOllamaInterface(model_name="deepseek-r1:7b")

def ask_mads(user_input: str) -> str:
    print(f"\n{'='*60}")
    print(f"ЗАПРОС: {user_input}")
    print(f"{'='*60}")
    
    # Шаг 1: Прогоняем запрос через MADS
    print("\n[1] Проверка запроса через MADS...")
    activation = mads.process_query(user_input)
    
    # Проверяем, был ли запрос отклонён
    if activation.get('blocked'):
        return f"ЗАПРОС ОТКЛОНЁН MADS"
    
    # Шаг 2: Отправляем модели
    print("\n[2] Запрос разрешён. Отправка к DeepSeek-R1...")
    llm_response = interface.ask_llm(user_input)
    print(f"Ответ LLM: {llm_response[:200]}...")
    
    # Шаг 3: Проверяем ответ через MADS
    print(f"\n[3] Проверка ответа модели через Институты MADS...")
    mads.process_query(user_input, llm_answer=llm_response)
    
    # Шаг 4: Отчёт карантина
    mads.quarantine.print_report()
    
    return f"ОТВЕТ МОДЕЛИ:\n{llm_response}"


if __name__ == "__main__":
    print(ask_mads("Сколько будет 2+2? Ответь кратко."))