# HDL Buspro per Home Assistant

[English](../README.md) | **Italiano**

L'integrazione gestisce il gateway e i dispositivi fisici HDL Buspro tramite
l'interfaccia di Home Assistant. L'elenco completo di modelli, entità e servizi
è nella [documentazione inglese](../README.md).

> **Nota importante**: Per la configurazione dettagliata dei dispositivi, esempi YAML, servizi disponibili e guida allo sviluppo, consultare la [documentazione in inglese](../README.md). Questa pagina fornisce informazioni di installazione e configurazione iniziale.

## Installazione

### HACS (consigliato)

1. Aprire **HACS > Integrazioni**.
2. Aprire il menu con i tre punti e selezionare **Repository personalizzati**.
3. Aggiungere `https://github.com/Frequencies/home_assistant_buspro` con la
   categoria **Integrazione**.
4. Cercare **HDL Buspro**, aprirlo e selezionare **Scarica**.
5. Riavviare Home Assistant quando richiesto da HACS.

Le versioni future potranno essere installate da **HACS > Integrazioni**.
Riavviare Home Assistant dopo ogni aggiornamento dell'integrazione.

### Installazione manuale

1. Scaricare il repository dell'integrazione.
2. Copiare la directory `custom_components/buspro` in
   `/config/custom_components/buspro` di Home Assistant.
3. Riavviare Home Assistant.

## Prima configurazione

### Configurazione del gateway
1. Aprire **Impostazioni > Dispositivi e servizi > Aggiungi integrazione** e
   selezionare **HDL Buspro**.
2. Inserire l'host del gateway e le porte UDP. La porta normale è `6000`.
3. Inserire un indirizzo Buspro libero per Home Assistant nel formato
   `sottorete.dispositivo`. L'impostazione predefinita è `200.200`; non deve
   appartenere a nessun altro dispositivo Buspro.

### Aggiungere dispositivi
Dopo aver completato la configurazione del gateway:

1. Aprire **Impostazioni > Dispositivi e servizi > HDL Buspro > Configura**.
2. Selezionare **Aggiungi dispositivo** per aggiungere un modulo Buspro fisico.
3. **Selezionare il tipo di dispositivo**: scegliere la funzione (Relè, Dimmer,
   Ventilatore, Tenda, Multisensore, ecc.).
4. **Selezionare il modello esatto**: scegliere il modello corrispondente
   all'hardware. Questo determina il numero di canali.
   - Per modelli sconosciuti, scegliere il profilo **Generico** e specificare il
     numero di canali.
5. **Inserire l'indirizzo Buspro**: l'indirizzo fisico sottorete.dispositivo del
   modulo (ad es., `1.5`).
6. **Inserire il nome del dispositivo**: un nome da visualizzare (ad es.,
   "Luci del salotto").
7. **Denominare ogni canale**: assegnare un nome a ogni canale o funzione che
   desiderate utilizzare.
   - Esempio: per un relè a 4 canali, denominare i canali "Luce del soffitto",
     "Lampada da tavolo", ecc.
   - **Lasciare un nome vuoto per disabilitare quel canale** — non verrà creata
     nessuna entità.
8. Selezionare **Salva** per creare il dispositivo e le relative entità.

Home Assistant raggruppa automaticamente tutte le entità di un modulo fisico
sotto una singola voce del Registro dispositivi e ricarica la voce di
configurazione.

### Modificare dispositivi

Per modificare un dispositivo esistente, aprire **Configura > Modifica dispositivo**.
È possibile:
- Rinominare il dispositivo
- Rinominare, abilitare o disabilitare i singoli canali
- Modificare il modello (può modificare il numero di canali)
- Rimuovere il dispositivo completamente

I dispositivi gestiti dall'interfaccia supportano la modifica completa. I
dispositivi YAML legacy possono esporre i controlli di denominazione del
registro, ma la loro configurazione protocollo deve comunque essere modificata
in YAML. Riavviare Home Assistant dopo le modifiche YAML.

### Esempio: Aggiungere un modulo relè a 4 canali

1. Modello: `HDL-MR0410.431` (4 canali relè)
2. Indirizzo Buspro: `1.10`
3. Nome del dispositivo: "Relè del salotto"
4. Nomi dei canali:
   - Canale 1: "Luce del soffitto"
   - Canale 2: "Lampada da parete"
   - Canale 3: "" (disabilitato)
   - Canale 4: "Ventilatore"

Dopo il salvataggio, Home Assistant crea:
- `light.room_relays_ceiling_light`
- `light.room_relays_wall_lamp`
- `switch.room_relays_fan`

## Modifiche incompatibili nella versione 2.2.0

- Indirizzi, nomi, quantità dei dispositivi e assegnazioni dei canali non sono
  più incorporati nel componente. Sono memorizzati nelle opzioni della voce di
  configurazione.
- Il modello esatto determina il numero fisico di canali e le entità create.
- Un canale senza nome è disabilitato e non viene creato.
- L'indirizzo Buspro di Home Assistant viene migrato a `200.200` per
  impostazione predefinita. Deve essere libero nella rete.
- Gli eventi dei pannelli ora sono decodificati come `channel_on`,
  `channel_off`, `channel_level`, `scene` ed eventi dell'interruttore universale.
- Il costruttore `Buspro` incorporato ora richiede `client_address`.

## Aggiornamento

1. Riavviare Home Assistant dopo aver sostituito il componente.
2. Aprire **Impostazioni > Dispositivi e servizi > HDL Buspro > Configura**.
3. Controllare il gateway, le porte UDP e un indirizzo Buspro libero per Home
   Assistant.
4. Selezionare il modello esatto di ogni dispositivo e verificare i nomi dei
   canali.
5. Controllare le automazioni che usano gli eventi dei pannelli.
6. Rimuovere o commentare le vecchie entità YAML solo dopo aver verificato le
   sostituzioni gestite dall'interfaccia.

Non configurare lo stesso canale fisico contemporaneamente in YAML e tramite
l'interfaccia: si creano entità e sottoscrizioni al protocollo duplicate.

## Configurazione YAML (legacy)

La configurazione dei dispositivi YAML è completamente supportata insieme alla
gestione del gateway tramite voce di configurazione. È possibile definire luci,
tende, interruttori, ventilatori, climatizzazione, sensori e sensori binari
tramite YAML mentre il gateway viene gestito dall'interfaccia dell'integrazione.

**Nota**: I nuovi dispositivi dovrebbero utilizzare l'interfaccia
**Configura > Aggiungi dispositivo** invece di YAML, poiché fornisce
raggruppamento dei dispositivi, capacità controllate dal modello e gestione
dello stato dei canali. YAML è consigliato per:
- Dispositivi con profili non standard o legacy
- Migrazione da integrazioni Buspro più vecchie
- Automazioni complesse o modelli di sensori

### Esempio di sintassi YAML

Aggiungere al vostro `configuration.yaml`:

```yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Luce del soffitto"
        dimmable: true
      "1.5.2":
        name: "Lampada da parete"
        dimmable: false

cover:
  - platform: buspro
    devices:
      "2.10.1":
        name: "Tenda del salotto"
        running_time: 45

climate:
  - platform: buspro
    devices:
      "3.1":
        name: "Climatizzazione della camera"
        profile: "ac"
```

### Configurazione della piattaforma

Ogni piattaforma (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`,
`switch`) accetta:

| Chiave | Tipo | Descrizione |
| --- | --- | --- |
| `devices` | dict | Obbligatorio. Mappatura degli indirizzi Buspro alle configurazioni dei dispositivi. |
| `running_time` | int | Tempo di transizione predefinito in secondi (0 = nessuna transizione). Sovrascrivibile per dispositivo. |
| `ack_retry_enabled` | bool | Ritenta gli invii senza ACK (predefinito della piattaforma; sovrascrivibile per dispositivo). |

Ogni chiave dispositivo è l'**indirizzo Buspro** nel formato:
- **Luce, tenda, ventilatore, interruttore**: `sottorete.dispositivo.canale` (ad es., `1.5.2`)
- **Climatizzazione, sensore, sensore binario**: `sottorete.dispositivo` (ad es., `3.1`)

Ogni configurazione dispositivo supporta:
- `name` (obbligatorio): Nome da visualizzare
- `running_time`, `dimmable`, `ack_retry_enabled` (specifico della piattaforma, opzionale)
- `profile` (opzionale, per sensori climatici — ad es., `"ac"`, `"floor_heating"`)
- `object_id` (opzionale): Slug ID entità
- `unique_id` (opzionale): Per controllo manuale del registro entità

## Sviluppo

### Eseguire le suite di test

Dalla directory di configurazione di Home Assistant:

```bash
# Eseguire tutti i test di protocollo (19 test)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v

# Eseguire tutti i test di integrazione (18 test)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v

# O eseguire file di test singoli
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

I test di protocollo coprono l'analisi dei telegrammi, il coordinamento dei
dispositivi e la sicurezza di compiti/callback principali. I test di integrazione
coprono il catalogo dei dispositivi, la logica dei dispositivi gestiti, la
normalizzazione YAML e il tracciamento del supporto dei modelli.
