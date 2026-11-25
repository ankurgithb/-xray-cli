import json
from pathlib import Path 

HISTORY_FILE = Path("chat_history.json")

def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return[]
    return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))

def save_history(history : list[dict]) -> None:
    HISTORY_FILE.write_text(json.dumps(history, indent = 2), encoding="utf-8")

def append_message(history: list[dict], role: str, content: str) -> None:
    history.append({"role": role,"content": content})
    save_history(history)    

def build_model_context(history: list[dict],window_size: int,stateless: bool = False) -> list[dict]:
    if stateless:
        return history[-1:] if history else []
    if window_size <= 0:
        return []    
    return history[-window_size:] 