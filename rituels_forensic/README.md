## WUP : Rituels de forensic

### Rituel du boutisme
Dans ce challenge, on dispose d'une image disque au format .img dans laquelle on doit retrouver un flag.

#### Montage du disque

Ma première idée a été de monter l'image disque dans un fichier local en utilisant la commande mount. J'ai obtenu les résultats suivants (enchaînement de commandes non contractuel mais c'est dans l'idée):
```bash
$ mount -r rituel-du-boutisme.img ./mnt
$ ls ./mnt
$ lost+found #en root:root
$ su root && ls lost+found 
$ # Rien dans le fichier 
```
#### Utilisation de strings

Première utilisation de strings : 
```bash
$ strings rituel-du-boutisme.img | grep flag
$ flag.txt
  flag.txt
  flag.txt
```
On est sûrs que le flag est dedans, même si on en doutait pas.  

Ensuite j'ai décidé de regarder les ressources fournies par le challenge, et notamment [SANS](https://www.sans.org/blog/strings-strings-are-wonderful-things/), qui donne des options sympatiques. J'ai trouvé le resultat en faisant la commande suivante :
```bash
$ strings -el rituel-du-boutisme.img| grep FCSC
FCSC{XXXXXXXXXXXXXXXXXXXXXXXXXXXXX}
```
L'option -e permet de spécifier un encodage pour les chaînes trouvées dans le fichier qui est passé en argument. Le **-el** permet de spécifier un encodage **Unicode UTF-16**.

### Rituel en chaîne

Pour cette deuxième partie, on va jouer sur les valeurs possibles de la commande strings avec l'option -e. Dans un premier temps j'ai testé la même que la partie précédente (on sait jamais) mais cela n'a pas marché. L'encodage n'est donc **PAS** de l'UTF-16.  

Maintenant il faut trouver le bon ! Strings propose plein d'options :

>_[Extrait du man de strings](https://linux.die.net/man/1/strings)_  
-e encoding  --encoding=encoding  
Select the character encoding of the strings that are to be found. Possible values for encoding are: **s = single-7-bit-byte characters ( ASCII , ISO 8859, etc., default)**,...  
>

Donc j'ai essayé avec cette option là : 
```bash
strings --encoding=s rituel-en-chaine.img| grep FCSC

FCSC{XXXXXX ON VOIT LE FLAG}
VFCSCr$q+
```

Bingo, ça marche ! Morale de l'histoire, Strings c'est super.