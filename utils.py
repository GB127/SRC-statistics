def time_str(duration):
    no_decimal = int(duration)
    return f"{no_decimal//3600}:{no_decimal% 3600 // 60:02}:{no_decimal % 3600 % 60 % 60:02}"
