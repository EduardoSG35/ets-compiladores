class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.current_position = 0
        self.current_char = self.text[self.current_position]

    def advance(self):
        self.current_position += 1
        if self.current_position < len(self.text):
            self.current_char = self.text[self.current_position]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token("INTEGER", self.integer())

            if self.current_char == "+":
                self.advance()
                return Token("PLUS")

            if self.current_char == "-":
                self.advance()
                return Token("MINUS")

            if self.current_char == "*":
                self.advance()
                return Token("MULTIPLY")

            if self.current_char == "/":
                self.advance()
                return Token("DIVIDE")

            if self.current_char == "(":
                self.advance()
                return Token("LPAREN")

            if self.current_char == ")":
                self.advance()
                return Token("RPAREN")

            raise ValueError(f"Carácter inválido: {self.current_char}")

        return Token("EOF")


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise ValueError(message)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Token incorrecto. Se esperaba {token_type} pero se encontró {self.current_token.type}")

    def factor(self):
        if self.current_token.type == "INTEGER":
            value = self.current_token.value
            self.eat("INTEGER")
            return value
        elif self.current_token.type == "LPAREN":
            self.eat("LPAREN")
            result = self.expression()
            self.eat("RPAREN")
            return result

        self.error(f"Factor inválido. Se esperaba INTEGER o LPAREN pero se encontró {self.current_token.type}")

    def term(self):
        result = self.factor()

        while self.current_token.type in ["MULTIPLY", "DIVIDE"]:
            token_type = self.current_token.type

            if token_type == "MULTIPLY":
                self.eat("MULTIPLY")
                result *= self.factor()
            elif token_type == "DIVIDE":
                self.eat("DIVIDE")
                divisor = self.factor()
                if divisor == 0:
                    self.error("División entre cero no está permitida")
                result /= divisor

        return result

    def expression(self):
        result = self.term()

        while self.current_token.type in ["PLUS", "MINUS"]:
            token_type = self.current_token.type

            if token_type == "PLUS":
                self.eat("PLUS")
                result += self.term()
            elif token_type == "MINUS":
                self.eat("MINUS")
                result -= self.term()

        return result

    def parse(self):
        return self.expression()


def main():
    while True:
        try:
            text = input("Ingrese una expresión aritmética (o 'exit' para salir): ")
            if text == "exit":
                break

            lexer = Lexer(text)
            parser = Parser(lexer)
            result = parser.parse()
            print(f"El resultado es: {result}")
        except ValueError as e:
            print("Error:", str(e))


if __name__ == "__main__":
    main()
