import csv
import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException, TwilioException

import settings


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in settings.ALLOWED_EXTENSIONS
    )


def valid_credentials(sid, token):
    client = Client(sid, token)
    try:
        messages = client.messages.list(limit=1)
    except TwilioException:
        return False
    return True


def check_numbers(numbers, sid, token):
    client = Client(sid, token)
    numbers_not_found = list()
    for number in numbers:
        try:
            client.lookups.phone_numbers(number[1]).fetch()
        except TwilioRestException:
            numbers_not_found.append(number)
    return numbers_not_found


def get_number_list(filename):
    number_list = list()
    file_path = os.path.join(
        settings.UPLOAD_FOLDER,
        filename
    )
    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            number_list.append(row)
    os.remove(file_path)
    return number_list


def send_messages(number_list, sid, token):
    client = Client(sid, token)
    flag = 0
    while flag < len(number_list):
        message = client.messages.create(
            body=number_list[flag][2],
            from_=number_list[flag][0],
            to=number_list[flag][1]
        )
        number_list[flag].append(message.status)
        number_list[flag].append(message.sid)
        flag += 1
    for item in number_list:
        current_message = client.messages.get(item[4]).fetch()
        item[3] = current_message.status
    return number_list
