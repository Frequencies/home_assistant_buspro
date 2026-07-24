# HDL Buspro
## Lingue

[![English](https://flagcdn.com/24x18/gb.png) English](README.md) |
[![Deutsch](https://flagcdn.com/24x18/de.png) Deutsch](README.de.md) |
[![Français](https://flagcdn.com/24x18/fr.png) Français](README.fr.md) |
[![Nederlands](https://flagcdn.com/24x18/nl.png) Nederlands](README.nl.md) |
[![Español](https://flagcdn.com/24x18/es.png) Español](README.es.md) |
[![Italiano](https://flagcdn.com/24x18/it.png) Italiano](README.it.md) |
[![Русский](https://flagcdn.com/24x18/ru.png) Русский](README.ru.md) |
[![Українська](https://flagcdn.com/24x18/ua.png) Українська](README.uk.md) |
[![Беларуская](https://flagcdn.com/24x18/by.png) Беларуская](README.be.md)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

L'integrazione HDL Buspro ti consente di controllare il tuo sistema HDL Buspro da Home Assistant.

## Installazione
In HACS -> Integrazioni, aggiungi il repository personalizzato "https://github.com/Frequencies/home_assistant_buspro" con la categoria "Integrazione". Seleziona l’integrazione chiamata "HDL Buspro" e scaricala.

Riavvia l'assistente domestico.

Vai su Impostazioni > Integrazioni e aggiungi integrazione "HDL Buspro". Digitare l'indirizzo IP e il numero di porta del gateway.

## Configurazione

#### Piattaforma leggera
   
Per utilizzare Buspro light nella tua installazione, aggiungi quanto segue al tuo file Configuration.yaml:

```yaml
light:
  - platform: buspro
    running_time: 3
    devices:
      1.89.1:
        name: Living Room Light
        running_time: 5
      1.89.2:
        name: Front Door Light
        dimmable: False
        ack_retry_enabled: True
```
+ **running_time** _(int) (Facoltativo)_: tempo di esecuzione predefinito in secondi per tutti i dispositivi. Il tempo di esecuzione è 0 secondi se non impostato.
+ **ack_retry_enabled** _(boolean) (Facoltativo)_: Abilita un unico tentativo di ritrasmissione se non arriva ACK entro 0,8 s. Predefinito: `True`.
+ **dispositivi** _(Obbligatorio)_: un elenco di dispositivi da configurare
  + **X.X.X** _(Obbligatorio)_: l'indirizzo del dispositivo nel formato "<ID subnet>.<ID dispositivo>.<numero canale>"
    + **name** _(string) (Obbligatorio)_: il nome del dispositivo
    + **running_time** _(int) (Facoltativo)_: il tempo di esecuzione in secondi per il dispositivo. Se omesso, viene utilizzato il tempo di esecuzione predefinito per tutti i dispositivi.
    + **ack_retry_enabled** _(boolean) (Facoltativo)_: Override per dispositivo per il retry ACK.
    + **dimmerabile** _(booleano) (facoltativo)_: il dispositivo è dimmerabile? L'impostazione predefinita è Vero.
    + **object_id** _(string) (facoltativo)_: object_id dispositivo. L'impostazione predefinita è generata automaticamente dal nome del dispositivo.

#### Cambia piattaforma

Per utilizzare lo switch Buspro nella tua installazione, aggiungi quanto segue al tuo file Configuration.yaml:

```yaml
switch:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Switch
      1.89.2:
        name: Front Door Switch
```
+ **dispositivi** _(Obbligatorio)_: un elenco di dispositivi da configurare
  + **X.X.X** _(Obbligatorio)_: l'indirizzo del dispositivo nel formato "<ID subnet>.<ID dispositivo>.<numero canale>"
    + **name** _(string) (Obbligatorio)_: il nome del dispositivo
    + **object_id** _(string) (facoltativo)_: object_id dispositivo. L'impostazione predefinita è generata automaticamente dal nome del dispositivo.

#### Piattaforma di sensori

Per utilizzare il sensore Buspro nella tua installazione, aggiungi quanto segue al file Configuration.yaml:

```yaml
sensor:
  - platform: buspro
    devices:
      - address: "1.74"
        name: Living Room
        type: temperature
        unit_of_measurement: °C
        device_class: temperature
        device: dlp
      - address: "1.74"
        name: Front Door
        type: illuminance
        unit_of_measurement: lux
      - address: "1.75"
        name: Hall
        type: humidity
        unit_of_measurement: "%"
```
+ **dispositivi** _(Obbligatorio)_: un elenco di dispositivi da configurare
  + **indirizzo** _(stringa) (obbligatorio)_: l'indirizzo del dispositivo sensore nel formato "<ID subnet>.<ID dispositivo>"
  + **name** _(string) (Obbligatorio)_: il nome del dispositivo
  + **type** _(string) (Obbligatorio)_: Tipo di sensore da monitorare.
    + Sensori disponibili:
     + temperatura
     + illuminamento
     + umidità
  + **unità_di_misura** _(stringa) (Facoltativo)_: testo da visualizzare come unità di misura
  + **object_id** _(string) (facoltativo)_: object_id dispositivo. L'impostazione predefinita è generata automaticamente dal nome del dispositivo.
  + **classe_dispositivo** _(stringa) (facoltativo)_: classe del dispositivo HASS, ad esempio "temperatura"
(https://www.home-assistant.io/components/sensor/)
  + **dispositivo** _(stringa) (facoltativo)_: il tipo di dispositivo sensore:
    + dlp

#### Piattaforma di sensori binari

Per utilizzare il sensore binario Buspro nella tua installazione, aggiungi quanto segue al tuo file Configuration.yaml:

```yaml
binary_sensor:
  - platform: buspro
    devices:
      - address: "1.74"
        name: Living Room
        type: motion
        device_class: motion
      - address: "1.74.100"
        name: Front Door
        type: universal_switch
      - address: "1.75.3"
        name: Kitchen switch
        type: single_channel
```
+ **dispositivi** _(Obbligatorio)_: un elenco di dispositivi da configurare
  + **indirizzo** _(stringa) (obbligatorio)_: l'indirizzo del dispositivo sensore nel formato "<ID sottorete>.<ID dispositivo>". Se
'type' = 'universal_switch' il numero dello switch universale deve essere aggiunto all'indirizzo.
  + **name** _(string) (Obbligatorio)_: il nome del dispositivo
  + **object_id** _(string) (facoltativo)_: object_id dispositivo. L'impostazione predefinita è generata automaticamente dal nome del dispositivo.
  + **type** _(string) (Obbligatorio)_: Tipo di sensore da monitorare.
    + Sensori disponibili:
      + movimento
      + contatto_secco_1
      + contatto_secco_2
      + interruttore_universale
      + canale_singolo
  + **classe_dispositivo** _(stringa) (facoltativo)_: classe del dispositivo HASS, ad esempio "movimento"
(https://www.home-assistant.io/components/binary_sensor/)

#### Piattaforma climatica

Per utilizzare il controllo climatico del pannello Buspro nella tua installazione, aggiungi quanto segue al file Configuration.yaml:

```yaml
climate:
  - platform: buspro
    devices:
      - address: "1.74"
        name: Bedroom AC
        type: ac
      - address: "1.74"
        name: Living Room
        type: floor_heating
        floor_heating_device_type: dlp
        preset_modes: 
          - none
          - away
          - home
          - sleep
      - address: "1.90"
        type: floor_heating
        floor_heating_device_type: module
        channel: 1
        name: Floor Heating Zone 1
```
+ **dispositivi** _(Obbligatorio)_: un elenco di dispositivi da configurare
  + **indirizzo** _(stringa) (obbligatorio)_: l'indirizzo del dispositivo sensore nel formato "<ID subnet>.<ID dispositivo>"
  + **name** _(string) (Obbligatorio)_: il nome del dispositivo
  + **tipo** _(stringa) (facoltativo)_: `ac` o `floor_heating`. L'impostazione predefinita è "riscaldamento_pavimento".
  + **tipo_dispositivo_riscaldamento_a_pavimento** _(stringa) (facoltativo)_: `dlp` o `modulo`.
Se omesso, `module` viene selezionato automaticamente quando viene fornito `channel`, altrimenti `dlp`.
  + **object_id** _(string) (facoltativo)_: object_id dispositivo. L'impostazione predefinita è generata automaticamente dal nome del dispositivo.
  + **preset_modes** _(list) (Facoltativo)_: elenco delle modalità preimpostate supportate. La selezione della modalità preimpostata è disabilitata se non impostata. I valori possibili sono mostrati nella tabella seguente. Le modalità corrispondenti devono essere abilitate in HDL (Riscaldamento a pavimento > Impostazioni di lavoro > Modalità).
  + **canale** _(int) (facoltativo)_: canale del modulo di riscaldamento a pavimento (`1..6`) per `tipo_dispositivo_di_riscaldamento_a_pavimento: modulo`.
    
| HA preset mode | HDL mode |
|:--------------:|:--------:|
|      none      |  Normal  |
|      away      |   Away   |
|      home      |   Day    |
|     sleep      |  Night   |


#### Piattaforma tende

Per usare le tende Buspro nella tua installazione, aggiungi quanto segue al file `configuration.yaml`:

```yaml
cover:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Curtain
        invert: false
        object_id: living_room_curtain
```
+ **devices** _(Obbligatorio)_: Mappatura dei canali tenda Buspro
  + **chiave** _(string)_: `<ID subnet>.<ID dispositivo>.<canale>`
  + **name** _(string) (Obbligatorio)_: Nome visualizzato
  + **invert** _(bool) (Opzionale)_: Inverte la direzione apertura/chiusura. Valore predefinito `false`.
  + **object_id** _(string) (Opzionale)_: `object_id` dell'entità. Predefinito auto-generato dal nome.

Funzionalità supportate:
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

---
## Servizi

#### Invio di un messaggio arbitrario:
```
Domain: buspro
Service: send_message
Service Data: {"address": [1,74], "operate_code": [4,78], "payload": [1,100,0,3]}
```
#### Attivazione di una scena:
```
Domain: buspro
Service: activate_scene
Service Data: {"address": [1,74], "scene_address": [3,5]}
```
#### Impostazione di un interruttore universale:
```
Domain: buspro
Service: set_universal_switch
Service Data: {"address": [1,74], "switch_number": 100, "status": 1}
```
