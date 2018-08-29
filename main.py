from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QStyle
from mainwindow import Ui_MainWindow
import keyboard

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.clipboard = app.clipboard()
        self.clipboard.dataChanged.connect(self.detectClipboardUrl)

        self.tray_icon = QtWidgets.QSystemTrayIcon()
        self.tray_icon.setIcon(QtGui.QIcon("resources\clipboard-paste.png"))

        self.tray_icon.activated.connect(self.restoreWindow)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def event(self, event):
        if (event.type() == QtCore.QEvent.WindowStateChange and self.isMinimized()):
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.Tool)
            self.tray_icon.show()
            return True
        else:
            return super(MainWindow, self).event(event)
    
    def minimizeToTray(self):
        self.tray_icon.show()
        self.hide()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(
            self,
            'Message',"Minimize to system tray?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.No:
            event.accept()
        else:
            self.minimizeToTray()
            event.ignore()

    def restoreWindow(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            self.tray_icon.hide()
            self.showNormal()

    def detectClipboardUrl(self):
        clipboardText = self.clipboard.text()
        if getattr(self.clipboard, 'lastClipboardUrl', None) != clipboardText:
            url = clipboardText
            setattr(self.clipboard, 'lastClipboardUrl', url)
            QTimer.singleShot(400, lambda:[setattr(self.clipboard, 'lastClipboardUrl', None), self.detectSameUrl()])
    
    #Detects if the url is the same or already in the list
    def detectSameUrl(self):
        doc = self.ui.textBrowser.toPlainText()
        txt = str(doc).split('\n')

        for cb in txt:
            if cb and cb.rstrip() == self.clipboard.text().rstrip():
                return

        self.ui.textBrowser.append(self.clipboard.text().rstrip())
        

if __name__ == "__main__":
    
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()

    keyboard.add_hotkey('end', lambda: app.exit(), suppress=True)
    app.exec()

