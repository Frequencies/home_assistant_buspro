# HDL Buspro Apparaatconfiguratie Voorbeelden

**Beschikbare talen:** [English](../en/DEVICE_EXAMPLES.md) | [Deutsch](../de/DEVICE_EXAMPLES.md) | [Français](../fr/DEVICE_EXAMPLES.md) | [Español](../es/DEVICE_EXAMPLES.md) | [Italiano](../it/DEVICE_EXAMPLES.md) | [Nederlands](../nl/DEVICE_EXAMPLES.md) | [Norsk](../no/DEVICE_EXAMPLES.md) | [Русский](../ru/DEVICE_EXAMPLES.md) | [Український](DEVICE_EXAMPLES.uk.md)

---

Deze handleiding biedt praktische UI- en YAML-configuratievoorbeelden voor alle ondersteunde apparaattypen in de HDL Buspro-integratie.

**Inhoudsopgave:**
- [Relaisapparaten](#relaisapparaten)
- [Dimmer-apparaten](#dimmer-apparaten)
- [Afdekking-apparaten (jaloezieën/luiken)](#afdekking-apparaten)
- [Ventilatorapparaten](#ventilatorapparaten)
- [Klimaatapparaten](#klimaatapparaten)
- [Sensorapparaten](#sensorapparaten)
- [Binaire sensorapparaten](#binaire-sensorapparaten)

---

## Relaisapparaten

Relaisapparaten zijn eenvoudige aan/uit-schakelaars die worden gebruikt voor verlichting, ventilatoren en andere binaire belastingen.

**Ondersteunde modellen:**
- `HDL-MR0410.431` - 4 relaiskanalen
- `HDL-MR0810.432` - 8 relaiskanalen
- `HDL-MR1210.433` - 12 relaiskanalen
- `HDL-MR1610.433` - 16 relaiskanalen
- HDL hoogvermogen relaisvarianten (MR0416, MR0816, MR1216, MR1616, MR0420C, etc.)

### UI-configuratievoorbeeld

**Stappen:**
1. Ga naar **Instellingen > Apparaten en services > HDL Buspro > Configureren**
2. Klik op **Apparaat toevoegen**
3. Selecteer apparaattype: **Relais**
4. Selecteer exact model: **HDL-MR0410.431** (4 kanalen)
5. Voer Buspro-adres in: `1.10`
6. Voer apparaatnaam in: "Woonkamerverlichting"
7. Noem de kanalen:
   - Kanaal 1: "Plafondlamp"
   - Kanaal 2: "Tafellamp"
   - Kanaal 3: "Wandlamp"
   - Kanaal 4: "" (leeg laten om uit te schakelen)
8. Klik op **Opslaan**

**Resultaat:**
- `light.woonkamerverlichting_plafondlamp`
- `light.woonkamerverlichting_tafellamp`
- `light.woonkamerverlichting_wandlamp`

### YAML-configuratievoorbeeld

**Entity-gericht (afzonderlijke bestanden):**

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

**Apparaat-gericht (volledige apparaatdefinitie):**

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

## Dimmer-apparaten

Dimmer-apparaten controleren de helderheid (0-255) voor dimmable verlichting.

**Ondersteunde modellen:**
- `HDL-MD0206.432` - 2 dimmerkanalen
- `HDL-MD0403.432` - 4 dimmerkanalen
- `HDL-MD0602.432` - 6 dimmerkanalen
- HDL trailing-edge dimmers (MDT0203, MDT04015, MDT06015, etc.)
- `HDL-MDLED0605.432` - 6 dimmerkanalen met diagnostiek

### UI-configuratievoorbeeld

**Stappen:**
1. Ga naar **Instellingen > Apparaten en services > HDL Buspro > Configureren**
2. Klik op **Apparaat toevoegen**
3. Selecteer apparaattype: **Dimmer**
4. Selecteer exact model: **HDL-MD0602.432** (6 kanalen)
5. Voer Buspro-adres in: `1.5`
6. Voer apparaatnaam in: "Slaapkamer dimmers"
7. Noem de kanalen:
   - Kanaal 1: "Hoofdverlichting"
   - Kanaal 2: "Bedlampje links"
   - Kanaal 3: "Bedlampje rechts"
   - Kanalen 4-6: laat leeg
8. Klik op **Opslaan**

**Resultaat:**
- `light.slaapkamer_dimmers_hoofdverlichting` (dimmable 0-255)
- `light.slaapkamer_dimmers_bedlampje_links` (dimmable 0-255)
- `light.slaapkamer_dimmers_bedlampje_rechts` (dimmable 0-255)

### YAML-configuratievoorbeeld

**Entity-gericht:**

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

**Apparaat-gericht:**

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

## Afdekking-apparaten

Afdekking-apparaten controleren gemotoriseerde jaloezieën, luiken en gordijnen.

**Ondersteunde modellen:**
- `HDL-MW02.431` - 2 gordijn-/afdekkingskanalen
- `HDL-MWM45.431` - Gordijn-/afdekkingsentiteiten (configureerbare kanalen)

### UI-configuratievoorbeeld

**Stappen:**
1. Ga naar **Instellingen > Apparaten en services > HDL Buspro > Configureren**
2. Klik op **Apparaat toevoegen**
3. Selecteer apparaattype: **Afdekking**
4. Selecteer exact model: **HDL-MW02.431** (2 kanalen)
5. Voer Buspro-adres in: `2.10`
6. Voer apparaatnaam in: "Woonkamerjaloezieën"
7. Noem de kanalen:
   - Kanaal 1: "Ramen"
   - Kanaal 2: "Patiodeur"
8. Klik op **Opslaan**

**Resultaat:**
- `cover.woonkamerjaloezieën_ramen`
- `cover.woonkamerjaloezieën_patiodeur`

### YAML-configuratievoorbeeld

**Apparaat-gericht:**

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

## Ventilatorapparaten

Ventilatorapparaten controleren ventilatoren met variabele snelheid.

**Ondersteunde modellen:**
- Generiek ventilatorconfiguratie (ventilatoren met variabele snelheid)

### UI-configuratievoorbeeld

**Stappen:**
1. Ga naar **Instellingen > Apparaten en services > HDL Buspro > Configureren**
2. Klik op **Apparaat toevoegen**
3. Selecteer apparaattype: **Ventilator**
4. Selecteer exact model: **Generiek** (geef aantal kanalen op)
5. Voer Buspro-adres in: `3.5`
6. Voer apparaatnaam in: "Badkamerventilator"
7. Noem het kanaal: "Hoofdventilator"
8. Klik op **Opslaan**

**Resultaat:**
- `fan.badkamerventilator_hoofdventilator` (snelheidscontrole 0-255)

### YAML-configuratievoorbeeld

**Apparaat-gericht:**

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

## Klimaatapparaten

Klimaatapparaten controleren temperatuur en HVAC-systemen.

**Ondersteunde modellen:**
- `HDL-MFH04.432` - 4 vloerverwarming kanalen
- `HDL-MFH06.432` - 6 vloerverwarming kanalen
- `HDL-M/HVAC8.1` - AC klimaatbeheer
- `HDL-MPED4.431` - AC klimaatbeheer
- Generiek AC profiel
- Generiek vloerverwarmingsprofiel

### UI-configuratievoorbeeld - AC-apparaat

**Stappen:**
1. Ga naar **Instellingen > Apparaten en services > HDL Buspro > Configureren**
2. Klik op **Apparaat toevoegen**
3. Selecteer apparaattype: **Klimaat**
4. Selecteer exact model: **HDL-M/HVAC8.1** (AC)
5. Voer Buspro-adres in: `3.1`
6. Voer apparaatnaam in: "Woonkamer AC"
7. Klik op **Opslaan**

**Resultaat:**
- `climate.woonkamer_ac` (doeltemperatuur, modus, energiebeheer)

### YAML-configuratievoorbeeld

**Apparaat-gericht:**

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

## Sensorapparaten

Sensorapparaten leveren temperatuur-, vochtigheidgraden-, verlichtings- en bewegingsgegevens.

**Ondersteunde modellen:**
- `HDL-MSP02.4C` - Temperatuur, verlichtingssterkte, beweging
- `HDL-MSP07M.4C` - Temperatuur, verlichtingssterkte, vochtigheid, beweging, 2 contacten
- `HDL-MS08M.4C` - Temperatuur, verlichtingssterkte, beweging
- `HDL-MS12M.4C` - Temperatuur, verlichtingssterkte, vochtigheid, beweging, 2 contacten
- `HDL-MCLog.431` - Logica controller (alleen-lezen)
- Paneel temperatuursensoren (MPTL, MP2B, MP4B, MPL8, etc.)

### UI-configuratievoorbeeld

**Stappen:**
1. Ga naar **Instellingen > Apparaten en services > HDL Buspro > Configureren**
2. Klik op **Apparaat toevoegen**
3. Selecteer apparaattype: **Multisensor**
4. Selecteer exact model: **HDL-MSP07M.4C**
5. Voer Buspro-adres in: `2.5`
6. Voer apparaatnaam in: "Woonkamersensor"
7. Klik op **Opslaan**

**Resultaat:**
- `sensor.woonkamersensor_temperatuur`
- `sensor.woonkamersensor_verlichtingssterkte`
- `sensor.woonkamersensor_vochtigheid`
- `binary_sensor.woonkamersensor_beweging`
- 2 aanvullende droge contacten

### YAML-configuratievoorbeeld

**Entity-gericht:**

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

**Apparaat-gericht:**

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

## Binaire sensorapparaten

Binaire sensorapparaten leveren aan/uit-status van droge contacten en deur-/raamsensoren.

**Ondersteunde modellen:**
- `HDL-MS04.432` - 4 droog contactkanalen
- `HDL-MS24.232` - 24 droog contactkanalen
- Multisensoren met geïntegreerde contacten (MSP07M, MS12M, etc.)

### UI-configuratievoorbeeld

**Stappen:**
1. Ga naar **Instellingen > Apparaten en services > HDL Buspro > Configureren**
2. Klik op **Apparaat toevoegen**
3. Selecteer apparaattype: **Droog contact**
4. Selecteer exact model: **HDL-MS04.432** (4 kanalen)
5. Voer Buspro-adres in: `1.20`
6. Voer apparaatnaam in: "Deur- en raamsensoren"
7. Noem de kanalen:
   - Kanaal 1: "Voordeur"
   - Kanaal 2: "Garagedeur"
   - Kanaal 3: "Woonkamerraam"
   - Kanaal 4: laat leeg
8. Klik op **Opslaan**

**Resultaat:**
- `binary_sensor.deur_en_raamsensoren_voordeur`
- `binary_sensor.deur_en_raamsensoren_garagedeur`
- `binary_sensor.deur_en_raamsensoren_woonkamerraam`

### YAML-configuratievoorbeeld

**Apparaat-gericht:**

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

## Complex multi-apparaat voorbeeld

Hier is een compleet configuratiebestand dat meerdere apparaattypen toont die samenwerken:

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

## Tips & best practices

1. **Gebruik UI voor eenvoudige instellingen** - De UI biedt een intuïtieve manier om apparaten toe te voegen en te beheren zonder YAML te hoeven schrijven.

2. **Gebruik YAML voor complexe of programmatische configuraties** - YAML is beter voor grote installaties of wanneer u versiebeheer nodig hebt.

3. **Adresbenaming** - Gebruik altijd het formaat `subnet.device` voor adressen (bijvoorbeeld `1.5`, `2.10`). De `subnet`- en `device`-waarden moeten geldige Buspro-adressen op uw netwerk zijn.

4. **Kanalnummering** - Kanalen zijn genummerd vanaf 1. Laat de naam van een kanaal leeg in de UI om het uit te schakelen, wat voorkomt dat entiteiten voor ongebruikte kanalen worden gemaakt.

5. **Apparaatnamen** - Gebruik beschrijvende, op locatie gebaseerde namen (bijvoorbeeld "Woonkamerverlichting" in plaats van "Relais"). Dit maakt automatiseringen en scènes gemakkelijker te begrijpen.

6. **Object-ID's** - In YAML is `object_id` optioneel maar aanbevolen. Het regelt de entiteit-ID-slug. Indien weggelaten, genereert Home Assistant er een op basis van de kanaal naam.

7. **Unieke ID's** - Voor geavanceerde gevallen waarbij u handmatig items in het entiteitenregister moet beheren, gebruikt u `unique_id` in de YAML-configuratie. Dit stelt Home Assistant in staat de entiteit betrouwbaar bij te houden, zelfs als de apparaatnaam verandert.

Voor meer informatie over YAML-configuratieformaten, zie [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md).
