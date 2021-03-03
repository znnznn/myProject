import sys

import math

from functools import partial
from typing import Union, NoReturn


from PyQt5.QtWidgets import (QApplication,
                             QComboBox,
                             QSizePolicy,
                             QWidget,
                             QVBoxLayout,
                             QGridLayout,
                             QMainWindow,
                             QPushButton,
                             QLineEdit,
                             QLabel)


class MyCalculatorInWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        """ Creates a calculator window"""
        super().__init__(*args, **kwargs)
        self.setWindowTitle('C A L C U L A T O R')
        self.widget = QWidget(self.setGeometry(600, 300, 500, 500))
        #  widget = QWidget(self.setFixedSize(550, 550))
        self.first_label = QLabel('<h1><b><i>Стандартний калькулятор</i></b></h1>')
        self.editArea = QLineEdit('')
        self.editArea.setReadOnly(True)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.first_label)
        mainLayout.addWidget(self.editArea)
        self.second_label = QLabel('')
        mainLayout.addWidget(self.second_label)

        buttonLayout = QGridLayout()
        self.button_round = QComboBox()
        mainLayout.addWidget(self.button_round)
        self.result = ['']
        self.work = False
        self.one_digit = ['0']
        self.two_digit = ['']
        self.mark = ['']
        self.calc_round = ['']
        self.button_round.addItems(['ЗАОКРУГЛЕННЯ',
                                    '1', '2', '3', '5', '6', '10'])
        buttons = [
            {
                'name': '1',
                'row': 3,
                'col': 0
            },
            {
                'name': '2',
                'row': 3,
                'col': 1
            },
            {
                'name': '3',
                'row': 3,
                'col': 2
            },
            {
                'name': '+',
                'row': 3,
                'col': 3
            },
            {
                'name': '4',
                'row': 2,
                'col': 0
            },
            {
                'name': '5',
                'row': 2,
                'col': 1
            },
            {
                'name': '6',
                'row': 2,
                'col': 2
            },
            {
                'name': '-',
                'row': 2,
                'col': 3
            },
            {
                'name': '7',
                'row': 1,
                'col': 0
            },
            {
                'name': '8',
                'row': 1,
                'col': 1
            },
            {
                'name': '9',
                'row': 1,
                'col': 2
            },
            {
                'name': '*',
                'row': 1,
                'col': 3
            },
            {
                'name': '0',
                'row': 4,
                'col': 1
            },
            {
                'name': '.',
                'row': 4,
                'col': 2
            },
            {
                'name': '=',
                'row': 4,
                'col': 3,
                'colSpan': 2
            },
            {
                'name': '00',
                'row': 4,
                'col': 0,
            },
            {
                'name': 'C',
                'row': 0,
                'col': 0,
            },
            {
                'name': '%',
                'row': 0,
                'col': 1,
            },
            {
                'name': '←',
                'row': 0,
                'col': 2,
            },
            {
                'name': '÷',
                'row': 0,
                'col': 3
            },
            {
                'name': 'X²',
                'row': 0,
                'col': 4
            },
            {
                'name': '√',
                'row': 1,
                'col': 4
            },
            {
                'name': 'X !',
                'row': 2,
                'col': 4
            },
            {
                'name': '+/-',
                'row': 3,
                'col': 4
            }
        ]
        self.buttons = {}
        for buttonConfig in buttons:
            name = buttonConfig.get('name', '')
            btn = QPushButton(name)
            btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            self.buttons[name] = btn
            buttonLayout.addWidget(btn,
                                   buttonConfig['row'],
                                   buttonConfig['col'],
                                   1,
                                   buttonConfig.get('colSpan', 1))
        mainLayout.addLayout(buttonLayout)
        self.widget.setLayout(mainLayout)
        self.setCentralWidget(self.widget)

        for buttonName in self.buttons:
            btn = self.buttons[buttonName]
            if buttonName == 'C':
                btn.clicked.connect(self.end)
            elif buttonName == '+':
                btn.clicked.connect(partial(self.addSecondLable, buttonName))
            elif buttonName == '-':
                btn.clicked.connect(partial(self.addSecondLable, buttonName))
            elif buttonName == '.':
                btn.clicked.connect(partial(self.point_only_once, buttonName))
            elif buttonName == '%':
                btn.clicked.connect(partial(self.result_percent))
            elif buttonName == '*':
                btn.clicked.connect(partial(self.addSecondLable, buttonName))
            elif buttonName == '÷':
                btn.clicked.connect(partial(self.addSecondLable, '/'))
            elif buttonName == '←':
                btn.clicked.connect(partial(self.editAreaText_pop))
            elif buttonName == '+/-':
                btn.clicked.connect(partial(self.positive_negative_number))
            elif buttonName == 'X²':
                btn.clicked.connect(partial(self.result_pow))
            elif buttonName == 'X !':
                btn.clicked.connect(partial(self.result_factorial))
            elif buttonName == '√':
                btn.clicked.connect(partial(self.result_root))
            elif buttonName == '=':
                btn.clicked.connect(partial(self.addSecondLable, str(self.mark[-1])))
            else:
                btn.clicked.connect(partial(self.change_text, buttonName))

    def editAreaText_pop(self) -> str:
        """Get display's text del last item."""
        return self.editArea.setText(str(self.editArea.text()[:-1]))

    def digit_round(self) -> NoReturn:
        """ returns the number of characters after the point """
        self.work = True
        if self.button_round.currentText() == 'ЗАОКРУГЛЕННЯ':
            self.calc_round[-1] = '0'
            return
        self.calc_round[-1] = str(self.button_round.currentText())

    def point_only_once(self, text) -> str:
        """ Сhecks whether a point has been pressed once """
        calc_line = str(self.editArea.text())
        if len(calc_line) > 0 and calc_line.count(text) == 0:
            return self.editArea.setText(self.editArea.text() + text)
        elif len(calc_line) == 0:
            return self.editArea.setText('0' + text)

    def result_pow(self) -> str:
        """ Returns the square of a number """
        try:
            self.digit_round()
            calc_line = str(self.editArea.text())
            if calc_line.count('e') > 0 or calc_line[0] == '-':
                raise ValueError
            if len(calc_line) == 0:
                self.second_label.setText('<h2><b><i>0</i></b></h2>')
                return self.editArea.setText('0')
            else:
                calc_line = str(self.editArea.text())
                text = f'Квадрат числа {calc_line} = '
            if float(calc_line):
                result = float(calc_line) ** 2
            else:
                result = int(calc_line) ** 2
            result_str = f'{result:.{int ( self.calc_round[-1] )}f}'
            self.result.append(f'{text}{result:.{int( self.calc_round[-1])}f}')
            self.second_label.setText(str(f'<h2><b><i>{self.result[-1]}</i></b></h2>'))
            self.editArea.setText(result_str)
        except :
            self.second_label.setText(str(f'<h2><b><i>=Неможливо обрахувати результат{calc_line}</i></b></h2>'))
            return self.editArea.setText('0')

    def result_root(self) -> str:
        """ Returns the square root of a number"""
        try:
            self.digit_round()
            calc_line = str(self.editArea.text())
            if len(calc_line) == 0:
                self.second_label.setText('<h2><b><i>0</i></b></h2>')
                return self.editArea.setText('0')
            else:
                calc_line = str(self.editArea.text())
                text = f'Квадратний корінь числа {calc_line} = '
            if calc_line.count('e') != 0 or calc_line.count('-'):
                raise ValueError
            result = float(calc_line) ** 0.5
            result_str = f'{result:.{int(self.calc_round[-1])}f}'
            self.result.append(f'{text}{result:.{int(self.calc_round[-1])}f}')
            self.second_label.setText(str(f'<h2><b><i>{self.result[-1]}</i></b></h2>'))
            self.editArea.setText(result_str)
        except Exception:
            self.second_label.setText(str(f'<h2><b><i>=Неможливо обрахувати результат {calc_line}</i></b></h2>'))
            return self.editArea.setText('0')

    def result_factorial(self) -> str:
        """ Returns the factorial of a number"""
        calc_line = str(self.editArea.text())
        self.digit_round()
        try:
            if len(calc_line) == 0:
                self.second_label.setText('<h2><b><i>0</i></b></h2>')
                return self.editArea.setText('0')
            elif len(calc_line) > 3 or calc_line.count('e') > 0:
                raise ValueError
            digit = math.trunc(float(calc_line))
            text = f'Факторіал числа {digit} = '
            result = math.factorial(digit)
            self.result.append(f'{text}{result:.{int(self.calc_round[-1])}f}')
            self.second_label.setText(str(f'<h2><b><i>{self.result[-1]}</i></b></h2>'))
            return self.editArea.setText(str(f'{result:.{int(self.calc_round[-1])}f}'))
        except ValueError:
            self.second_label.setText(str(f'<h2><b><i>=Завелике число для обрахунку {calc_line}</i></b></h2>'))
            return self.editArea.setText('0')

    def result_percent(self) -> str:
        """ Gives the result of processing the percentage button """
        try:
            self.digit_round()
            self.two_digit[-1] = self.editArea.text()
            calc_lable = str(self.one_digit[-1])
            calc_line = str(self.two_digit[-1])
            if calc_lable.count('e') > 0:
                raise ValueError
            if calc_lable.count('=') > 0 or len(calc_lable) == 0 or len(calc_line) == 0:
                result = calc_line
                text = f'Неймовірного числа не достатньо = '
                self.second_label.setText(f'<h2><b><i>{text}{result:.{int(self.calc_round[-1])}f}</i></b></h2>')
                return self.editArea.setText(str(f'{result:.{int(self.calc_round[-1])}f}'))
            mark = self.mark[-1]
            percent_expression = float(calc_lable) / 100 * float(calc_line)
            if mark == '+':
                result = float(calc_lable) + percent_expression
                self.second_label.clear()
                self.editArea.clear()
                text = f'{calc_lable} + {calc_line} % = '
                self.second_label.setText(f'<h2><b><i>{text}{result:.{int(self.calc_round[-1])}f}</i></b></h2>')
                return self.editArea.setText(str(f'{result:.{int(self.calc_round[-1])}f}'))
            elif mark == '-':
                result = float(calc_lable) - percent_expression
                self.second_label.clear()
                self.editArea.clear()
                text = f'{calc_lable} - {calc_line} % = '
                self.second_label.setText(f'<h2><b><i>{text}{result:.{int(self.calc_round[-1])}f}</i></b></h2>')
                return self.editArea.setText(str(f'{result:.{int(self.calc_round[-1])}f}'))
            elif mark == '/':
                result = float(calc_lable) * (100/float(calc_line))
                self.second_label.clear()
                self.editArea.clear()
                text = f'{calc_lable} / {calc_line} % = '
                self.second_label.setText(f'<h2><b><i>{text}{result:.{int(self.calc_round[-1])}f}</i></b></h2>')
                return self.editArea.setText(str(f'{result:.{int(self.calc_round[-1])}f}'))
            elif mark == '*':
                result = float(calc_lable) / (100/float(calc_line))
                self.second_label.clear()
                self.editArea.clear()
                text = f'{calc_lable} * {calc_line} % = '
                self.second_label.setText(f'<h2><b><i>{text}{result:.{int(self.calc_round[-1])}f}</i></b></h2>')
                return self.editArea.setText(str(f'{result:.{int(self.calc_round[-1])}f}'))
        except ZeroDivisionError:
            self.second_label.setText(str(f'<h2><b><i> =Увага ділення на ноль{calc_lable}</i></b></h2>'))
            return self.editArea.setText('0')
        except Exception as e:
            self.second_label.setText(str(f'<h2><b><i> =Неможливо обрахувати результат{calc_lable}</i></b></h2>'))
            return self.editArea.setText('0')

    def addSecondLable(self, text):
        """ Adds a number and a sign to second_lable """
        self.work = False
        if self.editArea.text() == '' == self.second_label.text():
            return self.second_label.setText('0')
        elif self.editArea.text() == '':
            self.two_digit[-1] = str(self.one_digit[-1])
            self.mark[-1] = text
            return self.addss()
        elif self.second_label.text() == '' or self.second_label.text().count('='):
            self.one_digit[-1] = str(self.editArea.text())
            self.second_label.setText(str(self.one_digit[-1]))
            self.mark[-1] = str(text)
            return self.editArea.clear()
        else:
            self.one_digit[-1] = str(self.second_label.text())
            self.two_digit[-1] = str(self.editArea.text())
            return self.addss()

    def addss(self) -> str:
        """  Checks which mark and returns the result of calculation """
        try:
            self.digit_round()
            if self.mark[-1] == '+':
                result = float(str(self.one_digit[-1])) + float(str(self.two_digit[-1]))
            elif self.mark[-1] == '-':
                result = float(str(self.one_digit[-1])) - float(str(self.two_digit[-1]))
            elif self.mark[-1] == '*':
                result = float(str(self.one_digit[-1])) * float(str(self.two_digit[-1]))
            elif self.mark[-1] == '/':
                result = float(str(self.one_digit[-1])) / float(str(self.two_digit[-1]))
            self.second_label.setText(str(f'<h2><b><i>Результат виразу {self.one_digit[-1]}'
                                          f'{self.mark[-1]}{self.two_digit[-1]} ='
                                          f' {result:.{int(self.calc_round[-1])}f}</i></b></h2>'))
            return self.editArea.setText(str(f' {result:.{int(self.calc_round[-1])}f}'))
        except ZeroDivisionError:
            self.second_label.setText(str(f'<h2><b><i> =Увага ділення на ноль {self.two_digit[-1]}</i></b></h2>'))
            return self.editArea.setText('0')
        except Exception:
            self.second_label.setText(str(f'<h2><b><i> =Неможливо обрахувати результат</i></b></h2>'))
            return self.editArea.setText('0')

    def change_text(self, text: str) -> str:
        """ Adds a button name to the string."""
        if self.work is True:
            self.one_digit[-1] = self.editArea.text()
            self.editArea.clear()
        self.work = False
        return self.editArea.setText(self.editArea.text() + text)

    def positive_negative_number(self) -> str:
        """Changes the sign of the number to positive or negative """
        calc_line = str(self.editArea.text())
        if len(calc_line) == 0:
            return self.editArea.setText(f'-')
        if calc_line[0] == '-':
            return self.editArea.setText(f'{calc_line[1:]}')
        elif calc_line[0] == '+':
            return self.editArea.setText(f'-{calc_line[1 :]}')
        return self.editArea.setText(f'-{calc_line[0:]}')

    def end(self) -> NoReturn:
        """ Cleans result QLabel and QLineEdit and QWidget """
        self.editArea.clear()
        self.second_label.clear()
        self.result = ['']
        self.mark = ['']
        self.one_digit = ['0']
        self.two_digit = ['']
        self.work = False
        self.widget = self.setGeometry(600, 300, 500, 500)


def main_window() -> None:
    """" calculator start function """
    app = QApplication(sys.argv)
    window = MyCalculatorInWindow()
    window.show()
    return_code = app.exec()
    sys.exit(return_code)


if __name__ == '__main__':
    main_window()
