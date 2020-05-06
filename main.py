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
        value1=self.children[0].evaluate(simbol_table)
        value2=self.children[1].evaluate(simbol_table)
        if(value1[1]=="string" or value2[1]=="string"):
            raise TypeError("ERRO: Tentativa de operação com str")
        if (self.value=="+"):
            return (int(value1[0]) + int(value2[0]),"int")
        if (self.value=="-"):
            return (int(value1[0]) - int(value2[0]),"int")
        if (self.value=="*"):
            return (int(value1[0]) * int(value2[0]),"int")
        if (self.value=="/"):
            return (int(value1[0]) // int(value2[0]),"int")
        if (self.value=="and"):
            return ((bool(value1[0]) and bool(value2[0])),"bool")
        if (self.value=="or"):
            return ((bool(value1[0]) or bool(value2[0])),"bool")
            
class RelacionalOP(Node):
    def evaluate(self,simbol_table):
        value1=self.children[0].evaluate(simbol_table)
        value2=self.children[1].evaluate(simbol_table)
        if (self.value=="=="):
            # check types
            if((value1[1]==value2[1]) or ((value1[1] =="bool" and value2[1] =="int") or value2[1] == "bool" and value1 == "int")):
                return ((value1[0] == value2[0]),"bool")
            else:
                raise TypeError("ERRO: tentativa de == com tipos não permitidos")
        if (self.value==">"):
            return ((value1[0] > value2[0]),"bool")
        if (self.value=="<"):
            return ((value1[0] < value2[0]),"bool")
        if (self.value=="."):
            if(value1[1] == "bool"):
                value1=(int(value1[0]),"int")
            if(value2[1] == "bool"):
                 value2=(int(value2[0]),"int")
            return (str(value1[0])+str(value2[0]),"str")
class UnOP(Node):
    def evaluate(self,simbol_table):
        value=self.children[0].evaluate(simbol_table)
        if (self.value=="+"):
            return (int(value[0]),"int")
        if (self.value=="-"):
            return (-int(value[0]),"int")
        if (self.value=="!" and value[1]!="string"):    
            return (not(value[0]),'bool')
        else:
            raise TypeError("ERRO: Trying to not a string")
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
        var=self.children[1].evaluate(simbol_table)
        simbol_table.setter(name=self.children[0].value,value=var)
class Echo(Node):
    def evaluate(self,simbol_table):
        print(self.children[0].evaluate(simbol_table)[0])
class While(Node):
    def evaluate(self,simbol_table):
        while (self.children[0].evaluate(simbol_table)[0]):
            self.children[1].evaluate(simbol_table)
class If(Node):
    def evaluate(self,simbol_table):
        if(self.children[0].evaluate(simbol_table)[0]):
            return self.children[1].evaluate(simbol_table)
        if(len(self.children)==3):  
            return self.children[2].evaluate(simbol_table)
        return

class ReadLine(Node):
    def evaluate(self,simbol_table):
       return (int(input()),"int")
class Commands(Node):
    def evaluate(self, simbol_table):
        for i in self.children:
            i.evaluate(simbol_table)
class BoolVal(Node):
    def evaluate(self, simbol_table):
        return self.value
class StringVal(Node):
    def evaluate(self, simbol_table):
        return (self.value)

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
    elif(str == "."):
        return "concatenação"  
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
                self.actual.value = int(self.actual.value)
                return
        if(self.origin[self.position] == "<" and \
           self.origin[self.position+1] == "?" and \
           self.origin[self.position+2] == "p" and \
           self.origin[self.position+3] == "h" and \
           self.origin[self.position+4] == "p"):
           self.actual.value = "<?php"
           self.position+=5
           return
        if(self.origin[self.position] == "?" and \
           self.origin[self.position+1] == ">"):
           self.actual.value = "?>"
           self.position+=2
           return    
        if(self.origin[self.position] == "!" or self.origin[self.position] == "<" or self.origin[self.position] == ">" ):
            self.actual.value = self.origin[self.position]
            self.type_= self.origin[self.position]
            self.position+=1
            return
        if(self.origin[self.position] == "="):
            if(self.origin[self.position+1] == "="):
                self.actual.value = "=="
                self.type_= "Relational =="
                self.position+=2
                return
        if(self.origin[self.position].isalpha()):
            bools=["true","false"]
            position=self.position
            palavra=self.origin[self.position].lower()
            while(self.origin[self.position+1].isalpha()):
                self.position+=1
                palavra+=self.origin[self.position].lower()
            if(palavra in bools):
                if(palavra == "true"):
                    self.actual.value=True
                else:
                    self.actual.value=False
                self.actual.type_="bool"
                self.position+=1
                return
            else:
                self.position=position
        if(self.origin[self.position].isalpha()):
            palavras_reservadas = ["echo","if","else","while","readline","or","and"]
            palavra=self.origin[self.position].lower()
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
                while(self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position] == "_"):
                    nome_var += self.origin[self.position]
                    self.position += 1
                self.actual.value=nome_var
                self.actual.type_="identifier"
                return
            else:
                raise TypeError("ERRO : VARIAVEL COMECA ERRADA")
        if(self.origin[self.position] == '"'):
            string=""
            self.position+=1
            while(self.origin[self.position]!= '"'):
                string+=self.origin[self.position]
                self.position+=1
            self.actual.value=string
            self.actual.type_="string"
            self.position+=1
            return        
        if(get_type(self.origin[self.position]) != 'int'):
            self.actual.type_ = get_type(self.origin[self.position])
            self.actual.value = self.origin[self.position]
            self.position += 1
            return
        return


class Parser(object):
    @staticmethod
    def program(tokenizador):
        if(tokenizador.actual.value == "<?php"):
            tokenizador.selectNext()
            node = Commands()
            node.children.append(Parser.command(tokenizador))
            if(tokenizador.actual.value == "?>"):
                tokenizador.selectNext()
                return node
            else:
                raise TypeError("ERRO: Não foi possivel encontrar a chave de fechamento '?>' ")
    @staticmethod
    def block(tokenizador):
        if(tokenizador.actual.value == "{"):
            tokenizador.selectNext()
            node = Commands()
            node.children.append(Parser.command(tokenizador))
            while (tokenizador.actual.value != "}"):
                node.children.append(Parser.command(tokenizador))
            tokenizador.selectNext()
            return node
        else:
            raise TypeError("ERRO : CODIGO INVALIDO")

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
                node.children.append(Parser.relexpr(tokenizador))
                if(tokenizador.actual.value == ";"):
                    tokenizador.selectNext()
                    return node
        elif(tokenizador.actual.value == "echo"):
            node = Echo()
            tokenizador.selectNext()
            node.children.append(Parser.relexpr(tokenizador))
            if(tokenizador.actual.value == ";"):
                tokenizador.selectNext()
                return node
        elif(tokenizador.actual.value == "while"):
            node = While()
            node.value=tokenizador.actual.value
            tokenizador.selectNext()
            if(tokenizador.actual.value == "("):
                node.children.append(Parser.relexpr(tokenizador))
                node.children.append(Parser.command(tokenizador))
                return node
            return TypeError("ERRO: NA formatação do While")
        elif(tokenizador.actual.value == "if"):
            node = If()
            node.value=tokenizador.actual.value
            tokenizador.selectNext()
            if(tokenizador.actual.value == "("):
                node.children.append(Parser.relexpr(tokenizador))
                node.children.append(Parser.command(tokenizador))
                # tokenizador.selectNext()
                if(tokenizador.actual.value == "else"):
                    tokenizador.selectNext()
                    node.children.append(Parser.command(tokenizador))
                    return node
                else:
                    return node
            return TypeError("ERRO: NA formatação do If")
            
            
        elif(tokenizador.actual.value == "{"):
            commands = Parser.block(tokenizador)
            return commands
        elif(tokenizador.actual.value == ";"):
            return
        else:
            raise TypeError(f"ERRO: COMMAND NOT FOUND {tokenizador.actual.value} ")
        
    @staticmethod
    def relexpr(tokenizador):
        node2 = Parser.parseExpression2(tokenizador)
        while(tokenizador.actual.value == "==" or tokenizador.actual.value == ">"\
             or tokenizador.actual.value == "<" or tokenizador.actual.value == "."):
            node = RelacionalOP()
            node.value=tokenizador.actual.value
            node.children.append(node2)
            node2=node
            tokenizador.selectNext()
            node.children.append(Parser.parseExpression2(tokenizador))
        return node2
    @staticmethod
    def factor(tokenizador):
        resultado = 0
        if(tokenizador.actual.type_ == "int"):
            node = IntVAL()
            node.value=(tokenizador.actual.value,'int')
            tokenizador.selectNext()
            return node
        if(tokenizador.actual.type_=="bool"):
            node = BoolVal()
            node.value=(tokenizador.actual.value,'bool')
            tokenizador.selectNext()
            return node
        if(tokenizador.actual.type_=="string"):
            node = StringVal()
            node.value=(tokenizador.actual.value,'string')
            tokenizador.selectNext()
            return node
        if(tokenizador.actual.type_ == "identifier"):
            node = Identifier()
            node.value=tokenizador.actual.value
            tokenizador.selectNext()
            return node
        if(tokenizador.actual.value == "+" or tokenizador.actual.value == "-" or tokenizador.actual.value == "!" ):
            node = UnOP()
            node.value = tokenizador.actual.value
            tokenizador.selectNext()
            node.children.append(Parser.factor(tokenizador))
            return node
        if(tokenizador.actual.value == "readline"):
            node = ReadLine()
            node.value = tokenizador.actual.value
            tokenizador.selectNext()
            if(tokenizador.actual.value == "("):
                tokenizador.selectNext()
                if(tokenizador.actual.value == ")"):
                    tokenizador.selectNext()
                    return node
            return TypeError("ERRO: Formatação do readline")
        elif(tokenizador.actual.value == "("):
            tokenizador.selectNext()
            resultado = Parser.relexpr(tokenizador)
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
        while(tokenizador.actual.value == "*" or tokenizador.actual.value == "/" or tokenizador.actual.value == "and"):
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
        while(tokenizador.actual.value == "+" or tokenizador.actual.value == "-" or tokenizador.actual.value == "or"):
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
        resultado = Parser.program(tokenizador)
        if(tokenizador.actual.type_ != "EOF"):
            raise TypeError("EOF not found")
        return resultado

def main():
    import sys
    parser = Parser()
    f = open(sys.argv[1], "r")
    entrada=f.read()
    resultado = parser.run(entrada)
    simpletable = Variaveis()
    f.close() 
    return resultado.evaluate(simbol_table=simpletable)


if __name__ == "__main__":
    main()
