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