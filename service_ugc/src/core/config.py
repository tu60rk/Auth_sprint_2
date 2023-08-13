from pydantic import BaseSettings, Field
import os


class UGCSettings(BaseSettings):
	PROJECT_NAME: str = Field("User-Generated Content API", env="UGC_PROJECT_NAME")
	PROJECT_DESCRIPTION: str = Field("API for handling user-generated content, such as film progress tracking.", env="UGC_PROJECT_DESCRIPTION")
	API_VERSION: str = Field("1.0.0", env="UGC_API_VERSION")

	UGC_APP_HOST: str
	UGC_APP_PORT: int

	UGC_REDIS_HOST: str
	UGC_REDIS_PORT: int

	KAFKA_INSTANCE: str = os.getenv("KAFKA_INSTANCE", "localhost:29092")

	class Config:
		case_sensitive = True
		env_file = "ugc.env"


ugc_settings = UGCSettings()
