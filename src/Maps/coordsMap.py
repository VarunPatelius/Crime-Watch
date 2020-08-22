from src.Maps.framework import *


class CoordinateMap(MainApp):
    def __init__(self, home):
        super().__init__(home)

        self.page2 = PageTwo()
        self.page3 = PageThree()
        self.page1 = PageOne(self.page2, self.page3, home, self)

        self.tabManager = TabManager(self, home, self.page1, self.page2, self.page3)
        self.tabManager.setGeometry(QtCore.QRect(0, 0, 710, 454))
        self.tabManager.setStyleSheet("background-color:rgb(255,255,255)")


class PageOne(FrontPage):
    def __init__(self, page2, page3, home, parent):
        super().__init__(home, parent)
        self.page2 = page2
        self.page3 = page3
        self.setupUi()

    def setupUi(self):
        DEFAULT_STYLE = "background-color:rgb(255, 255, 255);\n" \
                        "border-color:rgb(255, 255, 255);\n" \
                        "border-style:outset;\n" \
                        "border-width:2px;\n" \
                        "border-radius:10px;"

        self.map.setGeometry(QtCore.QRect(5, 40, 511, 391))

        self.latEntry = QtWidgets.QLineEdit(self)
        self.latEntry.setGeometry(QtCore.QRect(547, 110, 121, 21))
        self.latEntry.setStyleSheet("background-color:rgb(255,255,255)")

        self.lonEntry = QtWidgets.QLineEdit(self)
        self.lonEntry.setGeometry(QtCore.QRect(547, 190, 121, 21))
        self.lonEntry.setStyleSheet("background-color:rgb(255,255,255)")

        self.latLabel = QtWidgets.QLabel(self)
        self.latLabel.setGeometry(QtCore.QRect(547, 80, 60, 16))

        self.lonLabel = QtWidgets.QLabel(self)
        self.lonLabel.setGeometry(QtCore.QRect(547, 160, 71, 16))

        self.submitButton = QtWidgets.QPushButton(self)
        self.submitButton.setGeometry(QtCore.QRect(559, 261, 101, 21))
        self.submitButton.setStyleSheet(DEFAULT_STYLE)
        self.submitButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.submitButton.clicked.connect(self.updateData)

        self.errorMessage = QtWidgets.QLabel(self)
        self.errorMessage.setGeometry(QtCore.QRect(535, 365, 141, 20))
        self.errorMessage.setAlignment(QtCore.Qt.AlignCenter)

        self.setWindowTitle("Crime Watch")
        self.crimeScore.setText(f"<html><head/><body><p><span style=\" color:#ffffff;\">Crime score: {self.score}</span>"
                                f"</p></body></html>")
        self.latLabel.setText("<html><head/><body><p><span style=\" color:#ffffff;\">Latitude:</span>"
                              "</p></body></html>")
        self.lonLabel.setText("<html><head/><body><p><span style=\" color:#ffffff;\">Longitude:</span>"
                              "</p></body></html>")
        self.submitButton.setText("Submit")

    def updateData(self):
        self.mapSwitch.setChecked(False)
        lat, lon = self.latEntry.text(), self.lonEntry.text()
        data, CURR_COORDS = surroundLatLon(lat, lon)
        if len(data["crimes"]) == 0:
            self.increaseSearch.setDisabled(True)
            self.mapSwitch.setDisabled(True)
            self.errorMessage.setText("<html><head/><body><p><span style=\" color:#fc0107;\">Error: No Data Found</span></p></body></html>")
        else:
            self.increaseSearch.setDisabled(False)
            self.mapSwitch.setDisabled(False)
            self.errorMessage.setText(
                "<html><head/><body><p><span style=\" color:#fc0107;\"></span></p></body></html>")
            main_map = mapper(data, CURR_COORDS)

            stored = io.BytesIO()
            main_map.save(stored, close_file=False)
            self.map.setHtml(stored.getvalue().decode())

            self.score = crimeScore(data)
            self.crimeScore.setText(f"<html><head/><body><p><span style=\" color:#ffffff;\">Crime score: {self.score}</span></p></body></html>")

            self.page2.updateGraph(lat, lon)
            self.page3.cityData.clear()
            self.page3.cityData.setCityData(cityData(getStateLatLon(lat, lon)))

    def updateDistance(self):
        lat, lon = self.latEntry.text(), self.lonEntry.text()
        data, CURR_COORDS = surroundLatLon(lat, lon, "0.06")

        if self.clustering:
            main_map = mapper(data, CURR_COORDS, True)
            stored = io.BytesIO()
            main_map.save(stored, close_file=False)
            self.score = crimeScore(data, 0.06)

            self.map.setHtml(stored.getvalue().decode())
        else:
            main_map = mapper(data, CURR_COORDS)
            stored = io.BytesIO()
            main_map.save(stored, close_file=False)
            self.score = crimeScore(data, 0.06)

            self.map.setHtml(stored.getvalue().decode())

        self.crimeScore.setText(
            f"<html><head/><body><p><span style=\" color:#ffffff;\">Crime Score: {self.score}</span></p></body></html>")

        self.increaseSearch.setDisabled(True)

    def mapCluster(self):
        lat, lon = self.latEntry.text(), self.lonEntry.text()
        data, CURR_COORDS = surroundLatLon(lat, lon, "0.06")
        self.increaseSearch.setDisabled(False)
        self.score = crimeScore(data)

        if self.mapSwitch.isChecked():
            self.clustering = True
            main_map = mapper(data, CURR_COORDS, True)
            stored = io.BytesIO()
            main_map.save(stored, close_file=False)
            self.map.setHtml(stored.getvalue().decode())
        else:
            self.clustering = False
            main_map = mapper(data, CURR_COORDS)
            stored = io.BytesIO()
            main_map.save(stored, close_file=False)
            self.map.setHtml(stored.getvalue().decode())

        self.crimeScore.setText(
            f"<html><head/><body><p><span style=\" color:#ffffff;\">Crime Score: {self.score}</span></p></body></html>")
