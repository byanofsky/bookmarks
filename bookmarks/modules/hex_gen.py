import random
import string


def hex_gen():
    # Generates a six character string of upper/lower letters and digits
    return ''.join(random.choice(
        string.ascii_letters + string.digits) for _ in range(6))
