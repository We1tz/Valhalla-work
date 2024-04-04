from phonenumbers import geocoder
from phonenumbers import carrier
import phonenumbers
def phonnum():
    numbers = input("Enter phone number : | Введите номер телефона:\n")
    ch_num = phonenumbers.parse(numbers, 'CH')
    print(geocoder.description_for_number(ch_num, "en"))

    service_num = phonenumbers.parse(numbers, "RO")
    print(carrier.name_for_number(service_num, "en"))
    pass
