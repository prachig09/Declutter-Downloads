import os
from dotenv import load_dotenv

load_dotenv()

WATCH_DIR = os.getenv("WATCH_DIR", "./Downloads")
FALLBACK_DIR = os.getenv("FALLBACK_DIR", "./Unsorted")
DRY_RUN = os.getenv("DRY_RUN", "True").lower() == "true"

# Tag rules mapping: "tag": "Target Folder Path"
TAG_RULES = {
    "sem3_": "/mnt/c/Users/PRACHI/Documents/Uni/Sem3",
    "dissertation_": "/mnt/c/Users/PRACHI/Documents/Uni/Dissertation",
    "IF26_": "/mnt/c/Users/PRACHI/Documents/Uni/IF26",
    "sem4_": "/mnt/c/Users/PRACHI/Downloads/Uni/Sem4",
}