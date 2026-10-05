import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("COSMIC_NAME", "COSMIC AI")
APP_VERSION = os.getenv("COSMIC_VERSION", "0.1.0")
HOST = os.getenv("COSMIC_HOST", "127.0.0.1")
PORT = int(os.getenv("COSMIC_PORT", "8000"))
DATABASE_PATH = os.getenv("COSMIC_DATABASE", "data/local/cosmic.db")
