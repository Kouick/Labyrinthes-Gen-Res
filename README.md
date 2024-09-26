# Labyrinthes-Gen-Res
Ce projet a pour but de créer un algorithme de génération et de résolution performant de labyrinthes, afin de pouvoir créer et résoudre de très grands labyrinthes.

Je partage avec vous aujourd'hui les résultats de mon TIPE en tant qu'exemple ainsi qu'en tant que travail de recherche. Cette présentation a obtenu une note de 16,5 sur 20. Le thème de l'année était : le sport, les jeux.

Je publie sur ce sujet car il est actuellement difficile de trouver des informations précises dans le domaine des labyrinthes.

Ce projet comprend donc mon code commenté ainsi que mes algorithmes détaillés et expliqués, accompagnés de ma présentation au format PDF.

Les labyrinthes considérés correspondent, sauf information explicite du contraire, à des images précises au pixel près, où un pixel est une case "chemin" (on peut marcher dessus) ou une case mur (on ne peut pas s'y déplacer). L'entrée et la sortie ne sont que des variantes de cases "chemin".

### Résolution
Le programme ne résout actuellement que les labyrinthes acycliques, mais couplé à un détecteur de cycles, il est possible de le faire tourner sur des labyrinthes cycliques.

L'algorithme consiste à analyser le labyrinthe dans sa globalité et à considérer les cul-de-sac directs (les cases "chemin" autre que la sortie ou l'entrée n'ayant qu'au plus une case "chemin" accessible) comme des murs. Ainsi, seule la solution restera sur le labyrinthe après une itération suffisante de cette étape.

### Génération
Cet algorithmes génère uniquement des labyrinthes parfaits.

L'algorithme consiste à analyser le labyrinthe dans sa globalité et à considérer les cul-de-sac potentiels (les cases "mur" ayant exactement une case "chemin" accessible) pour les transformer en case "chemin" avec une probabilité donnée. Ainsi, le labyrinthe apparaîtra de lui-même après une itération suffisante de cette étape.

Pour obtenir un labyrinthe ayant une entrée et une sortie, il suffit de "faire pousser" deux labyrinthes et de les rejoindre en un point. Les origines de ces deux labyrinthes seront donc l'entrée et la sortie du labyrinthe obtenu.