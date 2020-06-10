# Compilador - v2.4.1
Simple Calculator - PHP
---
Falta atualizar o ds e concertar o return
## Run command example : 

```python
$ python main.py arquivo.php
```
Exemplo de arquivo.php
```python
<?php
function soma($x,$y){
    function echoes($b){
        echo $b;
    }
    $a=$x+$y;
    echoes($a);
}
$a=3;
soma($a,4);
?>
```
---
## Supported ops 
```python
tokens=["+","-","*","/","(",")","Number","if","while","else","==",">","<","!","true","false","string","functions"]
```
---
## Synthetic Diagram  
![diagrama sintatico](https://i.imgur.com/OXmMz4I.jpg)
