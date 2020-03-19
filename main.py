import re
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
    elif(str == "("):
        return "Abre"
    elif(str == ")"):
        return "Fecha"

class Preprocess():
    def remove_comments(code):
        return re.sub(re.compile("\/\*.*?\*\/",re.DOTALL),"",code)


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
    def factor(tokenizador):
        resultado = 0
        if(tokenizador.actual.value.isdigit()):
            resultado = tokenizador.actual.value
            tokenizador.selectNext()
            return resultado
        elif(tokenizador.actual.value == "+"):
            tokenizador.selectNext()
            resultado =+ int(Parser.factor(tokenizador))
            return resultado
        elif(tokenizador.actual.value == "-"):
            tokenizador.selectNext()
            resultado =- int(Parser.factor(tokenizador))
            return resultado
        elif(tokenizador.actual.value == "("):
            tokenizador.selectNext()
            resultado = Parser.parseExpression2(tokenizador)
            if(tokenizador.actual.value == ")"):
                tokenizador.selectNext()
                return resultado
            else:
                raise TypeError("ERRO: NO ')'")
        else:
            raise TypeError("ERRO: factor cant consume token")
        return resultado

    

    @staticmethod
    def parseTerm(tokenizador):
        resultado = int(Parser.factor(tokenizador))
        while(tokenizador.actual.value == "*" or tokenizador.actual.value == "/"):
            if(tokenizador.actual.value == "/"):
                tokenizador.selectNext()
                resultado //= int(Parser.factor(tokenizador))
            if(tokenizador.actual.value == "*"):
                tokenizador.selectNext()
                resultado *= int(Parser.factor(tokenizador))

        return int(resultado)

    @staticmethod
    def parseExpression2(tokenizador):
        # tokenizador.selectNext() 
        resultado = Parser.parseTerm(tokenizador)
        while(tokenizador.actual.value == "+" or tokenizador.actual.value == "-"):
            if(tokenizador.actual.value == "+"):
                tokenizador.selectNext()
                resultado += int(Parser.parseTerm(tokenizador))
            if(tokenizador.actual.value == "-"):
                tokenizador.selectNext()
                resultado -= int(Parser.parseTerm(tokenizador))
            # resultado = Parser.parseTerm(tokenizador)

        return resultado
   

    @staticmethod
    def run(code):
        tokenizador = Tokenizer("", 0, 0)
        tokenizador.origin = Preprocess.remove_comments(code)
        tokenizador.selectNext()
        resultado = Parser.parseExpression2(tokenizador)
        if(tokenizador.actual.type_ != "EOF"):
            raise TypeError("EOF not found")
        return resultado


def main():
    import sys
    parser = Parser()
    resultado = parser.run(sys.argv[1])
    print(resultado)


if __name__ == "__main__":
    main()
