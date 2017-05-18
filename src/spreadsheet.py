
import string
import polish_calc as pc


class Cell:
    def __init__(self, value='', row=0, column=0, spread_sheet=None):
        self.value = value.strip().upper()
        self.spread_sheet = spread_sheet
        if column > 25:
            raise ValueError('Max value of column is 25')
        if row > 99:
            raise ValueError('Max value of row is 99')
        self.row_number = row
        self.column_number = column
        self.reference = self.get_reference()

    def __repr__(self):
        return str(self.get_result())

    def __str__(self):
        return 'value       = "{val}" \n' \
               'reference   = {ref} \n' \
               'result      = {res} '.format(val=self.value,
                                             ref=self.reference,
                                             res=self.get_result())

    def evaluate(self):
        tokens = pc.parse(self.value)
        new_tokens = []
        for token in tokens:
            if pc.is_reference(token):
                x, y = pc.get_coordination(token)
                try:
                    val = str(self.spread_sheet[x][y].get_result())
                except:
                    return 'Error'
            else:
                val = token
            new_tokens.append(val)
        try:
            return eval(''.join(new_tokens[1:]))
        except:
            return 'Error'

    def is_formula(self):
        if self.value is not '':
            if self.value[0] == '=':
                return True
            else:
                return False
        else:
            return False

    def get_result(self):
        if not self.is_formula():
            return self.value
        else:
            #return pc.calc_polish(self.value[1:], self.spread_sheet)
            return self.evaluate()

    def parse(self):
        if not self.is_formula():
            return None
        else:
            return pc.polish(self.value[1:])

    def get_reference(self):
        return list(string.ascii_uppercase)[self.column_number] + str(self.row_number)

    def set_value(self, value=''):
        self.value = value.strip().upper()

    def is_reference(x):
        return x[0] in string.ascii_uppercase and pc.is_number(x[1:])

class SpreadSheetItems:
    def __init__(self):
        self.spread_sheet = []
        for i in range(0, 100):
            temp = []
            for j in range(0, 26):
                temp.append(Cell(row=i, column=j, spread_sheet=self.spread_sheet))
            self.spread_sheet.append(temp)

    def cell(self, i, j):
        return self.spread_sheet[i][j]

    def show(self):
        for i in self.spread_sheet:
            print(i)



if __name__ == '__main__':
    x = SpreadSheetItems()
    x.cell(0, 0).set_value('=A1+1')
    x.cell(0, 1).set_value('=A0 + 1')
    x.cell(0, 2).set_value('= 2^ (1+3 ')
    x.cell(0, 3).set_value('=2^2^2')
    x.cell(0, 4).set_value('= 2^(1+3)')

    x.show()
