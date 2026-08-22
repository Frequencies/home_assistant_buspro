# HDL Buspro pour Home Assistant

[English](../../README.md) | **Français**

L'intégration gère la passerelle et les appareils physiques HDL Buspro depuis
l'interface de Home Assistant. La liste complète des modèles, entités et
services est disponible dans la [documentation anglaise](../README.md).

> **Note importante**: Pour la configuration détaillée des appareils, les exemples YAML, les services disponibles et le guide de développement, consultez la [documentation en anglais](../README.md). Cette page fournit des informations d'installation et de configuration initiale.

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

### Configuration de la passerelle
1. Ouvrez **Paramètres > Appareils et services > Ajouter une intégration** et
   sélectionnez **HDL Buspro**.
2. Saisissez l'hôte de la passerelle et les ports UDP. Le port normal est `6000`.
3. Saisissez une adresse Buspro libre pour Home Assistant au format
   `sous-réseau.appareil`. La valeur par défaut est `200.200`; elle ne doit
   appartenir à aucun autre appareil Buspro.

### Ajouter des appareils
Après avoir complété la configuration de la passerelle :

1. Ouvrez **Paramètres > Appareils et services > HDL Buspro > Configurer**.
2. Sélectionnez **Ajouter un appareil** et choisissez le type (Relais, Gradateur, Ventilateur, Rideau, etc.).
3. Sélectionnez le modèle (ou **Générique** pour les modèles inconnus avec nombre de canaux).
4. Saisissez l'adresse Buspro, le nom de l'appareil et les noms des canaux (les noms vides désactivent les canaux).
5. Sélectionnez **Enregistrer**.

Home Assistant regroupe automatiquement toutes les entités sous une seule entrée du registre.

**Pour des exemples détaillés de configuration UI et YAML pour tous les types d'appareils, voir [../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md).**

### Modifier les appareils

Pour modifier un appareil existant, ouvrez **Configurer > Modifier l'appareil**.
Vous pouvez :
- Renommer l'appareil
- Renommer, activer ou désactiver les canaux individuels
- Modifier le modèle (peut changer le nombre de canaux)
- Supprimer l'appareil entièrement

Les appareils gérés par l'interface supportent la modification complète. Les
appareils YAML hérités peuvent exposer les contrôles de nommage du registre,
mais leur configuration protocolaire doit toujours être modifiée dans YAML.
Redémarrez Home Assistant après les modifications YAML.

### Exemple : Ajouter un module relais 4 canaux

1. Modèle : `HDL-MR0410.431` (4 canaux relais)
2. Adresse Buspro : `1.10`
3. Nom de l'appareil : "Relais du salon"
4. Noms des canaux :
   - Canal 1 : "Lumière du plafond"
   - Canal 2 : "Lampe murale"
   - Canal 3 : "" (désactivé)
   - Canal 4 : "Ventilateur"

Après l'enregistrement, Home Assistant crée :
- `light.room_relays_ceiling_light`
- `light.room_relays_wall_lamp`
- `switch.room_relays_fan`

Pour des exemples complets d'interface utilisateur et YAML pour tous les types d'appareils, consultez **[../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md)**.

## Options de configuration

L'intégration buspro prend en charge à la fois **la configuration par interface utilisateur** et **la configuration YAML** :

### Configuration par interface utilisateur
Le moyen le plus facile d'ajouter des appareils — consultez **[../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md)** pour des exemples étape par étape de tous les types d'appareils.

### Configuration YAML  
L'intégration prend en charge deux approches YAML complémentaires :
- **Basée sur les entités** (Legacy) — fichiers d'entités individuels, organisés par domaines
- **Basée sur les appareils** (Modern) — définitions complètes d'appareils avec tous les canaux

**Pour la documentation YAML complète, les exemples et les meilleures pratiques, consultez [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md)** (également disponible en [English](../en/DUAL_MODE_YAML.md) | [Беларуская](../en/DUAL_MODE_YAML.md) | [Deutsch](../en/DUAL_MODE_YAML.md) | [Español](../en/DUAL_MODE_YAML.md) | [Italiano](../en/DUAL_MODE_YAML.md) | [Nederlands](../en/DUAL_MODE_YAML.md) | [Norsk](../en/DUAL_MODE_YAML.md) | [Русский](../en/DUAL_MODE_YAML.md) | [Українська](../en/DUAL_MODE_YAML.md))

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

## Configuration YAML (hérité)

La configuration YAML des appareils est entièrement compatible avec la gestion
de la passerelle par entrée de configuration. Vous pouvez définir des lumières,
rideaux, interrupteurs, ventilateurs, climatisation, capteurs et capteurs binaires
via YAML tandis que la passerelle est gérée par l'interface de l'intégration.

**Remarque** : Les nouveaux appareils doivent utiliser l'interface
**Configurer > Ajouter un appareil** au lieu de YAML, car elle fournit le
regroupement des appareils, les capacités contrôlées par le modèle et la gestion
d'état des canaux. YAML est recommandé pour :
- Les appareils avec des profils non standard ou hérités
- La migration depuis des intégrations Buspro plus anciennes
- Les automatisations complexes ou les modèles de capteurs

### Exemple de syntaxe YAML

Ajoutez à votre `configuration.yaml` :

```yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Lumière du plafond"
        dimmable: true
      "1.5.2":
        name: "Lampe murale"
        dimmable: false

cover:
  - platform: buspro
    devices:
      "2.10.1":
        name: "Rideau du salon"
        running_time: 45

climate:
  - platform: buspro
    devices:
      "3.1":
        name: "Climatisation de la chambre"
        profile: "ac"
```

### Configuration de la plateforme

Chaque plateforme (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`,
`switch`) accepte :

| Clé | Type | Description |
| --- | --- | --- |
| `devices` | dict | Requis. Mappage des adresses Buspro aux configurations d'appareils. |
| `running_time` | int | Temps de transition par défaut en secondes (0 = pas de transition). Remplacé par appareil. |
| `ack_retry_enabled` | bool | Réessayer les envois sans ACK (par défaut de la plateforme ; remplacé par appareil). |

Chaque clé d'appareil est l'**adresse Buspro** au format :
- **Lumière, rideau, ventilateur, interrupteur** : `sous-réseau.appareil.canal` (p. ex., `1.5.2`)
- **Climatisation, capteur, capteur binaire** : `sous-réseau.appareil` (p. ex., `3.1`)

Chaque configuration d'appareil prend en charge :
- `name` (requis) : Nom d'affichage
- `running_time`, `dimmable`, `ack_retry_enabled` (spécifique à la plateforme, optionnel)
- `profile` (optionnel, pour les capteurs climatiques — p. ex., `"ac"`, `"floor_heating"`)
- `object_id` (optionnel) : Slug ID d'entité
- `unique_id` (optionnel) : Pour le contrôle manuel du registre des entités

## Configuration de la passerelle

Ajoutez **HDL Buspro** à partir de **Paramètres > Appareils et services** et configurez :

- **Hôte** : nom d'hôte ou adresse IPv4 de la passerelle HDL.
- **Port** : port UDP principal, généralement `6000`.
- **Ports d'envoi/réception UDP** : modifiez-les uniquement pour une passerelle non standard.
- **Adresse Buspro Home Assistant** : une identité `subnet.device` inutilisée, comme la migration par défaut `200.200`.

UDP n'a pas d'établissement de connexion. La configuration valide la résolution d'adresse, le routage et la création du socket de réception local sans supposer qu'un périphérique existe à une adresse Buspro codée en dur.

## Gestion des appareils

Ouvrez **Configurer** sur l'intégration et choisissez :

- **Paramètres de passerelle** pour mettre à jour les paramètres réseau et l'identité du client.
- **Ajouter un appareil** pour sélectionner un type d'appareil, un modèle, une adresse Buspro et des noms de canaux ou de capacités.
- **Modifier l'appareil** pour renommer les canaux, activer ou désactiver les canaux, supprimer un appareil géré par l'interface utilisateur ou corriger le modèle d'une entrée de registre existante.

Les adresses physiques sont affichées dans Home Assistant comme le numéro de série de l'appareil. Les entités appartenant à un module physique sont attachées à une seule entrée du registre des appareils.

## Modèles pris en charge

| Modèle | Prise en charge de Home Assistant |
| --- | --- |
| `HDL-MBUS01IP.431` | Métadonnées de l'appareil passerelle |
| `HDL-MCLog.431` | Connectivité, requête de micrologiciel, dernière visite, événements logiques |
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
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | 4/8/12 canaux de relais haute courant |
| `HDL-MD0206.432` | 2 canaux de variateur |
| `HDL-MD0403.432` | 4 canaux de variateur |
| `HDL-MD0602.432` | 6 canaux de variateur |
| `HDL-MDT0203.433` | 2 canaux de variateur à bord de fuite |
| `HDL-MDT0203.532` | 2 canaux de variateur à bord de fuite |
| `HDL-MDT04015.433` | 4 canaux de variateur à bord de fuite |
| `HDL-MDT04015.532` | 4 canaux de variateur à bord de fuite |
| `HDL-MDT06015.433` | 6 canaux de variateur à bord de fuite |
| `HDL-MDT06015.533` | 6 canaux de variateur à bord de fuite |
| `HDL-MDLED0605.432` | 6 canaux de variateur et diagnostics |
| `HDL-MRDA0610.432` | 6 canaux de variateur de contrôle de ballast |
| `HDL-MRDA0610.433` | 6 canaux de variateur de contrôle de ballast |
| `SB-DN-DALI64` | Jusqu'à 64 canaux DALI |
| `HDL-MS04.432` | 4 canaux de contact sec |
| `HDL-MS24.232` | 24 canaux de contact sec |
| `HDL-MSP02.4C` | Température, éclairement, mouvement |
| `HDL-MSP07M.4C` | Température, éclairement, humidité, mouvement, deux contacts |
| `HDL-MS08M.4C` | Température, éclairement, mouvement |
| `HDL-MS12M.4C` | Température, éclairement, humidité, mouvement, deux contacts |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Température et actions de panneau |
| `HDL-MPTL4.460` | Température et actions de panneau |
| `HDL-MP4S/TILE.48` | Température, quatre événements de bouton, actions de panneau |
| `HDL-MP2B/TILE.48` | Température, deux événements de bouton, actions de panneau |
| `HDL-MP4B-A/TILE.48` | Température, quatre événements de bouton, actions de panneau |
| `HDL-MP4B/TILE.48` | Température, quatre événements de bouton, actions de panneau |
| `HDL-MP2B.480` | Température, deux événements de bouton, actions de panneau |
| `HDL-MP4B.480` | Température, quatre événements de bouton, actions de panneau |
| `HDL-MPL8.431` | Température, huit événements de bouton, actions de panneau |
| `HDL-M/PT4.1` | Température, quatre événements de bouton, actions de panneau |
| `HDL-MFH04.432` | 4 canaux de chauffage au sol |
| `HDL-MFH06.432` | 6 canaux de chauffage au sol |
| `HDL-M/HVAC8.1` | Entités climatiques CA |
| `HDL-MPED4.431` | Entités climatiques CA |
| `HDL-MW02.431` | 2 canaux de rideau / couverture |
| `HDL-MWM45.431` | Entités de rideau / couverture (canaux configurables) |

Les profils génériques AC, rideau, ventilateur à vitesse variable, ventilateur marche/arrêt, commutateur universel et panneau sont également disponibles. Leur adresse physique et tout nombre de sorties configurable sont fournis par l'utilisateur ; ce n'est pas l'inventaire d'installation.

Certains modèles sont ajoutés via mappage de famille ou compatibilité de protocole générique. Lors du démarrage de l'intégration, Buspro enregistre des notes de support de modèle explicites pour ces modèles (par exemple, comportement validé par le modèle par rapport au comportement mappé par la famille) avec les adresses physiques détectées.

Pour les appareils YAML hérités, l'intégration normalise maintenant les profils manquants à l'aide des métadonnées du catalogue de modèles. Les modèles inconnus et les chaînes de profil non prises en charge sont signalés comme des avertissements au démarrage, puis reviennent au comportement générique `sensor_status` pour maintenir la fonctionnalité de la configuration.

## Assistant de maintenance du catalogue

Pour comparer le catalogue d'intégration avec la liste de modèles HDL officielle entretenue, exécutez :

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

L'assistant lit `custom_components/buspro/devices/official_models.json` et imprime :

- modèles officiels manquant dans `DEVICE_CATALOG`
- modèles de catalogue ne figurant pas dans la liste officielle
- modèles génériques virtuels intégrés uniquement

Utilisez le mode strict pour les vérifications de style CI (sortie non nulle lorsque les modèles officiels manquent du catalogue) :

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Comportement des entités

### Relais

Un coordinateur partagé interroge l'état du relais une fois par module physique et distribue la réponse à toutes les entités de canal activées. Les canaux désactivés ne s'abonnent pas et ne consultent pas le bus.

### Panneaux

Les panneaux de boutons connus créent une entité `event` par bouton physique, un événement `Action` et un capteur `Last action`. Les entités d'événements de bouton de l'interface utilisateur représentent les télégrammes de boutons Buspro physiques reçus ; elles ne simulent pas une pression matérielle.

### Variateurs

Les variateurs pris en charge peuvent exposer la connectivité, la luminosité maximale par canal, le type de charge et la luminosité minimale signalée par le protocole. `Not reported` signifie que l'appareil a renvoyé la sentinelle du protocole plutôt qu'une valeur utilisable.

### Contrôleur logique

`HDL-MCLog.431` expose une connectivité en lecture seule, la version du micrologiciel, la dernière visite et les entités d'événements logiques. Certains micrologiciels ne répondent pas à la requête standard de micrologiciel ; dans ce cas, l'entité du micrologiciel reste indisponible. Les blocs logiques ne sont pas inscriptibles car leur modification peut remplacer la programmation du contrôleur.

## Services

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` envoie une commande de protocole brute et ne doit être utilisé qu'avec un code d'opération HDL et une charge utile vérifiés.

## Développement

### Exécuter les suites de tests

Depuis le répertoire de configuration de Home Assistant :

```bash
# Exécuter tous les tests de protocole (19 tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v

# Exécuter tous les tests d'intégration (18 tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v

# Ou exécuter des fichiers de test individuels
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

Les tests de protocole couvrent l'analyse des télégrammes, la coordination des
appareils et la sécurité des tâches/rappels principaux. Les tests d'intégration
couvrent le catalogue des appareils, la logique des appareils gérés, la
normalisation YAML et le suivi du support des modèles.
