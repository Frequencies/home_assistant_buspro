# Esempi di Configurazione Dispositivi HDL Buspro

**Lingue disponibili:** [English](../en/DEVICE_EXAMPLES.md) | [Deutsch](../de/DEVICE_EXAMPLES.md) | [Français](../fr/DEVICE_EXAMPLES.md) | [Español](../es/DEVICE_EXAMPLES.md) | [Italiano](../it/DEVICE_EXAMPLES.md) | [Nederlands](../nl/DEVICE_EXAMPLES.md) | [Norsk](../no/DEVICE_EXAMPLES.md) | [Русский](../ru/DEVICE_EXAMPLES.md) | [Українська](../uk/DEVICE_EXAMPLES.md)

---

Questa guida fornisce esempi pratici di configurazione dell'interfaccia utente e YAML per tutti i tipi di dispositivi supportati nell'integrazione HDL Buspro.

**Indice dei contenuti:**
- [Dispositivi relè](#dispositivi-relè)
- [Dispositivi dimmer](#dispositivi-dimmer)
- [Dispositivi copertura (tapparelle/persiane)](#dispositivi-copertura)
- [Dispositivi ventola](#dispositivi-ventola)
- [Dispositivi climatici](#dispositivi-climatici)
- [Dispositivi sensore](#dispositivi-sensore)
- [Dispositivi sensore binari](#dispositivi-sensore-binari)

---

## Dispositivi relè

I dispositivi relè sono semplici interruttori acceso/spento utilizzati per illuminazione, ventole e altri carichi binari.

**Modelli supportati:**
- `HDL-MR0410.431` - 4 canali relè
- `HDL-MR0810.432` - 8 canali relè
- `HDL-MR1210.433` - 12 canali relè
- `HDL-MR1610.433` - 16 canali relè
- Varianti relè alta potenza HDL (MR0416, MR0816, MR1216, MR1616, MR0420C, etc.)

### Esempio di configurazione dell'interfaccia utente

**Passaggi:**
1. Vai a **Impostazioni > Dispositivi e servizi > HDL Buspro > Configura**
2. Fai clic su **Aggiungi dispositivo**
3. Seleziona tipo di dispositivo: **Relè**
4. Seleziona modello esatto: **HDL-MR0410.431** (4 canali)
5. Immetti indirizzo Buspro: `1.10`
6. Immetti nome dispositivo: "Luci del soggiorno"
7. Assegna nome ai canali:
   - Canale 1: "Luce a soffitto"
   - Canale 2: "Lampada da tavolo"
   - Canale 3: "Applique murale"
   - Canale 4: "" (lascia vuoto per disabilitare)
8. Fai clic su **Salva**

**Risultato:**
- `light.luci_del_soggiorno_luce_a_soffitto`
- `light.luci_del_soggiorno_lampada_da_tavolo`
- `light.luci_del_soggiorno_applique_murale`

### Esempio di configurazione YAML

**Centrato su entità (file individuali):**

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

**Centrato su dispositivo (definizione completa dispositivo):**

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

## Dispositivi dimmer

I dispositivi dimmer controllano i livelli di luminosità (0-255) per luci dimmerabili.

**Modelli supportati:**
- `HDL-MD0206.432` - 2 canali dimmer
- `HDL-MD0403.432` - 4 canali dimmer
- `HDL-MD0602.432` - 6 canali dimmer
- Dimmer trailing-edge HDL (MDT0203, MDT04015, MDT06015, etc.)
- `HDL-MDLED0605.432` - 6 canali dimmer con diagnostica

### Esempio di configurazione dell'interfaccia utente

**Passaggi:**
1. Vai a **Impostazioni > Dispositivi e servizi > HDL Buspro > Configura**
2. Fai clic su **Aggiungi dispositivo**
3. Seleziona tipo di dispositivo: **Dimmer**
4. Seleziona modello esatto: **HDL-MD0602.432** (6 canali)
5. Immetti indirizzo Buspro: `1.5`
6. Immetti nome dispositivo: "Dimmer della camera da letto"
7. Assegna nome ai canali:
   - Canale 1: "Luce principale"
   - Canale 2: "Lampada comodino sinistra"
   - Canale 3: "Lampada comodino destra"
   - Canali 4-6: lascia vuoti
8. Fai clic su **Salva**

**Risultato:**
- `light.dimmer_della_camera_da_letto_luce_principale` (dimmerabile 0-255)
- `light.dimmer_della_camera_da_letto_lampada_comodino_sinistra` (dimmerabile 0-255)
- `light.dimmer_della_camera_da_letto_lampada_comodino_destra` (dimmerabile 0-255)

### Esempio di configurazione YAML

**Centrato su entità:**

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

**Centrato su dispositivo:**

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

## Dispositivi copertura

I dispositivi copertura controllano tapparelle motorizzate, persiane e tende.

**Modelli supportati:**
- `HDL-MW02.431` - 2 canali tenda/copertura
- `HDL-MWM45.431` - Entità tenda/copertura (canali configurabili)

### Esempio di configurazione dell'interfaccia utente

**Passaggi:**
1. Vai a **Impostazioni > Dispositivi e servizi > HDL Buspro > Configura**
2. Fai clic su **Aggiungi dispositivo**
3. Seleziona tipo di dispositivo: **Copertura**
4. Seleziona modello esatto: **HDL-MW02.431** (2 canali)
5. Immetti indirizzo Buspro: `2.10`
6. Immetti nome dispositivo: "Persiane del soggiorno"
7. Assegna nome ai canali:
   - Canale 1: "Finestre"
   - Canale 2: "Porta patio"
8. Fai clic su **Salva**

**Risultato:**
- `cover.persiane_del_soggiorno_finestre`
- `cover.persiane_del_soggiorno_porta_patio`

### Esempio di configurazione YAML

**Centrato su dispositivo:**

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

## Dispositivi ventola

I dispositivi ventola controllano ventole a velocità variabile.

**Modelli supportati:**
- Profilo ventola generico (ventole a velocità variabile)

### Esempio di configurazione dell'interfaccia utente

**Passaggi:**
1. Vai a **Impostazioni > Dispositivi e servizi > HDL Buspro > Configura**
2. Fai clic su **Aggiungi dispositivo**
3. Seleziona tipo di dispositivo: **Ventola**
4. Seleziona modello esatto: **Generico** (specifica numero di canali)
5. Immetti indirizzo Buspro: `3.5`
6. Immetti nome dispositivo: "Ventola di estrazione bagno"
7. Assegna nome al canale: "Ventola principale"
8. Fai clic su **Salva**

**Risultato:**
- `fan.ventola_di_estrazione_bagno_ventola_principale` (controllo velocità 0-255)

### Esempio di configurazione YAML

**Centrato su dispositivo:**

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

## Dispositivi climatici

I dispositivi climatici controllano la temperatura e i sistemi HVAC.

**Modelli supportati:**
- `HDL-MFH04.432` - 4 canali riscaldamento a pavimento
- `HDL-MFH06.432` - 6 canali riscaldamento a pavimento
- `HDL-M/HVAC8.1` - Controllo climatico CA
- `HDL-MPED4.431` - Controllo climatico CA
- Profilo CA generico
- Profilo riscaldamento a pavimento generico

### Esempio di configurazione dell'interfaccia utente - Unità CA

**Passaggi:**
1. Vai a **Impostazioni > Dispositivi e servizi > HDL Buspro > Configura**
2. Fai clic su **Aggiungi dispositivo**
3. Seleziona tipo di dispositivo: **Clima**
4. Seleziona modello esatto: **HDL-M/HVAC8.1** (CA)
5. Immetti indirizzo Buspro: `3.1`
6. Immetti nome dispositivo: "CA del soggiorno"
7. Fai clic su **Salva**

**Risultato:**
- `climate.ca_del_soggiorno` (temperatura target, modalità, controllo alimentazione)

### Esempio di configurazione YAML

**Centrato su dispositivo:**

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

## Dispositivi sensore

I dispositivi sensore forniscono dati di temperatura, umidità, illuminazione e movimento.

**Modelli supportati:**
- `HDL-MSP02.4C` - Temperatura, illuminazione, movimento
- `HDL-MSP07M.4C` - Temperatura, illuminazione, umidità, movimento, 2 contatti
- `HDL-MS08M.4C` - Temperatura, illuminazione, movimento
- `HDL-MS12M.4C` - Temperatura, illuminazione, umidità, movimento, 2 contatti
- `HDL-MCLog.431` - Controllore logico (sola lettura)
- Sensori di temperatura pannello (MPTL, MP2B, MP4B, MPL8, etc.)

### Esempio di configurazione dell'interfaccia utente

**Passaggi:**
1. Vai a **Impostazioni > Dispositivi e servizi > HDL Buspro > Configura**
2. Fai clic su **Aggiungi dispositivo**
3. Seleziona tipo di dispositivo: **Multisensore**
4. Seleziona modello esatto: **HDL-MSP07M.4C**
5. Immetti indirizzo Buspro: `2.5`
6. Immetti nome dispositivo: "Sensore del soggiorno"
7. Fai clic su **Salva**

**Risultato:**
- `sensor.sensore_del_soggiorno_temperatura`
- `sensor.sensore_del_soggiorno_illuminazione`
- `sensor.sensore_del_soggiorno_umidità`
- `binary_sensor.sensore_del_soggiorno_movimento`
- 2 contatti secchi aggiuntivi

### Esempio di configurazione YAML

**Centrato su entità:**

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

**Centrato su dispositivo:**

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

## Dispositivi sensore binari

I dispositivi sensore binari forniscono lo stato acceso/spento dai contatti secchi e dai sensori porta/finestra.

**Modelli supportati:**
- `HDL-MS04.432` - 4 canali contatto secco
- `HDL-MS24.232` - 24 canali contatto secco
- Multisensori con contatti integrati (MSP07M, MS12M, etc.)

### Esempio di configurazione dell'interfaccia utente

**Passaggi:**
1. Vai a **Impostazioni > Dispositivi e servizi > HDL Buspro > Configura**
2. Fai clic su **Aggiungi dispositivo**
3. Seleziona tipo di dispositivo: **Contatto secco**
4. Seleziona modello esatto: **HDL-MS04.432** (4 canali)
5. Immetti indirizzo Buspro: `1.20`
6. Immetti nome dispositivo: "Sensori porta e finestra"
7. Assegna nome ai canali:
   - Canale 1: "Porta d'ingresso"
   - Canale 2: "Porta del garage"
   - Canale 3: "Finestra del soggiorno"
   - Canale 4: lascia vuoto
8. Fai clic su **Salva**

**Risultato:**
- `binary_sensor.sensori_porta_e_finestra_porta_d'ingresso`
- `binary_sensor.sensori_porta_e_finestra_porta_del_garage`
- `binary_sensor.sensori_porta_e_finestra_finestra_del_soggiorno`

### Esempio di configurazione YAML

**Centrato su dispositivo:**

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

## Esempio complesso multi-dispositivo

Ecco un file di configurazione completo che mostra più tipi di dispositivi che lavorano insieme:

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

## Suggerimenti e migliori pratiche

1. **Usa l'interfaccia utente per configurazioni semplici** - L'interfaccia utente fornisce un modo intuitivo per aggiungere e gestire dispositivi senza la necessità di scrivere YAML.

2. **Usa YAML per configurazioni complesse o programmatiche** - YAML è migliore per installazioni di grandi dimensioni o quando hai bisogno del controllo della versione.

3. **Denominazione degli indirizzi** - Usa sempre il formato `subnet.device` per gli indirizzi (ad es. `1.5`, `2.10`). I valori `subnet` e `device` devono essere indirizzi Buspro validi sulla tua rete.

4. **Numerazione dei canali** - I canali sono numerati a partire da 1. Lascia il nome di un canale vuoto nell'interfaccia utente per disabilitarlo, il che evita la creazione di entità per i canali non utilizzati.

5. **Nomi dei dispositivi** - Usa nomi descrittivi basati sulla posizione (ad es. "Luci del soggiorno" invece di "Relè"). Questo rende le automazioni e le scene più facili da comprendere.

6. **ID oggetto** - In YAML, `object_id` è facoltativo ma consigliato. Controlla lo slug ID entità. Se omesso, Home Assistant ne genera uno dal nome del canale.

7. **ID univoci** - Per i casi avanzati in cui devi controllare manualmente le voci del registro delle entità, usa `unique_id` nella configurazione YAML. Ciò consente a Home Assistant di tracciare l'entità in modo affidabile anche se il nome del dispositivo cambia.

Per ulteriori informazioni sui formati di configurazione YAML, consulta [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md).
