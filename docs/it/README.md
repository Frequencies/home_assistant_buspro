# HDL Buspro per Home Assistant

[English](../../README.md) | **Italiano**

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
2. Selezionare **Aggiungi dispositivo** e scegliere il tipo (Relè, Dimmer, Ventilatore, Tenda, ecc.).
3. Selezionare il modello (o **Generico** per modelli sconosciuti con numero di canali).
4. Inserire l'indirizzo Buspro, il nome del dispositivo e i nomi dei canali (nomi vuoti disabilitano i canali).
5. Selezionare **Salva**.

Home Assistant raggruppa automaticamente tutte le entità sotto una singola voce del Registro.

**Per esempi dettagliati di configurazione UI e YAML per tutti i tipi di dispositivi, consultare [../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md).**

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

Per esempi completi di interfaccia utente e YAML per tutti i tipi di dispositivi, consulta **[../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md)**.

## Opzioni di configurazione

L'integrazione buspro supporta sia **la configurazione tramite interfaccia utente** che **la configurazione YAML**:

### Configurazione tramite interfaccia utente
Il modo più semplice per aggiungere dispositivi — consulta **[../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md)** per esempi passo dopo passo di tutti i tipi di dispositivi.

### Configurazione YAML  
L'integrazione supporta due approcci YAML complementari:
- **Basato su entità** (Legacy) — file di entità individuali, organizzati per domini
- **Basato su dispositivi** (Modern) — definizioni complete di dispositivi con tutti i canali

**Per la documentazione YAML completa, esempi e best practice, consulta [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md)** (anche disponibile in [English](../en/DUAL_MODE_YAML.md) | [Беларуская](../en/DUAL_MODE_YAML.md) | [Deutsch](../en/DUAL_MODE_YAML.md) | [Español](../en/DUAL_MODE_YAML.md) | [Français](../en/DUAL_MODE_YAML.md) | [Nederlands](../en/DUAL_MODE_YAML.md) | [Norsk](../en/DUAL_MODE_YAML.md) | [Русский](../en/DUAL_MODE_YAML.md) | [Українська](../en/DUAL_MODE_YAML.md))

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

## Configurazione del gateway

Aggiungi **HDL Buspro** da **Impostazioni > Dispositivi e servizi** e configura:

- **Host**: nome host o indirizzo IPv4 del gateway HDL.
- **Porta**: porta UDP primaria, normalmente `6000`.
- **Porte invio/ricezione UDP**: cambia solo per un gateway non standard.
- **Indirizzo Buspro di Home Assistant**: un'identità `subnet.device` inutilizzata, come la migrazione predefinita `200.200`.

UDP non ha alcun handshake di connessione. La configurazione convalida la risoluzione degli indirizzi, il routing e la creazione del socket di ricezione locale senza assumere l'esistenza di un dispositivo a un indirizzo Buspro hardcoded.

## Gestione dei dispositivi

Apri **Configura** nell'integrazione e scegli:

- **Impostazioni gateway** per aggiornare le impostazioni di rete e l'identità del client.
- **Aggiungi dispositivo** per selezionare un tipo di dispositivo, modello, indirizzo Buspro e nomi di canali o capacità.
- **Modifica dispositivo** per rinominare i canali, abilitare o disabilitare i canali, rimuovere un dispositivo gestito dall'interfaccia utente o correggere il modello di una voce del registro esistente.

Gli indirizzi fisici vengono visualizzati in Home Assistant come numero di serie del dispositivo. Le entità appartenenti a un modulo fisico sono allegate a una singola voce del Registro dispositivi.

## Modelli supportati

| Modello | Supporto Home Assistant |
| --- | --- |
| `HDL-MBUS01IP.431` | Metadati del dispositivo gateway |
| `HDL-MCLog.431` | Connettività, query firmware, ultimo accesso, eventi logica |
| `HDL-MR0410.431` | 4 canali relè |
| `HDL-MR0810.432` | 8 canali relè |
| `HDL-MR1210.433` | 12 canali relè |
| `HDL-MR1610.433` | 16 canali relè |
| `HDL-MR0416.431` | 4 canali relè alta potenza |
| `HDL-MR0416C.431` | 4 canali relè alta potenza |
| `HDL-MR0416D.431` | 4 canali relè alta potenza |
| `HDL-MR0816.432` | 8 canali relè alta potenza |
| `HDL-MR0816C.232` | 8 canali relè alta potenza |
| `HDL-MR0816D.432` | 8 canali relè alta potenza |
| `HDL-MR1216.433` | 12 canali relè alta potenza |
| `HDL-MR1616.434` | 16 canali relè alta potenza |
| `HDL-MR1216D.433` | 12 canali relè alta potenza |
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | 4/8/12 canali relè alta corrente |
| `HDL-MD0206.432` | 2 canali dimmer |
| `HDL-MD0403.432` | 4 canali dimmer |
| `HDL-MD0602.432` | 6 canali dimmer |
| `HDL-MDT0203.433` | 2 canali dimmer trailing-edge |
| `HDL-MDT0203.532` | 2 canali dimmer trailing-edge |
| `HDL-MDT04015.433` | 4 canali dimmer trailing-edge |
| `HDL-MDT04015.532` | 4 canali dimmer trailing-edge |
| `HDL-MDT06015.433` | 6 canali dimmer trailing-edge |
| `HDL-MDT06015.533` | 6 canali dimmer trailing-edge |
| `HDL-MDLED0605.432` | 6 canali dimmer e diagnostica |
| `HDL-MRDA0610.432` | 6 canali dimmer controllo balasto |
| `HDL-MRDA0610.433` | 6 canali dimmer controllo balasto |
| `SB-DN-DALI64` | Fino a 64 canali DALI |
| `HDL-MS04.432` | 4 canali contatto secco |
| `HDL-MS24.232` | 24 canali contatto secco |
| `HDL-MSP02.4C` | Temperatura, illuminamento, movimento |
| `HDL-MSP07M.4C` | Temperatura, illuminamento, umidità, movimento, due contatti |
| `HDL-MS08M.4C` | Temperatura, illuminamento, movimento |
| `HDL-MS12M.4C` | Temperatura, illuminamento, umidità, movimento, due contatti |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Temperatura e azioni pannello |
| `HDL-MPTL4.460` | Temperatura e azioni pannello |
| `HDL-MP4S/TILE.48` | Temperatura, quattro eventi pulsante, azioni pannello |
| `HDL-MP2B/TILE.48` | Temperatura, due eventi pulsante, azioni pannello |
| `HDL-MP4B-A/TILE.48` | Temperatura, quattro eventi pulsante, azioni pannello |
| `HDL-MP4B/TILE.48` | Temperatura, quattro eventi pulsante, azioni pannello |
| `HDL-MP2B.480` | Temperatura, due eventi pulsante, azioni pannello |
| `HDL-MP4B.480` | Temperatura, quattro eventi pulsante, azioni pannello |
| `HDL-MPL8.431` | Temperatura, otto eventi pulsante, azioni pannello |
| `HDL-M/PT4.1` | Temperatura, quattro eventi pulsante, azioni pannello |
| `HDL-MFH04.432` | 4 canali riscaldamento pavimento |
| `HDL-MFH06.432` | 6 canali riscaldamento pavimento |
| `HDL-M/HVAC8.1` | Entità clima AC |
| `HDL-MPED4.431` | Entità clima AC |
| `HDL-MW02.431` | 2 canali tenda / copertura |
| `HDL-MWM45.431` | Entità tenda / copertura (canali configurabili) |

Sono disponibili anche profili generici AC, tenda, ventilatore a velocità variabile, ventilatore on/off, interruttore universale e pannello. Il loro indirizzo fisico e il numero di uscite configurabili sono forniti dall'utente; non sono inventario di installazione.

Alcuni modelli vengono aggiunti tramite mapping famiglia o compatibilità protocollo generica. Durante l'avvio dell'integrazione, Buspro registra note di supporto modello esplicite per questi modelli (ad esempio, comportamento convalidato da modello rispetto al comportamento mappato da famiglia) insieme agli indirizzi fisici rilevati.

Per dispositivi YAML legacy, l'integrazione ora normalizza i profili mancanti utilizzando i metadati del catalogo modelli. I modelli sconosciuti e le stringhe di profilo non supportate vengono segnalati come avvisi di avvio, quindi tornano al comportamento generico `sensor_status` per mantenere la funzionalità della configurazione.

## Assistente manutenzione catalogo

Per confrontare il catalogo di integrazione con l'elenco di modelli HDL ufficiale mantenuto, esegui:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

L'assistente legge `custom_components/buspro/devices/official_models.json` e stampa:

- modelli ufficiali mancanti in `DEVICE_CATALOG`
- modelli catalogo non presenti nell'elenco ufficiale
- modelli generici virtuali solo per integrazione

Usa modalità rigorosa per verifiche in stile CI (uscita diversa da zero quando mancano modelli ufficiali nel catalogo):

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Comportamento entità

### Relè

Un coordinatore condiviso interroga lo stato del relè una volta per modulo fisico e distribuisce la risposta a tutte le entità canale abilitate. I canali disabilitati non si sottoscrivono o non interrogano il bus.

### Pannelli

I pannelli pulsanti noti creano un'entità `event` per pulsante fisico, un evento `Action` e un sensore `Last action`. Le entità degli eventi pulsante dell'interfaccia utente rappresentano i telegrammi dei pulsanti Buspro fisici ricevuti; non simulano una pressione hardware.

### Dimmer

I dimmer supportati possono esporre connettività, luminosità massima per canale, tipo di carico e luminosità minima segnalata dal protocollo. `Not reported` significa che il dispositivo ha restituito la sentinella del protocollo anziché un valore utilizzabile.

### Controller logica

`HDL-MCLog.431` espone connettività di sola lettura, versione firmware, ultimo accesso ed entità eventi logica. Alcuni firmware non rispondono alla query firmware standard; in questo caso l'entità firmware rimane non disponibile. I blocchi logica non sono scrivibili perché modificarli può sovrascrivere la programmazione del controller.

## Servizi

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` invia un comando protocollo grezzo e deve essere utilizzato solo con un codice operazione HDL e un payload verificati.

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
