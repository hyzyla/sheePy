from PyQt5.Qt import *
import sys
from SpreadSheetClass import SpreadSheet
from StartWindow import StartWindow


class MainWindow(QMainWindow):

    def do_nothing(self):
        print("ENTER")
        self.sheet.setCurrentItem(None)

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.config_window()
        self.sheet = SpreadSheet(self)
        self.create_action()
        self.config_toolbar()
        self.config_spreadsheet()
        self.create_menus()

    def config_window(self):
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.setWindowIcon(QIcon("icons\\run-build.png"))
        self.setWindowTitle('SheePy')

    def config_spreadsheet(self):
        self.setCentralWidget(self.sheet)
        self.sheet.setRangeSelected(QTableWidgetSelectionRange(0, 0, 0, 0), True)
        self.sheet.edit(self.sheet.indexAt(QPoint()))

    def discard_changes(self):
        self.sheet.close_editor()
        self.line_edit.clearFocus()
        self.sheet.edit(self.sheet.selectedIndexes()[0])

    def create_action(self):
        self.cancel_edit = QAction(QIcon("icons\\application-exit.png"), "Undo editing", self)
        self.cancel_edit.triggered.connect(self.discard_changes)
        self.apply_edit = QAction(QIcon("icons\\run-build.png"), "&Apply editing", self)
        self.apply_edit.triggered.connect(self.sheet.applying_changes)

    def config_toolbar(self):
        self.toolbar = QToolBar("Toolbar")
        self.line_edit = QLineEdit("Select cell for editing")
        self.line_edit.returnPressed.connect(self.sheet.applying_changes)
        self.toolbar.addWidget(self.line_edit)
        self.toolbar.addAction(self.apply_edit)
        self.toolbar.addAction(self.cancel_edit)
        self.addToolBar(self.toolbar)

    def create_menus(self):
        self.file_menu = self.menuBar().addMenu('File')
        self.edit_menu = self.menuBar().addMenu('Edit')
        self.edit_menu.addAction(self.apply_edit)
        self.edit_menu.addAction(self.cancel_edit)
        self.about_menu = self.menuBar().addMenu('About')

if __name__ == '__main__':
    #sw = StartWindow().mainloop()
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec_()
    app.exit()
