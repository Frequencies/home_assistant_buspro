# HDL Buspro Enhetskonfigurasjonseksempler

**Tilgjengelige språk:** [🇧🇾 Беларуская](../be/DEVICE_EXAMPLES.md) | [🇩🇪 Deutsch](../de/DEVICE_EXAMPLES.md) | [🇬🇧 English](../en/DEVICE_EXAMPLES.md) | [🇪🇸 Español](../es/DEVICE_EXAMPLES.md) | [🇫🇷 Français](../fr/DEVICE_EXAMPLES.md) | [🇮🇹 Italiano](../it/DEVICE_EXAMPLES.md) | [🇳🇱 Nederlands](../nl/DEVICE_EXAMPLES.md) | 🇳🇴 Norsk | [🇷🇺 Русский](../ru/DEVICE_EXAMPLES.md) | [🇺🇦 Українська](../uk/DEVICE_EXAMPLES.md)

---

Denne veiledningen gir praktiske UI- og YAML-konfigurasjonseksempler for alle støttede enhetstyper i HDL Buspro-integrasjonen.

**Innholdsfortegnelse:**
- [Relèenheter](#relèenheter)
- [Dimmereneheter](#dimmereneheter)
- [Dekkingsenheter (persienner/lameller)](#dekkingsenheter)
- [Ventilatorenheter](#ventilatorenheter)
- [Klimaenheter](#klimaenheter)
- [Sensorenheter](#sensorenheter)
- [Binære sensorenheter](#binære-sensorenheter)

---

## Relèenheter

Relèenheter er enkle på/av-brytere som brukes til belysning, ventilatorer og andre binære belastninger.

**Støttede modeller:**
- `HDL-MR0410.431` - 4 relèkanaler
- `HDL-MR0810.432` - 8 relèkanaler
- `HDL-MR1210.433` - 12 relèkanaler
- `HDL-MR1610.433` - 16 relèkanaler
- HDL høyeffekt relèvarianter (MR0416, MR0816, MR1216, MR1616, MR0420C, etc.)

### Eksempel på UI-konfigurasjon

**Trinn:**
1. Gå til **Innstillinger > Enheter og tjenester > HDL Buspro > Konfigurer**
2. Klikk **Legg til enhet**
3. Velg enhettype: **Relè**
4. Velg eksakt modell: **HDL-MR0410.431** (4 kanaler)
5. Skriv inn Buspro-adresse: `1.10`
6. Skriv inn enhetsnavn: "Stuebelysning"
7. Gi navn til kanalene:
   - Kanal 1: "Taklampe"
   - Kanal 2: "Bordlampe"
   - Kanal 3: "Vegglampe"
   - Kanal 4: "" (la være tom for å deaktivere)
8. Klikk **Lagre**

**Resultat:**
- `light.stuebelysning_taklampe`
- `light.stuebelysning_bordlampe`
- `light.stuebelysning_vegglampe`

### Eksempel på YAML-konfigurasjon

**Entity-sentrert (individuelle filer):**

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

**Enhet-sentrert (komplett enhetsdefinisjon):**

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

## Dimmereneheter

Dimmereneheter kontrollerer lysstyrke (0-255) for dimmbare lys.

**Støttede modeller:**
- `HDL-MD0206.432` - 2 dimmerkanaler
- `HDL-MD0403.432` - 4 dimmerkanaler
- `HDL-MD0602.432` - 6 dimmerkanaler
- HDL trailing-edge dimmere (MDT0203, MDT04015, MDT06015, etc.)
- `HDL-MDLED0605.432` - 6 dimmerkanaler med diagnostikk

### Eksempel på UI-konfigurasjon

**Trinn:**
1. Gå til **Innstillinger > Enheter og tjenester > HDL Buspro > Konfigurer**
2. Klikk **Legg til enhet**
3. Velg enhettype: **Dimmer**
4. Velg eksakt modell: **HDL-MD0602.432** (6 kanaler)
5. Skriv inn Buspro-adresse: `1.5`
6. Skriv inn enhetsnavn: "Soveromsdimmere"
7. Gi navn til kanalene:
   - Kanal 1: "Hovedlys"
   - Kanal 2: "Sengelampe venstre"
   - Kanal 3: "Sengelampe høyre"
   - Kanaler 4-6: la være tomme
8. Klikk **Lagre**

**Resultat:**
- `light.soveromsdimmere_hovedlys` (dimmbar 0-255)
- `light.soveromsdimmere_sengelampe_venstre` (dimmbar 0-255)
- `light.soveromsdimmere_sengelampe_høyre` (dimmbar 0-255)

### Eksempel på YAML-konfigurasjon

**Entity-sentrert:**

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

**Enhet-sentrert:**

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

## Dekkingsenheter

Dekkingsenheter kontrollerer motoriserte persienner, lameller og gardiner.

**Støttede modeller:**
- `HDL-MW02.431` - 2 gardin-/dekkingskanaler
- `HDL-MWM45.431` - Gardin-/dekkingsentiteter (konfigurerbare kanaler)

### Eksempel på UI-konfigurasjon

**Trinn:**
1. Gå til **Innstillinger > Enheter og tjenester > HDL Buspro > Konfigurer**
2. Klikk **Legg til enhet**
3. Velg enhettype: **Dekning**
4. Velg eksakt modell: **HDL-MW02.431** (2 kanaler)
5. Skriv inn Buspro-adresse: `2.10`
6. Skriv inn enhetsnavn: "Stuelameller"
7. Gi navn til kanalene:
   - Kanal 1: "Vinduer"
   - Kanal 2: "Terassedør"
8. Klikk **Lagre**

**Resultat:**
- `cover.stuelameller_vinduer`
- `cover.stuelameller_terassedør`

### Eksempel på YAML-konfigurasjon

**Enhet-sentrert:**

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

## Ventilatorenheter

Ventilatorenheter kontrollerer ventilatorer med variabel hastighet.

**Støttede modeller:**
- Generisk ventilatorprofil (ventilatorer med variabel hastighet)

### Eksempel på UI-konfigurasjon

**Trinn:**
1. Gå til **Innstillinger > Enheter og tjenester > HDL Buspro > Konfigurer**
2. Klikk **Legg til enhet**
3. Velg enhettype: **Ventilator**
4. Velg eksakt modell: **Generisk** (spesifiser antall kanaler)
5. Skriv inn Buspro-adresse: `3.5`
6. Skriv inn enhetsnavn: "Badevannstrekksventilator"
7. Gi navn til kanalen: "Hovedventilator"
8. Klikk **Lagre**

**Resultat:**
- `fan.badevannstrekksventilator_hovedventilator` (hastighetscontrol 0-255)

### Eksempel på YAML-konfigurasjon

**Enhet-sentrert:**

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

## Klimaenheter

Klimaenheter kontrollerer temperatur og HVAC-systemer.

**Støttede modeller:**
- `HDL-MFH04.432` - 4 gulvvarmekanaler
- `HDL-MFH06.432` - 6 gulvvarmekanaler
- `HDL-M/HVAC8.1` - AC klimakontroll
- `HDL-MPED4.431` - AC klimakontroll
- Generisk AC-profil
- Generisk gulvvarmeprofil

### Eksempel på UI-konfigurasjon - AC-enhet

**Trinn:**
1. Gå til **Innstillinger > Enheter og tjenester > HDL Buspro > Konfigurer**
2. Klikk **Legg til enhet**
3. Velg enhettype: **Klima**
4. Velg eksakt modell: **HDL-M/HVAC8.1** (AC)
5. Skriv inn Buspro-adresse: `3.1`
6. Skriv inn enhetsnavn: "Stue AC"
7. Klikk **Lagre**

**Resultat:**
- `climate.stue_ac` (måltemperatur, modus, strømkontroll)

### Eksempel på YAML-konfigurasjon

**Enhet-sentrert:**

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

## Sensorenheter

Sensorenheter gir temperatur-, fuktighets-, belysnings- og bevegelsesdata.

**Støttede modeller:**
- `HDL-MSP02.4C` - Temperatur, belysningsstyrke, bevegelse
- `HDL-MSP07M.4C` - Temperatur, belysningsstyrke, fuktighet, bevegelse, 2 kontakter
- `HDL-MS08M.4C` - Temperatur, belysningsstyrke, bevegelse
- `HDL-MS12M.4C` - Temperatur, belysningsstyrke, fuktighet, bevegelse, 2 kontakter
- `HDL-MCLog.431` - Logikkstyrer (skrivebeskyttet)
- Paneltemperatursensorer (MPTL, MP2B, MP4B, MPL8, etc.)

### Eksempel på UI-konfigurasjon

**Trinn:**
1. Gå til **Innstillinger > Enheter og tjenester > HDL Buspro > Konfigurer**
2. Klikk **Legg til enhet**
3. Velg enhettype: **Multisensor**
4. Velg eksakt modell: **HDL-MSP07M.4C**
5. Skriv inn Buspro-adresse: `2.5`
6. Skriv inn enhetsnavn: "Stuesensor"
7. Klikk **Lagre**

**Resultat:**
- `sensor.stuesensor_temperatur`
- `sensor.stuesensor_belysningsstyrke`
- `sensor.stuesensor_fuktighet`
- `binary_sensor.stuesensor_bevegelse`
- 2 tilleggstørre kontakter

### Eksempel på YAML-konfigurasjon

**Entity-sentrert:**

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

**Enhet-sentrert:**

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

## Binære sensorenheter

Binære sensorenheter gir på/av-status fra tørrkontakter og dør-/vinduessensorer.

**Støttede modeller:**
- `HDL-MS04.432` - 4 tørrkontaktkanaler
- `HDL-MS24.232` - 24 tørrkontaktkanaler
- Multisensorer med integrerte kontakter (MSP07M, MS12M, etc.)

### Eksempel på UI-konfigurasjon

**Trinn:**
1. Gå til **Innstillinger > Enheter og tjenester > HDL Buspro > Konfigurer**
2. Klikk **Legg til enhet**
3. Velg enhettype: **Tørkontakt**
4. Velg eksakt modell: **HDL-MS04.432** (4 kanaler)
5. Skriv inn Buspro-adresse: `1.20`
6. Skriv inn enhetsnavn: "Dør- og vinduessensorer"
7. Gi navn til kanalene:
   - Kanal 1: "Inndør"
   - Kanal 2: "Garasjedør"
   - Kanal 3: "Stuevindu"
   - Kanal 4: la være tom
8. Klikk **Lagre**

**Resultat:**
- `binary_sensor.dør_og_vinduessensorer_inndør`
- `binary_sensor.dør_og_vinduessensorer_garasjedør`
- `binary_sensor.dør_og_vinduessensorer_stuevindu`

### Eksempel på YAML-konfigurasjon

**Enhet-sentrert:**

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

## Kompleks multi-enhet eksempel

Her er en fullstendig konfigurasjonsfil som viser flere enhetstyper som fungerer sammen:

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

## Tips og beste praksis

1. **Bruk UI for enkle oppsett** - Brukergrensesnittet gir en intuitiv måte å legge til og administrere enheter uten å måtte skrive YAML.

2. **Bruk YAML for komplekse eller programmatiske konfigurasjoner** - YAML er bedre for store installasjoner eller når du trenger versjonskontroll.

3. **Adressenavn** - Bruk alltid formatet `subnet.device` for adresser (f.eks. `1.5`, `2.10`). Verdiene `subnet` og `device` må være gyldige Buspro-adresser på nettverket ditt.

4. **Kanalnummerering** - Kanaler er nummerert fra 1. La et kanals navn være tomt i brukergrensesnittet for å deaktivere det, noe som forhindrer enhetsskapelse for ubrukte kanaler.

5. **Enhetsnavn** - Bruk beskrivende, stedsbaserte navn (f.eks. "Stuebelysning" i stedet for "Relè"). Dette gjør automationer og scener lettere å forstå.

6. **Object ID-er** - I YAML er `object_id` valgfritt men anbefalt. Det kontrollerer enhetens ID-slug. Hvis det utelates, genererer Home Assistant en fra kanalnavn.

7. **Unike ID-er** - For avanserte tilfeller hvor du trenger å kontrollere enhetsposter manuelt, bruk `unique_id` i YAML-konfigurasjonen. Dette gjør det mulig for Home Assistant å spore enheten pålitelig selv om enhetsnavnet endres.

For mer informasjon om YAML-konfigurasjonsformater, se [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md).
