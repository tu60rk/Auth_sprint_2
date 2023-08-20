from pydantic import BaseSettings, Field
import os


class UGCSettings(BaseSettings):
	PROJECT_NAME: str = Field("User-Generated Content API", env="UGC_PROJECT_NAME")
	PROJECT_DESCRIPTION: str = Field("API for handling user-generated content, such as film progress tracking.", env="UGC_PROJECT_DESCRIPTION")
	API_VERSION: str = Field("1.0.0", env="UGC_API_VERSION")

	UGC_APP_HOST: str
	UGC_APP_PORT: int

	KAFKA_HOST: str
	KAFKA_PORT: int
	KAFKA_INSTANCE: str = Field('Common')

	class Config:
		case_sensitive = True
		env_file = "ugc.env"


ugc_settings = UGCSettings()
ugc_settings.KAFKA_INSTANCE = f'{ugc_settings.KAFKA_HOST}:{ugc_settings.KAFKA_PORT}'
