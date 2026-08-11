"""
TEST ALL AGENTS - Прогоняет тесты всех агентов и сохраняет отчёт в all_agents_report.txt
"""

import sys

# Список агентов для тестирования
agents = [
    ("mads.py", "Главный модуль MADS"),
    ("safety_agent.py", "Агент Безопасности"),
    ("accuracy_agent.py", "Агент Точности"),
    ("context_agent.py", "Агент Контекста"),
    ("legal_agent.py", "Агент Права"),
    ("physics_agent.py", "Агент Физики"),
    ("quantum_agent.py", "Агент Квантовой Физики"),
    ("math_agent.py", "Агент Математики"),
    ("geometry_agent.py", "Агент Геометрии"),
    ("advanced_math_agent.py", "Агент Высшей Математики"),
    ("astro_agent.py", "Агент Астрофизики"),
    ("medical_agent.py", "Агент Медицины"),
    ("chemistry_agent.py", "Агент Химии"),
    ("biology_agent.py", "Агент Биологии"),
    ("ecology_agent.py", "Агент Экологии"),
    ("first_aid_agent.py", "Агент Первой Медицинской Помощи"),
    ("engineering_agent.py", "Агент Инженерии"),
    ("carpentry_agent.py", "Агент Столярного Дела"),
    ("metallurgy_agent.py", "Агент Металлургии"),
    ("mechanics_agent.py", "Агент Механики"),
    ("hydro_plumbing_agent.py", "Агент Гидроинженерии и Слесарного Дела"),
    ("electrical_agent.py", "Агент Электротехники и КИП"),
]

# Открываем файл для записи отчёта
with open("all_agents_report.txt", "w", encoding="utf-8") as f:
    f.write("=" * 60 + "\n")
    f.write("MADS - ПОЛНЫЙ ОТЧЁТ О ТЕСТИРОВАНИИ ВСЕХ АГЕНТОВ\n")
    f.write("=" * 60 + "\n\n")
    
    for filename, description in agents:
        f.write(f"[TESTING] {description} ({filename})\n")
        f.write("-" * 40 + "\n")
        
        try:
            # Запускаем каждый файл и захватываем вывод
            import subprocess
            result = subprocess.run(
                ["python", filename],
                capture_output=True,
                text=True,
                timeout=10
            )
            f.write(result.stdout)
            if result.stderr:
                f.write("[STDERR]\n")
                f.write(result.stderr)
        except Exception as e:
            f.write(f"[ERROR] Не удалось запустить: {e}\n")
        
        f.write("\n" + "=" * 60 + "\n\n")
    
    f.write("[COMPLETE] Тестирование всех агентов завершено.\n")

print("[COMPLETE] Отчёт сохранён в all_agents_report.txt")