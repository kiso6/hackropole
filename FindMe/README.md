## WUP : Find me  

_C'est parti pour un nouveau chall de forensic, j'adore ça !!!_  

Même histoire que d'habitude, on se retrouve face à un fichier non identifié. On commence par faire connaissance avec lui avec un petit file :

```bash
$ file find_me
find_me: Linux rev 1.0 ext4 filesystem data, UUID=9c0d2dc5-184c-496a-ba8e-477309e521d9, volume name "find_me" (needs journal recovery) (extents) (64bit) (large files) (huge files)
```

On voit alors que c'est :
* une mémoire en ext4 
* `UUID =9c0d2dc5-184c-496a-ba8e-477309e521d9`

On ne peut pas monter le répertoire, on va donc commencer par un `fls` pour voir ce qu'on trouve d'intéréssant là dedans : 

```bash
$ fls find_me
d/d 11:	lost+found
r/r 12:	unlock_me # Tiens...
r/r 13:	pass.b64 # ... Donc 
r/r * 14:	part00
# ....
```

Visiblement ce que l'on cherche à récupérer avec le mot de passe  _(peut être encodé en base64 ?)_ !!! Il est temps d'extraire tout ça du "disque" avec `icat`.  

Par curiosité j'essaye d'afficher unlock me (ça fait relativement n'importe quoi). Mais avec un `file unlock_me` j'obtiens quelques infos : 
 
```bash
 $ file unlock_me
unlock_me: LUKS encrypted file, ver 1 [aes, xts-plain64, sha256] UUID: 220745be-23df-4ef8-bff0-a36ab5cd1eff, at 0x1000 data, 32 key bytes, MK digest 0x75e4b897041923a463d14928c7cff72bc7639058, MK salt 0x0f17e360a9ae44396f85422e8b440644857912a0df3ab0ca9266a4a136ab8b90, 166124 MK iterations; slot #0 active, 0x8 material offset
```

On apprends que :
* On est face à un disque chiffré avec LUKS
* L'algo utilisé est AES-XTS-PLAIN64
* Intégrité sha256 ?

C'est des infos super utiles surtout qu'on à _récupéré la clé_... On peut afficher la clé et ... 
```bash
$ cat pass.b64
nothing here. password splited!
```
... On va donc devoir récupérer toutes les parties et recomposer la clé.

La clé en base 64 est : `TWYtOVkyb01OWm5IWEtzak04cThuUlRUOHgzVWRZ` et donc elle vaut`Mf-9Y2oMNZnHXKsjM8q8nRTT8x3UdY` une fois décodée !

Ensuite, on déchiffre le disque avec cryptsetup, puis on le monte dans un répertoire. Dans les fichiers cachés, on trouve le flag !!

```bash
$ sudo cryptsetup open --type luks unlock_me flag
$ sudo mount /dev/mapper/flag ./mnt
$ cd mnt
$ ls -la 
$ .you_found_me
```
  