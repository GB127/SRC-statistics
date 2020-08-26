import datetime


def input_which(length):
    """Command that will ask you to input a number or all.

        Args:
            length (list): list of items in which we need to select an entry.

        Returns: 2 possibilities.
            str: "all"  => Means that alls items of the list is "selected"
            int: X      => One item of the entry only.
        """

    #FIXME : Some checks

    command = input(f"[1 - {len(length)}, all] ")
    try:
        return int(command) - 1
    except ValueError:
        return command


def str_time(time):
    """Convert an amount of seconds into a readable time format.

        Args:
            time (int): Amount of seconds.

        Returns (str) : Time in a readable format.
    """
    return str(datetime.timedelta(seconds=time))


if __name__ == "__main__":
    pass