## WUP : 103_spx 

Après avoir extrait l'archive on se retrouve avec le fichier "USB_a_analyser".  

Première idée, on le passe dans string pour voir si y'a des choses intéréssantes :

```bash
$ strings USB_a_anayser | more
NTFS
This is not a bootable disk. Please insert a bootable fl
oppy and
press any key to try again ...
FILE0
FILE0

# On descends un peu ... 

Si un jour je relis ce message, le mot de passe utilis
 pour chiffrer mon plus grand secret
tait "vgrohhfyek0wkfi5fv13anexapy3sso6" et j'av
s utilis
 openssl.
En revanche, j'ai effac
 par erreur le fichier contenant mon plus grand secret (voir s'il existe des techniques de la mort pour le retrouver mon fichier secret
.xz sha256(0fb08681c2f8db4d3c127c4c721018416cc9f9b369d5f5f9cf420b89ee5dfe4e) de 136 octets) et de toute fa
on, impossible de me rappeler de l'algo utilis
 -_- (donc si je le retrouve... il faudra aussi retrouver l''algo pour utiliser ce mot de passe).

# Encore un peu ...

[Trash Info]
Path=secret.xz
DeletionDate=2019-07-06T14:14:16
```

Donc on sait que l'on a :  
* Une archive supprimée dans lequel on a un secret chiffré : **secret.xs**
* Le mot de passe utilisé pour chiffrer tout ça : **vgrohhfyek0wkfi5fv13anexapy3sso6**
* L'algo de chiffrement utilisé est dans OpenSSL (bon ça c'est un indice plutôt large ...)
* On a aussi l'empreinte hash du fichier pour voir si ça colle : **sha256(0fb08681c2f8db4d3c127c4c721018416cc9f9b369d5f5f9cf420b89ee5dfe4e) de 136 octets**

Voila donc une première analyse plutôt fructueuse ! On va maintenant chercher à extraire le fichier supprimé secret.xz.

#### SleutKit run (pas concluant)

On lance d'abord un fls pour voir comment sont organisés les fichiers dans cette clé :
```bash
$ fls USB_a_analyser
r/r 4-128-1:	$AttrDef
r/r 8-128-2:	$BadClus
r/r 8-128-1:	$BadClus:$Bad
r/r 6-128-1:	$Bitmap
r/r 7-128-1:	$Boot
d/d 11-144-2:	$Extend
r/r 2-128-1:	$LogFile
r/r 0-128-1:	$MFT
r/r 1-128-1:	$MFTMirr
r/r 9-128-2:	$Secure:$SDS
r/r 9-144-3:	$Secure:$SDH
r/r 9-144-4:	$Secure:$SII
r/r 10-128-1:	$UpCase
r/r 10-128-2:	$UpCase:$Info
r/r 3-128-3:	$Volume
d/d 132-144-2:	.Trash-1000
r/r 64-128-2:	message.txt
r/r 102-128-2:	Peugeot 103 SPX : tous les modèles de 1987 à 2003 | Actualités de la mobylette par Mobylette Mag.html
d/d 67-144-2:	Peugeot 103 SPX : tous les modèles de 1987 à 2003 | Actualités de la mobylette par Mobylette Mag_files
r/r 65-128-2:	Peugeot103SPXFILI.jpg
r/- * 0:	secret.xz #BINGO !
r/r * 66-128-2(realloc):	secret.xz
V/V 154:	$OrphanFiles
```

On essaye d'extraire le fichier maintenant grâce à la commande icat, et de les visualiser :

```bash
$ icat -i raw USB_a_analyser 66-128-2 > secret.xz
$ unxz secret.xz
$ cat secret | strings 
  Salted__
# Echec cuisant
```
#### Mount run

On met toutes les traces de ma run précédente dans un fichier, et on part sur quelque chose de nouveau.  

J'ai donc monté le répertoire dans un dossier mnt.  

```bash
$ ls
 message.txt            'Peugeot 103 SPX : tous les modèles de 1987 à 2003 | Actualités de la mobylette par Mobylette Mag_files' Peugeot103SPXFILI.jpg  'Peugeot 103 SPX : tous les modèles de 1987 à 2003 | Actualités de la mobylette par Mobylette Mag.html'
# On cherche un dossier caché 
$ la
 message.txt 
 Peugeot103SPXFILI.jpg 
 'Peugeot 103 SPX : tous les modèles de 1987 à 2003 | Actualités de la mobylette par Mobylette Mag_files' 'Peugeot 103 SPX : tous les modèles de 1987 à 2003 | Actualités de la mobylette par Mobylette Mag.html'
 .Trash-1000 #On se rappelle que le fichier était supprimé
$ cd .Trash-1000/files
$ ls
 "CERT-FR – Centre gouvernemental de veille, d'alerte et de réponse aux attaques informatiques_files"  
 'Peugeot 103 — Wikipédia.html'
 "CERT-FR – Centre gouvernemental de veille, d'alerte et de réponse aux attaques informatiques.html"    
 secret.xz # YEEEEEEEEEES !!!!!
 'Peugeot 103 — Wikipédia_files'
```

On extrait l'archive secret dans un dossier à nous et on change les droits dessus. Pour pouvoir le manipuler. A l'extraction on voit bien que c'est un fichier chiffré. Reste maintenant à retrouver l'algorithme utilisé !  

Pour cela on va boucler sur les algos d'open SSL en renseignant le password obtenu au début. On obtient !

```bash
file_aes-192-ecb:flag : lh_XXXXXXXXXXXXXXXXXXXXX
```