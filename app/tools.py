import os, csv

from twilio.rest import Client

import settings

client = Client(settings.SID, settings.TOKEN)

def check_numbers(numbers):
    numbers_not_found = list()
    for number in numbers:
        try:
            phone_number = client.lookups.phone_numbers(number[0]).fetch()
        except Exception as e:
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


def send_messages(number_list):
    flag = 0
    while flag < len(number_list):
        message = client.messages.create(
            body=number_list[flag][1],
            from_="APITest",
            to=number_list[flag][0]
        )
        number_list[flag].append(message.sid)
        flag += 1
    return number_list
