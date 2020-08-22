from PyQt5 import QtCore, QtGui, QtWidgets
from src.Maps.addressMap import AddressMap
from src.Maps.coordsMap import CoordinateMap
from src.Maps.currentMap import CurrentMap


class HomePage(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        DEFAULT_STYLE = "background-color:rgb(255, 255, 255);\n"\
                        "border-color:rgb(255, 255, 255);\n"\
                        "border-style:outset;\n"\
                        "border-width:2px;\n"\
                        "border-radius:10px;"
        BUTTON_WIDTH = 201
        BUTTON_HEIGHT = 27

        self.setObjectName("Dialog")
        self.resize(710, 454)
        self.setFixedWidth(710)
        self.setFixedHeight(454)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color:rgb(0,0,45)")
        self.setWindowIcon(QtGui.QIcon("src/Image Assets/Logos/crimeLogo.png"))

        self.logo = QtWidgets.QLabel(self)
        self.logo.setGeometry(QtCore.QRect(30, 30, 251, 261))
        self.logo.setPixmap(QtGui.QPixmap("src/Image Assets/Logos/clearLogo.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(470, 10, 201, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.currentMap = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.currentMap.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.currentMap.setStyleSheet(DEFAULT_STYLE)
        self.currentMap.setFixedWidth(BUTTON_WIDTH)
        self.currentMap.setFixedHeight(BUTTON_HEIGHT)
        self.currentMap.setObjectName("currentMap")
        self.verticalLayout.addWidget(self.currentMap)

        self.latLonMap = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.latLonMap.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.latLonMap.setStyleSheet(DEFAULT_STYLE)
        self.latLonMap.setFixedWidth(BUTTON_WIDTH)
        self.latLonMap.setFixedHeight(BUTTON_HEIGHT)
        self.latLonMap.setObjectName("latLonMap")
        self.verticalLayout.addWidget(self.latLonMap)

        self.addressMap = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addressMap.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addressMap.setStyleSheet(DEFAULT_STYLE)
        self.addressMap.setFixedWidth(BUTTON_WIDTH)
        self.addressMap.setFixedHeight(BUTTON_HEIGHT)
        self.addressMap.setObjectName("addressMap")
        self.verticalLayout.addWidget(self.addressMap)

        self.directions = QtWidgets.QLabel(self)
        self.directions.setGeometry(QtCore.QRect(340, 20, 101, 161))
        self.directions.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.directions.setStyleSheet("")
        self.directions.setAlignment(QtCore.Qt.AlignCenter)
        self.directions.setWordWrap(True)
        self.directions.setObjectName("directions")

        self.currentMap.clicked.connect(lambda: self.mapLoader("curr"))
        self.addressMap.clicked.connect(lambda: self.mapLoader("add"))
        self.latLonMap.clicked.connect(lambda: self.mapLoader("coord"))

        self.retranslateUi()

    def mapLoader(self, mapType):
        if mapType == "coord":
            self.ui = CoordinateMap(self)
            self.ui.show()
            self.close()
        elif mapType == "add":
            self.ui = AddressMap(self)
            self.ui.show()
            self.close()
        else:
            self.ui = CurrentMap(self)
            self.ui.show()
            self.close()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Crime Watch"))
        self.currentMap.setText(_translate("Dialog", "Use Current Location"))
        self.latLonMap.setText(_translate("Dialog", "Use Latitude and Longitude"))
        self.addressMap.setText(_translate("Dialog", "Use Address"))
        self.directions.setText(_translate("Dialog",
                                           "<html><head/><body><p><span style=\" color:#ffffff;\">Select an option to "
                                           "generate a crime map</span></p></body></html>"))