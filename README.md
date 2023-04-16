Programme BFS Game of Thrones


Ce programme permet de réaliser un parcours en largeur sur le site https://iceandfire.fandom.com, qui est une encyclopédie en ligne sur l'univers de la saga Game of Thrones. Il est également possible de trouver le plus court chemin entre deux pages spécifiques, ainsi que le plus court chemin en poids de caractères et la liste des couples incestueux de la saga.

Le programme est écrit en Python 3 et utilise les bibliothèques BeautifulSoup et Requests pour interagir avec le site web. Le parcours en largeur est réalisé en utilisant une file d'attente, et les résultats sont sauvegardés dans un fichier texte.

Le programme est divisé en plusieurs fonctions :

La fonction "liste_liens" prend une URL de page en entrée et renvoie tous les liens présents dans le corps de la page.

La fonction "svg_dico" permet de sauvegarder un dictionnaire dans un fichier texte.

La fonction "chg_dico" permet de charger un dictionnaire depuis un fichier texte.

La fonction "bfs3" permet de réaliser un parcours en largeur sur le site et de sauvegarder les résultats dans un fichier texte.

La fonction "plus_court_chemin" permet de trouver le plus court chemin entre deux pages spécifiques.

La fonction "nombre_voyelle" calcule le nombre de voyelles dans une chaîne de caractères.

La fonction "nombre_caractères" calcule le nombre de caractères dans une chaîne de caractères, en excluant les voyelles.

La fonction "nombre" calcule le poids d'une chaîne de caractères, en prenant en compte à la fois le nombre de caractères et le nombre de voyelles.

La fonction "pcc_voyelles" permet de trouver le plus court chemin en poids de caractères.

La fonction "Liste_personnages" permet de générer une liste de personnages présents dans l'univers de Game of Thrones.

La fonction "Relation" permet de sauvegarder les relations entre les personnages présents dans l'univers dans un dictionnaire.

La fonction "check_common_names" compare le type des relations entre les personnages et renvoie les couples incestueux de la saga


Le fichier "BFS.txt" contient les résultats du parcours en largeur, il est preferable de charger directement le dictionnaire depuis le fichier text à l'aide de la fonction chg_dico car l'execution du BFS prends plusieurs minutes.
