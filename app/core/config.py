from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    database_echo: bool = False
    test_database_url: str

    llm_provider: str = "ollama"
    ollama_model: str = "llama3.2"
    ollama_url: str = "http://localhost:11434"
    ollama_num_ctx: int = 4096

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        dotenv_filtering="only_existing",
    )


settings = Settings() # type: ignore 