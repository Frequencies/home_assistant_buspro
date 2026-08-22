# HDL Buspro voor Home Assistant

[🇧🇾 Беларуская](../be/README.md) | [🇩🇪 Deutsch](../de/README.md) | [🇬🇧 English](../../README.md) | [🇪🇸 Español](../es/README.md) | [🇫🇷 Français](../fr/README.md) | [🇮🇹 Italiano](../it/README.md) | 🇳🇱 Nederlands | [🇳🇴 Norsk](../no/README.md) | [🇷🇺 Русский](../ru/README.md) | [🇺🇦 Українська](../uk/README.md)

De integratie beheert de gateway en fysieke HDL Buspro-apparaten via de
Home Assistant-interface. De volledige lijst met modellen, entiteiten en
services staat in de [Engelse documentatie](../README.md).

> **Belangrijke opmerking**: Voor gedetailleerde configuratie van apparaten, YAML-voorbeelden, beschikbare services en ontwikkelingsgids, raadpleeg de [Engelse documentatie](../README.md). Deze pagina biedt informatie over installatie en initiële configuratie.

## Installatie

### HACS (aanbevolen)

1. Open **HACS > Integraties**.
2. Open het menu met de drie punten en selecteer **Aangepaste repositories**.
3. Voeg `https://github.com/Frequencies/home_assistant_buspro` toe met de
   categorie **Integratie**.
4. Zoek **HDL Buspro**, open het en selecteer **Downloaden**.
5. Start Home Assistant opnieuw wanneer HACS daarom vraagt.

Latere versies kunnen via **HACS > Integraties** worden geïnstalleerd. Start
Home Assistant na elke update van de integratie opnieuw.

### Handmatige installatie

1. Download de repository van de integratie.
2. Kopieer de map `custom_components/buspro` naar
   `/config/custom_components/buspro` in Home Assistant.
3. Start Home Assistant opnieuw.

## Eerste configuratie

### Gatewayconfiguratie
1. Open **Instellingen > Apparaten & diensten > Integratie toevoegen** en
   selecteer **HDL Buspro**.
2. Voer de gatewayhost en UDP-poorten in. De normale poort is `6000`.
3. Voer een vrij Buspro-adres voor Home Assistant in als `subnet.apparaat`.
   De standaardwaarde is `200.200`; deze mag niet aan een ander Buspro-apparaat
   toebehoren.

### Apparaten toevoegen
Nadat u de gatewayconfiguratie hebt voltooid:

1. Open **Instellingen > Apparaten & diensten > HDL Buspro > Configureren**.
2. Selecteer **Apparaat toevoegen** en kies het type (Relais, Dimmer, Ventilator, Gordijn, enz.).
3. Selecteer het model (of **Generiek** voor onbekende modellen met aantal kanalen).
4. Voer Buspro-adres, apparaatnaam en kanaalnamen in (lege namen schakelen kanalen uit).
5. Selecteer **Opslaan**.

Home Assistant groepeert automatisch alle entiteiten onder één apparaatregistervermelding.

**Voor gedetailleerde UI- en YAML-configuratievoorbeelden voor alle apparaattypes, zie [../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md).**

### Apparaten bewerken

Open **Configureren > Apparaat bewerken** om een bestaand apparaat te wijzigen.
U kunt:
- Het apparaat hernoemen
- Individuele kanalen hernoemen, inschakelen of uitschakelen
- Het model wijzigen (kan het aantal kanalen veranderen)
- Het apparaat volledig verwijderen

Via de interface beheerde apparaten ondersteunen volledige bewerking. Legacy
YAML-apparaten kunnen naamgevingsbesturingselementen van het register
beschikbaar stellen, maar hun protocolconfiguratie moet nog steeds in YAML
worden gewijzigd. Start Home Assistant opnieuw na YAML-wijzigingen.

### Voorbeeld: 4-kanaals relaismodule toevoegen

1. Model: `HDL-MR0410.431` (4 relaiskanalen)
2. Buspro-adres: `1.10`
3. Apparaatnaam: "Kamer relais"
4. Kanaalnamen:
   - Kanaal 1: "Plafondlicht"
   - Kanaal 2: "Wandlamp"
   - Kanaal 3: "" (uitgeschakeld)
   - Kanaal 4: "Ventilator"

Na het opslaan maakt Home Assistant:
- `light.room_relays_ceiling_light`
- `light.room_relays_wall_lamp`
- `switch.room_relays_fan`

Voor volledige UI- en YAML-voorbeelden voor alle apparaattypen, raadpleeg **[../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md)**.

## Configuratieopties

De buspro-integratie ondersteunt zowel **UI-instellingen** als **YAML-configuratie**:

### UI-instellingen
De gemakkelijkste manier om apparaten toe te voegen — raadpleeg **[../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md)** voor stap-voor-stap voorbeelden van alle apparaattypen.

### YAML-configuratie  
De integratie ondersteunt twee aanvullende YAML-benaderingen:
- **Entity-Centric** (Legacy) — individuele entiteitsbestanden, georganiseerd op domeinen
- **Device-Centric** (Modern) — volledige apparaatdefinities met alle kanalen

**Voor volledige YAML-documentatie, voorbeelden en best practices, raadpleeg [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md)** (ook beschikbaar in [English](../en/DUAL_MODE_YAML.md) | [Беларуская](../en/DUAL_MODE_YAML.md) | [Deutsch](../en/DUAL_MODE_YAML.md) | [Español](../en/DUAL_MODE_YAML.md) | [Français](../en/DUAL_MODE_YAML.md) | [Italiano](../en/DUAL_MODE_YAML.md) | [Norsk](../en/DUAL_MODE_YAML.md) | [Русский](../en/DUAL_MODE_YAML.md) | [Українська](../en/DUAL_MODE_YAML.md))

## Incompatibele wijzigingen in 2.2.0

- Adressen, namen, aantallen apparaten en kanaaltoewijzingen zijn niet langer
  ingebouwd in de integratie. Ze worden opgeslagen in de opties van de
  configuratie-entry.
- Het exacte model bepaalt het fysieke aantal kanalen en de gemaakte entiteiten.
- Een kanaal zonder naam is uitgeschakeld en wordt niet aangemaakt.
- Het Buspro-adres van Home Assistant wordt standaard gemigreerd naar
  `200.200`. Dit adres moet vrij zijn op het netwerk.
- Paneelgebeurtenissen worden nu gedecodeerd als `channel_on`, `channel_off`,
  `channel_level`, `scene` en universele-schakelaargebeurtenissen.
- De ingebouwde `Buspro`-constructor vereist nu `client_address`.

## Bijwerken

1. Start Home Assistant opnieuw nadat het component is vervangen.
2. Open **Instellingen > Apparaten & diensten > HDL Buspro > Configureren**.
3. Controleer de gateway, UDP-poorten en een vrij Buspro-adres voor Home
   Assistant.
4. Selecteer voor elk apparaat het exacte model en controleer de kanaalnamen.
5. Controleer automatiseringen die paneelgebeurtenissen gebruiken.
6. Verwijder oude YAML-entiteiten pas of zet ze pas in commentaar nadat de via
   de interface beheerde vervangers zijn gecontroleerd.

Configureer hetzelfde fysieke kanaal niet tegelijk in YAML en via de
interface. Dit veroorzaakt dubbele entiteiten en protocolabonnementen.

## YAML-configuratie (verouderd)

YAML-apparaatconfiguratie wordt volledig ondersteund naast gatewaybeheer via
configuratie-entry. U kunt lampen, gordijnen, schakelaars, ventilators,
klimaatbeheersing, sensoren en binaire sensoren via YAML definiëren terwijl de
gateway via de integratieinterface wordt beheerd.

**Opmerking**: Nieuwe apparaten moeten de interface **Configureren > Apparaat
toevoegen** gebruiken in plaats van YAML, omdat deze apparaatgroepering,
modelsturende mogelijkheden en beheer van kanaaltoestand biedt. YAML wordt
aanbevolen voor:
- Apparaten met niet-standaard of verouderde profielen
- Migratie van oudere Buspro-integraties
- Complexe automatisering of sensorsjablonen

### YAML-syntaxisvoorbeeld

Voeg toe aan uw `configuration.yaml`:

```yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Plafondlicht"
        dimmable: true
      "1.5.2":
        name: "Wandlamp"
        dimmable: false

cover:
  - platform: buspro
    devices:
      "2.10.1":
        name: "Woonkamergordijn"
        running_time: 45

climate:
  - platform: buspro
    devices:
      "3.1":
        name: "Slaapkamer klimaat"
        profile: "ac"
```

### Platformconfiguratie

Elk platform (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`,
`switch`) accepteert:

| Sleutel | Type | Beschrijving |
| --- | --- | --- |
| `devices` | dict | Vereist. Toewijzing van Buspro-adressen aan apparaatconfiguraties. |
| `running_time` | int | Standaard overgangstijd in seconden (0 = geen overgang). Per apparaat overschrijfbaar. |
| `ack_retry_enabled` | bool | Verzend opnieuw zonder ACK (platformstandaard; per apparaat overschrijfbaar). |

Elke apparaatsleutel is het **Buspro-adres** in formaat:
- **Lamp, gordijn, ventilator, schakelaar**: `subnet.apparaat.kanaal` (bijv., `1.5.2`)
- **Klimaat, sensor, binaire sensor**: `subnet.apparaat` (bijv., `3.1`)

Elke apparaatconfiguratie ondersteunt:
- `name` (vereist): Weergavenaam
- `running_time`, `dimmable`, `ack_retry_enabled` (platformspecifiek, optioneel)
- `profile` (optioneel, voor klimaatsensoren — bijv., `"ac"`, `"floor_heating"`)
- `object_id` (optioneel): Entity-ID-slug
- `unique_id` (optioneel): Voor handmatige bediening van entiteitregister

## Gateway-instellingen

Voeg **HDL Buspro** toe vanuit **Instellingen > Apparaten en services** en configureer:

- **Host**: hostnaam of IPv4-adres van de HDL-gateway.
- **Poort**: primaire UDP-poort, normaal `6000`.
- **UDP-verzend-/ontvangstpoorten**: wijzig deze alleen voor een niet-standaard gateway.
- **Home Assistant Buspro-adres**: een ongebruikte `subnet.device`-identiteit, zoals de migratie standaard `200.200`.

UDP heeft geen verbindingshandshake. Setup valideert adresresolutie, routering en creatie van de lokale ontvangersocket zonder aan te nemen dat een apparaat bestaat onder een hardgecodeerd Buspro-adres.

## Apparaatbeheer

Open **Configureren** in de integratie en kies:

- **Gateway-instellingen** om netwerkinstellingen en clientidentiteit bij te werken.
- **Apparaat toevoegen** om een apparaattype, model, Buspro-adres en kanaal- of capaciteitsnamen te selecteren.
- **Apparaat bewerken** om kanalen een nieuwe naam te geven, kanalen in of uit te schakelen, een door de gebruikersinterface beheerd apparaat te verwijderen of het model van een bestaande registervermelding te corrigeren.

Fysieke adressen worden in Home Assistant weergegeven als het serienummer van het apparaat. Entities die tot één fysieke module behoren, zijn gekoppeld aan één apparaatregistervermelding.

## Ondersteunde modellen

| Model | Home Assistant-ondersteuning |
| --- | --- |
| `HDL-MBUS01IP.431` | Metagegevens gatewayapparaat |
| `HDL-MCLog.431` | Connectiviteit, firmwarequery, laatst gezien, logicagebeurtenissen |
| `HDL-MR0410.431` | 4 relaiskanalen |
| `HDL-MR0810.432` | 8 relaiskanalen |
| `HDL-MR1210.433` | 12 relaiskanalen |
| `HDL-MR1610.433` | 16 relaiskanalen |
| `HDL-MR0416.431` | 4 relaiskanalen met hoog vermogen |
| `HDL-MR0416C.431` | 4 relaiskanalen met hoog vermogen |
| `HDL-MR0416D.431` | 4 relaiskanalen met hoog vermogen |
| `HDL-MR0816.432` | 8 relaiskanalen met hoog vermogen |
| `HDL-MR0816C.232` | 8 relaiskanalen met hoog vermogen |
| `HDL-MR0816D.432` | 8 relaiskanalen met hoog vermogen |
| `HDL-MR1216.433` | 12 relaiskanalen met hoog vermogen |
| `HDL-MR1616.434` | 16 relaiskanalen met hoog vermogen |
| `HDL-MR1216D.433` | 12 relaiskanalen met hoog vermogen |
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | 4/8/12 relaiskanalen met hoge stroom |
| `HDL-MD0206.432` | 2 dimkanalen |
| `HDL-MD0403.432` | 4 dimkanalen |
| `HDL-MD0602.432` | 6 dimkanalen |
| `HDL-MDT0203.433` | 2 trailing-edge dimkanalen |
| `HDL-MDT0203.532` | 2 trailing-edge dimkanalen |
| `HDL-MDT04015.433` | 4 trailing-edge dimkanalen |
| `HDL-MDT04015.532` | 4 trailing-edge dimkanalen |
| `HDL-MDT06015.433` | 6 trailing-edge dimkanalen |
| `HDL-MDT06015.533` | 6 trailing-edge dimkanalen |
| `HDL-MDLED0605.432` | 6 dimkanalen en diagnostiek |
| `HDL-MRDA0610.432` | 6 balastbesturings-dimkanalen |
| `HDL-MRDA0610.433` | 6 balastbesturings-dimkanalen |
| `SB-DN-DALI64` | Tot 64 DALI-kanalen |
| `HDL-MS04.432` | 4 droge contactkanalen |
| `HDL-MS24.232` | 24 droge contactkanalen |
| `HDL-MSP02.4C` | Temperatuur, verlichtingssterkte, beweging |
| `HDL-MSP07M.4C` | Temperatuur, verlichtingssterkte, vochtigheid, beweging, twee contacten |
| `HDL-MS08M.4C` | Temperatuur, verlichtingssterkte, beweging |
| `HDL-MS12M.4C` | Temperatuur, verlichtingssterkte, vochtigheid, beweging, twee contacten |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Temperatuur en paneelacties |
| `HDL-MPTL4.460` | Temperatuur en paneelacties |
| `HDL-MP4S/TILE.48` | Temperatuur, vier knopgebeurtenissen, paneelacties |
| `HDL-MP2B/TILE.48` | Temperatuur, twee knopgebeurtenissen, paneelacties |
| `HDL-MP4B-A/TILE.48` | Temperatuur, vier knopgebeurtenissen, paneelacties |
| `HDL-MP4B/TILE.48` | Temperatuur, vier knopgebeurtenissen, paneelacties |
| `HDL-MP2B.480` | Temperatuur, twee knopgebeurtenissen, paneelacties |
| `HDL-MP4B.480` | Temperatuur, vier knopgebeurtenissen, paneelacties |
| `HDL-MPL8.431` | Temperatuur, acht knopgebeurtenissen, paneelacties |
| `HDL-M/PT4.1` | Temperatuur, vier knopgebeurtenissen, paneelacties |
| `HDL-MFH04.432` | 4 vloerverwarming kanalen |
| `HDL-MFH06.432` | 6 vloerverwarming kanalen |
| `HDL-M/HVAC8.1` | AC-klimaatentities |
| `HDL-MPED4.431` | AC-klimaatentities |
| `HDL-MW02.431` | 2 gordijn-/ dekekanalen |
| `HDL-MWM45.431` | Gordijn-/ dekingentities (configureerbare kanalen) |

Generieke AC-, gordijn-, variabele snelheid ventilator-, aan/uit ventilator-, universele schakelaar- en paneelprofielen zijn ook beschikbaar. Hun fysieke adres en elk configureerbaar aantal uitgangen worden door de gebruiker verstrekt; ze zijn geen installatievoorraad.

Sommige modellen worden toegevoegd via familietoewijzing of generieke protocolcompatibiliteit. Bij het starten van integratie registreert Buspro expliciete modelondersteuningsnotities voor deze modellen (bijvoorbeeld modelgevalideerd versus familietoegekend gedrag) samen met gedetecteerde fysieke adressen.

Voor verouderde YAML-apparaten normaliseert de integratie nu ontbrekende profielen met behulp van catalogusmodelmetagegevens. Onbekende modellen en niet-ondersteunde profielreeksen worden gerapporteerd als startwaarschuwingen en vallen vervolgens terug op generiek `sensor_status`-gedrag om de functionaliteit van de setup te behouden.

## Hulpprogramma catalogusonderhoud

Om de integratiecatalogus te vergelijken met de onderhouden officiële HDL-modellenlijst, voert u uit:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

Het hulpprogramma leest `custom_components/buspro/devices/official_models.json` en drukt af:

- officiële modellen ontbreken in `DEVICE_CATALOG`
- catalogusmodellen niet aanwezig in de officiële lijst
- virtuele alleen-integratiegeneriekemodellen

Gebruik stricte modus voor CI-achtige controles (niet-nul uitgang wanneer officiële modellen ontbreken uit de catalogus):

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Entiteitgedrag

### Relais

Een gedeelde coördinator voert eenmaal per fysieke module een query uit op de relaisstatus en distribueert het antwoord naar alle ingeschakelde kanaalentiteiten. Uitgeschakelde kanalen abonneren zich niet en bevragen de bus niet.

### Paneelen

Bekende knoppenPaneelen maken per fysieke knop één `event`-entiteit, een `Action`-gebeurtenis en een `Last action`-sensor. UI-knopgebeurtenissentiteiten vertegenwoordigen ontvangen fysieke Buspro-knoptelegrammen; ze simuleren geen hardwaredruk.

### Dimmers

Ondersteunde dimmers kunnen connectiviteit, maximale helderheid per kanaal, laadtype en protocolgemelde minimale helderheid weergeven. `Not reported` betekent dat het apparaat de protocolsentinel in plaats van een bruikbare waarde retourneerde.

### Logicacontroller

`HDL-MCLog.431` stelt alleen-lezen connectiviteit, firmwareversie, laatst gezien en logicagebeurtenisentiteiten beschikbaar. Sommige firmware reageert niet op de standaard firmwarequery; in dat geval blijft de firmware-entiteit onbeschikbaar. Logicablokken kunnen niet worden geschreven omdat het wijzigen ervan controlleerprogrammering kan overschrijven.

## Services

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` verzendt een onbewerkt protocolcommando en mag alleen worden gebruikt met een geverifieerde HDL-bewerkingscode en payload.

## Ontwikkeling

### Test-suites uitvoeren

Vanuit de Home Assistant-configuratiemap:

```bash
# Alle protocoltests uitvoeren (19 tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v

# Alle integratietests uitvoeren (18 tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v

# Of afzonderlijke testbestanden uitvoeren
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

Protocoltests bestrijken telegramanalyse, apparaatcoördinatie en veiligheid van
kerntaken/callbacks. Integratietests bestrijken apparaatcatalogus, logica voor
beheerde apparaten, YAML-normalisatie en tracking van modelondersteuning.
