from input_data import safe_input
from email_sender import send_data
from log import write_log, sent_this_month


CHOSEN_SERVICE = 'gmail'

if __name__ == '__main__':
    values = safe_input()
    if values is not None and not sent_this_month():
        send_data(values, CHOSEN_SERVICE)
        write_log(values)
