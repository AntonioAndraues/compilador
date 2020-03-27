import re
class Node:
        def __init__(self):
            self.value = None
            self.children = []
        def evaluate(self):
            raise NotImplementedError    
class BinOP(Node):
    def evaluate(self):
        if (self.value=="+"):
            return int(self.children[0].evaluate()) + int(self.children[1].evaluate())
        if (self.value=="-"):
            return int(self.children[0].evaluate()) - int(self.children[1].evaluate())
        if (self.value=="*"):
            return int(self.children[0].evaluate()) * int(self.children[1].evaluate())
        if (self.value=="/"):
            return int(self.children[0].evaluate()) // int(self.children[1].evaluate())
class UnOP(Node):
    def evaluate(self):
        if (self.value=="+"):
            return self.children[0].evaluate()
        if (self.value=="-"):
            return -int(self.children[0].evaluate())
class IntVAL(Node):
    def evaluate(self):
        return self.value
class NoOP(Node):
    def evaluate(self):
            return super().evaluate()
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
    else:
        return "Não identificado"

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
            node = IntVAL()
            node.value=tokenizador.actual.value
            tokenizador.selectNext()
            return node
        if(tokenizador.actual.value == "+" or tokenizador.actual.value == "-"):
            node = UnOP()
            node.value = tokenizador.actual.value
            tokenizador.selectNext()
            node.children.append(Parser.factor(tokenizador))
            return node
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
        node2 = Parser.factor(tokenizador)
        while(tokenizador.actual.value == "*" or tokenizador.actual.value == "/"):
            node = BinOP()
            node.value=tokenizador.actual.value
            tokenizador.selectNext()
            node.children.append(node2)
            node2=node
            node.children.append((Parser.factor(tokenizador)))
        return node2

    @staticmethod
    def parseExpression2(tokenizador):
        # tokenizador.selectNext() 
        node2 = Parser.parseTerm(tokenizador)
        while(tokenizador.actual.value == "+" or tokenizador.actual.value == "-"):
            node = BinOP()
            node.value=tokenizador.actual.value
            node.children.append(node2)
            node2=node
            tokenizador.selectNext()
            node.children.append(Parser.parseTerm(tokenizador))
            # resultado = Parser.parseTerm(tokenizador)
        return node2
   

    @staticmethod
    def run(code):
        tokenizador = Tokenizer("", 0, 0)
        tokenizador.origin = Preprocess.remove_comments(code)
        tokenizador.selectNext()
        resultado = Parser.parseExpression2(tokenizador)
        if(tokenizador.actual.type_ != "EOF"):
            raise TypeError("EOF not found")
        return resultado.evaluate()

def main():
    import sys
    parser = Parser()
    f = open(sys.argv[1], "r")

    linhas = f.readlines()
    for linha in linhas:
        if("\n" in linha):
            linha=linha[:-1]
        resultado = parser.run(linha)
        print(resultado)

    f.close() 


if __name__ == "__main__":
    main()
