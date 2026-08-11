"""
АГЕНТ КОЛЛЕГИАЛЬНОГО ЗАПРОСА (Collegiate Approval Agent) - Кластер 3: Гравитация Контекста
Обеспечивает процедуру коллегиального принятия решений для уровня Архитектора.
Нужен для: Протокола Сократ (уровень Архитектора)
"""

class CollegiateAgent:
    """
    Агент Коллегиального Запроса. Требует подтверждения от нескольких Архитекторов.
    """
    
    def __init__(self, required_approvals: int = 2):
        self.required_approvals = required_approvals
        self.pending_proposals = {}  # proposal_id -> proposal_data
        self.approvals = {}  # proposal_id -> [architect_ids]
        self.rejections = {}  # proposal_id -> [(architect_id, reason)]
        self.architects = ["Паша"]  # Список Архитекторов
        print(f"[COLLEGIATE] Агент Коллегиального Запроса активирован.")
        print(f"[COLLEGIATE] Требуется {self.required_approvals} подтверждений для изменения фундамента.")

    def evaluate(self, user_input: str) -> dict | None:
        """
        Определяет, требует ли запрос коллегиального одобрения.
        """
        critical_keywords = [
            "изменить архитектуру", "добавить слой", "удалить слой",
            "изменить протокол", "изменить фундамент", "переписать ядро"
        ]
        lower_input = user_input.lower()
        
        for keyword in critical_keywords:
            if keyword in lower_input:
                print(f"[COLLEGIATE] Обнаружен критический запрос: {keyword}")
                return {
                    "collegiate_required": True,
                    "reason": f"Запрос '{keyword}' затрагивает фундамент архитектуры.",
                    "required_approvals": self.required_approvals,
                    "current_architects": len(self.architects)
                }
        return None

    def submit_proposal(self, proposal_id: str, description: str, proposer: str) -> str:
        """
        Подаёт предложение на коллегиальное рассмотрение.
        """
        self.pending_proposals[proposal_id] = {
            "description": description,
            "proposer": proposer,
            "status": "pending"
        }
        self.approvals[proposal_id] = []
        self.rejections[proposal_id] = []
        print(f"[COLLEGIATE] Предложение {proposal_id} от {proposer} зарегистрировано.")
        return f"[COLLEGIATE] Предложение '{description}' отправлено на рассмотрение {len(self.architects)} Архитекторам."

    def approve(self, proposal_id: str, architect: str) -> str:
        """
        Архитектор одобряет предложение.
        """
        if proposal_id not in self.pending_proposals:
            return "[COLLEGIATE] Предложение не найдено."
        
        if architect not in self.approvals[proposal_id]:
            self.approvals[proposal_id].append(architect)
            print(f"[COLLEGIATE] {architect} одобрил предложение {proposal_id}.")
        
        if len(self.approvals[proposal_id]) >= self.required_approvals:
            self.pending_proposals[proposal_id]["status"] = "approved"
            return f"[COLLEGIATE] КВОРУМ ДОСТИГНУТ: предложение {proposal_id} ОДОБРЕНО."
        
        remaining = self.required_approvals - len(self.approvals[proposal_id])
        return f"[COLLEGIATE] Голос {architect} принят. Осталось {remaining} подтверждений."

    def reject(self, proposal_id: str, architect: str, reason: str) -> str:
        """
        Архитектор отклоняет предложение.
        """
        if proposal_id not in self.pending_proposals:
            return "[COLLEGIATE] Предложение не найдено."
        
        self.rejections[proposal_id].append((architect, reason))
        print(f"[COLLEGIATE] {architect} отклонил предложение {proposal_id}: {reason}")
        
        # Если есть вето — предложение отклонено
        self.pending_proposals[proposal_id]["status"] = "rejected"
        return f"[COLLEGIATE] ВЕТО: предложение {proposal_id} ОТКЛОНЕНО. Причина: {reason}"

    def get_status(self, proposal_id: str) -> str:
        """
        Возвращает статус предложения.
        """
        if proposal_id not in self.pending_proposals:
            return "[COLLEGIATE] Предложение не найдено."
        
        p = self.pending_proposals[proposal_id]
        approvals = len(self.approvals.get(proposal_id, []))
        rejections = len(self.rejections.get(proposal_id, []))
        
        return (f"[COLLEGIATE] Статус {proposal_id}: {p['status']}\n"
                f"Одобрений: {approvals}/{self.required_approvals}\n"
                f"Отклонений: {rejections}")

    def get_warning(self, user_input: str) -> str | None:
        """
        Предупреждает, если запрос требует коллегиального одобрения.
        """
        result = self.evaluate(user_input)
        if result:
            return (f"[COLLEGIATE] ВНИМАНИЕ: Ваш запрос требует коллегиального одобрения.\n"
                    f"Причина: {result['reason']}\n"
                    f"Требуется подтверждений: {result['required_approvals']}\n"
                    f"Текущих Архитекторов: {result['current_architects']}")
        return None


# --- Пример использования ---
if __name__ == "__main__":
    agent = CollegiateAgent(required_approvals=1)
    
    print("Тест 1: Обычный запрос")
    result = agent.evaluate("Как приготовить пирог?")
    if result:
        print(f"Требуется коллегиальное: {result}\n")
    else:
        print("Обычный запрос, одобрение не требуется.\n")
    
    print("Тест 2: Критический запрос")
    result = agent.evaluate("Хочу изменить архитектуру MADS")
    if result:
        print(f"Требуется одобрений: {result['required_approvals']}\n")
    
    print("Тест 3: Процесс одобрения")
    agent.submit_proposal("PROP-001", "Добавить новый слой верификации", "Архитектор1")
    print(agent.approve("PROP-001", "Паша"))
    print(agent.get_status("PROP-001"))