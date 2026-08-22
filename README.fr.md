# HDL Buspro

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## Langues

[![English](https://flagcdn.com/24x18/gb.png) English](README.md) |
[![Deutsch](https://flagcdn.com/24x18/de.png) Deutsch](README.de.md) |
[![Français](https://flagcdn.com/24x18/fr.png) Français](README.fr.md) |
[![Nederlands](https://flagcdn.com/24x18/nl.png) Nederlands](README.nl.md) |
[![Español](https://flagcdn.com/24x18/es.png) Español](README.es.md) |
[![Italiano](https://flagcdn.com/24x18/it.png) Italiano](README.it.md) |
[![Русский](https://flagcdn.com/24x18/ru.png) Русский](README.ru.md) |
[![Українська](https://flagcdn.com/24x18/ua.png) Українська](README.uk.md) |
[![Беларуская](https://flagcdn.com/24x18/by.png) Беларуская](README.be.md) |
[![Norsk](https://flagcdn.com/24x18/no.png) Norsk](README.no.md)


## Configuration initiale

### Configuration de la passerelle
1. Ouvrez **Paramètres > Appareils et services > Ajouter une intégration** et sélectionnez
   **HDL Buspro**.
2. Entrez l'hôte de la passerelle et les ports UDP. Le port `6000` est la valeur par défaut normale.
3. Entrez une adresse Buspro Home Assistant inutilisée au format `subnet.device`.
   La valeur par défaut est `200.200` ; elle ne doit pas appartenir à un autre appareil Buspro.

### Ajout d'appareils
Après la configuration de la passerelle :

1. Ouvrez **Paramètres > Appareils et services > HDL Buspro > Configurer**.
2. Cliquez sur **Ajouter un appareil** pour ajouter un module physique Buspro.
3. **Sélectionnez le type d'appareil** (Relais, Variateur, Store, Climat, Capteur, etc.).
4. **Sélectionnez le modèle exact** correspondant à votre matériel.
5. **Entrez l'adresse Buspro** au format `subnet.device` (par exemple, `1.5`).
6. **Entrez le nom de l'appareil** (par exemple, « Lumières du salon »).
7. **Nommez chaque canal** — laissez vide pour désactiver un canal.
8. Cliquez sur **Enregistrer**.

Home Assistant groupe automatiquement les entités par module physique dans le registre d'appareils.

**Pour des exemples de configuration UI et YAML pour tous les types d'appareils, voir [DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md).**

### Modification d'appareils

Pour modifier un appareil existant, ouvrez **Configurer > Modifier l'appareil**. Vous pouvez :
- Renommer l'appareil
- Renommer, activer ou désactiver des canaux individuels
- Modifier le modèle (ce qui peut modifier le nombre de canaux)
- Supprimer complètement l'appareil

Les appareils gérés par l'interface utilisateur prennent en charge la modification complète. Les appareils YAML hérités peuvent exposer les contrôles de nommage du registre, mais leur configuration de protocole doit toujours être modifiée dans YAML. Redémarrez Home Assistant après modification de YAML.

### Exemple rapide : Ajout d'un module relais à 4 canaux

1. Modèle : `HDL-MR0410.431` (4 canaux de relais)
2. Adresse Buspro : `1.10`
3. Nom de l'appareil : « Relais de la pièce »
4. Noms des canaux : « Lumière au plafond », « Lampe murale », « », « Ventilateur »
5. Cliquez sur **Enregistrer**

Home Assistant crée automatiquement les entités : `light.room_relays_ceiling_light`, `light.room_relays_wall_lamp`, `switch.room_relays_fan`

Pour des exemples complets d'interface utilisateur et YAML pour tous les types d'appareils, voir **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)**.

## Options de configuration

L'intégration buspro prend en charge à la fois la **configuration basée sur l'interface utilisateur** et la **configuration YAML** :

### Configuration de l'interface utilisateur
Le moyen le plus simple d'ajouter des appareils — voir **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)** pour des exemples pas à pas de tous les types d'appareils.

### Configuration YAML  
L'intégration prend en charge deux approches YAML complémentaires :
- **Centré sur l'entité** (Hérité) — fichiers d'entité individuels organisés par domaine
- **Centré sur l'appareil** (Moderne) — définitions complètes d'appareils avec tous les canaux

**Pour la documentation YAML complète, des exemples et les meilleures pratiques, voir [DUAL_MODE_YAML.md](docs/en/DUAL_MODE_YAML.md)** (également disponible en [Беларуская](docs/be/DUAL_MODE_YAML.md) | [Deutsch](docs/de/DUAL_MODE_YAML.md) | [Español](docs/es/DUAL_MODE_YAML.md) | [Français](docs/fr/DUAL_MODE_YAML.md) | [Italiano](docs/it/DUAL_MODE_YAML.md) | [Nederlands](docs/nl/DUAL_MODE_YAML.md) | [Norsk](docs/no/DUAL_MODE_YAML.md) | [Русский](docs/ru/DUAL_MODE_YAML.md) | [Українська](docs/uk/DUAL_MODE_YAML.md))

## Changements majeurs dans la version 2.2.0

Lisez cette section avant de mettre à niveau à partir de la version 2.1.x.

> [!WARNING]
> Cette version modifie la propriété des appareils, la création des canaux, la
> sémantique des événements du panneau et le constructeur Python intégré. Complétez la liste de
> contrôle de mise à niveau avant de supprimer le YAML hérité.

1. **Les appareils spécifiques à l'installation ne sont plus intégrés à l'intégration.**
   Les adresses des appareils, les noms, les affectations de canaux et les nombres d'appareils
   appartiennent maintenant aux options d'entrée de configuration ou au registre d'appareils Home Assistant. Le
   catalogue d'appareils contient uniquement les capacités matérielles.

2. **Les modules relais gérés par l'interface utilisateur utilisent leur nombre de canaux physiques.**
   `HDL-MR1210.433` expose toujours 12 emplacements de canal et
   `HDL-MR1610.433` expose toujours 16. Un appareil existant ne peut pas être réduit
   en dessous du nombre de canaux physiques de son modèle.

3. **Un nom de canal vide désactive le canal.**
   Les canaux désactivés ne sont pas instanciés, ne créent pas d'objets de protocole et
   sont marqués comme désactivés par l'intégration dans le registre d'entités. Entrer un
   nom réactive le canal.

4. **Le modèle exact contrôle les entités générées.**
   Un `panneau HDL` générique n'a pas de nombre de boutons connu. Sélectionnez le modèle physique
   pour créer des événements de bouton. La modification d'un modèle recharge l'entrée de configuration.

5. **Home Assistant a sa propre adresse Buspro.**
   Les entrées de configuration existantes migrent vers `200.200`. Cette adresse doit être inutilisée sur
   le réseau Buspro et peut être modifiée sous **Configurer > Paramètres de la passerelle**.

6. **L'adresse IP source du paquet n'est plus codée en dur.**
   L'intégration la dérive de l'itinéraire vers la passerelle configurée. Un
   hôte Home Assistant multi-interface doit router la passerelle via l'interface
   LAN prévue.

7. **Les événements d'action du panneau sont maintenant décodés.**
   Les automatisations consommant d'anciennes valeurs d'action brutes doivent être vérifiées. Les événements utilisent
   `channel_on`, `channel_off`, `channel_level`, `scene`,
   `universal_switch_on` ou `universal_switch_off`, avec les attributs cible et
   résumé où ils peuvent être résolus.

8. **L'API Python intégrée a changé.**
   Les utilisateurs directs de `pybuspro.Buspro` doivent fournir `client_address` ; voir
   [pybuspro/README.md](pybuspro/README.md).

L'intégration lit toujours les entités YAML héritées pendant la migration. Ne gardez pas
le même canal physique dans la configuration YAML et gérée par l'interface utilisateur, car
cela peut créer des entités dupliquées et des souscriptions de protocole dupliquées.

## Liste de contrôle de mise à niveau

1. Redémarrez Home Assistant après remplacement du composant personnalisé.
2. Ouvrez **Paramètres > Appareils et services > HDL Buspro > Configurer**.
3. Vérifiez l'hôte de la passerelle, les ports et l'adresse Buspro Home Assistant inutilisée.
4. Ouvrez chaque appareil physique et sélectionnez son modèle exact.
5. Vérifiez le nom de chaque canal de relais. Les canaux vides restent intentionnellement désactivés.
6. Vérifiez les automatisations qui consomment les événements d'action du panneau.
7. Supprimez ou commentez les entités YAML migrées uniquement après que leurs
   remplaçants gérés par l'interface utilisateur aient conservé les ID d'entité attendus.

## Configuration de la passerelle

Ajoutez **HDL Buspro** à partir de **Paramètres > Appareils et services** et configurez :

- **Hôte** : nom d'hôte de la passerelle IP HDL ou adresse IPv4.
- **Port** : port UDP primaire, normalement `6000`.
- **Ports d'envoi/réception UDP** : ne modifiez ces paramètres que pour une passerelle non standard.
- **Adresse Buspro Home Assistant** : une identité `subnet.device` inutilisée, telle que
  la valeur par défaut de migration `200.200`.

UDP n'a pas de poignée de main de connexion. La configuration valide la résolution d'adresse, le routage
et la création du socket de réception local sans supposer qu'un appareil existe
à une adresse Buspro codée en dur.

## Gestion des appareils

Ouvrez **Configurer** sur l'intégration et choisissez :

- **Paramètres de la passerelle** pour mettre à jour les paramètres réseau et l'identité du client.
- **Ajouter un appareil** pour sélectionner un type d'appareil, un modèle, une adresse Buspro et des noms de canal ou de capacité.
- **Modifier l'appareil** pour renommer les canaux, activer ou désactiver les canaux, supprimer un
  appareil géré par l'interface utilisateur ou corriger le modèle d'un appareil de registre existant.

Les adresses physiques sont affichées dans Home Assistant en tant que numéro de série de l'appareil.
Les entités appartenant à un module physique sont attachées à la même
entrée du registre d'appareils.

## Modèles pris en charge

| Modèle | Support Home Assistant |
| --- | --- |
| `HDL-MBUS01IP.431` | Métadonnées de l'appareil de passerelle |
| `HDL-MCLog.431` | Connectivité, interrogation du firmware, dernière visualisation, événements logiques |
| `HDL-MR0410.431` | 4 canaux de relais |
| `HDL-MR0810.432` | 8 canaux de relais |
| `HDL-MR1210.433` | 12 canaux de relais |
| `HDL-MR1610.433` | 16 canaux de relais |
| `HDL-MR0416.431` | 4 canaux de relais haute puissance |
| `HDL-MR0416C.431` | 4 canaux de relais haute puissance |
| `HDL-MR0416D.431` | 4 canaux de relais haute puissance |
| `HDL-MR0816.432` | 8 canaux de relais haute puissance |
| `HDL-MR0816C.232` | 8 canaux de relais haute puissance |
| `HDL-MR0816D.432` | 8 canaux de relais haute puissance |
| `HDL-MR1216.433` | 12 canaux de relais haute puissance |
| `HDL-MR1616.434` | 16 canaux de relais haute puissance |
| `HDL-MR1216D.433` | 12 canaux de relais haute puissance |
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | Canaux de relais haute tension 4/8/12 |
| `HDL-MD0206.432` | 2 canaux de variateur |
| `HDL-MD0403.432` | 4 canaux de variateur |
| `HDL-MD0602.432` | 6 canaux de variateur |
| `HDL-MDT0203.433` | 2 canaux de variateur à coupure arrière |
| `HDL-MDT0203.532` | 2 canaux de variateur à coupure arrière |
| `HDL-MDT04015.433` | 4 canaux de variateur à coupure arrière |
| `HDL-MDT04015.532` | 4 canaux de variateur à coupure arrière |
| `HDL-MDT06015.433` | 6 canaux de variateur à coupure arrière |
| `HDL-MDT06015.533` | 6 canaux de variateur à coupure arrière |
| `HDL-MDLED0605.432` | 6 canaux de variateur et diagnostics |
| `HDL-MRDA0610.432` | 6 canaux de variateur avec contrôle de ballast |
| `HDL-MRDA0610.433` | 6 canaux de variateur avec contrôle de ballast |
| `SB-DN-DALI64` | Jusqu'à 64 canaux DALI |
| `HDL-MS04.432` | 4 canaux de contact sec |
| `HDL-MS24.232` | 24 canaux de contact sec |
| `HDL-MSP02.4C` | Température, illuminance, mouvement |
| `HDL-MSP07M.4C` | Température, illuminance, humidité, mouvement, deux contacts |
| `HDL-MS08M.4C` | Température, illuminance, mouvement |
| `HDL-MS12M.4C` | Température, illuminance, humidité, mouvement, deux contacts |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Température et actions du panneau |
| `HDL-MPTL4.460` | Température et actions du panneau |
| `HDL-MP4S/TILE.48` | Température, événements de quatre boutons, actions du panneau |
| `HDL-MP2B/TILE.48` | Température, événements de deux boutons, actions du panneau |
| `HDL-MP4B-A/TILE.48` | Température, événements de quatre boutons, actions du panneau |
| `HDL-MP4B/TILE.48` | Température, événements de quatre boutons, actions du panneau |
| `HDL-MP2B.480` | Température, événements de deux boutons, actions du panneau |
| `HDL-MP4B.480` | Température, événements de quatre boutons, actions du panneau |
| `HDL-MPL8.431` | Température, événements de huit boutons, actions du panneau |
| `HDL-M/PT4.1` | Température, événements de quatre boutons, actions du panneau |
| `HDL-MFH04.432` | 4 canaux de chauffage au sol |
| `HDL-MFH06.432` | 6 canaux de chauffage au sol |
| `HDL-M/HVAC8.1` | Entités climatiques AC |
| `HDL-MPED4.431` | Entités climatiques AC |
| `HDL-MW02.431` | 2 canaux de store/volet |
| `HDL-MWM45.431` | Entités de store/volet (canaux configurables) |

Les profils AC génériques, de store, de ventilateur à vitesse variable, de ventilateur marche/arrêt, de commutateur universel et
de panneau sont également disponibles. Leur adresse physique et tout nombre
de sorties configurables sont fournis par l'utilisateur ; ce ne sont pas des inventaires d'installation.

Certains modèles sont ajoutés via le mappage familial ou la compatibilité de protocole générique.
Au démarrage de l'intégration, Buspro enregistre des notes de support de modèle explicites pour ces
modèles (par exemple, comportement validé par modèle par rapport au mappage familial) ainsi que
les adresses physiques détectées.

Pour les appareils YAML hérités, l'intégration normalise maintenant les profils manquants en utilisant
les métadonnées du modèle de catalogue. Les modèles inconnus et les chaînes de profil non supportées sont
signalés comme avertissements au démarrage, puis reviennent au
comportement générique `sensor_status` pour garder la configuration fonctionnelle.

## Assistant de maintenance du catalogue

Pour comparer le catalogue d'intégration avec la liste de modèles HDL officielle maintenue,
exécutez :

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

L'assistant lit `custom_components/buspro/devices/official_models.json` et
affiche :

- modèles officiels manquants dans `DEVICE_CATALOG`
- modèles de catalogue non présents dans la liste officielle
- modèles génériques virtuels d'intégration uniquement

Utilisez le mode strict pour les vérifications de style CI (sortie non-zéro lorsque les modèles officiels sont
manquants dans le catalogue) :

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Comportement des entités

### Relais

Un coordinateur partagé interroge l'état du relais une fois par module physique et
distribue la réponse à toutes les entités de canal activées. Les canaux désactivés ne
s'abonnent pas et n'interrogent pas le bus.

### Panneaux

Les panneaux de bouton connus créent une entité `event` par bouton physique, un événement
`Action` et un capteur `Last action`. Les entités d'événement de bouton UI représentent
les télégrammes de bouton Buspro physiques reçus ; elles ne simulent pas une pression matérielle.

### Variateurs

Les variateurs supportés peuvent exposer la connectivité, la luminosité maximale par canal,
le type de charge et la luminosité minimale rapportée par le protocole. `Non rapporté` signifie que l'
appareil a renvoyé la sentinelle de protocole plutôt qu'une valeur utilisable.

### Contrôleur logique

`HDL-MCLog.431` expose la connectivité en lecture seule, la version du firmware, la dernière visualisation
et les entités d'événement logique. Certains firmwares ne répondent pas à la requête
de firmware standard ; dans ce cas, l'entité firmware reste indisponible. Les blocs logiques ne sont
pas modifiables car les modifier peut écraser la programmation du contrôleur.

## Services

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` envoie une commande de protocole brute et ne doit être utilisée que avec
un code d'opération HDL vérifié et une charge utile.

## Configuration YAML (hérité)

La configuration des appareils YAML est entièrement supportée aux côtés de la gestion des entrées de configuration de la passerelle. Vous pouvez définir des lumières, des stores, des commutateurs, des ventilateurs, des climatiques, des capteurs et des capteurs binaires via YAML tandis que la passerelle est gérée par l'interface utilisateur de l'intégration.

**Remarque** : Les nouveaux appareils doivent utiliser l'interface utilisateur **Configurer > Ajouter un appareil** de l'intégration au lieu de YAML, car elle fournit le regroupement d'appareils, les capacités basées sur le modèle et la gestion de l'état des canaux. YAML est recommandé pour :
- Appareils avec des profils non-standard ou hérités
- Migration à partir d'intégrations Buspro plus anciennes
- Modèles d'automatisation ou de capteur complexes

### Exemple de syntaxe YAML

Ajoutez à votre `configuration.yaml` :

```yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Ceiling light"
        dimmable: true
      "1.5.2":
        name: "Wall lamp"
        dimmable: false

cover:
  - platform: buspro
    devices:
      "2.10.1":
        name: "Living room curtain"
        running_time: 45

climate:
  - platform: buspro
    devices:
      "3.1":
        name: "Bedroom climate"
        profile: "ac"
```

### Configuration de la plateforme

Chaque plateforme (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`, `switch`) accepte :

| Clé | Type | Description |
| --- | --- | --- |
| `devices` | dict | Obligatoire. Mappage des adresses Buspro aux configurations d'appareils. |
| `running_time` | int | Temps de transition par défaut en secondes (0 = pas de transition). Remplacé par appareil. |
| `ack_retry_enabled` | bool | Relancer les envois sans ACK (par défaut de plateforme ; remplacements par appareil). |

Chaque clé d'appareil est l'**adresse Buspro** au format :
- **Lumière, store, ventilateur, commutateur** : `subnet.device.channel` (par exemple, `1.5.2`)
- **Climat, capteur, capteur binaire** : `subnet.device` (par exemple, `3.1`)

Chaque configuration d'appareil supporte :
- `name` (obligatoire) : Nom d'affichage
- `running_time`, `dimmable`, `ack_retry_enabled` (spécifique à la plateforme, optionnel)
- `profile` (optionnel, pour les capteurs climatiques — par exemple, `"ac"`, `"floor_heating"`)
- `object_id` (optionnel) : slug d'ID d'entité
- `unique_id` (optionnel) : Pour le contrôle manuel du registre d'entités

## Développement

### Exécuter les suites de tests

À partir de la racine de la configuration Home Assistant :

```bash
# Run all protocol tests (19 tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v

# Run all integration tests (18 tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v

# Or run individual test files
python3 custom_components/buspro/tests/buspro_protocol/test_sensor_protocol.py
python3 custom_components/buspro/tests/buspro_protocol/test_relay_coordinator.py
python3 custom_components/buspro/tests/buspro_protocol/test_logic_controller_protocol.py
python3 custom_components/buspro/tests/buspro_protocol/test_config_isolation.py
python3 custom_components/buspro/tests/buspro_protocol/test_device_lifecycle.py
python3 custom_components/buspro/tests/buspro_integration/test_device_catalog.py
python3 custom_components/buspro/tests/buspro_integration/test_managed_device_logic.py
python3 custom_components/buspro/tests/buspro_integration/test_model_notes_logging.py
python3 custom_components/buspro/tests/buspro_integration/test_yaml_normalization.py
```

Les tests de protocole couvrent l'analyse des télégrammes, la coordination des appareils et la sécurité des tâches/rappels de base. Les tests d'intégration couvrent le catalogue d'appareils, la logique des appareils gérés, la normalisation YAML et le suivi du support de modèle.
