# Exemples de configuration d'appareils HDL Buspro
[🇧🇾 Беларуская](../be/DEVICE_EXAMPLES.md) | [🇩🇪 Deutsch](../de/DEVICE_EXAMPLES.md) | [🇬🇧 English](../en/DEVICE_EXAMPLES.md) | [🇪🇸 Español](../es/DEVICE_EXAMPLES.md) | 🇫🇷 Français | [🇮🇹 Italiano](../it/DEVICE_EXAMPLES.md) | [🇳🇱 Nederlands](../nl/DEVICE_EXAMPLES.md) | [🇳🇴 Norsk](../no/DEVICE_EXAMPLES.md) | [🇷🇺 Русский](../ru/DEVICE_EXAMPLES.md) | [🇺🇦 Українська](../uk/DEVICE_EXAMPLES.md)

---

Ce guide fournit des exemples de configuration pratiques via l'interface utilisateur et YAML pour tous les types d'appareils pris en charge dans l'intégration HDL Buspro.

**Table des matières :**
- [Confirmation de Commande (NOUVEAU!)](#confirmation-de-commande-nouveau)
- [Appareils à relais](#appareils-à-relais)
- [Appareils gradateurs](#appareils-gradateurs)
- [Appareils de couverture (stores/volets)](#appareils-de-couverture)
- [Appareils ventilateurs](#appareils-ventilateurs)
- [Appareils climatiques](#appareils-climatiques)
- [Appareils capteurs](#appareils-capteurs)
- [Appareils capteurs binaires](#appareils-capteurs-binaires)

---

## Confirmation de Commande (NOUVEAU!)

### Qu'est-ce que la Confirmation de Commande?

La confirmation de commande garantit que les changements d'état des appareils ne sont reflétés dans Home Assistant qu'après que l'appareil physique confirme la réception et l'exécution de la commande. Cela prévient la désynchronisation de l'interface utilisateur lorsque des commandes sont perdues en raison d'interférences réseau.

**Sans Confirmation:**
- L'utilisateur clique sur "Activer"
- L'interface se met à jour immédiatement (~5ms)
- L'appareil reçoit la commande après ~100ms
- Si l'appareil ne reçoit pas → L'interface affiche un état incorrect

**Avec Confirmation:**
- L'utilisateur clique sur "Activer"
- Le système attend la confirmation de l'appareil (~100-500ms)
- L'appareil confirme la réception et l'exécution
- L'interface se met à jour uniquement après la confirmation
- Si l'appareil ne répond pas → Erreur de délai d'attente explicite

### Pourquoi en avez-vous besoin

Activez la confirmation pour:
- **Appareils critiques** - Relais d'urgence, disjoncteurs principaux
- **Réseaux peu fiables** - Interférences élevées, nombreuses collisions
- **Dépendances d'automatisation** - Automatisations nécessitant un état garanti
- **Appareils critiques pour la sécurité** - Systèmes CVAC, chauffage au sol

### Exemples de Configuration

#### Pour un Relais Critique

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.10.1":
        name: "Relais d'Arrêt d'Urgence"
        enable_confirmation: true
        confirmation_timeout: 5.0
        confirmation_retries: 3
```

#### Pour Plusieurs Appareils Critiques

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      # Critique - confirmer la réception
      "1.10.1":
        name: "Plafonnier Principal"
        enable_confirmation: true
      
      # Non critique - garder rapide (par défaut)
      "1.10.2":
        name: "Éclairage Ambiant"
        # enable_confirmation est false par défaut

cover:
  - platform: buspro
    devices:
      "2.10.1":
        name: "Rideaux de la Chambre"
        enable_confirmation: true
        confirmation_timeout: 10.0  # Plus long pour appareils mécaniques
        confirmation_retries: 2

climate:
  - platform: buspro
    devices:
      - address: "3.1"
        name: "Climatisation du Salon"
        enable_confirmation: true
        confirmation_timeout: 5.0
        confirmation_retries: 3
```

### Paramètres de Configuration

| Paramètre | Type | Défaut | Plage | Objectif |
|-----------|------|---------|-------|---------| 
| `enable_confirmation` | boolean | `false` | `true`/`false` | Activer/désactiver la confirmation |
| `confirmation_timeout` | float | `5.0` | 0.1-60 secondes | Attente maximale pour réponse appareil |
| `confirmation_retries` | integer | `3` | 0-10 | Tentatives de réessai à l'expiration |

### Recommandations par Type d'Appareil

| Type d'Appareil | Délai | Tentatives | Remarques |
|------------|---------|---------|-------|
| Relais/Interrupteur | 5.0s | 3 | Appareil électronique rapide |
| Lumière/Variateur | 5.0s | 3 | Appareil électronique rapide |
| Ventilateur | 5.0s | 3 | Appareil électronique rapide |
| Volet/Rideau | 10.0s | 2 | Appareil mécanique, plus lent |
| Climatisation AC | 5.0s | 3 | Appareil électronique |
| Chauffage au Sol | 5.0s | 3 | Appareil électronique |

### Impact sur l'Interface Utilisateur

Lorsque la confirmation est activée:
- **Latence:** Délai de 100-500ms (vs. 5-10ms sans)
- **Retour d'information:** Indication claire de succès/échec
- **Fiabilité:** Synchronisation d'état garantie

Lorsque la confirmation est désactivée (par défaut):
- **Latence:** ~5-10ms (inchangé)
- **Comportement:** Fire-and-forget (comportement actuel)
- **Risque:** Défaillances silencieuses de commandes possibles

---

## Appareils à relais

Les appareils à relais sont des interrupteurs simples marche/arrêt utilisés pour l'éclairage, les ventilateurs et autres charges binaires.

**Modèles pris en charge :**
- `HDL-MR0410.431` - 4 canaux de relais
- `HDL-MR0810.432` - 8 canaux de relais
- `HDL-MR1210.433` - 12 canaux de relais
- `HDL-MR1610.433` - 16 canaux de relais
- Variantes de relais haute puissance HDL (MR0416, MR0816, MR1216, MR1616, MR0420C, etc.)

### Exemple de configuration de l'interface utilisateur

**Étapes :**
1. Allez à **Paramètres > Appareils et services > HDL Buspro > Configurer**
2. Cliquez sur **Ajouter un appareil**
3. Sélectionnez le type d'appareil : **Relais**
4. Sélectionnez le modèle exact : **HDL-MR0410.431** (4 canaux)
5. Entrez l'adresse Buspro : `1.10`
6. Entrez le nom de l'appareil : "Lumières du salon"
7. Nommez les canaux :
   - Canal 1 : "Plafonnier"
   - Canal 2 : "Lampe de table"
   - Canal 3 : "Applique murale"
   - Canal 4 : "" (laissez vide pour désactiver)
8. Cliquez sur **Enregistrer**

**Résultat :**
- `light.lumières_du_salon_plafonnier`
- `light.lumières_du_salon_lampe_de_table`
- `light.lumières_du_salon_applique_murale`

### Exemple de configuration YAML

**Centré sur les entités (fichiers individuels) :**

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.10.1":
        name: "Living Room Ceiling Light"
        object_id: "ceiling_light"
      "1.10.2":
        name: "Living Room Table Lamp"
        object_id: "table_lamp"
      "1.10.3":
        name: "Living Room Wall Sconce"
        object_id: "wall_sconce"
```

**Centré sur l'appareil (définition complète de l'appareil) :**

```yaml
# configuration.yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 200.200
  devices:
    - address: "1.10"
      name: "Living Room Relays"
      model: "HDL-MR0410.431"
      device_type: "relay"
      channels:
        - number: 1
          name: "Ceiling Light"
          enabled: true
          object_id: "hdl_light_ceiling"
        - number: 2
          name: "Table Lamp"
          enabled: true
          object_id: "hdl_light_table"
        - number: 3
          name: "Wall Sconce"
          enabled: true
          object_id: "hdl_light_sconce"
        - number: 4
          enabled: false
```

---

## Appareils gradateurs

Les appareils gradateurs contrôlent les niveaux de luminosité (0-255) pour les lumières graduables.

**Modèles pris en charge :**
- `HDL-MD0206.432` - 2 canaux gradateur
- `HDL-MD0403.432` - 4 canaux gradateur
- `HDL-MD0602.432` - 6 canaux gradateur
- Gradateurs de queue arrière HDL (MDT0203, MDT04015, MDT06015, etc.)
- `HDL-MDLED0605.432` - 6 canaux gradateur avec diagnostics

### Exemple de configuration de l'interface utilisateur

**Étapes :**
1. Allez à **Paramètres > Appareils et services > HDL Buspro > Configurer**
2. Cliquez sur **Ajouter un appareil**
3. Sélectionnez le type d'appareil : **Gradateur**
4. Sélectionnez le modèle exact : **HDL-MD0602.432** (6 canaux)
5. Entrez l'adresse Buspro : `1.5`
6. Entrez le nom de l'appareil : "Gradateurs de chambre"
7. Nommez les canaux :
   - Canal 1 : "Lumière principale"
   - Canal 2 : "Lampe de chevet gauche"
   - Canal 3 : "Lampe de chevet droite"
   - Canaux 4-6 : laissez vides
8. Cliquez sur **Enregistrer**

**Résultat :**
- `light.gradateurs_de_chambre_lumière_principale` (graduable 0-255)
- `light.gradateurs_de_chambre_lampe_de_chevet_gauche` (graduable 0-255)
- `light.gradateurs_de_chambre_lampe_de_chevet_droite` (graduable 0-255)

### Exemple de configuration YAML

**Centré sur les entités :**

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Bedroom Main Light"
        dimmable: true
      "1.5.2":
        name: "Bedroom Bedside Left"
        dimmable: true
      "1.5.3":
        name: "Bedroom Bedside Right"
        dimmable: true
```

**Centré sur l'appareil :**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "1.5"
      name: "Bedroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
          object_id: "hdl_dimmer_main"
        - number: 2
          name: "Bedside Left"
          enabled: true
          object_id: "hdl_dimmer_left"
        - number: 3
          name: "Bedside Right"
          enabled: true
          object_id: "hdl_dimmer_right"
        - number: 4
          enabled: false
        - number: 5
          enabled: false
        - number: 6
          enabled: false
```

---

## Appareils de couverture

Les appareils de couverture contrôlent les stores motorisés, volets et rideaux.

**Modèles pris en charge :**
- `HDL-MW02.431` - 2 canaux de rideau/couverture
- `HDL-MWM45.431` - Entités de rideau/couverture (canaux configurables)

### Exemple de configuration de l'interface utilisateur

**Étapes :**
1. Allez à **Paramètres > Appareils et services > HDL Buspro > Configurer**
2. Cliquez sur **Ajouter un appareil**
3. Sélectionnez le type d'appareil : **Couverture**
4. Sélectionnez le modèle exact : **HDL-MW02.431** (2 canaux)
5. Entrez l'adresse Buspro : `2.10`
6. Entrez le nom de l'appareil : "Stores du salon"
7. Nommez les canaux :
   - Canal 1 : "Fenêtres"
   - Canal 2 : "Porte patio"
8. Cliquez sur **Enregistrer**

**Résultat :**
- `cover.stores_du_salon_fenêtres`
- `cover.stores_du_salon_porte_patio`

### Exemple de configuration YAML

**Centré sur l'appareil :**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "2.10"
      name: "Living Room Blinds"
      model: "HDL-MW02.431"
      device_type: "cover"
      channels:
        - number: 1
          name: "Windows"
          enabled: true
          object_id: "hdl_cover_windows"
        - number: 2
          name: "Patio Door"
          enabled: true
          object_id: "hdl_cover_patio"
```

---

## Appareils ventilateurs

Les appareils ventilateurs contrôlent les ventilateurs à vitesse variable.

**Modèles pris en charge :**
- Profil ventilateur générique (ventilateurs à vitesse variable)

### Exemple de configuration de l'interface utilisateur

**Étapes :**
1. Allez à **Paramètres > Appareils et services > HDL Buspro > Configurer**
2. Cliquez sur **Ajouter un appareil**
3. Sélectionnez le type d'appareil : **Ventilateur**
4. Sélectionnez le modèle exact : **Générique** (spécifiez le nombre de canaux)
5. Entrez l'adresse Buspro : `3.5`
6. Entrez le nom de l'appareil : "Ventilateur d'extraction de salle de bain"
7. Nommez le canal : "Ventilateur principal"
8. Cliquez sur **Enregistrer**

**Résultat :**
- `fan.ventilateur_d'extraction_de_salle_de_bain_ventilateur_principal` (contrôle de vitesse 0-255)

### Exemple de configuration YAML

**Centré sur l'appareil :**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "3.5"
      name: "Bathroom Exhaust Fan"
      device_type: "fan"
      channels:
        - number: 1
          name: "Main Fan"
          enabled: true
          object_id: "hdl_fan_exhaust"
```

---

## Appareils climatiques

Les appareils climatiques contrôlent la température et les systèmes HVAC.

**Modèles pris en charge :**
- `HDL-MFH04.432` - 4 canaux de chauffage par le sol
- `HDL-MFH06.432` - 6 canaux de chauffage par le sol
- `HDL-M/HVAC8.1` - Contrôle climatique CA
- `HDL-MPED4.431` - Contrôle climatique CA
- Profil CA générique
- Profil de chauffage par le sol générique

### Exemple de configuration de l'interface utilisateur - Unité CA

**Étapes :**
1. Allez à **Paramètres > Appareils et services > HDL Buspro > Configurer**
2. Cliquez sur **Ajouter un appareil**
3. Sélectionnez le type d'appareil : **Climat**
4. Sélectionnez le modèle exact : **HDL-M/HVAC8.1** (CA)
5. Entrez l'adresse Buspro : `3.1`
6. Entrez le nom de l'appareil : "Climatisation du salon"
7. Cliquez sur **Enregistrer**

**Résultat :**
- `climate.climatisation_du_salon` (température cible, mode, contrôle d'alimentation)

### Exemple de configuration YAML

**Centré sur l'appareil :**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "3.1"
      name: "Living Room AC"
      model: "HDL-M/HVAC8.1"
      device_type: "ac"
      object_id: "hdl_climate_ac"

    - address: "4.2"
      name: "Master Bedroom Floor Heating"
      model: "HDL-MFH06.432"
      device_type: "floor_heating"
      channels:
        - number: 1
          name: "Zone 1"
          enabled: true
        - number: 2
          name: "Zone 2"
          enabled: true
        - number: 3
          enabled: false
```

---

## Appareils capteurs

Les appareils capteurs fournissent des données de température, humidité, illuminance et mouvement.

**Modèles pris en charge :**
- `HDL-MSP02.4C` - Température, illuminance, mouvement
- `HDL-MSP07M.4C` - Température, illuminance, humidité, mouvement, 2 contacts
- `HDL-MS08M.4C` - Température, illuminance, mouvement
- `HDL-MS12M.4C` - Température, illuminance, humidité, mouvement, 2 contacts
- `HDL-MCLog.431` - Contrôleur logique (lecture seule)
- Capteurs de température de panneau (MPTL, MP2B, MP4B, MPL8, etc.)

### Exemple de configuration de l'interface utilisateur

**Étapes :**
1. Allez à **Paramètres > Appareils et services > HDL Buspro > Configurer**
2. Cliquez sur **Ajouter un appareil**
3. Sélectionnez le type d'appareil : **Capteur multiple**
4. Sélectionnez le modèle exact : **HDL-MSP07M.4C**
5. Entrez l'adresse Buspro : `2.5`
6. Entrez le nom de l'appareil : "Capteur du salon"
7. Cliquez sur **Enregistrer**

**Résultat :**
- `sensor.capteur_du_salon_température`
- `sensor.capteur_du_salon_illuminance`
- `sensor.capteur_du_salon_humidité`
- `binary_sensor.capteur_du_salon_mouvement`
- 2 contacts secs supplémentaires

### Exemple de configuration YAML

**Centré sur les entités :**

```yaml
# configuration.yaml
sensor:
  - platform: buspro
    devices:
      "2.5":
        name: "Living Room Sensor"
        model: "HDL-MSP07M.4C"
        profile: "12in1"
        entities:
          - type: temperature
            name: "Temperature"
            object_id: "hdl_temp_living_room"
          - type: illuminance
            name: "Light Level"
            object_id: "hdl_lux_living_room"
          - type: humidity
            name: "Humidity"
            object_id: "hdl_humidity_living_room"

binary_sensor:
  - platform: buspro
    devices:
      "2.5":
        name: "Living Room Sensor"
        model: "HDL-MSP07M.4C"
        profile: "12in1"
        entities:
          - type: motion
            name: "Motion"
            object_id: "hdl_motion_living_room"
          - type: dry_contact
            number: 1
            name: "Door Contact"
            object_id: "hdl_door_living_room"
          - type: dry_contact
            number: 2
            name: "Window Contact"
            object_id: "hdl_window_living_room"
```

**Centré sur l'appareil :**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "2.5"
      name: "Living Room Sensor"
      model: "HDL-MSP07M.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Temperature"
          object_id: "hdl_temp_living_room"
        - type: illuminance
          name: "Illuminance"
          object_id: "hdl_lux_living_room"
        - type: humidity
          name: "Humidity"
          object_id: "hdl_humidity_living_room"
        - type: motion
          name: "Motion"
          object_id: "hdl_motion_living_room"
        - type: dry_contact
          number: 1
          name: "Door Contact"
          object_id: "hdl_door_contact"
        - type: dry_contact
          number: 2
          name: "Window Contact"
          object_id: "hdl_window_contact"
```

---

## Appareils capteurs binaires

Les appareils capteurs binaires fournissent le statut marche/arrêt des contacts secs et des capteurs de porte/fenêtre.

**Modèles pris en charge :**
- `HDL-MS04.432` - 4 canaux de contact sec
- `HDL-MS24.232` - 24 canaux de contact sec
- Capteurs multiples avec contacts intégrés (MSP07M, MS12M, etc.)

### Exemple de configuration de l'interface utilisateur

**Étapes :**
1. Allez à **Paramètres > Appareils et services > HDL Buspro > Configurer**
2. Cliquez sur **Ajouter un appareil**
3. Sélectionnez le type d'appareil : **Contact sec**
4. Sélectionnez le modèle exact : **HDL-MS04.432** (4 canaux)
5. Entrez l'adresse Buspro : `1.20`
6. Entrez le nom de l'appareil : "Capteurs de porte et de fenêtre"
7. Nommez les canaux :
   - Canal 1 : "Porte d'entrée"
   - Canal 2 : "Porte de garage"
   - Canal 3 : "Fenêtre du salon"
   - Canal 4 : laissez vide
8. Cliquez sur **Enregistrer**

**Résultat :**
- `binary_sensor.capteurs_de_porte_et_de_fenêtre_porte_d'entrée`
- `binary_sensor.capteurs_de_porte_et_de_fenêtre_porte_de_garage`
- `binary_sensor.capteurs_de_porte_et_de_fenêtre_fenêtre_du_salon`

### Exemple de configuration YAML

**Centré sur l'appareil :**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "1.20"
      name: "Door & Window Sensors"
      model: "HDL-MS04.432"
      device_type: "dry_contact"
      channels:
        - number: 1
          name: "Front Door"
          enabled: true
          object_id: "hdl_door_front"
        - number: 2
          name: "Garage Door"
          enabled: true
          object_id: "hdl_door_garage"
        - number: 3
          name: "Living Room Window"
          enabled: true
          object_id: "hdl_window_living_room"
        - number: 4
          enabled: false
```

---

## Exemple complexe multi-appareils

Voici un fichier de configuration complet montrant plusieurs types d'appareils fonctionnant ensemble :

```yaml
# configuration.yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 200.200
  devices:
    # Relay devices
    - address: "1.10"
      name: "Living Room Lights"
      model: "HDL-MR0410.431"
      device_type: "relay"
      channels:
        - number: 1
          name: "Ceiling Light"
          enabled: true
        - number: 2
          name: "Table Lamp"
          enabled: true
        - number: 3
          name: "Wall Sconce"
          enabled: true
        - number: 4
          enabled: false

    # Dimmer devices
    - address: "1.5"
      name: "Bedroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
        - number: 2
          name: "Bedside Left"
          enabled: true
        - number: 3
          name: "Bedside Right"
          enabled: true
        - number: 4
          enabled: false
        - number: 5
          enabled: false
        - number: 6
          enabled: false

    # Cover devices (blinds)
    - address: "2.10"
      name: "Blinds"
      model: "HDL-MW02.431"
      device_type: "cover"
      channels:
        - number: 1
          name: "Living Room"
          enabled: true
        - number: 2
          name: "Patio"
          enabled: true

    # Climate
    - address: "3.1"
      name: "AC Unit"
      model: "HDL-M/HVAC8.1"
      device_type: "ac"

    # Sensors
    - address: "2.5"
      name: "Living Room Sensor"
      model: "HDL-MSP07M.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Temperature"
        - type: illuminance
          name: "Illuminance"
        - type: humidity
          name: "Humidity"
        - type: motion
          name: "Motion"
        - type: dry_contact
          number: 1
          name: "Door"
        - type: dry_contact
          number: 2
          name: "Window"

    # Dry contacts
    - address: "1.20"
      name: "Door Sensors"
      model: "HDL-MS04.432"
      device_type: "dry_contact"
      channels:
        - number: 1
          name: "Front Door"
          enabled: true
        - number: 2
          name: "Garage Door"
          enabled: true
        - number: 3
          enabled: false
        - number: 4
          enabled: false
```

---

## Conseils et meilleures pratiques

1. **Utiliser l'interface utilisateur pour les configurations simples** - L'interface utilisateur fournit un moyen intuitif d'ajouter et de gérer les appareils sans avoir besoin d'écrire YAML.

2. **Utiliser YAML pour les configurations complexes ou programmatiques** - YAML est meilleur pour les grandes installations ou lorsque vous avez besoin du contrôle de version.

3. **Nommage des adresses** - Utilisez toujours le format `subnet.device` pour les adresses (par exemple, `1.5`, `2.10`). Les valeurs `subnet` et `device` doivent être des adresses Buspro valides sur votre réseau.

4. **Numérotation des canaux** - Les canaux sont numérotés à partir de 1. Laissez le nom d'un canal vide dans l'interface utilisateur pour le désactiver, ce qui empêche la création d'entités pour les canaux non utilisés.

5. **Noms d'appareils** - Utilisez des noms descriptifs basés sur la localisation (par exemple, "Lumières du salon" au lieu de "Relais"). Cela rend les automatisations et les scènes plus faciles à comprendre.

6. **IDs d'objet** - En YAML, `object_id` est facultatif mais recommandé. Il contrôle le slug d'ID d'entité. S'il est omis, Home Assistant en génère un à partir du nom du canal.

7. **ID uniques** - Pour les cas avancés où vous devez contrôler manuellement les entrées du registre des entités, utilisez `unique_id` dans la configuration YAML. Cela permet à Home Assistant de suivre l'entité de manière fiable même si le nom de l'appareil change.

Pour plus d'informations sur les formats de configuration YAML, consultez [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md).
