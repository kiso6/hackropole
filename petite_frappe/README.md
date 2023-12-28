### WUP : Petite frappe

#### Partie 1 

On télécharge le fichier qui contient les résultats du keylogger et on l'ouvre.
![part1](part1.png "part1")
Les entrées clavier sont répertoriées dans la section SYN REPORT, entre les parenthèses KEY_U,KEY_N,KEY_E,...  
En lisant l'intégralité des KEY et en enlevant les redondances, on voit que le flag est **XXXXXXXX**. Ce qui est effectivement le cas ...

#### Partie 2

Voici un extrait du fichier mis à disposition par le challenge :
```txt
key press   46 
key release 46 
key press   24 
key press   65 
key release 24 
key release 65 
key press   39 
key release 39 
key press   32 
key release 32 
key press   46 
key release 46 
...
```

Pour analyser ça, il va falloir qu'on connaisse le mapping des touches d'un clavier (qu'on va supposer français et azerty).

#### Mauvaise idée 

La première idée est de récupérer la valeur des touches et de les passer dans [Dcode](https://www.dcode.fr/code-touches-javascript). Pour cela j'ai réalisé un [petit script python](parse.py) qui parse le fichier texte pour ressortir les codes des touches. En le passant dans dcode on obtient:
```
[DELETE][?24?]A[?24?]A[RIGHT ARROW →][RIGHT ARROW →] [DELETE][DELETE][?30?][?30?][?28?][?28?][?31?][?31?] 99AA[?24?][?24?]77[?26?][?26?]6A6A55[?31?][?31?]99[PAGE UP ⇞][PAGE UP ⇞][?30?][?30?][?28?][?28?]AA99[?26?]A[?26?]A[RIGHT ARROW →][RIGHT ARROW →][?26?][?26?][?47?][?47?]88[DELETE][DELETE][?26?]A[?26?]A[PAGE UP ⇞][PAGE UP ⇞][?24?][?24?][RIGHT ARROW →]A[RIGHT ARROW →]A[RIGHT ARROW →][RIGHT ARROW →][?30?][?30?][PAGE UP ⇞][PAGE UP ⇞][?26?][?26?][ESCAPE][ESCAPE]AA[PAGE UP ⇞][PAGE UP ⇞][ESCAPE][ESCAPE][?24?][?24?][?28?][?28?][?31?][?31?][UP ARROW ↑][UP ARROW ↑][?30?][?30?][?26?][?26?]AA[?24?]A[?24?]A[DOWN ARROW ↓][?26?][DOWN ARROW ↓][?26?]66 [DOWN ARROW ↓][DOWN ARROW ↓][?26?][?26?][ESCAPE][ESCAPE][?62?][?59?][?59?][?62?]AA[DELETE][DELETE][?26?]A[?26?]A[?41?][?41?][DELETE][DELETE][?24?][?24?][?42?][?42?]AA[?26?][?26?][RIGHT ARROW →][RIGHT ARROW →][?28?][?28?]AA[?30?][?30?]99[CTRL][CTRL]66[DELETE][DELETE][?24?][?24?]77[?31?][?31?][?26?][?26?][ESCAPE][ESCAPE][CTRL][CTRL][?24?][?24?][?25?][?25?][?26?][?26?][ESCAPE][ESCAPE][?28?][?28?][?29?][?29?][CTRL][CTRL][?26?][?26?]99[CTRL][CTRL]77[?24?][?24?][?30?][?30?][?28?][?28?][CTRL][CTRL][DOWN ARROW ↓][DOWN ARROW ↓][?26?][?26?][?30?][?30?]55
```
Ce qui ne me semble pas être la solution ...

#### La solution qui marche

Après ce cuisant échec, j'ai changé de technique d'approche. Comme ce fichier texte est le fruit d'un **keylogger**, j'ai cherché _"decode keylogger inputs"_ sur Google.  

La premier lien qui apparaît est celui d'un repo. Github qui s'appelle [xinput-keylog-decoder](https://github.com/Wh1t3Rh1n0/xinput-keylog-decoder) (_auteur: [Wh1t3Rh1n0](https://github.com/Wh1t3Rh1n0)_ ) qui semble faire ce que je recherche à première vue.  

Après quelques galères pour adapter le script, j'ai réussi à le lancer et voila le résultat : 

```bash
$ ./xinput-keylog-decoder.py ../hackropole/petite_frappe/petite_frappe_2.txt

lq<SPACE>solution<SPACE>qvec<SPACE>xinput<SPACE>ne<SPACE>se;ble<SPACE>pqs<SPACE>super<SPACE>prqtiaue<SPACE>q<SPACE>decoder<RSHIFT>+,<SPACE>le<SPACE>flqg<SPACE>est<SPACE>XXXXXXXXXXXXXXXX
```
En simplifiant :
>lq solution qvec xinput ne se;ble pqs super prqtique q decoder< le flqg est XXXXXXXXXXXXXXXX
>

Ce que l'on peut traduire par :
>"la solution avec xinput ne semble pas super pratique a decoder< le flag est XXXXXXXXXX"
>
