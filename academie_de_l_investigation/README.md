## WUP : Académie de l'investigation

### Partie 1 : C'est la rentrée


On récupère le dump mémoire et on le passe (comme souvent) sous forme de strings.

#### Hostname
On récupère d'abord le hostname :

```bash
$ strings dmp.mem | grep hostname 
  # On scrolle pas mal dans le résultat ...
  MESSAGE=<info>  [1585265017.0294] hostname: hostname changed from (none) to "challenge.fcsc"
```
Le hostname est donc **challenge.fcsc**

#### Username
On cherche ensuite à récuperer le username:
```bash
$ strings dmp.mem | grep user | more
users
user_data_indices
/run/user/1001
/home/Lesage/.config/systemd/user.control # Lesage ...
```
Le username semble donc être **Lesage**

#### Version du noyau

D'abord j'ai retenté comme la fois précédente en essayant de voir si la commande "uname -a" n'avait pas été utilisée pour récupérer le résultat. Mais cela ne donne rien de concluant.  

Le challenge donne l'architecture amd. Cela ne peut-être que du 32 ou 64 bits (mais je penche quand même plus pour 64...) donc on va tester de chercher cela dans l'image:

```bash
$ strings dmp.mem | grep amd64 | more

BOOT_IMAGE=/boot/vmlinuz-5.4.0-4-amd64 root=UUID=536c82dd-f1c5-43ce-b65d-c94e5c4a5031 ro quiet
5.4.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 9.2.1 20200203 (Debian 9.2.1-28)) #1 SMP Debian 5.4.19-1 (2020-02-13)
Linux 5.4.0-4-amd64 Debian GNU/Linux bullseye/sid
```
Et ça fonctionne ! On récupère la version du noyau (et même la distro) qui est : **Linux 5.4.0-4-amd64**

On peut donc récupérer notre premier flag.

### Partie 2 : Administration

### Partie 3 : Premiers Artéfacts

Dans cette partie, je décide d'utiliser volatility pour pouvoir analyser le dump mémoire. La config de volatility m'a pris un sacré paquet de temps, c'est assez galère de trouver ce qui marche bien.  

Pour utiliser volatility, il faut construire un profil adapté au kernel sur lequel la machine tournait. **Ici on est sur du Linux 5.4.0.4-amd64**.  

J'ai donc cherché comment le faire moi même, avant de vite voir que ça allait me prendre un temps fou. Donc j'ai cherché sur Google "volatility profile for debian 5.4.0-4-amd64" et je suis tombé sur ce repo [Github (auth: thibthib)](https://github.com/thithib/volatility-profiles/blob/master/Linux/DebianSid_Linux-5.4.0-4-amd64.zip) sur lequel un profil était dispo pour ma version du kernel pour un Debian ! Je l'ai donc téléchargé et ensuite utilisé dans mes commandes.  

J'ai déja utilisé une fois volatility, mais pour me rappeller des plugins, j'ai d'abord fait un :

```bash
$ python2 vol.py --plugins=../../hackropole/ --info | grep ps #liste les plugins dispos et cherche ps
#...
linux_psscan               - Scan physical memory for processes #semble pas trop mal ça !
```
On recherche alors le nom du processus associé au PID 1254:

```bash
# Ici j'ai utilisé la vieille version de volatility que j'avais déjà eu l'occasion d'utiliser
$ python2 vol.py --plugins=../../hackropole/ --profile=Linuxprofile_challx64 -f ../../hackropole/dmp.mem linux_psscan | grep 1254

Volatility Foundation Volatility Framework 2.6.1
0x000000003fdccd80 pool-xfconfd         1254            -               -1              -1     ------------------ -
```
Et voila ! Le processus semble donc être le **pool-xconfd** !  

On continue avec volatility désormais. On cherche à connaître l'historique des commandes qui à été utilisé, donc l'historique du bash. En cherchant sur internet "bash history with volatility" on tombe sur **linux_bash** qui semble être plutôt intéréssant car: 
>linux_bash - Recover bash history from bash process memory
>
On lance donc :

```bash
python2 vol.py --plugins=../../hackropole/ --profile=Linuxprofile_challx64 -f ../../hackropole/dmp.mem linux_bash
# On descends un peu et...
1523 bash                 2020-03-26 23:26:06 UTC+0000   rkhunter -c
1523 bash                 2020-03-26 23:29:19 UTC+0000   nmap -sS -sV 10.42.42.0/24
1523 bash                 2020-03-26 23:31:31 UTC+0000   ?+??U
1523 bash                 2020-03-26 23:31:31 UTC+0000   ip -c addr
```
A 23:31:31, la commande exécutée est **ip -c addr**.  

Enfin, on veut le nombre de connexions TCP et UDP ouvertes avec une Peer Adress unique. On utilise encore volatility et un pipe qui va bien :

```bash
python2 vol.py --plugins=../../hackropole/ --profile=Linuxprofile_challx64 -f ../../hackropole/dmp.mem linux_netstat | grep 'ESTABLISHED' | awk '{print $4}' | sort -u |wc -l
Volatility Foundation Volatility Framework 2.6.1
13
```

Petite explication du pipe :  
* **linux_netstat** on lance le plugin d'analyse des connections réseau de volatility
* **grep 'ESTABLISHED'** on ne garde que les connections établies
* **awk '{print $4}'** on ne garde que la 4ème colonne (IP dest)
* **sort -u** on trie le résultat de awk par unicité
* **wc -l** on compte le nombre de lignes restantes
