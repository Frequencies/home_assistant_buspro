# HDL Buspro

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## Talen

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

## Eerste installatie

### Gatewayconfiguratie
1. Open **Instellingen > Apparaten en services > Integratie toevoegen** en selecteer
   **HDL Buspro**.
2. Voer de gatewayhost en UDP-poorten in. Poort `6000` is de normale standaard.
3. Voer een ongebruikt Home Assistant Buspro-adres in `subnet.device`-indeling in.
   De standaardwaarde is `200.200`; deze mag niet tot een ander Buspro-apparaat behoren.

### Apparaten toevoegen
Nadat de gatewayconfiguratie is voltooid:

1. Open **Instellingen > Apparaten en services > HDL Buspro > Configureren**.
2. Klik op **Apparaat toevoegen** om een fysieke Buspro-module toe te voegen.
3. **Selecteer apparaattype** (Relay, Dimmer, Cover, Climate, Sensor, etc.).
4. **Selecteer exact model** dat overeenkomt met uw hardware.
5. **Voer Buspro-adres in** in `subnet.device`-indeling (bijv. `1.5`).
6. **Voer apparaatnaam in** (bijv. "Woonkamerlicht").
7. **Geef elk kanaal een naam** — laat leeg om een kanaal uit te schakelen.
8. Klik op **Opslaan**.

Home Assistant groepeert entiteiten automatisch per fysieke module in het Apparaatregister.

**Voor UI- en YAML-configuratievoorbeelden van alle apparaattypen, zie [DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md).**

### Apparaten bewerken

Om een bestaand apparaat te wijzigen, opent u **Configureren > Apparaat bewerken**. U kunt:
- Het apparaat hernoemen
- Afzonderlijke kanalen hernoemen, inschakelen of uitschakelen
- Het model wijzigen (wat het aantal kanalen kan veranderen)
- Het apparaat volledig verwijderen

Via de UI beheerde apparaten ondersteunen volledige bewerkingen. Verouderde YAML-apparaten kunnen registernaamcontroles zichtbaar maken, maar hun protocolconfiguratie moet nog steeds in YAML worden gewijzigd. Start Home Assistant opnieuw op na het wijzigen van YAML.

### Snelstart voorbeeld: Een 4-kanaal relaismodule toevoegen

1. Model: `HDL-MR0410.431` (4 relaiskanalen)
2. Buspro-adres: `1.10`
3. Apparaatnaam: "Kamerrelais"
4. Kanaalnamen: "Plafondlicht", "Wandlamp", "", "Ventilator"
5. Klik op **Opslaan**

Home Assistant maakt automatisch entiteiten: `light.room_relays_ceiling_light`, `light.room_relays_wall_lamp`, `switch.room_relays_fan`

Voor volledige UI- en YAML-voorbeelden voor alle apparaattypen, zie **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)**.

## Configuratieopties

De buspro-integratie ondersteunt zowel **UI-gebaseerde instellingen** als **YAML-configuratie**:

### UI-instellingen
De gemakkelijkste manier om apparaten toe te voegen — zie **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)** voor stapsgewijze voorbeelden van alle apparaattypen.

### YAML-configuratie  
De integratie ondersteunt twee complementaire YAML-benaderingen:
- **Entity-gericht** (Verouderd) — afzonderlijke entiteitbestanden, ingedeeld per domein
- **Apparaat-gericht** (Modern) — volledige apparaatdefinities met alle kanalen

**Voor volledige YAML-documentatie, voorbeelden en best practices, zie [DUAL_MODE_YAML.md](docs/en/DUAL_MODE_YAML.md)** (ook beschikbaar in [Беларуская](docs/be/DUAL_MODE_YAML.md) | [Deutsch](docs/de/DUAL_MODE_YAML.md) | [Español](docs/es/DUAL_MODE_YAML.md) | [Français](docs/fr/DUAL_MODE_YAML.md) | [Italiano](docs/it/DUAL_MODE_YAML.md) | [Nederlands](docs/nl/DUAL_MODE_YAML.md) | [Norsk](docs/no/DUAL_MODE_YAML.md) | [Русский](docs/ru/DUAL_MODE_YAML.md) | [Українська](docs/uk/DUAL_MODE_YAML.md))

## Wijzigingen in versie 2.2.0

Lees dit onderdeel voordat u een upgrade uitvoert van 2.1.x.

> [!WARNING]
> Deze versie wijzigt apparaateigendom, kanaalcreatie, paneelgebeurtenissemantiek
> en de ingebouwde Python-constructor. Voltooi de upgradecontrolekaart
> voordat u verouderde YAML verwijdert.

1. **Installatiespecifieke apparaten zijn niet meer ingebouwd in de integratie.**
   Apparaatadressen, namen, kanaaltoewijs en apparaattellingen behoren nu
   tot config-entry-opties of het Home Assistant Apparaatregister. De apparaatcatalogus
   bevat alleen hardwaremogelijkheden.

2. **Via de UI beheerde relaismodules gebruiken hun fysieke kanaalwaarde.**
   `HDL-MR1210.433` stelt altijd 12 kanaalssleuven beschikbaar en
   `HDL-MR1610.433` stelt altijd 16 beschikbaar. Een bestaand apparaat kan niet
   onder de fysieke kanaalwaarde van het model worden teruggebracht.

3. **Een lege kanaalnaam schakelt het kanaal uit.**
   Uitgeschakelde kanalen zijn niet geïnstantieerd, maken geen protocolobjecten aan, en
   zijn gemarkeerd als uitgeschakeld door de integratie in het Entiteitenregister. Het invoeren van een
   naam schakelt het kanaal opnieuw in.

4. **Het exacte model bepaalt gegenereerde entiteiten.**
   Een generiek `HDL-paneel` heeft geen bekende knopwaarde. Selecteer het fysieke model
   om knoopgebeurtenissen te creëren. Als u een model wijzigt, wordt de config-entry opnieuw geladen.

5. **Home Assistant heeft zijn eigen Buspro-adres.**
   Bestaande config-entries migreren naar `200.200`. Dit adres moet ongebruikt zijn op
   het Buspro-netwerk en kan worden gewijzigd onder **Configureren > Gatewaytinstellingen**.

6. **Pakketbron-IP is niet meer hardgecodeerd.**
   De integratie leidt dit af van de route naar de geconfigureerde gateway. Een
   Home Assistant-host met meerdere interfaces moet de gateway routeren via de
   beoogde LAN-interface.

7. **Paneelactigebeurtenissen zijn nu gedecodeerd.**
   Automatiseringen die oude onbewerkte actiewaarden gebruiken, moeten worden gecontroleerd. Gebeurtenissen gebruiken
   `channel_on`, `channel_off`, `channel_level`, `scene`,
   `universal_switch_on`, of `universal_switch_off`, met doel- en samenvattingskenmerken
   waar deze kunnen worden opgelost.

8. **De ingebouwde Python-API is gewijzigd.**
   Directe `pybuspro.Buspro`-gebruikers moeten `client_address` verstrekken; zie
   [pybuspro/README.md](pybuspro/README.md).

De integratie leest nog steeds verouderde YAML-entiteiten tijdens migratie. Voer niet
hetzelfde fysieke kanaal in beide YAML en UI-beheerde configuratie in, omdat
dit kan leiden tot dubbele entiteiten en dubbele protocolabonnementen.

## Upgradecontrolekaart

1. Start Home Assistant opnieuw op na het vervangen van het aangepaste onderdeel.
2. Open **Instellingen > Apparaten en services > HDL Buspro > Configureren**.
3. Controleer de gatewayhost, -poorten en ongebruikt Home Assistant Buspro-adres.
4. Open elk fysiek apparaat en selecteer het exacte model.
5. Controleer elke relaiskanaalnaam. Lege kanalen blijven opzettelijk uitgeschakeld.
6. Controleer automatiseringen die paneelactigebeurtenissen gebruiken.
7. Verwijder of verwijder gemigreerde YAML-entiteiten alleen nadat hun UI-beheerde
   vervangingen de verwachte entiteit-ID's hebben behouden.

## Gatewaytup

Voeg **HDL Buspro** toe vanuit **Instellingen > Apparaten en services** en configureer:

- **Host**: HDL IP-gatewayhostnaam of IPv4-adres.
- **Poort**: primaire UDP-poort, doorgaans `6000`.
- **UDP-poorten verzenden/ontvangen**: wijzig deze alleen voor een niet-standaard gateway.
- **Home Assistant Buspro-adres**: een ongebruikte `subnet.device`-identiteit, zoals
  de standaardmigratie `200.200`.

UDP heeft geen verbindingshanddruk. De installatie valideert adresresolutie, routering
en creatie van de lokale ontvangzocket zonder aan te nemen dat een apparaat
aanwezig is op een hardgecodeerd Buspro-adres.

## Apparaatbeheer

Open **Configureren** op de integratie en kies:

- **Gatewaytinstellingen** om netwerkinstellingen en clientidentiteit bij te werken.
- **Apparaat toevoegen** om een apparaattype, model, Buspro-adres en kanaal- of
  mogelijkheidsnamen te selecteren.
- **Apparaat bewerken** om kanaalnamen te wijzigen, kanalen in- of uit te schakelen, een
  UI-beheerd apparaat te verwijderen, of het model van een bestaand registerapparaat te corrigeren.

Fysieke adressen worden in Home Assistant weergegeven als het serienummer van het apparaat.
Entiteiten die tot één fysieke module behoren, zijn gekoppeld aan dezelfde
Apparaatregistervermelding.

## Ondersteunde modellen

| Model | Home Assistant-ondersteuning |
| --- | --- |
| `HDL-MBUS01IP.431` | Metadata apparaatgateway |
| `HDL-MCLog.431` | Verbinding, firmwarequery, laatst gezien, logica-events |
| `HDL-MR0410.431` | 4 relaiskanalen |
| `HDL-MR0810.432` | 8 relaiskanalen |
| `HDL-MR1210.433` | 12 relaiskanalen |
| `HDL-MR1610.433` | 16 relaiskanalen |
| `HDL-MR0416.431` | 4 hogedruk relaiskanalen |
| `HDL-MR0416C.431` | 4 hogedruk relaiskanalen |
| `HDL-MR0416D.431` | 4 hogedruk relaiskanalen |
| `HDL-MR0816.432` | 8 hogedruk relaiskanalen |
| `HDL-MR0816C.232` | 8 hogedruk relaiskanalen |
| `HDL-MR0816D.432` | 8 hogedruk relaiskanalen |
| `HDL-MR1216.433` | 12 hogedruk relaiskanalen |
| `HDL-MR1616.434` | 16 hogedruk relaiskanalen |
| `HDL-MR1216D.433` | 12 hogedruk relaiskanalen |
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | 4/8/12 relaiskanalenmet hoge stroom |
| `HDL-MD0206.432` | 2 dimmerkanalen |
| `HDL-MD0403.432` | 4 dimmerkanalen |
| `HDL-MD0602.432` | 6 dimmerkanalen |
| `HDL-MDT0203.433` | 2 uitvloeiende dimmerkanalen |
| `HDL-MDT0203.532` | 2 uitvloeiende dimmerkanalen |
| `HDL-MDT04015.433` | 4 uitvloeiende dimmerkanalen |
| `HDL-MDT04015.532` | 4 uitvloeiende dimmerkanalen |
| `HDL-MDT06015.433` | 6 uitvloeiende dimmerkanalen |
| `HDL-MDT06015.533` | 6 uitvloeiende dimmerkanalen |
| `HDL-MDLED0605.432` | 6 dimmerkanalen en diagnostische gegevens |
| `HDL-MRDA0610.432` | 6 ballastbesturingdimmerkanalen |
| `HDL-MRDA0610.433` | 6 ballastbesturingdimmerkanalen |
| `SB-DN-DALI64` | Tot 64 DALI-kanalen |
| `HDL-MS04.432` | 4 droog-contactkanalen |
| `HDL-MS24.232` | 24 droog-contactkanalen |
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
| `HDL-M/HVAC8.1` | AC-klimaatentiteiten |
| `HDL-MPED4.431` | AC-klimaatentiteiten |
| `HDL-MW02.431` | 2 gordijn-/bedekking kanalen |
| `HDL-MWM45.431` | Gordijn-/bedekking entiteiten (configureerbare kanalen) |

Generieke AC, gordijn, variabele snelheid ventilator, aan/uit ventilator, universele schakelaar en
paneelprofielen zijn ook beschikbaar. Hun fysieke adres en eventuele configureerbare
uitvoerwaarde worden door de gebruiker verstrekt; ze zijn geen installatievoorraad.

Sommige modellen worden toegevoegd via family mapping of generieke protocolcompatibiliteit.
Tijdens integratie startup registreert Buspro expliciete modelondersteuningsnotities voor
modellen (bijvoorbeeld modelgevalideerd versus family-gemapped gedrag) samen met
gedetecteerde fysieke adressen.

Voor verouderde YAML-apparaten normaliseert de integratie nu ontbrekende profielen met
catalogusmodelmetadata. Onbekende modellen en niet-ondersteunde profieltekenreeksen worden
gerapporteerd als opstartwaarschuwingen, vervolgens fallback naar generieke `sensor_status`
gedrag om de setup functioneel te houden.

## Helper voor catalogusherstel

Om de integratiecatalogus te vergelijken met de onderhouden officiële HDL-modellijst,
voert u uit:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

De helper leest `custom_components/buspro/devices/official_models.json` en
drukt af:

- officiële modellen die ontbreken in `DEVICE_CATALOG`
- catalogusmodellen die niet aanwezig zijn in de officiële lijst
- virtuele integratie-alleen generieke modellen

Gebruik strikte modus voor CI-achtige controles (niet-nul exit wanneer officiële modellen
ontbreken in de catalogus):

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Entiteitgedrag

### Relais

Één gedeelde coördinator vraagt relaistatus eenmaal per fysieke module op en
verspreidt het antwoord naar alle ingeschakelde kanaalentiteiten. Uitgeschakelde kanalen
melden zich niet aan bij of vragen de bus niet op.

### Panelen

Bekende knoppanelen creëren één `event`-entiteit per fysieke knop, een `Action`-
gebeurtenis en een `Last action`-sensor. UI-knopgebeurtenissentiteiten vertegenwoordigen ontvangen
fysieke Buspro-knoptelegrammen; zij simuleren geen hardwaredruk.

### Dimmers

Ondersteunde dimmers kunnen verbinding, maximale helderheid per kanaal,
laadtype en door het protocol gerapporteerde minimale helderheid zichtbaar maken. `Not reported` betekent
dat het apparaat het protocolsentinel heeft geretourneerd in plaats van een bruikbare waarde.

### Logicacontroller

`HDL-MCLog.431` stelt alleen-lezen verbinding, firmwareversie, laatst gezien,
en logica-gebeurtenisentiteiten beschikbaar. Sommige firmware beantwoordt de standaard firmwarequery niet;
in dat geval blijft de firmwareentiteit niet beschikbaar. Logicablokken zijn
niet schrijfbaar omdat het wijzigen ervan programmering van de controller kan overschrijven.

## Services

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` verzendt een onbewerkte protocolcommando en mag alleen worden gebruikt met
een geverifieerde HDL-operationcode en payload.

## YAML-configuratie (verouderd)

YAML-apparaatconfiguratie wordt volledig ondersteund naast config-entry-gatewaybeheer. U kunt lichten, bedekking, schakelaars, ventilatoren, klimaat, sensoren en binaire sensoren via YAML definiëren terwijl de gateway wordt beheerd door de integratie-UI.

**Opmerking**: Nieuwe apparaten moeten de integratie **Configureren > Apparaat toevoegen** gebruiken in plaats van YAML, omdat deze apparaatgroepering, door modellen aangestuurde mogelijkheden en kanaalstatusherstel biedt. YAML wordt aanbevolen voor:
- Apparaten met niet-standaard of verouderde profielen
- Migratie van oudere Buspro-integraties
- Complexe automatisering of sensortemplates

### YAML-syntaxisvoorbeeld

Voeg aan uw `configuration.yaml` toe:

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

### Platformconfiguratie

Elk platform (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`, `switch`) accepteert:

| Sleutel | Type | Beschrijving |
| --- | --- | --- |
| `devices` | dict | Vereist. Mapping van Buspro-adressen tot apparaatconfiguraties. |
| `running_time` | int | Standaard overgangstijd in seconden (0 = geen overgang). Overschreven per apparaat. |
| `ack_retry_enabled` | bool | Verzendingen opnieuw proberen bij geen ACK (platformstandaard; per-apparaat overschrijft). |

Elke apparaatsleutel is het **Buspro-adres** in indeling:
- **Licht, bedekking, ventilator, schakelaar**: `subnet.device.channel` (bijv. `1.5.2`)
- **Klimaat, sensor, binaire_sensor**: `subnet.device` (bijv. `3.1`)

Elke apparaatconfiguratie ondersteunt:
- `name` (vereist): Weergavenaam
- `running_time`, `dimmable`, `ack_retry_enabled` (platformspecifiek, optioneel)
- `profile` (optioneel, voor klimaatsensoren — bijv. `"ac"`, `"floor_heating"`)
- `object_id` (optioneel): Entity ID-slug
- `unique_id` (optioneel): Voor handmatige entiteitenregistercontrole

## Ontwikkeling

### Voer de testsuites uit

Vanuit de Home Assistant-configuratieroot:

```bash
# Voer alle protocoltests uit (19 tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v

# Voer alle integratietests uit (18 tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v

# Of voer afzonderlijke testbestanden uit
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

Protocoltests bestrijken telegramparsering, apparaatcoördinatie en kernveiligheid op teamniveau/callback. Integratietests bestrijken apparaatcatalogus, beheerde-apparaatlogica, YAML-normalisatie en modelondersteuningstracking.
