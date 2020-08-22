from PyQt5 import QtWidgets
import sys
from src.Maps.homePage import HomePage


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    home = HomePage()
    home.show()
    sys.exit(app.exec_())