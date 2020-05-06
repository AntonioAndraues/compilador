# Compilador - v2.3.1
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
    $a = "";
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
        $i = 0;
        while (3 > $i) {
            $a = $a."a";
            $i = $i + 1;
        }
        echo $a;
    }
}
```
---
## Supported ops 
```python
tokens=["+","-","*","/","(",")","Number","if","while","else","==",">","<","!","true","false","string"]
```
---
## Synthetic Diagram  
![diagrama sintatico](https://i.imgur.com/OXmMz4I.jpg)
