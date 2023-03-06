import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from constants import MAIL_PARAMETERS
from input_data import WaterValue
from exceptions import EmailError


def _data_preparing(data_ordered: WaterValue, sender, recipient) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = 'Показания счетчиков воды'
    message = f"""
    Адрес: пр-т Музрукова, д. 39, кор. 3, кв. 98.
    Имя: Евграшин Павел Юрьевич.

    ГВС (кухня) – {data_ordered.HOT_KITCHEN} куб. м
        (с/узел) – {data_ordered.HOT_BATH} куб. м
    ХВС (кухня) – {data_ordered.COLD_KITCHEN} куб. м
        (с/узел) – {data_ordered.COLD_BATH} куб. м
    """
    msg.attach(MIMEText(message))
    return msg


def send_data(data_ordered: WaterValue, service: str = 'yandex') -> None:
    """ Send message with water values to service company by email """
    sender, smtp, password, recipient = MAIL_PARAMETERS[service]
    msg = _data_preparing(data_ordered, sender, recipient)
    try:
        mailserver = smtplib.SMTP(smtp, 587)
        # mailserver.set_debuglevel(True)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(sender, password)
        mailserver.sendmail(sender, recipient, msg.as_string())
        mailserver.quit()
    except smtplib.SMTPException:
        print('Error: impossible to send message')
        raise EmailError
