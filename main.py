from code_SRC.api import api
from code_SRC.user import User
"""
Habituellement c'est assez simple, un CTRL+SHIFT+F à la grandeur du projet, replace
from PyQt.QtWidgets
Pour
from PySide6.QtWidgets
Et c'est quasi clef en main
"""




if __name__ == "__main__":
    api.get_cache_api()
    test = User(input("Analyse who? "))
    api.cache_api()