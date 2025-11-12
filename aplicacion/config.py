# aplicacion/config.py
import os
from dotenv import load_dotenv

# Carga variables desde .env si existe
load_dotenv()

def env_str(key: str, default: str = "") -> str:
    v = os.getenv(key, default)
    return v if isinstance(v, str) else str(v)

def env_int(key: str, default: int = 0) -> int:
    try:
        return int(os.getenv(key, default))
    except Exception:
        return default

# ---- Config BD ----
DB_HOST     = env_str("DB_HOST", "127.0.0.1")
DB_PORT     = env_int("DB_PORT", 3306)
DB_NAME     = env_str("DB_NAME", "bdpoo")
DB_USER     = env_str("DB_USER", "root")
DB_PASSWORD = env_str("DB_PASSWORD", "")

# ---- Seguridad ----
BCRYPT_ROUNDS = env_int("BCRYPT_ROUNDS", 12)
