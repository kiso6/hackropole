## WUP : Seven sins

Ici tout réside dans le fait de ne pas se planter en recopiant.

Un input est de la forme : **D/C/B/A/E/F/EN/G/DP** où EN=1 et DP=0.  

Un sept segments se présente sous la forme: 
![img](SEPTSEG.png "replacement")  

Alors :  
* F = AFEG   = 000111110
* C = AFED  =  100111100 
* S = AFGCD =  110101110
* C = AFED  =  100111100 
* 2 = ABGED =  101110110
* 0 = AFEDCB=  111111100
* 2 = ABGED =  101110110
* 2.= ABGED =  101110111

_Attention: subtilité, le dernier 2 est suivi d'un "." donc le bit DP a 1 ... J'ai pas vu ça au début..._

Donc le flag est :
FCSC{**La suite de bits qui va bien**}
