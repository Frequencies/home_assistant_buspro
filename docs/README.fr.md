# HDL Buspro pour Home Assistant

[English](../README.md) | **Français**

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
2. Sélectionnez **Ajouter un appareil** pour ajouter un module Buspro physique.
3. **Sélectionnez le type d'appareil** : choisissez la capacité (Relais,
   Gradateur, Ventilateur, Rideau, Capteur multi, etc.).
4. **Sélectionnez le modèle exact** : choisissez le modèle correspondant à votre
   matériel. Cela détermine le nombre de canaux.
   - Pour les modèles inconnus, choisissez le profil **Générique** et spécifiez le nombre de canaux.
5. **Saisissez l'adresse Buspro** : l'adresse physique sous-réseau.appareil du
   module (p. ex., `1.5`).
6. **Saisissez le nom de l'appareil** : un nom d'affichage (p. ex.,
   "Lumières du salon").
7. **Nommez chaque canal** : attribuez un nom à chaque canal ou capacité que vous
   souhaitez utiliser.
   - Exemple : pour un relais 4 canaux, nommez les canaux "Lumière du plafond",
     "Lampe de table", etc.
   - **Laissez un nom vide pour désactiver ce canal** — aucune entité ne sera créée.
8. Sélectionnez **Enregistrer** pour créer l'appareil et ses entités.

Home Assistant regroupe automatiquement toutes les entités d'un module physique
sous une seule entrée du registre des appareils et recharge l'entrée de
configuration.

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
