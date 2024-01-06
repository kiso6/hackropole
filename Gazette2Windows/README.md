## WUP : La gazette de windows 

Ici, challenge ou on va aller lire des logs Windows. Pour être tout a fait honnête, c'est la première fois que j'en regarde.  

D'abord, j'ai installé un outil pour parser ces logs pour que ce soit lisible, vu que je travaille sur Linux. Il s'avère que **evtxexport** marche plutôt bien. On l'utilise donc pour aller regarder ce qu'il se passe dans ces logs.  

```bash
$ evtxexport MWPO.evtx > MWPOexp
$ more MWPOexp
```

On se balade un peu, _le fichier est pas trop long c'est bien_, et on tombe sur un premier truc bizarre : 

```ps1
Event number			: 1108 #On note
Creation time			: Mar 16, 2023 17:18:06.001286100 UTC
Written time			: Mar 16, 2023 17:18:06.001286100 UTC
Event level			: Warning (3)
User security identifier	: S-1-5-21-3727796838-1318123174-2233927406-1105
Computer name			: DESKTOP-AL3DV8F.fcsc.fr
Source name			: Microsoft-Windows-PowerShell
Event identifier		: 0x00001008 (4104)
Number of strings		: 5
String: 1			: 1
String: 2			: 1
String: 3			: if((Get-ExecutionPolicy ) -ne 'AllSigned') { Set-ExecutionPolicy -Scope Process Bypass }; & 'C:\Users
\jmichel\Downloads\payload.ps1' # On note aussi
String: 4			: dcb325dd-1c30-46bd-8363-81083ac85323
String: 5			:
```
On voit que l'evenement 1108 à l'air d'exécuter  le script powershell situé en `C:\Users \jmichel\Downloads\payload.ps1`. Intéréssant ! 

Logiquement on s'intéresse à l'evenement suivant et ... Bingo, on trouve l'execution du script payload.ps1 !!! Qui ressemble à ça, pour les parties qui nous intéressent ... 

```ps1
# Avant, grossomodo, il ouvre un socket vers 10.255.255.16:1337

$l = 0x46, 0x42, 0x51, 0x40, 0x7F, 0x3C, 0x3E, 0x64, 0x31, 0x31, 0x6E, 0x32, 0x34, 0x68, 0x3B, 0x6E, 0x25, 0x25,0x24, 0x77, 0x77, 0x73, 0x20, 0x75, 0x29, 0x7C, 0x7B, 0x2D,0x79, 0x29, 0x29, 0x29, 0x10, 0x13, 0x1B, 0x14, 0x16, 0x40,0x47, 0x16, 0x4B, 0x4C, 0x13, 0x4A, 0x48, 0x1A, 0x1C, 0x19, 0x2, 0x5, 0x4, 0x7, 0x2, 0x5, 0x2, 0x0, 0xD, 0xA, 0x59, 0xF,0x5A, 0xA, 0x7, 0x5D, 0x73, 0x20, 0x20, 0x27, 0x77, 0x38, 0x4B, 0x4D
$s = ""
for ($i = 0; $i -lt 72; $i++) {
    $s += [char]([int]$l[$i] -bxor $i)
}

# Il fait d'autres traitements
```
On voit quelque chose qui pourrait être une chaîne ASCII - **$l** - et une chaîne vide **$s**. On remarque aussi une boucle derrière qui viens concatener à $s, le caractère représenté par **le xor de la valeur de $l à l'indice i avec l'indice i**. $s pourrait alors totalement être notre flag ! Pour en être sûr, j'ai recopié cette partie de payload.ps1 dans le fichier lol.ps1 auquel j'ai rajouté un simple `echo $s` en fin de traitement. On l'exécute et ...

```bash
$ pwsh lol.ps1
FCSC{.............................}
```
Et c'est gagné !!! 