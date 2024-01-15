from dataclasses import dataclass
from environs import Env

from .constants import MAIL_SMTP, REMINDER


@dataclass
class TgBot:
    token: str


@dataclass
class Mail:
    mail: str
    password: str
    smtp_server: str


@dataclass
class Config:
    tg_bot: TgBot
    admin_ids: list[int]
    recipient: str
    recipient_test: str
    mails: dict[str, Mail]
    reminder: dict[str, str]


def _load_ids(ids: str) -> list[int]:
    row: list[int] = []
    for number_id in ids.split(', '):
        try:
            row.append(int(number_id))
        except ValueError:
            return [0]
    return row


def _load_mail(env: Env, mail_service: str) -> Mail:
    text = env(mail_service)
    return Mail(mail=text.split(':')[0],
                password=text.split(':')[1],
                smtp_server=MAIL_SMTP[mail_service])


def load_config(path: str | None = None) -> Config | bool:
    env: Env = Env()
    env.read_env(path)

    admin_ids: list[int] = _load_ids(env('ADMIN_IDS'))
    mails: dict = {mail: _load_mail(env, mail) for mail in MAIL_SMTP.keys()}

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  admin_ids=admin_ids,
                  recipient=env('RECIPIENT'),
                  recipient_test=env('RECIPIENT_TEST'),
                  mails=mails,
                  reminder=REMINDER
                  )


bot_config: Config = load_config()
