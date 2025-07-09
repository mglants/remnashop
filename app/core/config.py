import re
from typing import Self, Type

from pydantic import Field, SecretStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

from app.core.constants import API_V1, BASE_DIR, DOMAIN_REGEX, WEBHOOK_PATH
from app.core.enums import Locale
from app.core.utils.types import LocaleList, StringList


def _validate_not_change_me(value: object, info: FieldValidationInfo) -> None:
    if isinstance(value, SecretStr):
        value = value.get_secret_value()

    full_env_var_name = "UNKNOWN_FIELD"

    if info.config and hasattr(info.config, "get"):
        model_env_prefix = info.config.get("env_prefix", "")

        if isinstance(model_env_prefix, str):
            model_prefix_str = model_env_prefix.upper()
        else:
            model_prefix_str = ""

        if info.field_name:
            full_env_var_name = f"{model_prefix_str}{info.field_name.upper()}"
        else:
            full_env_var_name = "UNKNOWN_FIELD"

    if not value or str(value).strip().lower() in {"change_me", ""}:
        raise ValueError(f"{full_env_var_name} must be set and not equal to 'change_me'")


class BotConfig(BaseSettings, env_prefix="BOT_"):
    token: SecretStr
    secret_token: SecretStr
    dev_id: int

    reset_webhook: bool
    drop_pending_updates: bool
    setup_commands: bool
    use_banners: bool

    @field_validator("token", "secret_token")
    @classmethod
    def validate_bot_fields(
        cls: Type["BotConfig"],
        field: object,
        info: FieldValidationInfo,
    ) -> object:
        _validate_not_change_me(field, info)
        return field

    @property
    def webhook_path(self) -> str:
        return f"{API_V1}{WEBHOOK_PATH}"

    def webhook_url(self, domain: SecretStr) -> SecretStr:
        url = f"https://{domain.get_secret_value()}{self.webhook_path}"
        return SecretStr(url)

    def safe_webhook_url(self, domain: SecretStr) -> str:
        return f"https://{domain}{self.webhook_path}"


class RemnaConfig(BaseSettings, env_prefix="REMNA_"):
    # TODO: Ensure connection to the panel within a single Docker network
    host: SecretStr
    token: SecretStr

    @field_validator("host")
    @classmethod
    def validate_host(cls: Type["RemnaConfig"], field: SecretStr) -> SecretStr:
        host = field.get_secret_value()

        if not host:
            raise ValueError("REMNA_HOST cannot be empty")

        if host == "remnawave":
            return field

        if re.match(DOMAIN_REGEX, host):
            return field

        raise ValueError(
            "REMNA_HOST must be 'remnawave' (docker) or a valid domain (e.g., example.com)"
        )

    @field_validator("token")
    @classmethod
    def validate_remna_token(
        cls,
        field: SecretStr,
        info: FieldValidationInfo,
    ) -> SecretStr:
        _validate_not_change_me(field, info)
        return field

    @property
    def url(self) -> SecretStr:
        url = f"https://{self.host.get_secret_value()}"
        return SecretStr(url)


class DatabaseConfig(BaseSettings, env_prefix="DB_"):
    host: str
    port: int
    name: str
    user: str
    password: SecretStr

    @field_validator("password")
    @classmethod
    def validate_db_password(
        cls: Type["DatabaseConfig"],
        field: SecretStr,
        info: FieldValidationInfo,
    ) -> SecretStr:
        _validate_not_change_me(field, info)
        return field

    @property
    def dsn(self) -> str:
        return str(
            URL.build(
                scheme="postgresql+asyncpg",
                user=self.user,
                password=self.password.get_secret_value(),
                host=self.host,
                port=self.port,
                path=f"/{self.name}",
            )
        )


class RedisConfig(BaseSettings, env_prefix="REDIS_"):
    host: str
    port: int
    name: str
    password: SecretStr

    @field_validator("password")
    @classmethod
    def validate_redis_password(
        cls: Type["RedisConfig"],
        field: SecretStr,
        info: FieldValidationInfo,
    ) -> SecretStr:
        _validate_not_change_me(field, info)
        return field

    @property
    def dsn(self) -> str:
        return str(
            URL.build(
                scheme="redis",
                password=self.password.get_secret_value(),
                host=self.host,
                port=self.port,
                path=f"/{self.name}",
            )
        )


class I18nConfig(BaseSettings, env_prefix="I18N_"):
    locales: LocaleList
    default_locale: Locale


class SQLAlchemyConfig(BaseSettings, env_prefix="ALCHEMY_"):
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int
    pool_timeout: int
    pool_recycle: int


class AppConfig(BaseSettings, env_prefix="APP_"):
    domain: SecretStr
    host: str
    port: int
    origins: StringList = StringList("")  # NOTE: For miniapp

    bot: BotConfig = Field(default_factory=BotConfig)
    remna: RemnaConfig = Field(default_factory=RemnaConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    i18n: I18nConfig = Field(default_factory=I18nConfig)
    alchemy: SQLAlchemyConfig = Field(default_factory=SQLAlchemyConfig)

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )

    @classmethod
    def get(cls) -> Self:
        return cls()

    @field_validator("domain")
    @classmethod
    def validate_domain(
        cls: Type["AppConfig"],
        field: SecretStr,
        info: FieldValidationInfo,
    ) -> SecretStr:
        _validate_not_change_me(field, info)

        if not re.match(DOMAIN_REGEX, field.get_secret_value()):
            raise ValueError("APP_DOMAIN has invalid format")

        return field
