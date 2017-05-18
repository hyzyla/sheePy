from PyQt5.Qt import *
from LineEditDelegate import LineEditDelegate
from CellClass import Cell
import string


class SpreadSheet(QTableWidget):

    def __init__(self, parent=None):
        self.parent = parent
        QTableWidget.__init__(self, parent)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.delegate = LineEditDelegate(self)
        self.setItemDelegate(self.delegate)
        self.setColumnCount(28)
        self.setRowCount(60)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setItemPrototype(Cell('99', self))
        for i in range(0, 28):
            for j in range(0, 60):
                self.setItem(j, i, Cell('', self))

        self.setHorizontalHeaderLabels([x for x in string.ascii_uppercase])
        self.cellClicked.connect(self.open_editor)
        self.cellActivated.connect(self.open_editor)
        self.itemSelectionChanged.connect(self.set_line_edit)
        self.cellChanged.connect(self.close_editor)
        self.itemPressed.connect(self.open_editor)
        self.delete_item = QAction("Видалити вміст клітинки", self)
        self.delete_item.setShortcut(Qt.Key_Delete)
        self.delete_item.triggered.connect(self.delete_cell)
        self.addAction(self.delete_item)


    def delete_cell(self):
        x = self.currentIndex().row()
        y = self.currentIndex().column()
        self.removeCellWidget(x, y)
        self.setItem(x, y, Cell('', self))
        self.update_sheet()

    def update_sheet(self):
        for i in range(0, 60):
            for j in range(0, 28):
                result = self.item(i, j).getResult()
                model_index = self.model().index(i, j)
                self.model().setData(model_index, result)

    def applying_changes(self):
        x = self.selectedIndexes()[0].row()
        y = self.selectedIndexes()[0].column()
        self.setItem(x, y, Cell(self.parent.line_edit.text(), self))
        self.update_sheet()
        self.parent.line_edit.clearFocus()
        self.setFocus()

    def set_line_edit(self):
        self.parent.line_edit.setText(self.selectedItems()[0].formula)

    def open_editor(self):
        self.edit(self.selectedIndexes()[0])
        self.set_line_edit()

    def close_editor(self):
        self.closeEditor(self.delegate.editor, QAbstractItemDelegate.NoHint)