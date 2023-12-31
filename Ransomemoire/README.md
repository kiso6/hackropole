## WUP : Ransomémoire

### Partie 0 : Pour commencer  

On commence par extraire l'archive avec `7za e fcsc.7z`. On se retrouve avec un fichier **.dmp** dont on commence par déterminer le type :
```bash
$ file fcsc.dmp
fcsc.dmp: ELF 64-bit LSB core file, x86-64, version 1 (SYSV)
```

On peut donc éliminer les options de montage du disque et d'utilisation de SleuthKit. On commence donc par utiliser strings pour lister le contenu du dump.

```bash
strings -el fcsc.dmp | grep user 
# Il y a beaucoup de résultats ...
c:\users\admin\desktop
c:\users\admin\appdata
c:\users\admin\desktop
c:\users\admin\appdata
c:\users\admin\appdata
# ...
```
On obtient quelques infos intéréssantes sur la cible :  
* C'est du windows (au vu de l'arborescence de fichiers)
* Le user semble être __admin__.

En ce qui concerne le navigateur, j'utilise la même commande qu'avant en changeant le grep user par un grep Browser :

```bash
\Device\HarddiskVolume2\Users\Admin\AppData\Local\BraveSoftware\Brave-Browser\User Data\afalakplffnnnlkncjhbmahjfjhmlkal\1.0.295\1\scripts\brave_rewards\publisher\twitter\_locales\ro\messages.json
```
On trouve alors que le navigateur utilisé est **Brave**.

En ce qui concerne le nom de la machine, je sais que sur Linux, il y a la variable d'environnement HOST qui répertorie le nom de la machine. 

Je suis complètement débutant en Windows, donc j'ai fait une recherche sur les variables d'environnement qui existent dessus et ... BINGO ! Il existe une variable d'environnement __COMPUTERNAME__ qui correspond, selon [la doc Microsoft](https://learn.microsoft.com/fr-fr/windows-hardware/customize/desktop/unattend/microsoft-windows-shell-setup-computername), au "nom de l’ordinateur utilisé pour accéder à l’ordinateur à partir du réseau".  

Donc j'ai recherché avec strings encore une fois la valeur de cette variable :

```bash
COMPUTERNAME=DESKTOP-PI234GP
```
Et on peut alors récupérer notre premier flag dans cette série !
