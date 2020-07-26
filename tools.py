import datetime


def str_time(time):
    return str(datetime.timedelta(seconds=time))

def str_rank(place, length):
    calculation = str(round(100 * (length - place) / length,2)) + " %"
    return str(f'{place}/{length} ({calculation})')

if __name__ == "__main__":
    print(str_rank(63, 100))