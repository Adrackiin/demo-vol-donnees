# Vol de données

## Description du projet

L'objectif du projet est de mettre en avant la facilité à s'introduire dans une machine et voler des données.
Nous allons principalement exploiter la négligence humaine.
Pour illustrer le projet, nous mettrons en place 3 situations.

### Vol de données

La finalité de cette section est de voler toutes les données d'un disque.

### Remplacement de données

L'objectif de cette partie est de remplacer des données dans une machine de façon la plus discrète possible.

### Vol de mot de passe

Le but ici est de réussir à voler des mots de passe via un KeyLogger.

## Démonstrateur

**Réussir son contrôle pour les nuls**

### Scénario

Ce scénario a pour but de mettre en avant la facilité à exploiter la négligence humaine.
Nous prendrons l'exemple d'un lycéen moyen qui a quelques facilités en informatique. Il est tellement occupé à geeker qu'il a oublié de réviser pour le contrôle du lendemain.
Il se dit qu'il va essayer de s'introduire dans l'ordinateur de son professeur pour voir s'il peut tricher.

Dans un premier temps il va voler tout le contenu du disque. Pour ce faire, il envoie un mail piégé à son professeur lui demandant de 
corriger un exercice préparatoire. Le professeur ouvre la pièce jointe, téléchargeant ainsi le programme. Ce dernier copie et envoie à
à l'adolescent tout le contenu du disque. Par chance dans ce dernier se trouve le sujet du contrôle du lendemain.

Dans un second temps, l'élève a envoyé son contrôle à son professeur. Il se rend compte qu'il s'est trompé et a envoyé une version fausse de son contrôle.
Il va essayer d'avoir accès à distance à l'ordinateur du professeur afin de corriger son erreur.
Il va donc supprimer sur l'ordinateur distant le mauvais contrôle et va téléverser le bon contrôle.

Enfin, malgré tous ses efforts, il obtient quand même une mauvaise note. Il va essayer de récupérer le mot de passe ENT de son professeur afin de changer sa note.
Pour ce faire il utilise une Rubber Ducky et installe un KeyLogger dessus. Lorsque son professeur a le dos tourné, il branche la clé sur son PC.
À la fin de l'heure, il récupère la clé. Il retrouve le mot de passe et peut donc améliorer sa note.

Lors d'une démonstration, le spectateur sera dans le rôle de la victime. Notre but à nous est de réussir à passer les 3 scénarios sans qu'il ne se rende compte de quelque chose.
- Ici le spectateur va donc cliquer sur différents mails dont le mail piégé. Il essaiera à chaque fois de voir si quelque chose de malveillant a été effectué.
On pourra ainsi mettre en avant que parmi plusieurs mails il est facile de dissimuler un piège.
- Parmi une liste de fichiers le but sera de déterminer lequel a été remplacé. Ce scénario a pour objectif de montrer qu'avec un accès distant il est facile d'agir sur le PC de quelqu'un.
- Enfin ici nous simulerons un cours de 2 minutes durant lequel le spectateur devra rentrer un mot de passe au clavier. 
Nous devrons brancher et récupérer la clé sans qu'il s'en rende compte. À la fin nous pourrons révéler le piège et ainsi montrer que l'on a récupéré le mot de passe.

## Convention sur les commits

- `add` : ajout d'un nouveau fichier
- `feat` : ajout d’une nouvelle fonctionnalité
- `continue` : avancée normal du projet
- `bug` : signalement d'un problème
- `fix` : correction d’un bug
- `perf` : amélioration des performances
- `test` : ajout ou modification de tests
- `refactor` : modification qui n’apporte ni nouvelle fonctionnalité ni d’amélioration de performances
- `style` : changement qui n’apporte aucune altération fonctionnelle ou sémantique (indentation, mise en forme, ajout d’espace, renommage d’une variable…)
- `docs` : rédaction ou mise à jour de documentation