# HDL Buspro voor Home Assistant

[English](../README.md) | **Nederlands**

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
2. Selecteer **Apparaat toevoegen** om een fysieke Buspro-module toe te voegen.
3. **Selecteer apparaattype**: kies de mogelijkheid (Relais, Dimmer, Ventilator,
   Gordijn, Multisensor, enz.).
4. **Selecteer exact model**: kies het model dat uw hardware overeenkomt. Dit
   bepaalt het aantal kanalen.
   - Kies voor onbekende modellen het profiel **Generiek** en geef het aantal
     kanalen op.
5. **Voer Buspro-adres in**: het fysieke subnet.apparaat-adres van de module
   (bijv. `1.5`).
6. **Voer apparaatnaam in**: een weergavenaam (bijv. "Woonkamerlichten").
7. **Noem elk kanaal**: wijs een naam toe aan elk kanaal of functie dat u wilt
   gebruiken.
   - Voorbeeld: voor een 4-kanaals relais, noem kanalen "Plafondlicht",
     "Tafellamp", enz.
   - **Laat een naam leeg om dat kanaal uit te schakelen** — er wordt geen
     entiteit gemaakt.
8. Selecteer **Opslaan** om het apparaat en de entiteiten ervan te maken.

Home Assistant groepeert automatisch alle entiteiten van een fysieke module
onder één apparaatregistervermelding en laadt de configuratie-entry opnieuw.

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
