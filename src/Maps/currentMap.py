from src.Maps.framework import *


class CurrentMap(MainApp):
    def __init__(self, home):
        super().__init__(home)

        self.page1 = PageOne(home, self)
        self.page2 = PageTwo()
        self.page3 = PageThree()

        self.tabManager = TabManager(self, home, self.page1, self.page2, self.page3)
        self.tabManager.setGeometry(QtCore.QRect(0, 0, 710, 454))
        self.tabManager.setStyleSheet("background-color:rgb(255,255,255)")


class PageOne(FrontPage):
    def __init__(self, home, parent):
        super().__init__(home, parent)
        self.setupUi()

    def setupUi(self):
        self.map.setGeometry(QtCore.QRect(10, 40, 661, 391))
        self.increaseSearch.setDisabled(False)
        self.mapSwitch.setDisabled(False)

    def updateDistance(self):
        data, CURR_COORDS = surroundCurrent(distance="0.06")

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

        self.crimeScore.setText(f"<html><head/><body><p><span style=\" color:#ffffff;\">Crime Score: {self.score}</span></p></body></html>")
        self.increaseSearch.setDisabled(True)

    def mapCluster(self):
        data, CURR_COORDS = surroundCurrent()
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