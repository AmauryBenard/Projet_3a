# Projet_3a

Titre du projet : Générateur de presets de synthétiseur basé sur une seed numérique
1. Contexte et idée générale

L’objectif du projet est de concevoir un programme capable de générer automatiquement les paramètres d’un synthétiseur à partir d’une seed — c’est-à-dire une suite de chiffres aléatoires servant de base à la création d’un preset complet.
Chaque chiffre (ou groupe de chiffres) de cette seed correspond à un paramètre spécifique du synthétiseur, comme la fréquence de coupure d’un filtre, la quantité de réverbération, la forme d’onde, ou encore le niveau de mixage d’un effet.

Ainsi, une seed donnée (par exemple 1239583729507) produira toujours la même configuration sonore, tandis qu’une autre seed générera un son différent.
Ce procédé permet de recréer des presets uniques et reproductibles, de manière automatique et contrôlée.

2. Objectifs du projet

Créer un système capable de transformer une seed numérique en un ensemble de paramètres sonores cohérents.

Générer et manipuler des presets de synthé de manière algorithmique, sans intervention manuelle.

Explorer le lien entre la génération pseudo-aléatoire et la création musicale.

3. Étapes du projet
Étape 1 – Prototype en Python

Dans un premier temps, le projet sera développé en Python afin de valider le concept.
Le programme :

Génère une seed aléatoire (ou prend une seed saisie par l’utilisateur).

Décompose la seed en chiffres ou sous-groupes de chiffres.

Associe chaque valeur à un paramètre de synthétiseur (ex. :

0–3 : type d’oscillateur

4–6 : niveau de mixage d’un effet

7–9 : intensité de modulation)

Envoie ces valeurs via MIDI CC (Control Change) à un synthétiseur virtuel externe (ex : Vital, Serum, Pigments), en utilisant une interface MIDI virtuelle (loopMIDI sur Windows ou IAC Driver sur macOS).

Cette première version permettra d’entendre en temps réel les variations sonores générées par différentes seeds.

Étape 2 – Intégration dans un plugin (JUCE / C++)

Une fois le concept validé, la seconde phase consistera à créer un plugin audio autonome (VST3/AU) à l’aide du framework JUCE en C++.
Le plugin intégrera :

Un moteur de synthèse simple (oscillateurs, filtres, enveloppes, effets).

Un générateur de seed interne.

Une interface graphique affichant la seed et les paramètres associés.

La possibilité d’importer ou d’exporter des seeds pour retrouver un preset.

Ce plugin pourra être chargé directement dans un DAW (Ableton Live, FL Studio, Reaper, etc.), et utilisé comme un synthétiseur classique.

4. Intérêt pédagogique et technique

Le projet combine plusieurs domaines :

Programmation audio (synthèse sonore, contrôle MIDI, DSP).

Génération procédurale (conversion d’une seed en données exploitables).

Interaction homme–machine (interface pour visualiser et manipuler la seed).

Créativité musicale assistée par ordinateur, en explorant la génération algorithmique de sons.

Il offre donc une approche interdisciplinaire entre informatique, musique et conception sonore.

5. Résultat attendu

Une application Python capable de générer des presets à partir de seeds et de les envoyer à un synthétiseur externe.

(À terme) Un plugin audio complet, intégrable dans un DAW, permettant de créer des sons uniques et reproductibles à partir d’une simple seed.
