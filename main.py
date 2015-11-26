from PyQt4.QtGui import *
from PyQt4.QtCore import *

#Contains Mainwindow
from main_window import *		

def main():
    app = QApplication(sys.argv)
    win = central()
    win.setWindowTitle("Syncer")
    win.resize(1300, 650)
    win.move(30, 30)

    win.setStyleSheet("QMainWindow::separator { width : 1px;}")
    pal = QPalette()
    pal.setColor(QPalette.Background, Qt.white)
    win.setPalette(pal)
        
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

#01078525
