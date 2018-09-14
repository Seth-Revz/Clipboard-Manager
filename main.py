from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QStyle
from mainwindow import Ui_MainWindow
import keyboard, sys, os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.clipboard = app.clipboard()
        self.clipboard.dataChanged.connect(self.detectClipboardUrl)

        self.tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(self.resource_path("resources\clipboard.png")), app)
        #self.tray_icon.setIcon()
        self.menu = QtWidgets.QMenu()
        self.exitAction = self.menu.addAction("Exit")
        self.exitAction.triggered.connect(self.exitApp)
        self.tray_icon.setContextMenu(self.menu)
        
        self.tray_icon.activated.connect(self.onTrayIconActivated)
        self.disambiguateTimer = QTimer(self)
        self.disambiguateTimer.setSingleShot(True)
        self.disambiguateTimer.timeout.connect(self.disambiguateTimerTimeout)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tray_icon.show()
        self.tray_icon.hide()

    def event(self, event):
        if (event.type() == QtCore.QEvent.WindowStateChange and self.isMinimized()):
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.Tool)
            self.tray_icon.show()
            return True
        else:
            return super(MainWindow, self).event(event)

    def exitApp(self):
        self.tray_icon.hide()
        QtWidgets.QApplication.exit()
    
    def minimizeToTray(self):
        self.tray_icon.show()
        self.hide()
        #self.tray_icon.showMessage("Clipboard", "I'll be down here now", QtWidgets.QSystemTrayIcon.Information, 1000)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(
            self,
            'Message',"Minimize to system tray?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.No:
            self.tray_icon.hide()
            event.accept()
        else:
            self.minimizeToTray()
            event.ignore()

    def onTrayIconActivated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.disambiguateTimer.start(QtWidgets.QApplication.doubleClickInterval())
        elif reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            self.disambiguateTimer.stop()
            self.tray_icon.hide()
            self.showNormal()

    def disambiguateTimerTimeout(self):
        print("Tray icon single clicked")

    def detectClipboardUrl(self):
        clipboardText = self.clipboard.text()
        if getattr(self.clipboard, 'lastClipboardUrl', None) != clipboardText:
            url = clipboardText
            setattr(self.clipboard, 'lastClipboardUrl', url)
            QTimer.singleShot(400, lambda:[setattr(self.clipboard, 'lastClipboardUrl', None), self.detectSameUrl()])
    
    #Detects if the url is the same or already in the list
    def detectSameUrl(self):
        fullText = self.ui.textBrowser.toPlainText()
        textList = str(fullText).split('\n')

        for entry in textList:
            if entry and entry.rstrip() == self.clipboard.text().rstrip():
                return

        self.ui.textBrowser.append(self.clipboard.text().rstrip())
        
        fullText = self.ui.textBrowser.toPlainText()
        textList = str(fullText).split('\n')

        self.menu = QtWidgets.QMenu()
        print(len(textList))
        # if len(textList) >= 1:
        #     print(fullText)
        #     self.firstAction = self.menu.addAction("Current: {}".format(textList[-1]))
        #     self.firstAction.triggered.connect(lambda: self.clipboard.setText(textList[-1]))
        if len(textList) >= 2:
            self.secondAction = self.menu.addAction("ReCopy: {}".format(textList[-2]))  
            self.secondAction.triggered.connect(lambda: self.clipboard.setText(textList[-2]))  
        if len(textList) >= 3:
            self.thirdAction = self.menu.addAction("ReCopy: {}".format(textList[-3]))
            self.thirdAction.triggered.connect(lambda: self.clipboard.setText(textList[-3]))
        
        self.exitAction = self.menu.addAction("Exit")
        self.exitAction.triggered.connect(self.exitApp)
        self.tray_icon.setContextMenu(self.menu)

    def aboutAction(self):
        QtWidgets.QMessageBox.about(self, "About", "\n--Clipboard Manager Alpha--\n\nhttps://github.com/Seth-Revz")

    def clearAction(self):
        self.ui.textBrowser.clear()
        
    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()

    keyboard.add_hotkey('end', lambda: app.exit(), suppress=True)
    app.exec()

