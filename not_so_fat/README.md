## WUP : Not so fat !
**Tags:** _SleuthKit / images disque / forensic_

Dans ce challenge, on récupère une image disque au format .dd : **not-so-fat.dd**. On sait qu'elle contient un flag qu'on doit récupérer.

### Tâtonnement initial...
Dans un premier temps, ça pourrait être intéréssant de lister le contenu du disque. Pour cela, ma première idée a été de faire:
```bash
strings not-so-fat.dd
``` 
Qui m'a renvoyé ...
```bash
$ strings not-so-fat.dd
mkfs.fat
;NO NAME    FAT16
This is not a bootable disk.  Please insert a bootable floppy and
press any key to try again ...
IEUYRJW
LAG    ZIP
flag.txtUT	
flag.txtUT
```
C'est sûrement pas l'outil le plus adapté, mais on récupère quand même quelques infos intéréssantes sur l'image disque :
* C'est un format **FAT**, pourquoi pas...
* "LAG    ZIP" pourrait être un "FLAG ZIP"
* "flag.txt" ressemble à quelque chose qu'on veut

Naturellement, j'ai pensé a monter l'image disque dans un répertoire 
```bash
sudo mount -r ../not-so-fat.dd .
ls -la
#retourne rien du tout
```
Bon, il va falloir trouver autre chose qui marche mieux.

### Quelque chose d'un peu plus sérieux 
En cherchant sur internet comment lister les fichiers d'une image de disque, je suis tombé sur la [page Wikipédia du SleuthKit](https://fr.wikipedia.org/wiki/The_Sleuth_Kit) qui mentionne un outil :  
> fls : liste les noms de fichiers alloués et non alloués dans un système de fichiers
>
Qui semble faire vraiment ce que je recherche... On regarde un peu le man de ce binaire pour composer la commande a rentrer
```bash
fls not-so-fat.dd
r/r * 4:	ziEuYrJW
r/r * 6:	flag.zip # mhhh... interessant
v/v 523203:	$MBR
v/v 523204:	$FAT1
v/v 523205:	$FAT2
V/V 523206:	$OrphanFiles
```
On retrouve un "flag.zip" qu'on avait deviné avec strings tout à l'heure.  

### Extraction !

Maintenant, on va essayer d'extraire tout ça du fichier. Toujours dans le SleuthKit, on dispose de l'utilitaire **icat** qui, selon le man, fait :
>icat - Output the contents of a file based on its inode number.
>
En regardant dans le man de fls, on voit que si on ne précise pas de inode, il par du noeud racine. Donc on devine que le inode a utiliser est 6 on obtient

```bash
icat not-so-fat.dd 6 >> flag.zip
```
Et on récupèreune super archive ! On peut alors l'unzip et récupérer le flag ! 
```bash
unzip flag.zip
Archive:  file.zip
[file.zip] flag.txt password:
```
Il faut un mot de passe ... Deux options s'offrent à nous : soit on a de la chance et on tombe sur le mot de passe en devinant, soit on bruteforce. Comme c'est un challenge d'intro j'ai naivement tenté "**motdepasse**"(qui n'a pas fonctionné) et... "**password**" qui a fonctionné !  

On peut alors afficher le flag en faisant un ```cat flatg.txt```
