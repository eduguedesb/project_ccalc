import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ScientificCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Científica")
        self.setGeometry(100, 100, 400, 600)  # Ajustando o tamanho da janela
        self.initUI()

    def initUI(self):
        # Criação do widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Campo de resultado (visor)
        self.result_field = QLineEdit(self)
        self.result_field.setAlignment(Qt.AlignRight)
        self.result_field.setFixedHeight(50)  # Tamanho do visor
        self.result_field.setFont(QFont('Arial', 20, QFont.Bold))  # Fonte do visor
        self.result_field.setReadOnly(True)
        self.result_field.setStyleSheet("background-color: #D3D3D3; color: black; border: 2px solid #A9A9A9; padding: 10px;")  # Visor cinza claro com texto preto

        # Layout principal vertical
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.result_field)

        # Layout em grade para os botões
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(10)

        # Lista dos botões da calculadora científica
        buttons = [
            ('²√x', 0, 0), ('π', 0, 1), ('e', 0, 2), ('C', 0, 3), ('⌫', 0, 4),
            ('x²', 1, 0), ('|x|', 1, 1), ('exp', 1, 2), ('mod', 1, 3), ('÷', 1, 4),
            ('x^y', 2, 0), ('(', 2, 1), (')', 2, 2), ('n!', 2, 3), ('×', 2, 4),
            ('10^x', 3, 0), ('7', 3, 1), ('8', 3, 2), ('9', 3, 3), ('-', 3, 4),
            ('log', 4, 0), ('4', 4, 1), ('5', 4, 2), ('6', 4, 3), ('+', 4, 4),
            ('ln', 5, 0), ('1', 5, 1), ('2', 5, 2), ('3', 5, 3),
            ('1/x', 6, 0), ('0', 6, 1), ('.', 6, 2), ('+/-', 6, 3)
        ]

        # Criação dos botões e adição ao layout em grade
        for btn_text, row, col, rowspan, colspan in [(btn[0], btn[1], btn[2], 1, 1) if len(btn) == 3 else btn for btn in buttons]:
            button = QPushButton(btn_text)
            button.setFixedSize(60, 60)  # Tamanho dos botões
            button.setFont(QFont('Arial', 12, QFont.Bold))  # Fonte dos botões
            
            # Definindo cores dos botões
            if btn_text in ['÷', '×', '-', '+', '=', 'C', '⌫', 'mod']:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #8B0000;
                        color: white;
                        border: 2px solid #B22222;
                    }
                    QPushButton:pressed {
                        background-color: #B22222;
                    }
                """)  # Efeito de pressionamento: vermelho escuro ao clicar
            elif btn_text in ['π', 'e', '²√x', 'x²', 'x^y', '10^x', 'log', 'ln', 'exp', 'n!', '1/x', '|x|', '(', ')']:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #1E90FF;
                        color: white;
                        border: 2px solid #4682B4;
                    }
                    QPushButton:pressed {
                        background-color: #4682B4;
                    }
                """)  # Efeito de pressionamento: azul mais escuro ao clicar
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #A9A9A9;
                        color: black;
                        border: 2px solid #696969;
                    }
                    QPushButton:pressed {
                        background-color: #696969;
                    }
                """)  # Efeito de pressionamento: cinza mais escuro ao clicar

            button.clicked.connect(lambda checked, txt=btn_text: self.on_click(txt))
            grid_layout.addWidget(button, row, col, rowspan, colspan)

        # Botão de igual, alinhado com o topo do botão 3 e a base do botão +/-
        equal_button = QPushButton("=")
        equal_button.setFixedSize(60, 120)  # Ocupa duas linhas verticais
        equal_button.setFont(QFont('Arial', 12, QFont.Bold))
        equal_button.setStyleSheet("""
            QPushButton {
                background-color: #006400;
                color: white;
                border: 2px solid #228B22;
            }
            QPushButton:pressed {
                background-color: #228B22;
            }
        """)  # Efeito de pressionamento: verde mais escuro ao clicar
        equal_button.clicked.connect(lambda: self.on_click('='))
        grid_layout.addWidget(equal_button, 5, 4, 2, 1)  # Ocupa da linha do botão "3" até o botão "+/-"

        # Adicionando o layout de botões ao layout principal
        main_layout.addLayout(grid_layout)

        # Define o layout no widget central
        central_widget.setLayout(main_layout)

        # Estilo da janela principal (fundo preto)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
        """)

    def on_click(self, char):
        try:
            if char == 'C':
                self.result_field.clear()
            elif char == '⌫':
                current_text = self.result_field.text()
                self.result_field.setText(current_text[:-1])  # Apaga o último caractere
            elif char == '=':
                self.evaluate_expression()
            elif char == 'exp':
                self.result_field.setText(self.result_field.text() + 'e')
            elif char == 'mod':
                self.result_field.setText(self.result_field.text() + '%')
            elif char == 'π':
                self.result_field.setText(self.result_field.text() + str(math.pi))
            elif char == 'e':
                self.result_field.setText(self.result_field.text() + str(math.e))
            elif char == 'n!':
                self.calculate_factorial()
            elif char == 'x²':
                self.square_number()
            elif char == '²√x':
                self.square_root()
            elif char == 'x^y':
                self.result_field.setText(self.result_field.text() + '**')
            elif char == 'log':
                self.logarithm_base_10()
            elif char == 'ln':
                self.natural_logarithm()
            elif char == '|x|':
                self.absolute_value()
            elif char == '10^x':
                self.result_field.setText(self.result_field.text() + '10**')
            elif char == '1/x':
                self.reciprocal()
            elif char == '+/-':
                self.negate()
            else:
                current_text = self.result_field.text()
                self.result_field.setText(current_text + char)
        except Exception:
            self.result_field.setText("Erro")

    def evaluate_expression(self):
        try:
            expression = self.result_field.text()
            expression = expression.replace('÷', '/').replace('×', '*').replace('^', '**').replace('%', ' % ')
            result = eval(expression)
            self.result_field.setText(str(self.format_result(result)))
        except:
            self.result_field.setText("Erro")

    def format_result(self, result):
        """Função para formatar o resultado, removendo o .0 se for um inteiro"""
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result

    def calculate_factorial(self):
        try:
            current_value = int(self.result_field.text())
            self.result_field.setText(str(math.factorial(current_value)))
        except Exception:
            self.result_field.setText("Erro")

    def square_number(self):
        try:
            current_value = float(self.result_field.text())
            self.result_field.setText(str(self.format_result(current_value ** 2)))
        except Exception:
            self.result_field.setText("Erro")

    def square_root(self):
        try:
            current_value = float(self.result_field.text())
            self.result_field.setText(str(self.format_result(math.sqrt(current_value))))
        except Exception:
            self.result_field.setText("Erro")

    def logarithm_base_10(self):
        try:
            current_value = float(self.result_field.text())
            self.result_field.setText(str(self.format_result(math.log10(current_value))))
        except Exception:
            self.result_field.setText("Erro")

    def natural_logarithm(self):
        try:
            current_value = float(self.result_field.text())
            self.result_field.setText(str(self.format_result(math.log(current_value))))
        except Exception:
            self.result_field.setText("Erro")

    def absolute_value(self):
        try:
            current_value = float(self.result_field.text())
            self.result_field.setText(str(self.format_result(abs(current_value))))
        except Exception:
            self.result_field.setText("Erro")

    def reciprocal(self):
        try:
            current_value = float(self.result_field.text())
            if current_value == 0:
                self.result_field.setText("Erro")
            else:
                self.result_field.setText(str(self.format_result(1 / current_value)))
        except Exception:
            self.result_field.setText("Erro")

    def negate(self):
        try:
            current_text = self.result_field.text()
            if current_text and current_text[0] == '-':
                self.result_field.setText(current_text[1:])  # Remove o sinal negativo
            else:
                self.result_field.setText('-' + current_text)  # Adiciona o sinal negativo
        except Exception:
            self.result_field.setText("Erro")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ScientificCalculator()
    window.show()
    sys.exit(app.exec_())
