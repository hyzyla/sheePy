from PyQt5.Qt import *

class LineEditDelegate(QItemDelegate):
    def __init__(self, sheet):
        QItemDelegate.__init__(self)
        self.sheet = sheet
        self._isEdit = False

    def createEditor(self, parent, style_option_view, model_index):
        self.editor = QLineEdit(parent)
        print("CREATE DELEGATE")
        return self.editor

    def setEditorData(self, widget, model_index):
        self.sheet.set_line_edit()
        self._isEdit = True
        x = model_index.row()
        y = model_index.column()
        formula = self.sheet.item(x, y).formula
        self.editor.setText(formula)
        print("START DELEGATE")

    def setModelData(self, widget, abstract_model_item, model_item, res=None):
        self._isEdit = False
        x = model_item.row()
        self.sheet.set_line_edit()
        y = model_item.column()
        if res is None:
            self.sheet.item(x, y).setText(self.editor.text())
        else:
            self.sheet.item(x, y).setText(self.sheet.parent.line_edit.text())
        result = self.sheet.item(x, y).getResult()
        abstract_model_item.setData(model_item, result)

        for i in range(0, 60):
            for j in range(0, 28):
                result = self.sheet.item(i, j).getResult()
                model_index = abstract_model_item.index(i, j)
                abstract_model_item.setData(model_index, result)

        self.sheet.update(model_item)
        print("SET MODEL DATA")

    def closeEditor(self, *args, **kwargs):
        print("CLOSE DELEGATE")
        self.editor.close()
        self._isEdit = False

    def destroyEditor(self, QWidget, QModelIndex):
        print("DESTROY DELEGATE")
        self.closeEditor()
        self._isEdit = False

    def isEditing(self):
        return self._isEdit