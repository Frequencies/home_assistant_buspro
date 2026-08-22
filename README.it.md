# HDL Buspro

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## Lingue

[![English](https://flagcdn.com/24x18/gb.png) English](README.md) |
[![Deutsch](https://flagcdn.com/24x18/de.png) Deutsch](README.de.md) |
[![Français](https://flagcdn.com/24x18/fr.png) Français](README.fr.md) |
[![Nederlands](https://flagcdn.com/24x18/nl.png) Nederlands](README.nl.md) |
[![Español](https://flagcdn.com/24x18/es.png) Español](README.es.md) |
[![Italiano](https://flagcdn.com/24x18/it.png) Italiano](README.it.md) |
[![Русский](https://flagcdn.com/24x18/ru.png) Русский](README.ru.md) |
[![Українська](https://flagcdn.com/24x18/ua.png) Українська](README.uk.md) |
[![Беларуская](https://flagcdn.com/24x18/by.png) Беларуская](README.be.md) |
[![Norsk](https://flagcdn.com/24x18/no.png) Norsk](README.no.md)


## Configurazione iniziale

### Configurazione del gateway
1. Aprire **Settings > Devices & services > Add integration** e selezionare
   **HDL Buspro**.
2. Inserire l'host del gateway e le porte UDP. La porta `6000` è il valore predefinito normale.
3. Inserire un indirizzo Buspro di Home Assistant non utilizzato nel formato `subnet.device`.
   L'impostazione predefinita è `200.200`; non deve appartenere a un altro dispositivo Buspro.

### Aggiunta di dispositivi
Dopo che la configurazione del gateway è completata:

1. Aprire **Settings > Devices & services > HDL Buspro > Configure**.
2. Fare clic su **Add device** per aggiungere un modulo fisico Buspro.
3. **Selezionare il tipo di dispositivo** (Relay, Dimmer, Cover, Climate, Sensor, ecc.).
4. **Selezionare il modello esatto** che corrisponde all'hardware.
5. **Inserire l'indirizzo Buspro** nel formato `subnet.device` (ad es., `1.5`).
6. **Inserire il nome del dispositivo** (ad es., "Living room lights").
7. **Assegnare un nome a ciascun canale** — lasciare vuoto per disabilitare un canale.
8. Fare clic su **Save**.

Home Assistant raggruppa automaticamente le entità per modulo fisico nel Device Registry.

**Per esempi di configurazione UI e YAML per tutti i tipi di dispositivo, vedere [DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md).**

### Modifica dei dispositivi

Per modificare un dispositivo esistente, aprire **Configure > Edit device**. È possibile:
- Rinominare il dispositivo
- Rinominare, abilitare o disabilitare i singoli canali
- Modificare il modello (che potrebbe cambiare il numero di canali)
- Rimuovere completamente il dispositivo

I dispositivi gestiti dall'UI supportano la modifica completa. I dispositivi legacy YAML possono esporre i controlli di denominazione del registro, ma la loro configurazione del protocollo deve comunque essere modificata in YAML. Riavviare Home Assistant dopo la modifica di YAML.

### Esempio rapido: Aggiunta di un modulo relay a 4 canali

1. Modello: `HDL-MR0410.431` (4 canali relay)
2. Indirizzo Buspro: `1.10`
3. Nome del dispositivo: "Room relays"
4. Nomi dei canali: "Ceiling light", "Wall lamp", "", "Fan"
5. Fare clic su **Save**

Home Assistant crea automaticamente le entità: `light.room_relays_ceiling_light`, `light.room_relays_wall_lamp`, `switch.room_relays_fan`

Per esempi completi di UI e YAML per tutti i tipi di dispositivo, vedere **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)**.

## Opzioni di configurazione

L'integrazione buspro supporta sia la **configurazione basata su UI** che la **configurazione YAML**:

### Configurazione UI
Il modo più semplice per aggiungere dispositivi — vedere **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)** per esempi dettagliati di tutti i tipi di dispositivo.

### Configurazione YAML  
L'integrazione supporta due approcci YAML complementari:
- **Entity-Centric** (Legacy) — file di entità individuali organizzati per dominio
- **Device-Centric** (Modern) — definizioni complete dei dispositivi con tutti i canali

**Per la documentazione YAML completa, gli esempi e le best practice, vedere [DUAL_MODE_YAML.md](docs/en/DUAL_MODE_YAML.md)** (disponibile anche in [Беларуская](docs/be/DUAL_MODE_YAML.md) | [Deutsch](docs/de/DUAL_MODE_YAML.md) | [Español](docs/es/DUAL_MODE_YAML.md) | [Français](docs/fr/DUAL_MODE_YAML.md) | [Italiano](docs/it/DUAL_MODE_YAML.md) | [Nederlands](docs/nl/DUAL_MODE_YAML.md) | [Norsk](docs/no/DUAL_MODE_YAML.md) | [Русский](docs/ru/DUAL_MODE_YAML.md) | [Українська](docs/uk/DUAL_MODE_YAML.md))

## Modifiche non retrocompatibili nella versione 2.2.0

Leggere questa sezione prima di eseguire l'aggiornamento dalla versione 2.1.x.

> [!WARNING]
> This release changes device ownership, channel creation, panel event
> semantics, and the embedded Python constructor. Complete the upgrade
> checklist before removing legacy YAML.

1. **I dispositivi specifici dell'installazione non sono più integrati nell'integrazione.**
   Gli indirizzi dei dispositivi, i nomi, le assegnazioni dei canali e il numero di dispositivi appartengono
   ora alle opzioni della voce di configurazione o al Device Registry di Home Assistant. Il catalogo dei dispositivi contiene solo le capacità hardware.

2. **I moduli relay gestiti dall'UI utilizzano il numero di canali fisici.**
   `HDL-MR1210.433` espone sempre 12 slot di canale e
   `HDL-MR1610.433` espone sempre 16. Un dispositivo esistente non può essere ridotto
   al di sotto del numero di canali fisici del modello.

3. **Un nome di canale vuoto disabilita il canale.**
   I canali disabilitati non vengono istanziati, non creano oggetti di protocollo e
   sono contrassegnati come disabilitati dall'integrazione nel Device Registry. L'inserimento di un
   nome abilita di nuovo il canale.

4. **Il modello esatto controlla le entità generate.**
   Un `HDL panel` generico non ha un numero di pulsanti noto. Selezionare il modello fisico
   per creare gli eventi dei pulsanti. La modifica di un modello ricarica la voce di configurazione.

5. **Home Assistant ha il suo indirizzo Buspro.**
   Le voci di configurazione esistenti vengono migrate a `200.200`. Questo indirizzo deve essere inutilizzato sulla
   rete Buspro e può essere modificato in **Configure > Gateway settings**.

6. **L'IP di origine dei pacchetti non è più hardcoded.**
   L'integrazione lo deriva dalla rotta verso il gateway configurato. Un
   host Home Assistant con più interfacce deve instradare il gateway attraverso l'interfaccia
   LAN desiderata.

7. **Gli eventi delle azioni del pannello sono ora decodificati.**
   Le automazioni che utilizzano i vecchi valori di azione grezza devono essere controllate. Gli eventi utilizzano
   `channel_on`, `channel_off`, `channel_level`, `scene`,
   `universal_switch_on`, o `universal_switch_off`, con attributi target e summary dove
   possono essere risolti.

8. **L'API Python incorporata è stata modificata.**
   Gli utenti diretti di `pybuspro.Buspro` devono fornire `client_address`; vedere
   [pybuspro/README.md](pybuspro/README.md).

L'integrazione continua a leggere le entità YAML legacy durante la migrazione. Non mantenere
lo stesso canale fisico sia nella configurazione YAML che in quella gestita dall'UI, perché
ciò potrebbe creare entità duplicate e sottoscrizioni di protocollo duplicate.

## Checklist di aggiornamento

1. Riavviare Home Assistant dopo aver sostituito il componente personalizzato.
2. Aprire **Settings > Devices & services > HDL Buspro > Configure**.
3. Controllare l'host del gateway, le porte e l'indirizzo Buspro di Home Assistant inutilizzato.
4. Aprire ogni dispositivo fisico e selezionare il modello esatto.
5. Controllare il nome di ogni canale relay. I canali vuoti rimangono intenzionalmente disabilitati.
6. Verificare le automazioni che utilizzano gli eventi delle azioni del pannello.
7. Rimuovere o commentare le entità YAML migrate solo dopo che i loro sostituti gestiti dall'UI
   hanno mantenuto gli ID entità previsti.

## Configurazione del gateway

Aggiungere **HDL Buspro** da **Settings > Devices & services** e configurare:

- **Host**: nome host del gateway IP HDL o indirizzo IPv4.
- **Port**: porta UDP primaria, normalmente `6000`.
- **UDP send/receive ports**: modificare solo per un gateway non standard.
- **Home Assistant Buspro address**: un'identità `subnet.device` inutilizzata, come
  il valore predefinito di migrazione `200.200`.

UDP non ha un handshake di connessione. La configurazione convalida la risoluzione degli indirizzi, il routing,
e la creazione del socket di ricezione locale senza presupporre che un dispositivo esista
a un indirizzo Buspro hardcoded.

## Gestione dei dispositivi

Aprire **Configure** sull'integrazione e scegliere:

- **Gateway settings** per aggiornare le impostazioni di rete e l'identità del client.
- **Add device** per selezionare un tipo di dispositivo, un modello, un indirizzo Buspro e nomi di canali o
  capacità.
- **Edit device** per rinominare i canali, abilitare o disabilitare i canali, rimuovere un
  dispositivo gestito dall'UI, o correggere il modello di una voce di registro esistente.

Gli indirizzi fisici sono visualizzati in Home Assistant come il numero di serie del dispositivo.
Le entità appartenenti a un modulo fisico sono allegate alla stessa voce del Device
Registry.

## Modelli supportati

| Modello | Supporto di Home Assistant |
| --- | --- |
| `HDL-MBUS01IP.431` | Metadati del dispositivo gateway |
| `HDL-MCLog.431` | Connettività, query del firmware, ultimo accesso, eventi logici |
| `HDL-MR0410.431` | 4 canali relay |
| `HDL-MR0810.432` | 8 canali relay |
| `HDL-MR1210.433` | 12 canali relay |
| `HDL-MR1610.433` | 16 canali relay |
| `HDL-MR0416.431` | 4 canali relay ad alta potenza |
| `HDL-MR0416C.431` | 4 canali relay ad alta potenza |
| `HDL-MR0416D.431` | 4 canali relay ad alta potenza |
| `HDL-MR0816.432` | 8 canali relay ad alta potenza |
| `HDL-MR0816C.232` | 8 canali relay ad alta potenza |
| `HDL-MR0816D.432` | 8 canali relay ad alta potenza |
| `HDL-MR1216.433` | 12 canali relay ad alta potenza |
| `HDL-MR1616.434` | 16 canali relay ad alta potenza |
| `HDL-MR1216D.433` | 12 canali relay ad alta potenza |
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | 4/8/12 canali relay ad alta corrente |
| `HDL-MD0206.432` | 2 canali dimmer |
| `HDL-MD0403.432` | 4 canali dimmer |
| `HDL-MD0602.432` | 6 canali dimmer |
| `HDL-MDT0203.433` | 2 canali dimmer a margine posteriore |
| `HDL-MDT0203.532` | 2 canali dimmer a margine posteriore |
| `HDL-MDT04015.433` | 4 canali dimmer a margine posteriore |
| `HDL-MDT04015.532` | 4 canali dimmer a margine posteriore |
| `HDL-MDT06015.433` | 6 canali dimmer a margine posteriore |
| `HDL-MDT06015.533` | 6 canali dimmer a margine posteriore |
| `HDL-MDLED0605.432` | 6 canali dimmer e diagnostica |
| `HDL-MRDA0610.432` | 6 canali dimmer di controllo del ballast |
| `HDL-MRDA0610.433` | 6 canali dimmer di controllo del ballast |
| `SB-DN-DALI64` | Fino a 64 canali DALI |
| `HDL-MS04.432` | 4 canali a contatto secco |
| `HDL-MS24.232` | 24 canali a contatto secco |
| `HDL-MSP02.4C` | Temperatura, illuminamento, movimento |
| `HDL-MSP07M.4C` | Temperatura, illuminamento, umidità, movimento, due contatti |
| `HDL-MS08M.4C` | Temperatura, illuminamento, movimento |
| `HDL-MS12M.4C` | Temperatura, illuminamento, umidità, movimento, due contatti |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Temperatura e azioni del pannello |
| `HDL-MPTL4.460` | Temperatura e azioni del pannello |
| `HDL-MP4S/TILE.48` | Temperatura, quattro eventi pulsante, azioni pannello |
| `HDL-MP2B/TILE.48` | Temperatura, due eventi pulsante, azioni pannello |
| `HDL-MP4B-A/TILE.48` | Temperatura, quattro eventi pulsante, azioni pannello |
| `HDL-MP4B/TILE.48` | Temperatura, quattro eventi pulsante, azioni pannello |
| `HDL-MP2B.480` | Temperatura, due eventi pulsante, azioni pannello |
| `HDL-MP4B.480` | Temperatura, quattro eventi pulsante, azioni pannello |
| `HDL-MPL8.431` | Temperatura, otto eventi pulsante, azioni pannello |
| `HDL-M/PT4.1` | Temperatura, quattro eventi pulsante, azioni pannello |
| `HDL-MFH04.432` | 4 canali di riscaldamento a pavimento |
| `HDL-MFH06.432` | 6 canali di riscaldamento a pavimento |
| `HDL-M/HVAC8.1` | Entità climatiche AC |
| `HDL-MPED4.431` | Entità climatiche AC |
| `HDL-MW02.431` | 2 canali tenda / cover |
| `HDL-MWM45.431` | Entità tenda / cover (canali configurabili) |

I profili generici AC, tenda, ventilatore a velocità variabile, ventilatore on/off, universal-switch e
panel sono inoltre disponibili. L'indirizzo fisico e il numero di output configurabile sono
forniti dall'utente; non sono inventario di installazione.

Alcuni modelli vengono aggiunti tramite mappatura familiare o compatibilità del protocollo generico.
Durante l'avvio dell'integrazione, il log di Buspro esplicita le note di supporto del modello per quei
modelli (ad esempio, comportamento convalidato dal modello rispetto a comportamento mappato per famiglia) insieme con
gli indirizzi fisici rilevati.

Per i dispositivi YAML legacy, l'integrazione ora normalizza i profili mancanti utilizzando
i metadati del modello di catalogo. I modelli sconosciuti e le stringhe di profilo non supportate sono
segnalati come avvisi di avvio, quindi ricadono nel comportamento generico `sensor_status`
per mantenere la configurazione funzionante.

## Helper per la manutenzione del catalogo

Per confrontare il catalogo dell'integrazione con l'elenco ufficiale dei modelli HDL mantenuto, eseguire:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

L'helper legge `custom_components/buspro/devices/official_models.json` e
stampa:

- modelli ufficiali mancanti in `DEVICE_CATALOG`
- modelli di catalogo non presenti nell'elenco ufficiale
- modelli generici virtuali solo per l'integrazione

Utilizzare la modalità strict per controlli in stile CI (uscita diversa da zero quando i modelli ufficiali sono
mancanti nel catalogo):

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Comportamento delle entità

### Relay

Un coordinatore condiviso esegue una query dello stato del relay una volta per modulo fisico e
distribuisce la risposta a tutte le entità di canale abilitate. I canali disabilitati non
si sottoscrivono né eseguono query sul bus.

### Pannelli

I pannelli di pulsanti noti creano un'entità `event` per ogni pulsante fisico, un evento `Action`,
e un sensore `Last action`. Le entità degli eventi dei pulsanti dell'UI rappresentano i telegrammi fisici dei pulsanti Buspro ricevuti; non simulano una pressione hardware.

### Dimmer

I dimmer supportati possono esporre connettività, luminosità massima per canale,
tipo di carico e luminosità minima segnalata dal protocollo. `Not reported` significa che il
dispositivo ha restituito il sentinel del protocollo piuttosto che un valore utilizzabile.

### Controllore logico

`HDL-MCLog.431` espone entità di connettività, versione del firmware, ultimo accesso,
e eventi logici in sola lettura. Alcuni firmware non rispondono alla query del firmware standard;
in tal caso l'entità del firmware rimane non disponibile. I blocchi logici non sono scrivibili perché
modificarli può sovrascrivere la programmazione del controller.

## Servizi

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` invia un comando di protocollo grezzo e deve essere utilizzato solo con
un codice di operazione HDL verificato e un payload.

## Configurazione YAML (legacy)

La configurazione del dispositivo YAML è completamente supportata insieme alla gestione del gateway basata su voce di configurazione. È possibile definire luci, cover, switch, ventilatori, climate, sensori e sensori binari via YAML mentre il gateway è gestito dall'UI dell'integrazione.

**Nota**: I nuovi dispositivi devono utilizzare l'UI **Configure > Add device** dell'integrazione invece di YAML, poiché fornisce raggruppamento dei dispositivi, capacità guidate dal modello e gestione dello stato dei canali. YAML è consigliato per:
- Dispositivi con profili non standard o legacy
- Migrazione da integrazioni Buspro precedenti
- Template di automazione o sensore complessi

### Esempio di sintassi YAML

Aggiungere al vostro `configuration.yaml`:

```yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Ceiling light"
        dimmable: true
      "1.5.2":
        name: "Wall lamp"
        dimmable: false

cover:
  - platform: buspro
    devices:
      "2.10.1":
        name: "Living room curtain"
        running_time: 45

climate:
  - platform: buspro
    devices:
      "3.1":
        name: "Bedroom climate"
        profile: "ac"
```

### Configurazione della piattaforma

Ogni piattaforma (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`, `switch`) accetta:

| Chiave | Tipo | Descrizione |
| --- | --- | --- |
| `devices` | dict | Obbligatorio. Mappatura degli indirizzi Buspro alle configurazioni dei dispositivi. |
| `running_time` | int | Tempo di transizione predefinito in secondi (0 = nessuna transizione). Sostituito per dispositivo. |
| `ack_retry_enabled` | bool | Riprovare gli invii in caso di nessun ACK (impostazione predefinita della piattaforma; gli override per dispositivo). |

Ogni chiave del dispositivo è l'**indirizzo Buspro** nel formato:
- **Luce, cover, ventilatore, switch**: `subnet.device.channel` (ad es., `1.5.2`)
- **Climate, sensore, sensore binario**: `subnet.device` (ad es., `3.1`)

Ogni configurazione del dispositivo supporta:
- `name` (obbligatorio): Nome visualizzato
- `running_time`, `dimmable`, `ack_retry_enabled` (specifico della piattaforma, opzionale)
- `profile` (opzionale, per sensori climate — ad es., `"ac"`, `"floor_heating"`)
- `object_id` (opzionale): Slug dell'ID entità
- `unique_id` (opzionale): Per il controllo manuale del device registry

## Sviluppo

### Eseguire le suite di test

Dalla root di configurazione di Home Assistant:

```bash
# Eseguire tutti i test del protocollo (19 test)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v

# Eseguire tutti i test di integrazione (18 test)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v

# O eseguire file di test individuali
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

I test del protocollo coprono l'analisi dei telegrammi, il coordinamento dei dispositivi e la sicurezza di task/callback di base. I test di integrazione coprono catalogo dei dispositivi, logica dei dispositivi gestiti, normalizzazione YAML e tracciamento del supporto del modello.
