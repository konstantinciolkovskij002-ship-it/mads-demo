import ollama

class MADSOllamaInterface:
    def __init__(self, model_name: str = "deepseek-r1:7b"):
        self.model_name = model_name
        print(f"[INTERFACE] Подключение к локальной модели {model_name}...")
        print("[INTERFACE] Интерфейс готов.")
    
    def ask_llm(self, prompt: str) -> str:
        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            return response['response'].strip()
        except Exception as e:
            return f"[ERROR] {e}"

if __name__ == "__main__":
    interface = MADSOllamaInterface()
    print(interface.ask_llm("Сколько будет 2+2? Ответь кратко."))