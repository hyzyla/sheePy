from PyQt5.Qt import *
import string
from polish_calc import calc_polish, polish

class Cell(QTableWidgetItem):
    def __init__(self, formula, sheet):
        QTableWidgetItem.__init__(self)
        self.sheet = sheet
        self.formula = ''
        self.result = ''
        self.setText(formula)
        QTableWidgetItem.setText(self, self.result)

    def setText(self, text):
        self.formula = text.strip().replace(' ', '')
        self.setResult()

    def getResult(self):
        self.setResult()
        return self.result

    def setResult(self):
        if self.formula == '':
            self.result = ''
        elif self.formula[0] == '=':
            self.formula = self.formula.upper()
            self.result = self.evaluate()
        else:
            self.result = self.formula

    def is_num(self, token):
        try:
            float(token)
        except:
            return False
        else:
            return True

    def is_ref(self, token):
        letter = string.ascii_letters
        if token[0] in letter and self.is_num(token[1:]):
            return True
        else:
            return False

    def get_xy(self, token):
        token = token.upper()
        return [string.ascii_uppercase.find(token[0]), int(token[1:])-1]

    @staticmethod
    def mod_func(a, b):
        return a % b

    @staticmethod
    def min_func(a, b):
        return min(a, b)

    @staticmethod
    def max_func(a, b):
        return max(a, b)

    @staticmethod
    def div_func(a, b):
        return int(a) // int(b)

    def evaluate(self):
        tools = {'MOD': self.mod_func,
                 'DIV': self.div_func,
                 'MIN': self.min_func,
                 'MAX': self.max_func}
        formula = self.formula[1:]
        print(formula)
        tokens = self.tokenize(formula)
        new_tokens = []
        for token in tokens:
            if self.is_ref(token):
                x, y = self.get_xy(token)
                try:
                    val = str(self.sheet.item(y, x).getResult())
                except:
                    return 'Reference Error'
            else:
                val = token
            if 'Error' in val:
                return 'Error: Link on the cell with error'
            new_tokens.append(val)
        print(new_tokens)
        try:
            return str(calc_polish(polish(new_tokens)))
            # return str(eval(''.join(new_tokens), tools))
        except SyntaxError as err:
            return err.msg
            # return 'Error'

    def tokenize(self, x):

        letters_and_digits = string.ascii_uppercase + string.digits + '.'
        x = ''.join(x.upper().split())

        ex = []
        temp = ''

        for i in x:
            if i in letters_and_digits:
                temp += i
                continue
            else:
                if temp is not '':
                    ex.append(temp)
                    temp = ''
                ex.append(i)
        if temp is not '':
            ex.append(temp)

        return ex
