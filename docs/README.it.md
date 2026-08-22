# HDL Buspro per Home Assistant

[English](../README.md) | **Italiano**

L'integrazione gestisce il gateway e i dispositivi fisici HDL Buspro tramite
l'interfaccia di Home Assistant. L'elenco completo di modelli, entità e servizi
è nella [documentazione inglese](../README.md).

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

1. Aprire **Impostazioni > Dispositivi e servizi > Aggiungi integrazione** e
   selezionare **HDL Buspro**.
2. Inserire l'indirizzo del gateway e le porte UDP. La porta predefinita
   abituale è `6000`.
3. Inserire un indirizzo Buspro libero per Home Assistant nel formato
   `sottorete.dispositivo`. Il valore predefinito `200.200` non deve
   appartenere a un altro dispositivo Buspro.
4. Aprire **Configura > Aggiungi dispositivo**, selezionare il tipo e il modello
   esatto, quindi inserire l'indirizzo Buspro fisico e un nome.
5. Assegnare un nome ai canali o alle funzioni necessari. Un nome vuoto lascia
   il canale disabilitato e impedisce la creazione della relativa entità.

I modelli noti usano il numero fisso di canali o l'elenco delle funzioni del
catalogo. Per i profili generici, l'utente specifica un numero di canali entro
il limite supportato. Dopo il salvataggio, la voce di configurazione viene
ricaricata e le entità vengono raggruppate sotto un solo dispositivo fisico.

Per apportare modifiche, aprire **Configura > Modifica dispositivo**. Per i
dispositivi gestiti dall'interfaccia è possibile modificare modello, nome e
canali oppure rimuovere il dispositivo. La configurazione di protocollo dei
vecchi dispositivi YAML deve ancora essere modificata in YAML; riavviare Home
Assistant dopo la modifica.

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

## Verifica catalogo e test

Per confrontare il catalogo modelli con l'elenco ufficiale HDL mantenuto:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

Per i dispositivi YAML legacy, l'integrazione ora normalizza i profili
mancanti usando i metadati del modello. Modelli sconosciuti o profili non
validi vengono registrati come warning e ricadono su `sensor_status`.

Test mirati dell'integrazione:

```bash
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -p 'test_*.py'
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -p 'test_*.py'
```
