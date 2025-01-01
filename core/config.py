from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    OPENAI_KEY: str
    DEBUG: bool
    ENV: str
    class Config:
        env_file = ".env"

class DevelopmentConfig(Settings):
    DEBUG: bool = True
    TESTING: bool = True

class ProductionConfig(Settings):
    DEBUG: bool = False
    TESTING: bool = False

config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def get_config() -> Settings:
    # Load initial settings to read the ENV variable
    initial_settings = Settings()
    config_class = config_dict.get(initial_settings.ENV)
    # Return the appropriate configuration class
    return config_class()

# Load the appropriate configuration
config = get_config()


