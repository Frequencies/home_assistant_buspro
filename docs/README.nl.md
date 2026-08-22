# HDL Buspro voor Home Assistant

[English](../README.md) | **Nederlands**

De integratie beheert de gateway en fysieke HDL Buspro-apparaten via de
Home Assistant-interface. De volledige lijst met modellen, entiteiten en
services staat in de [Engelse documentatie](../README.md).

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

1. Open **Instellingen > Apparaten & diensten > Integratie toevoegen** en
   selecteer **HDL Buspro**.
2. Voer het gatewayadres en de UDP-poorten in. De gebruikelijke standaardpoort
   is `6000`.
3. Voer een vrij Buspro-adres voor Home Assistant in als `subnet.apparaat`. De
   standaardwaarde `200.200` mag niet aan een ander Buspro-apparaat toebehoren.
4. Open **Configureren > Apparaat toevoegen**, selecteer het type en exacte
   model en voer het fysieke Buspro-adres en een naam in.
5. Geef de benodigde kanalen of functies een naam. Een lege naam houdt het
   kanaal uitgeschakeld en voorkomt dat de entiteit wordt aangemaakt.

Bekende modellen gebruiken het vaste aantal kanalen of de functielijst uit de
apparaatcatalogus. Bij generieke profielen geeft de gebruiker een kanaalaantal
binnen de ondersteunde limiet op. Na het opslaan wordt de configuratie-entry
opnieuw geladen en worden de entiteiten onder één fysiek apparaat gegroepeerd.

Open **Configureren > Apparaat bewerken** om wijzigingen aan te brengen. Voor
apparaten die via de interface worden beheerd, kunnen model, naam en kanalen
worden gewijzigd of kan het apparaat worden verwijderd. De
protocolconfiguratie van oudere YAML-apparaten moet nog steeds in YAML worden
gewijzigd; start Home Assistant daarna opnieuw.

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

## Cataloguscontrole en tests

Om de modelcatalogus te vergelijken met de bijgehouden officiële HDL-lijst:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

Voor legacy YAML-apparaten normaliseert de integratie nu ontbrekende profielen
op basis van modelmetadata. Onbekende modellen of ongeldige profielen worden
als waarschuwing gelogd en vallen terug op `sensor_status`.

Gerichte tests van de integratie:

```bash
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -p 'test_*.py'
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -p 'test_*.py'
```
