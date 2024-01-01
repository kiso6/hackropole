## WUP : Cryptolocker v1

On commence par identifier le fichier avec un `file cryptolocker-v1.dmp` et on obtient le résultat :  

```bash
cryptolocker-v1.dmp: MS Windows 32bit crash dump, PAE, full dump, 262030 pages
```
On voit que c'est un dump windows, ça va être utile pour qu'on puisse utiliser volatility3 avec les bonnes options.  

On recherche d'abord le nom du malware pour pouvoir voir quels sont les processus qu'il à engendré. Pour cela, on va analyser le dump avec volatility en utilisant pstree: 

```bash
./vol.py -f ../CryptoLocker_v1/cryptolocker-v1.dmp windows.pstree
# On se balade dans les résultats du dump et ...... la dernière ligne est super suspecte
PID	PPID	ImageFileName	Offset(V)	Threads	Handles	SessionId	Wow64	CreateTime	ExitTime
* 3388	1432	update_v0.5.ex	0x83de43a8	2	61	1	False	2020-04-13 18:38:00.000000 	N/A
```

On remarque un fichier suspect peut regarder **update_v0.5.ex**. On note que son PID est 3388, parce qu'on va le dump pour l'analyser.

Pour dumper on lance la commande `./vol.py -f ../CryptoLocker_v1/cryptolocker-v1.dmp windows.dumpfile --pid=3388` (**Attention : y'a pas mal de fichiers qui sortent, je crois qu'il y a une option pour spécifier la sortie...**) et on place les fichier dans un dosier `/malware` pour les analyser.  

On remarque quelques fichiers intéréssants telx que `file.0x84f66b60.0x85279860.DataSectionObject.update_v0.5.exe.dat` (le .img aussi) et un `file.0x84f13898.0x854fbc98.DataSectionObject.key.txt.dat` qui peut toujours servir (key c'est un truc sympa en général...)  


```bash
$ strings --byte=16 ./file.0x84f66b60.0x8548c008.ImageSectionObject.update_v0.5.exe.img
!This program cannot be run in DOS mode.
[info] entering the folder : %s
flag.txt
[info] file encryptable found : %s
[error] can't read the key-file :s
****Chiffrement termin
e ! Envoyez l'argent !
_matherr(): %s in %s(%g, %g)  (retval=%g)
Argument domain error (DOMAIN)
Argument singularity (SIGN)
Overflow range error (OVERFLOW)
The result is too small to be represented (UNDERFLOW)
Total loss of significance (TLOSS)
Partial loss of significance (PLOSS)
Mingw-w64 runtime failure:
Address %p has no image-section
  VirtualQuery failed for %d bytes at address %p
  VirtualProtect failed with code 0x%x
  Unknown pseudo relocation protocol version %d.
  Unknown pseudo relocation bit size %d.
```
On voit bien que la clé est utilisée pour chiffrer le fichier flag.txt

On va alors chercher le fichier chiffré `file.txt` dans le dump :

```bash
./vol.py -f ../CryptoLocker_v1/cryptolocker-v1.dmp windows.filescan | grep flag

0x3ed139f0	100.0\Users\IEUser\Desktop\flag.txt.enc	128
```

On l'extrait de la même manière que le malware :

```bash
./vol.py -f ../CryptoLocker_v1/cryptolocker-v1.dmp windows.dumpfile --physaddr 0x3ed139f0
Volatility 3 Framework 2.5.2
Progress:  100.00		PDB scanning finished
Cache	FileObject	FileName	Result

DataSectionObject	0x3ed139f0	flag.txt.enc	file.0x3ed139f0.0x855651e0.DataSectionObject.flag.txt.enc.dat
```
Génial !!!! On a le fichier chiffré, et la clé de chiffrement, on devrait pouvoir récupérer le flag. Reste plus qu'a trouver l'algo utilisé.

On fait un cat du fichier de clé et on obtient `0ba883a22afb84506c8d8fd9e42a5ce4e8eb1cc87c315a28dd`.

Pour le fichier de flag, il est dans un format bien dégueu, donc on le récupère sous forme de chaîne hexa :
```bash
hexdump -C file.0x3ed139f0.0x855651e0.DataSectionObject.flag.txt.enc.dat
00000000  27 7b 6b 70 1a 01 00 55  05 07 5d 0c 53 55 05 55  |'{kp...U..].SU.U|
00000010  09 5d 59 5e 06 5c 04 02  06 54 07 51 00 55 01 5e  |.]Y^.\...T.Q.U.^|
00000020  55 57 52 5b 57 5c 51 54  50 07 51 07 0b 5e 55 51  |UWR[W\QTP.Q..^UQ|
00000030  55 56 02 59 5a 07 05 02  57 51 52 01 0f 03 57 02  |UV.YZ...WQR...W.|
00000040  06 01 5a 50 0f 1b 6e 00  00 00 00 00 00 00 00 00  |..ZP..n.........|
00000050  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001000
```
Le flag chiffré vaut alors : 
277b6b701a01005505075d0c53550555095d595e065c0402065407510055015e5557525b575c5154500751070b5e5551555602595a070502575152010f03570206015a500f1b6e

On utilise ensuite le script python pour xorer les deux 