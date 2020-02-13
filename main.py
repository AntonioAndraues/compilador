import sys
ops=["+", "-"]
def recursion(string,soma):
    if ops[0] not in string and ops[1] not in string:
        soma+=int(string)
        return soma
    for i in range(len(string)-1,0,-1):
        if string[i] in ops:
            numero=string[i+1:]
            if string[i] == ops[0]:
                soma+=int(numero)
            else:
                soma+=int(numero)*-1
            string=string[0:i]
            break
    soma=recursion(string,soma)
    return soma

def main():
    
    soma=0
    soma=recursion(sys.argv[1],soma)
    print(f'{soma}')
    return soma
    

if __name__ == "__main__":
    main()