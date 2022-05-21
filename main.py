from code_SRC.user import User
"""
Habituellement c'est assez simple, un CTRL+SHIFT+F à la grandeur du projet, replace
from PyQt.QtWidgets
Pour
from PySide6.QtWidgets
Et c'est quasi clef en main
"""

test = User(input("Which user?"))
# test = User("niamek")
test()