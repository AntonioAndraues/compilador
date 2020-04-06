import re
class Variaveis:
    def __init__(self):
        self.dict = {}

    def getter(self,value):
        return self.dict[value]

    def setter(self,name,value):
        self.dict[name] = value
class Node:
        def __init__(self):
            self.value = None
            self.children = []
        def evaluate(self,simbol_table):
            raise NotImplementedError    
class BinOP(Node):
    def evaluate(self,simbol_table):
        if (self.value=="+"):
            return int(self.children[0].evaluate(simbol_table)) + int(self.children[1].evaluate(simbol_table))
        if (self.value=="-"):
            return int(self.children[0].evaluate(simbol_table)) - int(self.children[1].evaluate(simbol_table))
        if (self.value=="*"):
            return int(self.children[0].evaluate(simbol_table)) * int(self.children[1].evaluate(simbol_table))
        if (self.value=="/"):
            return int(self.children[0].evaluate(simbol_table)) // int(self.children[1].evaluate(simbol_table))
class UnOP(Node):
    def evaluate(self,simbol_table):
        if (self.value=="+"):
            return self.children[0].evaluate(simbol_table)
        if (self.value=="-"):
            return -int(self.children[0].evaluate(simbol_table))
class IntVAL(Node):
    def evaluate(self,simbol_table):
        return self.value
class NoOP(Node):
    def evaluate(self,simbol_table):
        return super().evaluate(simbol_table)
class Identifier(Node):
    def evaluate(self,simbol_table):
        return simbol_table.getter(self.value)
class Assign(Node):
    def evaluate(self,simbol_table):
        simbol_table.setter(name=self.children[0].value,value=self.children[1].evaluate(simbol_table))
class Echo(Node):
    def evaluate(self,simbol_table):
        print(self.children[0].evaluate(simbol_table))
class Commands(Node):
    def evaluate(self, simbol_table):
        for i in self.children:
            i.evaluate(simbol_table)


class Token(object):
    def __init__(self, type_="", value=""):
        self.type_ = type_
        self.value = value


def get_type(str):
    if(str == "+"):
        return "soma"
    elif(str == "-"):
        return "sub"
    elif(str == " " or str == '\n'):
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
    elif(str == "{"):
        return "Abre_bloco"
    elif(str == "}"):
        return "Fecha_bloco" 
    elif(str == "="):
        return "assign"   
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
        while(self.origin[self.position] == " " or ord(self.origin[self.position]) == 10):
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
        if(self.origin[self.position].isalpha()):
            palavras_reservadas = ["echo"]
            palavra=self.origin[self.position]
            while(self.origin[self.position+1].isalpha()):
                self.position+=1
                palavra+=self.origin[self.position].lower()
            if(palavra in palavras_reservadas):
                self.actual.value=palavra
                self.type_=palavra
                self.position+=1
                return
            else:
                raise ValueError("ERRO: palavra reservada")

        if(self.origin[self.position] == "$"):
            nome_var = ""
            self.position += 1
            if(self.origin[self.position].isalpha()):
                nome_var += self.origin[self.position]
                self.position += 1
                while(self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position] == "-"):
                    nome_var += self.origin[self.position]
                    self.position += 1
                self.actual.value=nome_var
                self.actual.type_="identifier"
                return
            else:
                raise TypeError("ERRO : VARIAVEL COMECA ERRADA")
        

            # if(self.origin[self.position] == "="):
            #    valor_variavel=""
            #    self.position+=1
            #    while(self.origin[self.position] != ";"):
            #        valor_variavel+=self.origin[self.position]
            #        self.position+=1
       
        if(get_type(self.origin[self.position]) != 'int'):
            self.actual.type_ = get_type(self.origin[self.position])
            self.actual.value = self.origin[self.position]
            self.position += 1
            return
        return


class Parser(object):
    @staticmethod
    def block(tokenizador):
        if(tokenizador.actual.value == "{"):
            tokenizador.selectNext()
            node = Commands()
            node.children.append(Parser.command(tokenizador))
            while(tokenizador.actual.value != "}"):
                node.children.append(Parser.command(tokenizador))
                
            tokenizador.selectNext()
            return node

    @staticmethod
    def command(tokenizador):
        if(tokenizador.actual.type_ == "identifier"):
            filho_esquerda = Identifier()
            filho_esquerda.value = tokenizador.actual.value
            tokenizador.selectNext()
            if(tokenizador.actual.value == "="):
                node = Assign()
                node.children.append(filho_esquerda)
                node.value=tokenizador.actual.value
                tokenizador.selectNext()
                node.children.append(Parser.parseExpression2(tokenizador))
                if(tokenizador.actual.value == ";"):
                    tokenizador.selectNext()
                    return node
        elif(tokenizador.actual.value == "echo"):
            node = Echo()
            tokenizador.selectNext()
            node.children.append(Parser.parseExpression2(tokenizador))
            if(tokenizador.actual.value == ";"):
                tokenizador.selectNext()
                return node
        elif(tokenizador.actual.value == "{"):
            Parser.block(tokenizador)
        elif(tokenizador.actual.value == ";"):
            return
        else:
            raise TypeError("ERRO: COMMAND NOT FOUND")
        
            
    @staticmethod
    def factor(tokenizador):
        resultado = 0
        if(tokenizador.actual.value.isdigit()):
            node = IntVAL()
            node.value=tokenizador.actual.value
            tokenizador.selectNext()
            return node
        if(tokenizador.actual.type_ == "identifier"):
            node = Identifier()
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
        # elif(tokenizador.actual.value == "$"):
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
        tokenizador.origin = tokenizador.origin.replace('\\n','\n')
        tokenizador.selectNext()
        resultado = Parser.block(tokenizador)
        if(tokenizador.actual.type_ != "EOF"):
            raise TypeError("EOF not found")
        simpletable = Variaveis()
        return resultado.evaluate(simbol_table=simpletable)

def main():
    import sys
    parser = Parser()
    f = open("teste.php", "r")
    entrada=f.read()
    print(entrada)
    resultado = parser.run(entrada)
    # print(resultado)
    f.close() 


if __name__ == "__main__":
    main()
