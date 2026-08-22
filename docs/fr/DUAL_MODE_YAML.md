# Configuration YAML Dual-Mode

**Documentation:** [English](../en/DUAL_MODE_YAML.md) | [Русский](../ru/DUAL_MODE_YAML.md) | [Беларуская](../be/DUAL_MODE_YAML.md) | [Deutsch](../de/DUAL_MODE_YAML.md) | [Español](../es/DUAL_MODE_YAML.md) | **Français** | [Italiano](../it/DUAL_MODE_YAML.md) | [Nederlands](../nl/DUAL_MODE_YAML.md) | [Norsk](../no/DUAL_MODE_YAML.md) | [Українська](../uk/DUAL_MODE_YAML.md)

Le composant personnalisé buspro prend en charge deux approches de configuration YAML complémentaires :

1. **Centré sur l'entité** (Legacy) - Définitions d'entités individuelles
2. **Centré sur l'appareil** (Modern) - Définitions complètes d'appareil avec tous les canaux

Vous pouvez utiliser **l'une ou l'autre approche ou les deux simultanément** dans votre configuration Home Assistant.

## Format centré sur l'entité (Legacy)

Définissez les entités individuellement. Utile pour organiser les entités par domaine (lumières, interrupteurs, capteurs).

### Caractéristiques
- Une entité par entrée YAML
- Focus sur les types de capteurs ou sorties spécifiques
- Groupement automatique des appareils par préfixe d'adresse
- Adapté à l'organisation des entités individuelles

### Exemple
```yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 1.1
  devices:
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"
        - type: illuminance
          name: "Kitchen Illuminance"
          object_id: "hdl_sensor_illuminance_kitchen_ceiling"
```

### Organisation des fichiers

```
entities/
├── buspro_devices/
│   └── kitchen/
│       └── multisensor_2_10.yaml    # Configuration d'entité centrée sur l'appareil
```

## Format centré sur l'appareil (Modern)

Définissez les appareils complets avec tous leurs canaux/entités. Utile pour gérer tous les aspects d'un appareil au même endroit.

### Caractéristiques
- Un appareil = un fichier YAML
- Tous les canaux définis ensemble
- Groupement et structure clairs des appareils
- Adapté à la gestion complète des appareils
- Correspond directement au registre des appareils buspro

### Exemple
```yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 1.1
  devices:
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
          object_id: "hdl_switch_light_bathroom_main"
        - number: 2
          name: "Exhaust Fan"
          enabled: true
          object_id: "hdl_switch_fan_bathroom_exhaust"

    - address: "2.5"
      name: "Guestroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Bra Okno"
          enabled: true
          object_id: "hdl_switch_light_guestroom_bra_window"
        - number: 2
          name: "Bra Dver"
          enabled: true
          object_id: "hdl_switch_light_guestroom_bra_door"
```

### Organisation des fichiers

```
entities/
├── switches/
│   ├── light/
│   │   ├── guestroom/
│   │   │   ├── switch_light_guestroom_bra_window.yaml  # Centré sur l'appareil
│   │   │   └── switch_light_guestroom_bra_door.yaml
│   │   └── bathroom/
│   │       └── switch_light_bathroom_main.yaml
```

## Détails du format de canal centré sur l'appareil

### Champs obligatoires

```yaml
address: "2.5"                    # Adresse du dispositif (sous-réseau.appareil)
name: "Device Name"               # Nom de l'appareil lisible
model: "HDL-MD0606.32"           # Modèle d'appareil du catalogue
device_type: "relay|dimmer|..."  # Type d'entité
channels:                         # Liste des canaux/entités
  - number: 1                     # Numéro de canal (1-N) ou nom de capacité
    name: "Channel Name"          # Nom d'affichage du canal
    enabled: true                 # Créer une entité (par défaut : true)
```

### Champs optionnels

```yaml
channels:
  - number: 1
    name: "Channel Name"
    enabled: true
    object_id: "hdl_switch_light_guestroom_bra_window"  # Suffixe de l'ID d'entité
    unique_id: "buspro-2.5-relay-1"                     # Identifiant unique
```

## Types d'appareils pris en charge

**Éclairage:**
- `relay` - Interrupteurs simples on/off
- `dimmer` - Lumières dimmables (contrôle de luminosité 0-255)

**Capteurs et entrées:**
- `dry_contact` - Capteurs binaires (contacts portes/fenêtres)
- `multisensor` - Capteurs environnementaux composés
- `universal_switch` - Entrées d'interrupteur universel avec logique jour/nuit

**Climat et HVAC:**
- `floor_heating` - Modules de chauffage par le sol/contrôle de température
- `ac` - Contrôleurs de climatisation

**Motorisé:**
- `cover` - Moteurs de stores/volets avec contrôle de position
- `fan` - Régulateurs de vitesse de ventilateur

## Mélanger les deux approches

Vous pouvez utiliser les deux formats simultanément, tant qu'ils ne sont pas en conflit:

```yaml
buspro:
  devices:
    # Centré sur l'entité: multi-capteur
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"

    # Centré sur l'appareil: relais avec canaux
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          object_id: "hdl_switch_light_bathroom_main"
```

**Important:** Chaque adresse ne peut être définie qu'une seule fois. N'utilisez pas la même adresse dans les deux formats.

## Groupement du registre des appareils

Les deux formats regroupent automatiquement les entités sous leur appareil parent dans le registre des appareils de Home Assistant:

- Les appareils sont identifiés par **adresse de base** (par exemple, `2.5`)
- Toutes les entités avec les adresses `2.5.1`, `2.5.2`, ... sont regroupées sous l'appareil `2.5`
- Les propriétés de l'appareil (nom, modèle, fabricant) s'appliquent à toutes les entités

### Exemple de hiérarchie du registre des appareils

```
Appareil: Guestroom Relay (2.5)
├── Entité: Bra Okno (2.5.1) [dimmer/switch]
└── Entité: Bra Dver (2.5.2) [dimmer/switch]

Appareil: Bathroom Relay (2.4)
├── Entité: Main Light (2.4.1) [relay/switch]
└── Entité: Exhaust Fan (2.4.2) [relay/switch]
```

## Bonnes pratiques

### Pour centré sur l'entité:
- Organisez les fichiers par domaine (`entities/sensors/`, `entities/lights/`)
- Une entité par fichier
- Utilisez des noms de fichiers descriptifs
- Adapté aux configurations centrées sur les capteurs

### Pour centré sur l'appareil:
- Organisez les fichiers par pièce ou groupe d'appareils
- Tous les canaux dans un fichier
- Utilisez une dénomination cohérente pour tous les canaux
- Adapté à la gestion organisée des appareils

### Pour les deux:
- Ne dupliquez pas les adresses entre les formats
- Utilisez le format qui correspond à votre flux de travail
- Considérez les préférences de votre équipe
- Documentez votre choix dans CLAUDE.md ou README
