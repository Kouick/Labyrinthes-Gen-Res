Alors, honnêtement, ce n'est vraiment pas optimisé pour les raisons suivantes :

-Les animations en rigidbody provoquent des ralentissements.
-Il y a besoin de deux layer physiques pour les blocs et les "casters".
-Le code est mal structuré, peu détaillé, et certaines fonctions manquent de logique.
-Il reste potentiellement des morceaux d'assets que je n'ai pas correctement supprimés, mais que j'ai dû enlever car je n'ai pas le droit de vous les fournir.

Tous ces problèmes peuvent être réglés aisément et je le ferai probablement un jour, mais je privilégie pour l'instant le fait de vous communiquer un système fonctionnel, quitte à y revenir ensuite.

Il s'agit d'une traduction directe de l'algorithme de génération de labyrinthes sans sortie (en Python).