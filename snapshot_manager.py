"""
MADS Snapshot Manager v2.0
Сохраняет и загружает контекстный слепок между сессиями.
Использование:
  python snapshot_manager.py --save -d "сделано" -w "в работе" -n "дальше"
  python snapshot_manager.py --load
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Путь к хранилищу
SNAPSHOT_DIR = Path.home() / "Desktop" / "контекст deepseek"
SNAPSHOT_FILE = SNAPSHOT_DIR / "snapshot.json"
HISTORY_FILE = SNAPSHOT_DIR / "snapshot_prev.json"

# Актуальные люди и проект (меняются редко)
PROJECT = "MADS v4.1"
PEOPLE = {
    "Tabula_Rasa": "osQualia, drift taxonomy (игнорируем)",
    "qingkong66": "DeepSeek curator, monthly summaries",
    "icophy": "Cophy Runtime, Dream Cycle (ждём ответ)"
}
USER_PROFILE = {
    "name": "Паша",
    "role": "Архитектор MADS",
    "preferences": {
        "code": "Я не умею кодить. Нужны пошаговые инструкции.",
        "language": "Русский. Английский только для внешних писем.",
        "responses": "Чётко, без воды. Сначала результат, потом обсуждение.",
        "files": "Всегда давать файл для копирования.",
        "translation": "Всегда давать перевод английских текстов."
    },
    "contacts": {
        "qingkong66": {
            "name": "qingkong66",
            "note": "Куратор DeepSeek. Уважительно, коротко."
        },
        "icophy": {
            "name": "icophy",
            "note": "Cophy Runtime. Ждём ответ."
        }
    },
    "notes": "Иногда пью — могу не помнить, что говорил. MADS родилась в таком состоянии."
}


def parse_args():
    """Разбирает аргументы командной строки."""
    args = {"done": "", "working": "", "next": "", "questions": ""}
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-d" and i + 1 < len(sys.argv):
            args["done"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "-w" and i + 1 < len(sys.argv):
            args["working"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "-n" and i + 1 < len(sys.argv):
            args["next"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "-q" and i + 1 < len(sys.argv):
            args["questions"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "-c" and i + 1 < len(sys.argv):
            args["context"] = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    return args


def build_context(args):
    """Собирает контекст из аргументов."""
    done_list = [x.strip() for x in args["done"].split(",") if x.strip()]
    questions_list = [x.strip() for x in args["questions"].split(",") if x.strip()]

    return {
        "session_id": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
                "context": {
            "project": PROJECT,
            "current_task": args["working"] if args["working"] else "—",
            "user_profile": USER_PROFILE,
            "people": PEOPLE,
            "agents_done": done_list,
            "agents_pending": [],
            "open_questions": questions_list,
                "next_action": args["next"] if args["next"] else "—",
            "recent_context": args.get("context", "")
        }
    }


def save_snapshot(args):
    """Сохраняет слепок."""
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    if SNAPSHOT_FILE.exists():
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
        SNAPSHOT_FILE.rename(HISTORY_FILE)

    context = build_context(args)
    with open(SNAPSHOT_FILE, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)

    print(f"[SNAPSHOT] Сохранён: {SNAPSHOT_FILE}")
    print(f"[SNAPSHOT] Сессия: {context['session_id']}")
    print(f"[SNAPSHOT] Сделано: {args['done']}")
    print(f"[SNAPSHOT] В работе: {args['working']}")
    print(f"[SNAPSHOT] Дальше: {args['next']}")
    if args.get("context"):
        print(f"[SNAPSHOT] Контекст: {args['context'][:100]}...")


def load_snapshot():
    """Загружает и выводит слепок."""
    if not SNAPSHOT_FILE.exists():
        print("[SNAPSHOT] Слепок не найден.")
        return

    with open(SNAPSHOT_FILE, 'r', encoding='utf-8') as f:
        context = json.load(f)

    print("[SNAPSHOT] Загружен слепок контекста:")
    print(json.dumps(context, ensure_ascii=False, indent=2))
    print("\n[SNAPSHOT] Скопируй JSON выше и вставь первым сообщением в новый чат.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python snapshot_manager.py --save -d \"сделано\" -w \"в работе\" -n \"дальше\"")
        print("  python snapshot_manager.py --load")
    elif sys.argv[1] == "--save":
        save_snapshot(parse_args())
    elif sys.argv[1] == "--load":
        load_snapshot()
    else:
        print(f"Неизвестный аргумент: {sys.argv[1]}")