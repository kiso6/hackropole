## WUP : StegCryptoDIY - PNG

Ici, on doit retrouver le flag contenu dans un échange de pramètres cryptographiques caché dans cette image : 

![target](leHACK19_chall.png "pic")  

On commence par un exiftool, pour voir si ce n'est pas caché dans les métadonnées :
```bash
$ exiftool leHACK19_chall.png

ExifTool Version Number         : 12.57
File Name                       : leHACK19_chall.png
Directory                       : .
File Size                       : 146 kB
File Modification Date/Time     : 2023:12:29 14:41:51+01:00
File Access Date/Time           : 2023:12:29 14:43:58+01:00
File Inode Change Date/Time     : 2023:12:29 14:43:09+01:00
File Permissions                : -rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 1150
Image Height                    : 599
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Image Size                      : 1150x599
Megapixels                      : 0.689
```
Il s'avère que ce n'est pas dedans. Donc l'idée d'après est de transformer l'image en chaînes de caractères pour voir si quelque chose semble bizarre :

```bash
$ strings leHACK19_chall.png | more
$ IHDR
IDATx
H4PB=
0C<@
EQ<$?
wQ(k
K^[^\u}o
,wZa
t`|,
_Svo
# ... De longues lignes incompréhensibles de caractères plus tard ...
h0za@
-*36,
gKyv
@duMBTiA9IDExNzU1MDY4OTQ0MTQyOTY5NDk4NzQzMjQ1OTg0NzYxMTgxMzI1NjA1MzA0NjI1Mjg2OTU4NzIxMzkxNzY2MDkxMjgzMTMyMzk4NDM3NjQ1MDM4MzQ5Nzc1ODk4OTIzNDY1MzMxMjYwMzA4MDY0NjExMTY3OTI2MTg3Mzk5Mzg0NzIzMzYwOTQxODgzNzMyMTc0OTAxNjY2ODAzICxnMSA9IDM4MDg4MTk1MDU1NjQ5OTk1NDUyNTI2MjM2MzExOTI1MDMyMTIxODY1OTgwODg1NTUzNDM3MzgxMTExNjUzODI2MjM0MjE3MjAxMTk4Mzc1NDQ2NTgxNzM4MjI0NjE4MzQwNzYzNDc3OTUxNTkzNjY1OTMxNzc2NjkwNTg3MDUwODcyNjY4OTg0NDQ4MTg5MjY2Njg1ODQ1MTksIGcyID0gODcyMTc4NzQwMDMyNzc4Mzc0ODAxNDg0OTAzNzYyNjAzOTM5NzgwNzYxMjM3MjgwNDAxNjY0MzY1MzA0NzU3NTk3NjAwOTgyNzAwMzQ0Nzc3ODg2MTI2MjAzNjc1MjMyNjgyNzYxMzA3ODM0NjIyNTE5MjU4MTcwODI0MDgyMDMyNTg2NzY1ODc0MjA3ODY5NDQ0NTY3Nzg3NyBJIHVzZSB0aGlzIGZ1bmN0b25zIGZvciBlbmNpcGhlcmluZyBvdXIgc2tleSA6IGVuY2lwaGVyKGludC5mcm9tX2J5dGVzKHNrZXksJ2JpZycpLGcxLGcyLE4pIHdpdGggZGVmIGVuY2lwaGVyKG0sZzEsZzIsTik6IHMxPXJhbmRvbS5yYW5kcmFuZ2UoMioqMTI3LDIqKjEyOCkgczI9cmFuZG9tLnJhbmRyYW5nZSgyKioxMjcsMioqMTI4KSByZXR1cm4gKG0qcG93KGcxLHMxLE4pKSVOLCAobSpwb3coZzIsczIsTikpJU4gYW5kIGhlcmUgaXMgYSBmbGFnOiBsZWhhY2syMDE5e2FlZjk1NTZhNTc1Y2M5ZGU4ZmM5NjA5YmQwMzRkNjNmZTBhMDE0NzBlYjQwMTM3ODI1M2Y3MjNiYmM1Y2MxNmN9
IEND
```
En scrollant dans le résultat de la commande more, on ne voit rien d'intéréssant jusqu'à la fin, ou quelque chose dénote du reste.  

J'ai donc copié-collé cette chaîne dans Dcode pour identifier le type, et il s'avère que c'est de la base64. On passe alors tout cela dans un base64 decoder et on obtient :

>vN = 11755068944142969498743245984761181325605304625286958721391766091283132398437645038349775898923465331260308064611167926187399384723360941883732174901666803 ,g1 = 3808819505564999545252623631192503212186598088555343738111165382623421720119837544658173822461834076347795159366593177669058705087266898444818926668584519, g2 = 8721787400327783748014849037626039397807612372804016643653047575976009827003447778861262036752326827613078346225192581708240820325867658742078694445677877 __I use this functons for enciphering our skey : encipher(int.from_bytes(skey,'big'),g1,g2,N) with def encipher(m,g1,g2,N): s1=random.randrange(2\*\*127,2\*\*128) s2=random.randrange(2\*\*127,2*\*128) return (m\*pow(g1,s1,N))%N, (m*pow(g2,s2,N))%N and here is a flag: lehack2019{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}__
>
Bingo, on obtient le bon flag.