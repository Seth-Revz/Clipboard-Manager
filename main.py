from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
import keyboard

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.clipboard = app.clipboard()
        self.clipboard.dataChanged.connect(self.detectClipboardUrl)

        #self.ui = Ui_MainWindow()
        #self.ui.setupUi(self)
    
    def detectClipboardUrl(self):
        clipboardText = self.clipboard.text()
        if getattr(self.clipboard, 'lastClipboardUrl', None) != clipboardText:
            url = clipboardText
            setattr(self.clipboard, 'lastClipboardUrl', url)
            QTimer.singleShot(400, lambda:setattr(self.clipboard, 'lastClipboardUrl', None))
            QTimer.singleShot(400, lambda:print(self.clipboard.text()))
            print("p")

if __name__ == "__main__":
    
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    #mainWindow.show()

    mainWindow.detectClipboardUrl()

    keyboard.add_hotkey('end', lambda: app.exit(), suppress=True)
    app.exec()

