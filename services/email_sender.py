import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config_data import bot_config
from utils import WaterValue
from lexicon import LEXICON


def _data_preparing(values: WaterValue,
                    sender: str,
                    recipient: str) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = LEXICON['letter_title']
    message = f"""
    Адрес: {LEXICON['sender_address']}.
    Имя: {LEXICON['sender_name']}.

    ГВС (кухня) – {values.HOT_KITCHEN} куб. м
        (с/узел) – {values.HOT_BATH} куб. м
    ХВС (кухня) – {values.COLD_KITCHEN} куб. м
        (с/узел) – {values.COLD_BATH} куб. м
    """
    msg.attach(MIMEText(message))
    return msg


def send_data(data_ordered: WaterValue, service: str = 'YANDEX') -> bool:
    """ Send message with water values to service company by email """
    sender: str = bot_config.mails[service].mail
    password: str = bot_config.mails[service].password
    smtp: str = bot_config.mails[service].smtp_server
    recipient: str = bot_config.recipient
    msg: MIMEMultipart = _data_preparing(data_ordered, sender, recipient)
    try:
        mailserver = smtplib.SMTP(smtp, 587)
        # mailserver.set_debuglevel(True)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(sender, password)
        mailserver.sendmail(sender, recipient, msg.as_string())
        mailserver.quit()
        return True
    except smtplib.SMTPException:
        return False
