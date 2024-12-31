from pydantic_settings import BaseSettings
import os

# Ensure the .env file is loaded from the same directory as this script
current_dir = os.path.dirname(__file__)
env_file_path = os.path.join(current_dir, ".env")


class Settings(BaseSettings):
    OPENAI_API_KEY: str  # This will be loaded from the .env file
    ENV: str = "development"

    class Config:
        env_file = env_file_path
        extra = "ignore"  # Allow extra keys in the environment file


# Define configuration classes for different environments
class DevelopmentConfig(Settings):
    pass


class ProductionConfig(Settings):
    pass


# Map environment values to configuration classes
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}


def get_config() -> Settings:
    try:
        initial_settings = Settings()
        # Fetch the appropriate config class
        config_class = config_dict.get(initial_settings.ENV, DevelopmentConfig)
        return config_class()
    except Exception as e:
        print("Error loading settings:", e)
        raise


# Load the appropriate configuration
config = get_config()

