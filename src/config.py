from pydantic_settings import BaseSettings
import toml
from pathlib import Path

# Load secrets.toml
secrets_path = Path(__file__).resolve().parent.parent / ".streamlit/secrets.toml"
secrets = toml.load(secrets_path)

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_BASE_URL: str
    FRONTEND_PORT: int
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    NEO4J_DATABASE: str

# Create Settings from TOML
settings = Settings(
    PROJECT_NAME=secrets["frontend"]["PROJECT_NAME"],
    API_BASE_URL=secrets["frontend"]["API_BASE_URL"],
    FRONTEND_PORT=secrets["frontend"]["FRONTEND_PORT"],
    NEO4J_URI=secrets["neo4j"]["uri"],
    NEO4J_USER=secrets["neo4j"]["user"],
    NEO4J_PASSWORD=secrets["neo4j"]["password"],
    NEO4J_DATABASE=secrets["neo4j"]["database"],
)
