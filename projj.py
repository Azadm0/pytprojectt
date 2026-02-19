import tkinter
import math

class Calculator:
    def __init__(self):
        self.button_values = [
            ['HEX','DEC','BIN','OCT'],
            ['AC','+/','%','÷'],
            ['7','8','9','×'],
            ['4','5','6','-'],
            ['1','2','3','+'],
            ['0','.','√','=']
        ]
        self.topsymbols = ['HEX','DEC','BIN','OCT']
        self.rightsymbols = ['÷','×','-','+','=']
        self.greyy = "#999E97"
        self.darkgrey = "#545454"
        self.orange = "#e55c26"
        self.wwhite = "#ffffff"
        self.window = tkinter.Tk()
        self.window.title('pyproject')
        self.window.resizable(False, False)

        self.frame = tkinter.Frame(self.window)
        self.frame.pack()

        self.label = tkinter.Label(
            self.frame, text="0", font=("Arial", 45),
            background=self.greyy, foreground=self.wwhite,
            anchor='e', width=4
        )
        self.label.grid(row=0, column=0, columnspan=4, sticky='we')
        self.state = {
            'first_number': None,
            'operator': None,
            'base': 'DEC',
            'label': self.label,
            'buttons': {}
        }
        self.create_buttons()
        self.update_buttons()
        self.window.mainloop()

    def reset(self):
        self.state['first_number'] = None
        self.state['operator'] = None
        self.state['base'] = 'DEC'
        self.state['label']['text'] = '0'
        self.update_buttons()

    def format_number(self, n):
        if n % 1 == 0:
            return str(int(n))
        return str(n)
    def valid_dec(self, text):
        if text == '' or text == '-' or text == '.':
            return False
        if text.count('.') > 1:
            return False
        if text.startswith('-'):
            text = text[1:]
        return text.replace('.', '', 1).isdigit()

    def valbin(self, text):
        if text == '': 
            return False
        return all(c in '01' for c in text)

    def valoct(self, text):
        if text == '': 
            return False
        return all(c in '01234567' for c in text)

    def valhex(self, text):
        if text == '': 
            return False
        return all(c in '0123456789ABCDEFabcdef' for c in text)

    def button_clicked(self, value):
        state = self.state
        
        if value in '0123456789':
            if state['label']['text'] == '0':
                state['label']['text'] = value
            else:
                state['label']['text'] += value

        elif value == '.':
            if '.' not in state['label']['text']:
                state['label']['text'] += '.'

        elif value == 'AC':
            self.reset()

        elif value == '+/':
            if state['base'] == 'DEC' and self.valid_dec(state['label']['text']):
                state['label']['text'] = self.format_number(float(state['label']['text']) * -1)

        elif value == '%':
            if state['base'] == 'DEC' and self.valid_dec(state['label']['text']):
                state['label']['text'] = self.format_number(float(state['label']['text']) / 100)

        elif value == '√':
            if state['base'] != 'DEC' or not self.valid_dec(state['label']['text']):
                state['label']['text'] = 'Error'
                return
            num = float(state['label']['text'])
            if num < 0:
                state['label']['text'] = 'Error'
                return
            state['label']['text'] = self.format_number(math.sqrt(num))

        elif value in '+-×÷':
            if state['base'] != 'DEC' or not self.valid_dec(state['label']['text']):
                state['label']['text'] = 'Error'
                return
            current = float(state['label']['text'])
            if state['first_number'] is None:
                state['first_number'] = current
            else:
                if state['operator'] == '+': state['first_number'] += current
                elif state['operator'] == '-': state['first_number'] -= current
                elif state['operator'] == '×': state['first_number'] *= current
                elif state['operator'] == '÷': state['first_number'] /= current

            state['operator'] = value
            state['label']['text'] = '0'

        elif value == '=':
            if state['base'] != 'DEC' or state['first_number'] is None or state['operator'] is None:
                return
            if not self.valid_dec(state['label']['text']):
                state['label']['text'] = 'Error'
                return
            second = float(state['label']['text'])
            if state['operator'] == '+': 
                result = state['first_number'] + second
            elif state['operator'] == '-': 
                result = state['first_number'] - second
            elif state['operator'] == '×': 
                result = state['first_number'] * second
            elif state['operator'] == '÷':
                result = state['first_number'] / second
            state['label']['text'] = self.format_number(result)
            state['first_number'] = None
            state['operator'] = None

        elif value in self.topsymbols:
            text = state['label']['text']
            if state['base'] == 'DEC' and self.valid_dec(text):
                num = int(float(text))
            elif state['base'] == 'BIN' and self.valbin(text): 
                num = int(text, 2)
            elif state['base'] == 'OCT' and self.valoct(text): 
                num = int(text, 8)
            elif state['base'] == 'HEX' and self.valhex(text): 
                num = int(text, 16)
            else:
                state['label']['text'] = 'Error'
                return

            if value == 'BIN':
                state['label']['text'] = bin(num)[2:]
                state['base'] = 'BIN'
            elif value == 'HEX':
                state['label']['text'] = hex(num)[2:]
                state['base'] = 'HEX'
            elif value == 'OCT':
                state['label']['text'] = oct(num)[2:]
                state['base'] = 'OCT'
            elif value == 'DEC':
                state['label']['text'] = str(num)
                state['base'] = 'DEC'

            self.update_buttons()

    def update_buttons(self):
        for v in ['+','-','×','÷','√','%','+/','.','=']:
            if self.state['base'] == 'DEC':
                self.state['buttons'][v]['state'] = 'normal'
            else:
                self.state['buttons'][v]['state'] = 'disabled'

    def create_buttons(self):
        for r in range(len(self.button_values)):
            for c in range(4):
                v = self.button_values[r][c]
                b = tkinter.Button(
                    self.frame, text=v, font=("Arial", 30),
                    width=3, height=1,
                    command=lambda x=v: self.button_clicked(x)
                )
                b.grid(row=r+1, column=c)
                self.state['buttons'][v] = b

                if v in self.topsymbols:
                    b.config(background=self.greyy, foreground=self.wwhite)
                elif v in self.rightsymbols:
                    b.config(background=self.orange, foreground=self.wwhite)
                else:
                    b.config(background=self.darkgrey, foreground=self.wwhite)
Calculator()
