"""
Class for managing chain-link configuration variables.
Code contributors: Koa Wells koa.wells@hotmail.com
"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
  """
  Global application configuration settings.
  """
  DISCORD_TOKEN: str = ''
  EMAIL: str = ''
  EMAIL_PASSWORD: str = ''
  SMTP_SERVER: str = ''
  SMTP_PORT: int = 465
  RECIPIENTS_FILE: str = ''

  model_config = SettingsConfigDict(env_file='.config', env_file_encoding='utf-8')

  @field_validator('DISCORD_TOKEN')
  @classmethod
  def check_discord_token(cls, value: str) -> str:
    """
    Checks to see if the DISCORD_TOKEN environment variable is set.
    :param value: value of DISCORD_TOKEN
    :return: str
    """
    if not value:
      raise ValueError('DISCORD_TOKEN must be set')
    return value

  @field_validator('EMAIL')
  @classmethod
  def check_email(cls, value: str) -> str:
    """
    Checks to see if the EMAIL environment variable is set.
    :param value: value of EMAIL
    :return: str
    """
    if not value:
      raise ValueError('EMAIL must be set')
    return value

  @field_validator('EMAIL_PASSWORD')
  @classmethod
  def check_email_password(cls, value: str) -> str:
    """
    Checks to see if the EMAIL_PASSWORD environment variable is set.
    :param value: value of EMAIL_PASSWORD
    :return: str
    """
    if not value:
      raise ValueError('EMAIL_PASSWORD must be set')
    return value

  @field_validator('SMTP_SERVER')
  @classmethod
  def check_smtp_server(cls, value: str) -> str:
    """
    Checks to see if the SMTP_SERVER environment variable is set.
    :param value: value of SMTP_SERVER
    :return: str
    """
    if not value:
      raise ValueError('SMTP_SERVER must be set')
    return value

  @field_validator('SMTP_PORT')
  @classmethod
  def check_smtp_port(cls, value: int) -> int:
    if not value:
      raise ValueError('SMTP_PORT must be set')
    return value

  @field_validator('RECIPIENTS_FILE')
  @classmethod
  def check_recipients_file(cls, value: str) -> Path:
    """
    Checks to see if RECIPIENTS_FILE environment variable is set.
    :param value: value of RECIPIENTS_FILE
    :return: Path
    """
    if not value:
      raise ValueError('RECIPIENTS_FILE must be set')
    recipients_file_path = Path(__file__).parent / 'data' / value
    if not recipients_file_path.exists():
      raise ValueError('RECIPIENTS_FILE does not exist')
    return recipients_file_path

CONF = Settings()