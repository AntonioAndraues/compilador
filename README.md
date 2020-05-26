# Compilador - v3.0.1
Simple Calculator - PHP
---
## Run command example : 

```python
$ python main.py arquivo.php
```
Exemplo de arquivo.php
```python
<?php
    $i=2;
    $n=5;
    $f=1;
    while($i<$n+1){
        $f=$f*$i;$i=$i+1;
    }
    echo$f;
?>
```
---
## Supported ops 
```python
tokens=["+","-","*","/","(",")","Number","if","while","else","==",">","<","!","true","false","string"]
```
---
## Synthetic Diagram  
![diagrama sintatico](https://i.imgur.com/OXmMz4I.jpg)
