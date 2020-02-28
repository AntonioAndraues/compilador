class Token(object):
    def __init__(self, type_="", value=""):
        self.type_ = type_
        self.value = value


def get_type(str):
    if(str == "+"):
        return "soma"
    elif(str == "-"):
        return "sub"
    elif(str == " "):
        return "espaço"
    elif(str.isdigit()):
        return "int"
    elif(str == "/"):
        return "div"
    elif(str == "*"):
        return "mult"


class Tokenizer(object):
    def __init__(self, origin, position, actual):
        self.origin = origin
        self.position = 0
        self.actual = Token()

    def selectNext(self):
        self.actual.value = ""
        if(len(self.origin) == self.position):
            self.actual.value = ""
            self.actual.type_ = "EOF"
            return
        while(self.origin[self.position] == " "):
            self.position += 1
            if(self.position == len(self.origin)):
                self.actual.value = ""
                self.actual.type_ = "EOF"
                return
        while(self.origin[self.position].isdigit()):
            self.actual.value += self.origin[self.position]
            self.actual.type_ = "int"
            self.position += 1
            if(len(self.origin) == self.position):
                return
            if(get_type(self.origin[self.position]) != 'int'):
                return

        if(get_type(self.origin[self.position]) != 'int'):
            self.actual.type_ = get_type(self.origin[self.position])
            self.actual.value = self.origin[self.position]
            self.position += 1
            return
        return


class Parser(object):
    @staticmethod
    def parseExpression(tokenizador):
        resultado = 0
        tokenizador.selectNext()
        if(tokenizador.actual.value.isdigit()):
            resultado = int(tokenizador.actual.value)
            tokenizador.selectNext()
            while(tokenizador.actual.value == "+" or tokenizador.actual.value == "-" or tokenizador.actual.value == "/" or tokenizador.actual.value == "*"):
                if(tokenizador.actual.value == "+"):
                    tokenizador.selectNext()
                    if(tokenizador.actual.value.isdigit()):
                        resultado += int(tokenizador.actual.value)
                    else:
                        raise TypeError("ERRO:")
                if(tokenizador.actual.value == "-"):
                    tokenizador.selectNext()
                    if(tokenizador.actual.value.isdigit()):
                        resultado += int(tokenizador.actual.value)*-1
                    else:
                        raise TypeError("ERRO:")
                if(tokenizador.actual.value == "/"):
                    tokenizador.selectNext()
                    if(tokenizador.actual.value.isdigit()):
                        resultado /= int(tokenizador.actual.value)
                    else:
                        raise TypeError("ERRO:")
                if(tokenizador.actual.value == "*"):
                    tokenizador.selectNext()
                    if(tokenizador.actual.value.isdigit()):
                        resultado *= int(tokenizador.actual.value)
                    else:
                        raise TypeError("ERRO:")
                tokenizador.selectNext()
            if(tokenizador.actual.type_ != "EOF"):
                raise TypeError("EOF not found")
            else:
                print(resultado)
                return resultado
        else:
            raise TypeError("ERRO: Innitial not a number")

    @staticmethod
    def run(code):
        tokenizador = Tokenizer("", 0, 0)
        tokenizador.origin = code
        return Parser.parseExpression(tokenizador)


def main():
    import sys
    parser = Parser()
    resultado = parser.run(sys.argv[1])


if __name__ == "__main__":
    main()
