import datetime


def str_time(time):
    return str(datetime.timedelta(seconds=time))


if __name__ == "__main__":
    print(str_rank(63, 100))