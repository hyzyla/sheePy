from PyQt5.Qt import *
import sys

class StartWindow(QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QMainWindow.__init__(self)
        self.config_window()

    def mainloop(self):
        self.show()
        self.app.exec_()
        self.app.exit()

    def config_window(self):
        self.setMinimumHeight(400)
        self.setMinimumWidth(400)
        self.setMaximumWidth(400)
        self.setMaximumHeight(400)
        self.setWindowIcon(QIcon("icons/document-new.png"))
        self.setWindowTitle("Вітаю у моїй програмі!")
        self.setWindowFlags(Qt.Dialog)

        self.box = QGridLayout()
        self.okButton = QPushButton("Почати редагування", self)
        self.okButton.setMaximumWidth(200)

        self.okButton.clicked.connect(self.exit_window)
        self.textInfo = QLabel(self)
        self.textInfo.setAlignment(Qt.AlignLeft)
        self.textInfo.setWordWrap(True)
        self.textInfo.setText('Вітаю у моєму рахувальнику. '
                                'Ця програма копіює поведінку'
                                'комерційної програми Microsoft Excel. '
                                'Але має свої недоліки і переваги, '
                                'а також є повністю безкоштовною!\n\n'
                                'Синтаксис виразу у програмі:\n\n'
                                '<вираз> ::= =<формула>\n\n'
                                '<формула> ::= <дужкова форма> | \n'
                                '\t\t<формула>{<операція><формула>} | \n'
                                '\t\t<посилання> | <число> | <функція> \n\n'
                                '<операція> ::= * | ^ | / | + | - \n\n'
                                '<дужкова форма> ::= ( <формула> )\n\n'
                                '<посилання> ::= <буква><число>\n\n'
                                '<число> ::= <цифра>{<цифра>}\n\n'
                                '<цифра> ::= 1|2|3|...|8|9| "0"\n\n'
                                '<буква> ::= a|b|...|y|z \n\n'
                                '<функція> ::= <назва функції> ( <функція> ) \n\n'
                                '<назва функції> ::= dec | inc')

        self.box.addWidget(self.textInfo, 0, 0)
        self.box.addWidget(self.okButton, 1, 0)
        self.box.setAlignment(self.okButton, Qt.AlignHCenter)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.box)

    def exit_window(self):
        self.close()

if __name__ == '__main__':
    sw = StartWindow().mainloop()