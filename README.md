# Compilador - v2.2
Simple Calculator - PHP
---
## Run command example : 

```python
$ python main.py arquivo.php
```
Exemplo de arquivo.php
```python
{
    $interable=0;
    $max=2;
    while($interable<$max){
        $a = readline();
        $b = readline();
        if(($a > 9) and !($b == 5)){
            echo 1;
        }else{
            echo 0;
        }
        if(($a==10) or ($a==11)){
                echo $a;
            }
        $interable = $interable + 1;
    }
    
}
```
---
## Supported ops 
```python
tokens=["+","-","*","/","(",")","Number","if","while","else","==",">","<","!"]
```
---
## Synthetic Diagram  
![diagrama sintatico](https://i.imgur.com/OzUKkOe.png)
