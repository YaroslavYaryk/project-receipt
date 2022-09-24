import phonenumbers


def validate_phone(string):
    try:
        my_number = phonenumbers.parse(string)
        return phonenumbers.is_possible_number(my_number), "no error"
    except Exception as e:
        return False, e
