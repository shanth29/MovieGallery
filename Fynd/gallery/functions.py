from random import randint


def send_otp(phone):
    if phone:
        return randint(9999,99999)
    else:
        return False