from user import User

if __name__ == "__main__":
    src_user = User(input("Enter the username of a runner on SRC: "))
    print(src_user.__dict__)
    