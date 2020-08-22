from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import io
from src.Data.crimeData import *


class MainApp(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Crime Watch")
        self.resize(710, 454)
        self.setFixedWidth(710)
        self.setFixedHeight(454)
        self.setStyleSheet("background-color:rgb(0,0,45)")
        self.setWindowIcon(QtGui.QIcon("src/Image Assets/Logos/crimeLogo.png"))


class TabManager(QtWidgets.QWidget):
    def __init__(self, parent, home, tab1, tab2, tab3):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("background-color:rgb(0,0,45)")
        self.tab1 = tab1
        self.tab2 = tab2
        self.tab3 = tab3
        self.tabs.resize(300, 200)

        self.tabs.addTab(self.tab1, "Crime Map")
        self.tabs.addTab(self.tab2, "State Crime Data")
        self.tabs.addTab(self.tab3, "City Crime Data")

        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class FrontPage(QtWidgets.QWidget):
    def __init__(self, home, parent):
        super().__init__()
        self.home = home
        self.parent = parent
        self.initialUI()

    def initialUI(self):
        DEFAULT_STYLE = "background-color:rgb(255, 255, 255);\n" \
                        "border-color:rgb(255, 255, 255);\n" \
                        "border-style:outset;\n" \
                        "border-width:2px;\n" \
                        "border-radius:10px;"
        self.layout()
        self.resize(710, 454)
        self.setStyleSheet("background-color:rgb(0,0,45)")
        self.clustering = False

        data, CURR_COORDS = surroundCurrent()
        main_map = mapper(data, CURR_COORDS)
        stored = io.BytesIO()
        main_map.save(stored, close_file=False)
        self.score = crimeScore(data)

        self.map = QtWebEngineWidgets.QWebEngineView(self)
        self.map.setStyleSheet("background-color:rgb(255,255,255)")
        self.map.setHtml(stored.getvalue().decode())

        self.returnHomeButton = QtWidgets.QPushButton(self)
        self.returnHomeButton.setText("Home")
        self.returnHomeButton.setStyleSheet(DEFAULT_STYLE)
        self.returnHomeButton.setGeometry(QtCore.QRect(10, 10, 70, 23))
        self.returnHomeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.returnHomeButton.clicked.connect(self.returnHome)

        self.increaseSearch = QtWidgets.QPushButton(self)
        self.increaseSearch.setText("Increase Search Distance")
        self.increaseSearch.setStyleSheet(DEFAULT_STYLE)
        self.increaseSearch.setGeometry(QtCore.QRect(85, 10, 190, 23))
        self.increaseSearch.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.increaseSearch.clicked.connect(self.updateDistance)
        self.increaseSearch.setDisabled(True)

        self.mapSwitch = QtWidgets.QCheckBox(self)
        self.mapSwitch.setStyleSheet('''
                    QCheckBox::indicator:unchecked {
                        image: url(src/Image Assets/Switches/offSwitch.png);
                    }
                    QCheckBox::indicator:checked {
                        image: url(src/Image Assets/Switches/onSwitch.png);
                    }''')
        self.mapSwitch.move(620, 12)
        self.mapSwitch.clicked.connect(self.mapCluster)
        self.mapSwitch.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mapSwitch.setChecked(False)
        self.mapSwitch.setDisabled(True)

        self.crimeScore = QtWidgets.QLabel(self)
        self.crimeScore.setGeometry(QtCore.QRect(280, 10, 181, 23))

        self.setWindowTitle("Crime Watch")
        self.crimeScore.setText(f"<html><head/><body><p><span style=\" color:#ffffff;\">Crime score: {self.score}"
                                f"</span></p></body></html>")

    def returnHome(self):
        self.parent.close()
        self.home.show()


class PageTwo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(710, 454)
        self.setStyleSheet("background-color:rgb(0,0,45)")

        state = getStateCurrent()
        stateAbbr = stateToStateAbbr(state)
        mainData, dataYears = stateData(stateAbbr)
        graph = stateGraphMaker(mainData, dataYears)

        self.graph = QtWebEngineWidgets.QWebEngineView(self)
        self.graph.setGeometry(QtCore.QRect(5, 10, 671, 421))
        self.graph.setStyleSheet("background-color:rgb(0,0,45)")
        self.graph.setHtml(graph)

        self.setWindowTitle("Crime Watch")

    def updateGraph(self, lat, lon):
        state = stateToStateAbbr(getStateLatLon(lat, lon))
        mainData, dataYears = stateData(state)
        graph = stateGraphMaker(mainData, dataYears)

        self.graph.setHtml(graph)


class DataTable(QtWidgets.QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def setCityData(self, data):
        self.data = data
        rowNames = list(self.data.keys())

        self.setRowCount(len(self.data))
        self.setColumnCount(1)

        self.setVerticalHeaderLabels(rowNames)
        self.setHorizontalHeaderLabels(["City Data"])

        rowCounter = 0

        for city in rowNames:
            beginning = f"The crime incident count of {city} was "
            sentences = self.data[city].split(beginning)
            data = beginning + "\n\t- ".join(sentences)

            processed = QtWidgets.QTableWidgetItem(data)
            processed.setFlags(QtCore.Qt.ItemIsEnabled)

            self.setItem(rowCounter, 0, processed)
            rowCounter += 1

        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setColumnWidth(0, 575)


class PageThree(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(710, 454)
        self.setStyleSheet("background-color:rgb(0,0,45)")

        self.cityData = DataTable(self)
        self.cityData.setCityData(cityData(getStateCurrent()))
        self.cityData.setGeometry(QtCore.QRect(5, 10, 671, 421))
        self.cityData.setStyleSheet("background-color:rgb(255,255,255)")

        self.setWindowTitle("Crime Watch")