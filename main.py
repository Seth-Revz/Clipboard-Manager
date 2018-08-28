from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from mainwindow import Ui_MainWindow
import keyboard

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.clipboard = app.clipboard()
        self.clipboard.dataChanged.connect(self.detectClipboardUrl)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
    def detectClipboardUrl(self):
        clipboardText = self.clipboard.text()
        if getattr(self.clipboard, 'lastClipboardUrl', None) != clipboardText:
            url = clipboardText
            setattr(self.clipboard, 'lastClipboardUrl', url)
            QTimer.singleShot(400, lambda:[setattr(self.clipboard, 'lastClipboardUrl', None), self.detectSameUrl()])

    def detectSameUrl(self):
        doc = self.ui.textBrowser.toPlainText()
        txt = str(doc).split('\n')

        #ignore the print debug statements

        for cb in txt:
            if cb:
                if cb.rstrip() == self.clipboard.text().rstrip():
                    print("caught")
                    return
                if cb in self.clipboard.text():
                    print("poop")
                    if len(cb) == len(self.clipboard.text()) + 1:
                        print("poopity")
                        return
                    if "\n" in cb or "\r" in cb :
                        print("scoop")
                        return

        self.ui.textBrowser.append("<a>" + self.clipboard.text() + "</a>")
        

if __name__ == "__main__":
    
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()

    keyboard.add_hotkey('end', lambda: app.exit(), suppress=True)
    app.exec()

