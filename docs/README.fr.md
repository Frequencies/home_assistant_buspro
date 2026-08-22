# HDL Buspro pour Home Assistant

[English](../README.md) | **Français**

L'intégration gère la passerelle et les appareils physiques HDL Buspro depuis
l'interface de Home Assistant. La liste complète des modèles, entités et
services est disponible dans la [documentation anglaise](../README.md).

## Installation

### HACS (recommandé)

1. Ouvrez **HACS > Intégrations**.
2. Ouvrez le menu à trois points et sélectionnez **Dépôts personnalisés**.
3. Ajoutez `https://github.com/Frequencies/home_assistant_buspro` avec la
   catégorie **Intégration**.
4. Recherchez **HDL Buspro**, ouvrez-le et sélectionnez **Télécharger**.
5. Redémarrez Home Assistant lorsque HACS le demande.

Les versions suivantes pourront être installées depuis **HACS > Intégrations**.
Redémarrez Home Assistant après chaque mise à jour de l'intégration.

### Installation manuelle

1. Téléchargez le dépôt de l'intégration.
2. Copiez son répertoire `custom_components/buspro` dans
   `/config/custom_components/buspro` de Home Assistant.
3. Redémarrez Home Assistant.

## Première configuration

1. Ouvrez **Paramètres > Appareils et services > Ajouter une intégration** et
   sélectionnez **HDL Buspro**.
2. Saisissez l'adresse de la passerelle et les ports UDP. Le port habituel est
   `6000`.
3. Saisissez une adresse Buspro libre pour Home Assistant au format
   `sous-réseau.appareil`. La valeur par défaut `200.200` ne doit appartenir à
   aucun autre appareil Buspro.
4. Ouvrez **Configurer > Ajouter un appareil**, sélectionnez le type et le
   modèle exact, puis saisissez son adresse Buspro physique et un nom.
5. Nommez les canaux ou fonctions nécessaires. Un nom vide laisse le canal
   désactivé et empêche la création de son entité.

Les modèles connus utilisent le nombre fixe de canaux ou la liste de fonctions
du catalogue. Pour un profil générique, l'utilisateur indique un nombre de
canaux dans la limite prise en charge. Après l'enregistrement, l'entrée de
configuration est rechargée et les entités sont regroupées sous un seul
appareil physique.

Pour apporter des modifications, ouvrez **Configurer > Modifier l'appareil**.
Pour les appareils gérés depuis l'interface, le modèle, le nom et les canaux
peuvent être modifiés, ou l'appareil supprimé. La configuration protocolaire
des anciens appareils YAML doit toujours être modifiée dans YAML ; redémarrez
ensuite Home Assistant.

## Changements incompatibles dans la version 2.2.0

- Les adresses, noms, nombres d'appareils et affectations de canaux ne sont
  plus intégrés au composant. Ils sont stockés dans les options de l'entrée de
  configuration.
- Le modèle exact détermine le nombre physique de canaux et les entités créées.
- Un canal sans nom est désactivé et n'est pas créé.
- L'adresse Buspro de Home Assistant est migrée vers `200.200` par défaut. Elle
  doit être libre sur le réseau.
- Les événements des panneaux sont maintenant décodés en `channel_on`,
  `channel_off`, `channel_level`, `scene` et événements de commutateur universel.
- Le constructeur `Buspro` intégré exige désormais `client_address`.

## Mise à niveau

1. Redémarrez Home Assistant après avoir remplacé le composant.
2. Ouvrez **Paramètres > Appareils et services > HDL Buspro > Configurer**.
3. Vérifiez la passerelle, les ports UDP et une adresse Buspro libre pour Home
   Assistant.
4. Sélectionnez le modèle exact de chaque appareil et vérifiez les noms des
   canaux.
5. Vérifiez les automatisations qui utilisent les événements des panneaux.
6. Supprimez ou commentez les anciennes entités YAML uniquement après avoir
   vérifié leurs remplacements gérés depuis l'interface.

Ne configurez pas le même canal physique dans YAML et dans l'interface en même
temps : cela crée des entités et des abonnements au protocole en double.

## Vérification du catalogue et tests

Pour comparer le catalogue des modèles à la liste officielle HDL maintenue :

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

Pour les appareils YAML hérités, l'intégration normalise désormais les profils
manquants à partir des métadonnées de modèle. Les modèles inconnus ou profils
invalides sont consignés en avertissement puis basculent vers `sensor_status`.

Tests ciblés de l'intégration :

```bash
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -p 'test_*.py'
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -p 'test_*.py'
```
