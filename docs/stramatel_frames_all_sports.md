# STRAMATEL RS-485 frame layouts (all sports)

This file is a **direct, structured transcription** of the "COMPOSITION DES TRAMES" tables from the PDF.

## Frame basics

- Transport: RS-485, **19200 baud, 8N1**.

- Each transmitted frame is **54 bytes** long.

- Byte 0 is always **START = 0xF8**.

- Byte 1 is **CODE SPORT** (varies by frame type / mode).

- Byte 53 is always **END = 0x0D**.

- Table row `01` corresponds to **byte index 0**, row `54` to **byte index 53**.


## Notes / enums referenced by tables

The tables reference the following notes (verbatim meaning preserved, lightly formatted):

```text
Note 1 : "F8" : Format Hexadecimal
Note 2 : L = EQUIPE "LOCAUX" V = EQUIPE "VISITEURS"
Note 3 : Pas de format spécifié --> ASCII
Note 4 : Possession de balle ="31" --> LOCAUX ="32" --> VISITEURS Autre valeur --> éteint
Note 5 : Klaxon ="31" --> allumé Autre valeur --> éteint
Note 6 : start/stop chronomètre ="31" --> allumé Autre valeur --> éteint
Note 7 : Affichage 24" ="31" --> allumé Autre valeur --> éteint
Note 8 : Hand : Pénalités en cours
="31"-->1ère pénalité ="32"-->1ère & 2ème pénalités ="33"-->1ère, 2ème & 3ème pénalités
="34"-->2ème pénalité ="35" -->3rd pénalité ="36" --> 2ème & 3ème pénalités ="37" --> 1ère & 3ème pénalités
Note 9 : Affichage Horloge/Chronomètre ="31" --> Horloge Autre valeur --> Chronomètre
Note 10 : Service ="31"--> LOCAUX – 1er service ="32"--> LOCAUX – 2ème service
="33"--> VISITEURS – 1er service ="34"--> VISITEURS – 2ème service
Note 11 : Gagnant ="31" --> LOCAUX ="32" --> VISITEURS Autre valeur --> PAS DE GAGNANT
Note 12 : Tie-Break ="31" --> En cours Autre valeur --> pas de tie-break
Note 13 : Exercice/Repos ="31" --> Exercice Autre valeur --> Repos
Note 14 : Mode test ="20" --> Test standard "30" à “39” --> Mode test 0 à 9
Note 15 : Joueur : ="30" "31"-->1er joueur ="30" "37"-->7ème joueur
="30" "32"-->2ème joueur ="30" "38"-->8ème joueur
="30" "33"-->3ème joueur ="30" "39"-->9ème joueur
="30" "34"-->4ème joueur ="31" "30"-->10ème joueur
="30" "35"-->5ème joueur ="31" "31"-->11ème joueur
="30" "36"-->6ème joueur ="31" "32"-->12ème joueur
CЄ
UFBE09046_CODES_A Page 2
```

## BASKET-BALL / POINTS INDIVIDUELS (PDF page 3)

Header/context:

```text
COMPOSITION DES TRAMES
BASKET-BALL / POINTS INDIVIDUELS
CODE DANS BASKET avec P oints Individuels LOCAUX Points Individuels VISITEURS
LA TRAME Fautes Individuelles BASKET/HAND/HOCKEY/FOOT BASKET/HAND/HOCKEY/FOOT
```

Frame layout (rows 01..54):

```text
01 CODE START = "F8" CODE START = "F8" CODE START = "F8"
02 CODE SPORT ="33" CODE SPORT ="38" CODE SPORT ="37"
03 "20" "20" "20"
04 Possession balle (note 4) "20" Possession balle (note 4)
05 Chrono. (digit 1) Chrono. (digit 1) Chrono. (digit 1)
06 Chrono. (digit 2) Chrono. (digit 2) Chrono. (digit 2)
07 Chrono. (digit 3) Chrono. (digit 3) Chrono. (digit 3)
08 Chrono. (digit 4) Chrono. (digit 4) Chrono. (digit 4)
09 L : points (digit 1) "20" "20"
10 L : points (digit 2) "20" "20"
11 L : points (digit 3) "20" "20"
12 V : points (digit 1) L : Points indiv. joueur 14 (digit 1) V : Points indiv. joueur 14 (digit 1)
13 V : points (digit 2) L : Points indiv. joueur 14 (digit 2) V : Points indiv. joueur 14 (digit 2)
14 V : points (digit 3) "20" "20"
15 Periode "20" "20"
16 L : fautes d'équipe "20" "20"
17 V : fautes d'équipe "20" "20"
18 L : Nombre de temps-morts "20" "20"
19 V : Nombre de temps-morts "20" "20"
20 Klaxon (note 5) Klaxon (note 5) Klaxon (note 5)
21 Start/Stop Chrono. (note 6) Start/Stop Chrono. (note 6) Start/Stop Chrono. (note 6)
22 Chrono. temps-mort (digit1) "20" "20"
23 L : Fautes individuelles joueur 1 L : Points indiv. joueur 1 (digit 1) V : Points indiv. joueur 1 (digit 1)
24 L : Fautes individuelles joueur 2 L : Points indiv. joueur 1 (digit 2) V : Points indiv. joueur 1 (digit 2)
25 L : Fautes individuelles joueur 3 L : Points indiv. joueur 2 (digit 1) V : Points indiv. joueur 2 (digit 1)
26 L : Fautes individuelles joueur 4 L : Points indiv. joueur 2 (digit 2) V : Points indiv. joueur 2 (digit 2)
27 L : Fautes individuelles joueur 5 L : Points indiv. joueur 3 (digit 1) V : Points indiv. joueur 3 (digit 1)
28 L : Fautes individuelles joueur 6 L : Points indiv. joueur 3 (digit 2) V : Points indiv. joueur 3 (digit 2)
29 L : Fautes individuelles joueur 7 L : Points indiv. joueur 4 (digit 1) V : Points indiv. joueur 4 (digit 1)
30 L : Fautes individuelles joueur 8 L : Points indiv. joueur 4 (digit 2) V : Points indiv. joueur 4 (digit 2)
31 L : Fautes individuelles joueur 9 L : Points indiv. joueur 5 (digit 1) V : Points indiv. joueur 5 (digit 1)
32 L : Fautes individuelles joueur 10 L : Points indiv. joueur 5 (digit 2) V : Points indiv. joueur 5 (digit 2)
33 L : Fautes individuelles joueur 11 L : Points indiv. joueur 6 (digit 1) V : Points indiv. joueur 6 (digit 1)
34 L : Fautes individuelles joueur 12 L : Points indiv. joueur 6 (digit 2) V : Points indiv. joueur 6 (digit 2)
35 V : Fautes individuelles joueur 1 L : Points indiv. joueur 7 (digit 1) V : Points indiv. joueur 7 (digit 1)
36 V : Fautes individuelles joueur 2 L : Points indiv. joueur 7 (digit 2) V : Points indiv. joueur 7 (digit 2)
37 V : Fautes individuelles joueur 3 L : Points indiv. joueur 8 (digit 1) V : Points indiv. joueur 8 (digit 1)
38 V : Fautes individuelles joueur 4 L : Points indiv. joueur 8 (digit 2) V : Points indiv. joueur 8 (digit 2)
39 V : Fautes individuelles joueur 5 L : Points indiv. joueur 9 (digit 1) V : Points indiv. joueur 9 (digit 1)
40 V : Fautes individuelles joueur 6 L : Points indiv. joueur 9 (digit 2) V : Points indiv. joueur 9 (digit 2)
41 V : Fautes individuelles joueur 7 L : Points indiv. joueur 10 (digit 1) V : Points indiv. joueur 10 (digit 1)
42 V : Fautes individuelles joueur 8 L : Points indiv. joueur 10 (digit 2) V : Points indiv. joueur 10 (digit 2)
43 V : Fautes individuelles joueur 9 L : Points indiv. joueur 11 (digit 1) V : Points indiv. joueur 11 (digit 1)
44 V : Fautes individuelles joueur 10 L : Points indiv. joueur 11 (digit 2) V : Points indiv. joueur 11 (digit 2)
45 V : Fautes individuelles joueur 11 L : Points indiv. joueur 12 (digit 1) V : Points indiv. joueur 12 (digit 1)
46 V : Fautes individuelles joueur 12 L : Points indiv. joueur 12 (digit 2) V : Points indiv. joueur 12 (digit 2)
47 Chrono. temps-mort (digit2) L : Points indiv. joueur 13 (digit 1) V : Points indiv. joueur 13 (digit 1)
48 Chrono. temps-mort (digit3) L : Points indiv. joueur 13 (digit 2) V : Points indiv. joueur 13 (digit 2)
49 Chrono. 24" (digit 1) Chrono. 24" (digit 1) Chrono. 24" (digit 1)
50 Chrono. 24" (digit 2) Chrono. 24" (digit 2) Chrono. 24" (digit 2)
51 Klaxon 24" (note 5) Klaxon 24" (note 5) Klaxon 24" (note 5)
52 Start/Stop 24" (note 6) Start/Stop 24" (note 6) Start/Stop 24" (note 6)
53 Affichage 24" (note 7) Affichage 24" (note 7) Affichage 24" (note 7)
54 "0D" "0D" "0D"
```

## HANDBALL / FOOTBALL / VOLLEY-BALL / TENNIS (PDF page 4)

Header/context:

```text
COMPOSITION DES TRAMES
HANDBALL / FOOTBALL / VOLLEY-BALL / TENNIS
CODE DANS
LA TRAME HANDBALL / FOOTBALL VOLLEY-BALL TENNIS
```

Frame layout (rows 01..54):

```text
01 CODE START = "F8" CODE START = "F8" CODE START = "F8"
02 CODE SPORT ="35" CODE SPORT ="36" CODE SPORT ="39"
03 "20" "20" "20"
04 "20" "20" "20"
05 Chrono. (digit 1) Chrono. (digit 1) Chrono. (digit 1)
06 Chrono. (digit 2) Chrono. (digit 2) Chrono. (digit 2)
07 Chrono. (digit 3) Chrono. (digit 3) Chrono. (digit 3)
08 Chrono. (digit 4) Chrono. (digit 4) Chrono. (digit 4)
09 "20" "20" "20"
10 L : points (digit 1) L : points (digit 1) L : points (digit 1)
11 L : points (digit 2) L : points (digit 2) L : points (digit 2)
12 "20" "20" "20"
13 V : points (digit 1) V : points (digit 1) V : points (digit 1)
14 V : points (digit 2) V : points (digit 2) V : points (digit 2)
15 Periode Set Set
16 L : Pénalités en cours (note 8) L : Sets gagnés L : Sets gagnés
17 V : Pénalités en cours (note 8) V : Sets gagnés V : Sets gagnés
18 L : Nombre de temps-morts L : Nombre de temps-morts "20"
19 V : Nombre de temps-morts V : Nombre de temps-morts "20"
20 Klaxon (note 5) Klaxon (note 5) "20"
21 Start/Stop Chrono. (note 6) Start/Stop Chrono. (note 6) Chrono. Start/Stop (note 6)
22 "20" Affichage Horloge/Chrono. (note 9) Affichage Horloge/Chrono. (note 9)
23 L : Chrono. Pénalité 1 (digit 1) "20" L : Jeux gagnés dans le set (digit 1)
24 L : Chrono. Pénalité 1 (digit 2) "20" L : Jeux gagnés dans le set (digit 2)
25 L : Chrono. Pénalité 1 (digit 3) L : Points dans le 1er Set (digit 1) L : Jeux dans le 1er set (digit 1)
26 L : Chrono. Pénalité 2 (digit 1) L : Points dans le 1er Set (digit 2) L : Jeux dans le 1er set (digit 2)
27 L : Chrono. Pénalité 2 (digit 2) V : Points dans le 1er Set (digit 1) V : Jeux dans le 1er set (digit 1)
28 L : Chrono. Pénalité 2 (digit 3) V : Points dans le 1er Set (digit 2) V : Jeux dans le 1er set (digit 2)
29 L : Chrono. Pénalité 3 (digit 1) L : Points dans le 2ème Set (digit 1) L : Jeux dans le 2ème set (digit 1)
30 L : Chrono. Pénalité 3 (digit 2) L : Points dans le 2ème Set (digit 2) L : Jeux dans le 2ème set (digit 2)
31 L : Chrono. Pénalité 3 (digit 3) V : Points dans le 2ème Set (digit 1) V : Jeux dans le 2ème set (digit 1)
32 "20" V : Points dans le 2ème Set (digit 2) V : Jeux dans le 2ème set (digit 2)
33 "20" L : Points dans le 3ème Set (digit 1) "20"
34 "20" L : Points dans le 3ème Set (digit 2) "20"
35 "20" V : Points dans le 3ème Set (digit 1) "20"
36 V : Chrono. Pénalité 1 (digit 1) V : Points dans le 3ème Set (digit 2) V : Jeux gagnés dans le set (digit 1)
37 V : Chrono. Pénalité 1 (digit 2) L : Points dans le 4ème Set (digit 1) V : Jeux gagnés dans le set (digit 2)
38 V : Chrono. Pénalité 1 (digit 3) L : Points dans le 4ème Set (digit 2) L : Jeux dans le 3ème set (digit 1)
39 V : Chrono. Pénalité 2 (digit 1) V : Points dans le 4ème Set (digit 1) L : Jeux dans le 3ème set (digit 2)
40 V : Chrono. Pénalité 2 (digit 2) V : Points dans le 4ème Set (digit 2) V : Jeux dans le 3ème set (digit 1)
41 V : Chrono. Pénalité 2 (digit 3) "20" V : Jeux dans le 3ème set (digit 2)
42 V : Chrono. Pénalité 3 (digit 1) "20" L : Jeux dans le 4ème set (digit 1)
43 V : Chrono. Pénalité 3 (digit 2) "20" L : Jeux dans le 4ème set (digit 2)
44 V : Chrono. Pénalité 3 (digit 3) "20" V : Jeux dans le 4ème set (digit 1)
45 "20" "20" V : Jeux dans le 4ème set (digit 2)
46 "20" "20" "20"
47 "20" "20" "20"
48 "20" "20" "20"
49 "20" "20" "20"
50 "20" "20" "20"
51 "20" Service (note 10) Service (note 10)
52 "20" Gagnant (note 11) Gagnant (note 11)
53 "20" "20" Tie-break (note 12)
54 "0D" "0D" "0D"
```

## TENNIS DE TABLE / BADMINTON / CHRONOMETRE SIMPLE (PDF page 5)

Header/context:

```text
COMPOSITION DES TRAMES
TENNIS DE TABLE / BADMINTON / CHRONOMETRE SIMPLE
CODE DANS
LA TRAME TENNIS DE TABLE BADMINTON CHRONOMETRE SIMPLE
```

Frame layout (rows 01..54):

```text
01 CODE START = "F8" CODE START = "F8" CODE START = "F8"
02 CODE SPORT ="3A" CODE SPORT ="6C" CODE SPORT ="9A"
03 "20" "20" "20"
04 "20" "20" "20"
05 Chrono. (digit 1) Chrono. (digit 1) Chrono. (digit 1)
06 Chrono. (digit 2) Chrono. (digit 2) Chrono. (digit 2)
07 Chrono. (digit 3) Chrono. (digit 3) Chrono. (digit 3)
08 Chrono. (digit 4) Chrono. (digit 4) Chrono. (digit 4)
09 "20" "20" "20"
10 L : points (digit 1) L : points (digit 1) "20"
11 L : points (digit 2) L : points (digit 2) "20"
12 "20" "20" "20"
13 V : points (digit 1) V : points (digit 1) "20"
14 V : points (digit 2) V : points (digit 2) "20"
15 Set Set "20"
16 L : Sets gagnés L : Sets gagnés "20"
17 V : Sets gagnés V : Sets gagnés "20"
18 "20" "20" "20"
19 "20" "20" "20"
20 "20" "20" Klaxon (note 5)
21 Start/Stop Chrono. (note 6) Start/Stop Chrono. (note 6) Start/Stop Chrono. (note 6)
22 Affichage Horloge/Chrono. (note 9) Affichage Horloge/Chrono. (note 9) Affichage Horloge/Chrono. (note 9)
23 "20" "20" "20"
24 "20" "20" "20"
25 L : Points dans le 1er Set (digit 1) L : Points dans le 1er Set (digit 1) "20"
26 L : Points dans le 1er Set (digit 2) L : Points dans le 1er Set (digit 2) "20"
27 V : Points dans le 1er Set (digit 1) V : Points dans le 1er Set (digit 1) "20"
28 V : Points dans le 1er Set (digit 2) V : Points dans le 1er Set (digit 2) "20"
29 L : Points dans le 2ème Set (digit 1) L : Points dans le 2ème Set (digit 1) "20"
30 L : Points dans le 2ème Set (digit 2) L : Points dans le 2ème Set (digit 2) "20"
31 V : Points dans le 2ème Set (digit 1) V : Points dans le 2ème Set (digit 1) "20"
32 V : Points dans le 2ème Set (digit 2) V : Points dans le 2ème Set (digit 2) "20"
33 L : Points dans le 3ème Set (digit 1) L : Points dans le 3ème Set (digit 1) "20"
34 L : Points dans le 3ème Set (digit 2) L : Points dans le 3ème Set (digit 2) "20"
35 V : Points dans le 3ème Set (digit 1) V : Points dans le 3ème Set (digit 1) "20"
36 V : Points dans le 3ème Set (digit 2) V : Points dans le 3ème Set (digit 2) "20"
37 L : Points dans le 4ème Set (digit 1) "20" "20"
38 L : Points dans le 4ème Set (digit 2) "20" "20"
39 V : Points dans le 4ème Set (digit 1) "20" "20"
40 V : Points dans le 4ème Set (digit 2) "20" "20"
41 "20" "20" "20"
42 "20" "20" "20"
43 "20" "20" "20"
44 "20" "20" "20"
45 "20" "20" "20"
46 "20" "20" "20"
47 "20" "20" "20"
48 "20" "20" "20"
49 "20" "20" "20"
50 "20" "20" "20"
51 Service (note 10) Service (note 10) "20"
52 Gagnant (note 11) Gagnant (note 11) "20"
53 "20" "20" "20"
54 "0D" "0D" "0D"
```

## MISE A L'HEURE / ENTRAINEMENT / TEST DES LEDS (PDF page 6)

Header/context:

```text
COMPOSITION DES TRAMES
MISE A L'HEURE / ENTRAINEMENT / TEST DES LEDS
CODE DANS
LA TRAME MISE A L'HEURE ENTRAINEMENT TEST DES LEDS
```

Frame layout (rows 01..54):

```text
01 CODE START = "F8" CODE START = "F8" CODE START = "F8"
02 CODE SPORT ="99" CODE SPORT ="9C" CODE SPORT ="66"
03 "20" "20" "20"
04 "20" "20" Mode test (note 14)
05 Heure (digit 1) Chrono. (digit 1) "20"
06 Heure (digit 2) Chrono. (digit 2) L : Test ligne
07 Heure (digit 3) Chrono. (digit 3) V : Test ligne
08 Heure (digit 4) Chrono. (digit 4) "20"
09 "20" "20" "20"
10 Horaire d'affichage (digit 1) cycles (digit 1) "20"
11 Horaire d'affichage (digit 2) cycles (digit 2) "20"
12 Horaire d'affichage (digit 3) "20" "20"
13 Horaire d'affichage (digit 4) "20" "20"
14 "20" "20" "20"
15 Horaire d'extinction (digit 1) "20" "20"
16 Horaire d'extinction (digit 2) "20" "20"
17 Horaire d'extinction (digit 3) "20" "20"
18 Horaire d'extinction (digit 4) "20" "20"
19 "20" "20" "20"
20 "20" Klaxon (note 5) Klaxon (note 5)
21 "20" Start/Stop Chrono. (note 6) "20"
22 "20" Affichage Horloge/Chrono. (note 9) "20"
23 "20" "20" "20"
24 "20" "20" "20"
25 "20" "20" "20"
26 "20" "20" "20"
27 "20" "20" "20"
28 "20" "20" "20"
29 "20" "20" "20"
30 "20" "20" "20"
31 "20" "20" "20"
32 "20" "20" "20"
33 "20" "20" "20"
34 "20" "20" "20"
35 "20" "20" "20"
36 "20" "20" "20"
37 "20" "20" "20"
38 "20" "20" "20"
39 "20" "20" "20"
40 "20" "20" "20"
41 "20" "20" "20"
42 "20" "20" "20"
43 "20" "20" "20"
44 "20" "20" "20"
45 "20" "20" "20"
46 "20" "20" "20"
47 "20" "20" "20"
48 "20" "20" "20"
49 "20" "20" "20"
50 "20" "20" "20"
51 "20" Exercice/Repos (note 13) "20"
52 "20" "20" "20"
53 "20" "20" "20"
54 "0D" "0D" "0D"
```

## HOCKEY / FLOORBALL / BOXE / NETBALL (PDF page 7)

Header/context:

```text
COMPOSITION DES TRAMES
HOCKEY / FLOORBALL / BOXE / NETBALL
CODE DANS
LA TRAME HOCKEY / FLOORBALL BOXE NETBALL
```

Frame layout (rows 01..54):

```text
01 CODE START = "F8" CODE START = "F8" CODE START = "F8"
02 CODE SPORT ="35" CODE SPORT ="35" CODE SPORT ="33"
03 "20" "20" "20"
04 "20" "20" Possession balle (note 4)
05 Chrono. (digit 1) Chrono. (digit 1) Chrono. (digit 1)
06 Chrono. (digit 2) Chrono. (digit 2) Chrono. (digit 2)
07 Chrono. (digit 3) Chrono. (digit 3) Chrono. (digit 3)
08 Chrono. (digit 4) Chrono. (digit 4) Chrono. (digit 4)
09 "20" "20" "20"
10 L : points (digit 1) "20" L : points (digit 2)
11 L : points (digit 2) L : avertissements L : points (digit 3)
12 "20" "20" "20"
13 V : points (digit 1) "20" V : points (digit 2)
14 V : points (digit 2) V : avertissements V : points (digit 3)
15 Periode Periode Periode
16 L : Pénalités en cours (note 8) "20" "20"
17 V : Pénalités en cours (note 8) "20" "20"
18 L : Nombre de temps-morts "20" "20"
19 V : Nombre de temps-morts "20" "20"
20 Klaxon (note 5) Klaxon (note 5) Klaxon (note 5)
21 Start/Stop Chrono. (note 6) Start/Stop Chrono. (note 6) Start/Stop Chrono. (note 6)
22 "20" "20" "20"
23 L : Chrono. Pénalité 1 (digit 1) "20" "20"
24 L : Chrono. Pénalité 1 (digit 2) "20" "20"
25 L : Chrono. Pénalité 1 (digit 3) "20" "20"
26 L : Chrono. Pénalité 2 (digit 1) "20" "20"
27 L : Chrono. Pénalité 2 (digit 2) "20" "20"
28 L : Chrono. Pénalité 2 (digit 3) "20" "20"
29 L : Chrono. Pénalité 3 (digit 1) "20" "20"
30 L : Chrono. Pénalité 3 (digit 2) "20" "20"
31 L : Chrono. Pénalité 3 (digit 3) "20" "20"
32 "20" "20" "20"
33 "20" "20" "20"
34 "20" "20" "20"
35 "20" "20" "20"
36 V : Chrono. Pénalité 1 (digit 1) "20" "20"
37 V : Chrono. Pénalité 1 (digit 2) "20" "20"
38 V : Chrono. Pénalité 1 (digit 3) "20" "20"
39 V : Chrono. Pénalité 2 (digit 1) "20" "20"
40 V : Chrono. Pénalité 2 (digit 2) "20" "20"
41 V : Chrono. Pénalité 2 (digit 3) "20" "20"
42 V : Chrono. Pénalité 3 (digit 1) "20" "20"
43 V : Chrono. Pénalité 3 (digit 2) "20" "20"
44 V : Chrono. Pénalité 3 (digit 3) "20" "20"
45 "20" "20" "20"
46 "20" "20" "20"
47 "20" "20" "20"
48 "20" "20" "20"
49 "20" "20" "20"
50 "20" "20" "20"
51 "20" "20" "20"
52 "20" "20" "20"
53 "20" "20" "20"
54 "0D" "0D" "0D"
```

## OPTION MESSAGES DEFILANTS (PDF page 8)

Header/context:

```text
COMPOSITION DES TRAMES
OPTION MESSAGES DEFILANTS
CODE DANS
LA TRAME MESSAGES CONFIGURATION MESSAGES
```

Frame layout (rows 01..54):

```text
01 CODE START = "F8" CODE START = "F8"
02 CODE SPORT ="4D" ( M ) CODE SPORT ="43" ( C )
03 Index trame Type message
04 Numéro Message Type message
05 Chrono. (digit 1) Chrono. (digit 1)
06 Chrono. (digit 2) Chrono. (digit 2)
07 Chrono. (digit 3) Chrono. (digit 3)
08 Chrono. (digit 4) Chrono. (digit 4)
09 Caractère 1 - Octet 1 (UTF16) Type Message 1
10 Caractère 1 - Octet 2 (UTF16) Type Message 2
11 Caractère 2 - Octet 1 (UTF16) Type Message 3
12 Caractère 2 - Octet 2 (UTF16) Type Message 4
13 Caractère 3 - Octet 1 (UTF16) Cycle (digit 1)
14 Caractère 3 - Octet 2 (UTF16) Cycle (digit 2)
15 Caractère 4 - Octet 1 (UTF16) Type Message 1
16 Caractère 4 - Octet 2 (UTF16) Type Message 2
17 Caractère 5 - Octet 1 (UTF16) Type Message 3
18 Caractère 5 - Octet 2 (UTF16) Type Message 4
19 Caractère 6 - Octet 1 (UTF16) "20"
20 Klaxon (note 5) Klaxon (note 5)
21 Start/Stop Chrono. (note 6) Start/Stop Chrono. (note 6)
22 Caractère 6 - Octet 2 (UTF16) Chronologie (digit 1)
23 Caractère 7 - Octet 1 (UTF16) Chronologie (digit 2)
24 Caractère 7 - Octet 2 (UTF16) Chronologie (digit 3)
25 Caractère 8 - Octet 1 (UTF16) Chronologie (digit 4)
26 Caractère 8 - Octet 2 (UTF16) "20"
27 Caractère 9 - Octet 1 (UTF16) "20"
28 Caractère 9 - Octet 2 (UTF16) "20"
29 Caractère 10 - Octet 1 (UTF16) "20"
30 Caractère 10 - Octet 2 (UTF16) "20"
31 Caractère 11 - Octet 1 (UTF16) "20"
32 Caractère 11 - Octet 2 (UTF16) "20"
33 Caractère 12 - Octet 1 (UTF16) "20"
34 Caractère 12 - Octet 2 (UTF16) "20"
35 Caractère 13 - Octet 1 (UTF16) "20"
36 Caractère 13 - Octet 2 (UTF16) "20"
37 Caractère 14 - Octet 1 (UTF16) "20"
38 Caractère 14 - Octet 2 (UTF16) "20"
39 Caractère 15 - Octet 1 (UTF16) "20"
40 Caractère 15 - Octet 2 (UTF16) "20"
41 Caractère 16 - Octet 1 (UTF16) "20"
42 Caractère 16 - Octet 2 (UTF16) "20"
43 Caractère 17 - Octet 1 (UTF16) "20"
44 Caractère 17 - Octet 2 (UTF16) "20"
45 Caractère 18 - Octet 1 (UTF16) "20"
46 Caractère 18 - Octet 2 (UTF16) "20"
47 Caractère 19 - Octet 1 (UTF16) "20"
48 Caractère 19 - Octet 2 (UTF16) "20"
49 Chrono. 24" (digit 1) Chrono. 24" (digit 1)
50 Chrono. 24" (digit 2) Chrono. 24" (digit 2)
51 Klaxon 24" (note 5) Klaxon 24" (note 5)
52 Start/Stop 24" (note 6) Start/Stop 24" (note 6)
53 Affichage 24" (note 7) Affichage 24" (note 7)
54 "0D" "0D"
```

## NOMS DES EQUIPES / NOMS ET NUMEROS DES JOUEURS (PDF page 9)

Header/context:

```text
COMPOSITION DES TRAMES
NOMS DES EQUIPES / NOMS ET NUMEROS DES JOUEURS
CODE DANS EQUIPES JOUEURS JOUEURS
LA TRAME LOCAUX & VISITEURS LOCAUX VISITEURS
```

Frame layout (rows 01..54):

```text
01 CODE START = "F8" CODE START = "F8" CODE START = "F8"
02 CODE SPORT ="77" ou "62" CODE SPORT ="77" CODE SPORT="62"
03 "20" Joueur concerné ("30" à "3B") Joueur concerné ("30" à "3B")
04 "20" Caractère 1 - Octet 1 (UTF16) Caractère 1 - Octet 1 (UTF16)
05 "20" Caractère 1 - Octet 2 (UTF16) Caractère 1 - Octet 2 (UTF16)
06 "20" Caractère 2 - Octet 1 (UTF16) Caractère 2 - Octet 1 (UTF16)
07 Caractère 1 - Octet 1 (UTF16) Caractère 2 - Octet 2 (UTF16) Caractère 2 - Octet 2 (UTF16)
08 Caractère 1 - Octet 2 (UTF16) Caractère 3 - Octet 1 (UTF16) Caractère 3 - Octet 1 (UTF16)
09 Caractère 2 - Octet 1 (UTF16) Caractère 3 - Octet 2 (UTF16) Caractère 3 - Octet 2 (UTF16)
10 Caractère 2 - Octet 2 (UTF16) Caractère 4 - Octet 1 (UTF16) Caractère 4 - Octet 1 (UTF16)
11 Caractère 3 - Octet 1 (UTF16) Caractère 4 - Octet 2 (UTF16) Caractère 4 - Octet 2 (UTF16)
12 Caractère 3 - Octet 2 (UTF16) Caractère 5 - Octet 1 (UTF16) Caractère 5 - Octet 1 (UTF16)
13 Caractère 4 - Octet 1 (UTF16) Caractère 5 - Octet 2 (UTF16) Caractère 5 - Octet 2 (UTF16)
14 Caractère 4 - Octet 2 (UTF16) Caractère 6 - Octet 1 (UTF16) Caractère 6 - Octet 1 (UTF16)
15 Caractère 5 - Octet 1 (UTF16) Caractère 6 - Octet 2 (UTF16) Caractère 6 - Octet 2 (UTF16)
16 Caractère 5 - Octet 2 (UTF16) Caractère 7 - Octet 1 (UTF16) Caractère 7 - Octet 1 (UTF16)
17 Caractère 6 - Octet 1 (UTF16) Caractère 7 - Octet 2 (UTF16) Caractère 7 - Octet 2 (UTF16)
18 Caractère 6 - Octet 2 (UTF16) Caractère 8 - Octet 1 (UTF16) Caractère 8 - Octet 1 (UTF16)
19 Caractère 7 - Octet 1 (UTF16) Caractère 8 - Octet 2 (UTF16) Caractère 8 - Octet 2 (UTF16)
20 Caractère 7 - Octet 2 (UTF16) Caractère 9 - Octet 1 (UTF16) Caractère 9 - Octet 1 (UTF16)
21 Caractère 8 - Octet 1 (UTF16) Caractère 9 - Octet 2 (UTF16) Caractère 9 - Octet 2 (UTF16)
22 Caractère 8 - Octet 2 (UTF16) Caractère 10 - Octet 1 (UTF16) Caractère 10 - Octet 1 (UTF16)
23 Caractère 9 - Octet 1 (UTF16) Caractère 10 - Octet 2 (UTF16) Caractère 10 - Octet 2 (UTF16)
24 Caractère 9 - Octet 2 (UTF16) "20" "20"
25 Caractère 10 - Octet 1 (UTF16) "20" "20"
26 Caractère 10 - Octet 2 (UTF16) "20" "20"
27 Caractère 11 - Octet 1 (UTF16) "20" "20"
28 Caractère 11 - Octet 2 (UTF16) "20" "20"
29 Caractère 12 - Octet 1 (UTF16) "20" "20"
30 Caractère 12 - Octet 2 (UTF16) "20" "20"
31 Caractère 13 - Octet 1 (UTF16) "20" "20"
32 Caractère 13 - Octet 2 (UTF16) "20" "20"
33 Caractère 14 - Octet 1 (UTF16) "20" "20"
34 Caractère 14 - Octet 2 (UTF16) "20" "20"
35 Caractère 15 - Octet 1 (UTF16) "20" "20"
36 Caractère 15 - Octet 2 (UTF16) "20" "20"
37 Caractère 16 - Octet 1 (UTF16) "20" "20"
38 Caractère 16 - Octet 2 (UTF16) "20" "20"
39 Caractère 17 - Octet 1 (UTF16) "20" "20"
40 Caractère 17 - Octet 2 (UTF16) "20" "20"
41 Caractère 18 - Octet 1 (UTF16) "20" "20"
42 Caractère 18 - Octet 2 (UTF16) "20" "20"
43 Caractère 19 - Octet 1 (UTF16) "20" "20"
44 Caractère 19 - Octet 2 (UTF16) "20" "20"
45 Caractère 20 - Octet 1 (UTF16) "20" "20"
46 Caractère 20 - Octet 2 (UTF16) "20" "20"
47 Caractère 21 - Octet 1 (UTF16) "20" "20"
48 Caractère 21 - Octet 2 (UTF16) "20" "20"
49 "20" "20" "20"
50 "20" "20" "20"
51 "20" "20" "20"
52 "20" Numéro dossard (digit 1) Numéro dossard (digit 1)
53 "20" Numéro dossard (digit 2) Numéro dossard (digit 2)
54 "0D" "0D" "0D"
```
