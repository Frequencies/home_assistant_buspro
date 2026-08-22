# HDL Buspro for Home Assistant

[🇧🇾 Беларуская](../be/README.md) | [🇩🇪 Deutsch](../de/README.md) | [🇬🇧 English](../../README.md) | [🇪🇸 Español](../es/README.md) | [🇫🇷 Français](../fr/README.md) | [🇮🇹 Italiano](../it/README.md) | [🇳🇱 Nederlands](../nl/README.md) | 🇳🇴 Norsk | [🇷🇺 Русский](../ru/README.md) | [🇺🇦 Українська](../uk/README.md)

Integrasjonen administrerer gatewayen og fysiske HDL Buspro-enheter gjennom
Home Assistant-grensesnittet. En fullstendig liste over modeller, entiteter og
tjenester finnes i den [engelske dokumentasjonen](../README.md).

## Installasjon

### HACS (anbefalt)

1. Åpne **HACS > Integrasjoner**.
2. Åpne menyen med tre prikker, og velg **Egendefinerte repositorier**.
3. Legg til `https://github.com/Frequencies/home_assistant_buspro` med
   kategorien **Integrasjon**.
4. Søk etter **HDL Buspro**, åpne den, og velg **Last ned**.
5. Start Home Assistant på nytt når HACS ber om det.

Senere versjoner kan installeres fra **HACS > Integrasjoner**. Start Home
Assistant på nytt etter hver oppdatering av integrasjonen.

### Manuell installasjon

1. Last ned integrasjonens repository.
2. Kopier katalogen `custom_components/buspro` til
   `/config/custom_components/buspro` i Home Assistant.
3. Start Home Assistant på nytt.

## Første oppsett

### Gatewaykonfigurasjon
1. Åpne **Innstillinger > Enheter og tjenester > Legg til integrasjon** og velg
   **HDL Buspro**.
2. Skriv inn gatewayvert og UDP-porter. Normal port er `6000`.
3. Skriv inn en ledig Buspro-adresse for Home Assistant på formatet
   `subnett.enhet`. Standardverdien er `200.200`; den må ikke tilhøre en annen
   Buspro-enhet.

### Legge til enheter
Etter at gatewaykonfigurasjonen er fullført:

1. Åpne **Innstillinger > Enheter og tjenester > HDL Buspro > Konfigurer**.
2. Velg **Legg til enhet** og velg type (Relé, Dimmer, Vifte, Gardin, osv.).
3. Velg modellen (eller **Generisk** for ukjente modeller med antall kanaler).
4. Skriv inn Buspro-adresse, enhetsnavn og kanaalnavn (tomme navn deaktiverer kanaler).
5. Velg **Lagre**.

Home Assistant grupperer automatisk alle entiteter under en enkelt enhetregistreringspost.

**For detaljerte UI- og YAML-konfigurasjonseksempler for alle enhetstypene, se [../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md).**

### Redigere enheter

For å endre en eksisterende enhet, åpne **Konfigurer > Rediger enhet**. Du kan:
- Gi enheten nytt navn
- Gi individuelt navn til, aktivere eller deaktivere kanaler
- Endre modell (kan endre antallet kanaler)
- Fjerne enheten helt

Via grensesnittet administrerte enheter støtter full redigering. Legacy
YAML-enheter kan vise navnegivingskontroller for registeret, men deres
protokollkonfigurasjon må fortsatt endres i YAML. Start Home Assistant på
nytt etter YAML-endringer.

### Eksempel: Legge til 4-kanals relaismodul

1. Modell: `HDL-MR0410.431` (4 relaiskanaler)
2. Buspro-adresse: `1.10`
3. Enhetsnavn: "Romrelé"
4. Kanalnavn:
   - Kanal 1: "Taklampe"
   - Kanal 2: "Vegglampe"
   - Kanal 3: "" (deaktivert)
   - Kanal 4: "Vifte"

Etter lagring opprett Home Assistant:
- `light.room_relays_ceiling_light`
- `light.room_relays_wall_lamp`
- `switch.room_relays_fan`

For komplette UI- og YAML-eksempler for alle enhetstyper, se **[../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md)**.

## Konfigurasjonsalternativer

Buspro-integrasjonen støtter både **UI-oppsett** og **YAML-konfigurasjon**:

### UI-oppsett
Den enkleste måten å legge til enheter — se **[../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md)** for trinn-for-trinn eksempler på alle enhetstyper.

### YAML-konfigurasjon  
Integrasjonen støtter to komplementære YAML-tilnærminger:
- **Entity-Centric** (Legacy) — individuelle enhetsfiler, organisert etter domener
- **Device-Centric** (Modern) — komplette enhetsdefinisioner med alle kanaler

**For fullstendig YAML-dokumentasjon, eksempler og beste praksis, se [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md)** (også tilgjengelig på [English](../en/DUAL_MODE_YAML.md) | [Беларуская](../en/DUAL_MODE_YAML.md) | [Deutsch](../en/DUAL_MODE_YAML.md) | [Español](../en/DUAL_MODE_YAML.md) | [Français](../en/DUAL_MODE_YAML.md) | [Italiano](../en/DUAL_MODE_YAML.md) | [Nederlands](../en/DUAL_MODE_YAML.md) | [Русский](../en/DUAL_MODE_YAML.md) | [Українська](../en/DUAL_MODE_YAML.md))

## Inkompatible endringer i 2.2.0

- Adresser, navn, antall enheter og kanaltilordninger er ikke lenger innebygd i
  integrasjonen. De lagres i alternativene for konfigurasjonsoppføringen.
- Den nøyaktige modellen bestemmer fysisk antall kanaler og opprettede entiteter.
- En kanal uten navn er deaktivert og opprettes ikke.
- Home Assistants Buspro-adresse migreres som standard til `200.200`. Adressen
  må være ledig på nettverket.
- Panelhendelser dekodes nå som `channel_on`, `channel_off`, `channel_level`,
  `scene` og hendelser for universalbryter.
- Den innebygde `Buspro`-konstruktøren krever nå `client_address`.

## Oppgradering

1. Start Home Assistant på nytt etter at komponenten er erstattet.
2. Åpne **Innstillinger > Enheter og tjenester > HDL Buspro > Konfigurer**.
3. Kontroller gateway, UDP-porter og en ledig Buspro-adresse for Home Assistant.
4. Velg nøyaktig modell for hver enhet, og kontroller kanalnavnene.
5. Kontroller automasjoner som bruker panelhendelser.
6. Fjern eller kommenter gamle YAML-entiteter først etter at erstatningene som
   administreres i grensesnittet, er kontrollert.

Ikke konfigurer samme fysiske kanal i både YAML og grensesnittet. Det vil
opprette dupliserte entiteter og protokollabonnementer.

## YAML-konfigurasjon (legacy)

YAML-enhetskonfigurasjon er fullt ut støttet sammen med gatewayadministrasjon
via konfigurasjonsoppføring. Du kan definere lamper, gardiner, brytere,
viftere, klimakontroll, sensorer og binære sensorer via YAML mens gatewayen
administreres av integrasjonens grensesnitt.

**Merknad**: Nye enheter bør bruke **Konfigurer > Legg til enhet**-grensesnittet
i stedet for YAML, da det gir enhetgruppering, modelldrevne funksjoner og
administrasjon av kanaltilstand. YAML anbefales for:
- Enheter med ikke-standard eller legacy-profiler
- Migrering fra eldre Buspro-integrasjoner
- Kompleks automatisering eller sensormaler

### YAML-syntakseksempel

Legg til i `configuration.yaml`:

```yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Taklampe"
        dimmable: true
      "1.5.2":
        name: "Vegglampe"
        dimmable: false

cover:
  - platform: buspro
    devices:
      "2.10.1":
        name: "Stuegardin"
        running_time: 45

climate:
  - platform: buspro
    devices:
      "3.1":
        name: "Soveromsklimat"
        profile: "ac"
```

### Plattformkonfigurasjon

Hver plattform (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`,
`switch`) godtar:

| Nøkkel | Type | Beskrivelse |
| --- | --- | --- |
| `devices` | dict | Påkrevd. Tilordning av Buspro-adresser til enhetskonfigurasjoner. |
| `running_time` | int | Standard overgangstid i sekunder (0 = ingen overgang). Overstyrt per enhet. |
| `ack_retry_enabled` | bool | Prøv på nytt sendinger uten ACK (plattformstandard; overstyrt per enhet). |

Hver enhetsnøkkel er **Buspro-adressen** i formatet:
- **Lampe, gardin, vifte, bryter**: `subnett.enhet.kanal` (f.eks., `1.5.2`)
- **Klimakontroll, sensor, binær sensor**: `subnett.enhet` (f.eks., `3.1`)

Hver enhetskonfigurasjon støtter:
- `name` (påkrevd): Visningsnavn
- `running_time`, `dimmable`, `ack_retry_enabled` (plattformspesifikk, valgfri)
- `profile` (valgfri, for klimasensorer — f.eks., `"ac"`, `"floor_heating"`)
- `object_id` (valgfri): Entity-ID-slug
- `unique_id` (valgfri): For manuell enhetregisterkontroll

## Gatewayoppsett

Legg til **HDL Buspro** fra **Innstillinger > Enheter og tjenester** og konfigurer:

- **Vert**: vertsnavn eller IPv4-adresse for HDL-gatewayen.
- **Port**: primær UDP-port, normalt `6000`.
- **UDP-send-/mottaksporter**: endre disse bare for en ikke-standard gateway.
- **Home Assistant Buspro-adresse**: en ubrukt `subnet.device`-identitet, som for eksempel migrasjons standard `200.200`.

UDP har ingen tilkoblingshåndtrykk. Oppsett validerer adresseoppløsning, ruting og opprettelse av lokal mottakssocket uten å anta at en enhet finnes på en hardkodet Buspro-adresse.

## Enhetsstyring

Åpne **Konfigurer** på integrasjonen og velg:

- **Gateway-innstillinger** for å oppdatere nettverksinnstillinger og klientidentitet.
- **Legg til enhet** for å velge enhetens type, modell, Buspro-adresse og kanal- eller kapasitetsnavn.
- **Rediger enhet** for å gi kanaler nytt navn, aktivere eller deaktivere kanaler, fjerne en UI-administrert enhet eller korrigere modellen for en eksisterende registreringsoppføring.

Fysiske adresser vises i Home Assistant som enhetens serienummer. Enheter som tilhører en fysisk modul, er knyttet til en enkelt enhetsregisteroppføring.

## Støttede modeller

| Modell | Home Assistant-støtte |
| --- | --- |
| `HDL-MBUS01IP.431` | Metadata for gatewayenhet |
| `HDL-MCLog.431` | Tilkoblingsmulighet, fastvareforespørsel, sist sett, logikhendelser |
| `HDL-MR0410.431` | 4 relékana |
| `HDL-MR0810.432` | 8 relékana |
| `HDL-MR1210.433` | 12 relékana |
| `HDL-MR1610.433` | 16 relékana |
| `HDL-MR0416.431` | 4 høyeffekt relekanaler |
| `HDL-MR0416C.431` | 4 høyeffekt relekanaler |
| `HDL-MR0416D.431` | 4 høyeffekt relekanaler |
| `HDL-MR0816.432` | 8 høyeffekt relekanaler |
| `HDL-MR0816C.232` | 8 høyeffekt relekanaler |
| `HDL-MR0816D.432` | 8 høyeffekt relekanaler |
| `HDL-MR1216.433` | 12 høyeffekt relekanaler |
| `HDL-MR1616.434` | 16 høyeffekt relekanaler |
| `HDL-MR1216D.433` | 12 høyeffekt relekanaler |
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | 4/8/12 høystrøms relekanaler |
| `HDL-MD0206.432` | 2 dimmkanaler |
| `HDL-MD0403.432` | 4 dimmkanaler |
| `HDL-MD0602.432` | 6 dimmkanaler |
| `HDL-MDT0203.433` | 2 sluttkantkort dimmkanaler |
| `HDL-MDT0203.532` | 2 sluttkantkort dimmkanaler |
| `HDL-MDT04015.433` | 4 sluttkantkort dimmkanaler |
| `HDL-MDT04015.532` | 4 sluttkantkort dimmkanaler |
| `HDL-MDT06015.433` | 6 sluttkantkort dimmkanaler |
| `HDL-MDT06015.533` | 6 sluttkantkort dimmkanaler |
| `HDL-MDLED0605.432` | 6 dimmkanaler og diagnostikk |
| `HDL-MRDA0610.432` | 6 ballastkontroll dimmkanaler |
| `HDL-MRDA0610.433` | 6 ballastkontroll dimmkanaler |
| `SB-DN-DALI64` | Opptil 64 DALI-kanaler |
| `HDL-MS04.432` | 4 tørrkontaktkanaler |
| `HDL-MS24.232` | 24 tørrkontaktkanaler |
| `HDL-MSP02.4C` | Temperatur, belysningsstyrke, bevegelse |
| `HDL-MSP07M.4C` | Temperatur, belysningsstyrke, fuktighet, bevegelse, to kontakter |
| `HDL-MS08M.4C` | Temperatur, belysningsstyrke, bevegelse |
| `HDL-MS12M.4C` | Temperatur, belysningsstyrke, fuktighet, bevegelse, to kontakter |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Temperatur og panelhandlinger |
| `HDL-MPTL4.460` | Temperatur og panelhandlinger |
| `HDL-MP4S/TILE.48` | Temperatur, fire knapphendelser, panelhandlinger |
| `HDL-MP2B/TILE.48` | Temperatur, to knapphendelser, panelhandlinger |
| `HDL-MP4B-A/TILE.48` | Temperatur, fire knapphendelser, panelhandlinger |
| `HDL-MP4B/TILE.48` | Temperatur, fire knapphendelser, panelhandlinger |
| `HDL-MP2B.480` | Temperatur, to knapphendelser, panelhandlinger |
| `HDL-MP4B.480` | Temperatur, fire knapphendelser, panelhandlinger |
| `HDL-MPL8.431` | Temperatur, åtte knapphendelser, panelhandlinger |
| `HDL-M/PT4.1` | Temperatur, fire knapphendelser, panelhandlinger |
| `HDL-MFH04.432` | 4 varmekanaler for gulvoppvarming |
| `HDL-MFH06.432` | 6 varmekanaler for gulvoppvarming |
| `HDL-M/HVAC8.1` | AC klimaenheter |
| `HDL-MPED4.431` | AC klimaenheter |
| `HDL-MW02.431` | 2 gardin-/dekningskanaler |
| `HDL-MWM45.431` | Gardin-/dekningsenheter (konfigurerbare kanaler) |

Generiske AC-, gardin-, variabel hastighet ventilator-, av/på ventilator-, universalbryter- og panelprofiler er også tilgjengelige. Deres fysiske adresse og eventuell konfigurerbar utgangstelling leveres av brukeren; de er ikke installasjonslagerbeholdning.

Noen modeller legges til via familiemapping eller generisk protokollkompatibilitet. Under integrasjonsstarten logger Buspro eksplisitte modellstøtteaviser for disse modellene (for eksempel modellvalidert versus familiemappet atferd) sammen med oppdagede fysiske adresser.

For eldre YAML-enheter normaliserer integrasjonen nå manglende profiler ved hjelp av katalogmodellmetadata. Ukjente modeller og ustøttede profilstrenger rapporteres som oppstartsadvarsler, og faller deretter tilbake til generisk `sensor_status`-atferd for å opprettholde funksjonaliteten til oppsettet.

## Katalogvedlikeholdshjelper

For å sammenligne integrasjonskatalogen med den vedlikeholdte offisielle HDL-modelllisten, kjør:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

Hjelperen leser `custom_components/buspro/devices/official_models.json` og skriver ut:

- offisielle modeller mangler i `DEVICE_CATALOG`
- katalogmodeller som ikke finnes i den offisielle listen
- virtuelle integrasjonsonly generiske modeller

Bruk strengt modus for CI-lignende kontroller (avslutning med ikke-null når offisielle modeller mangler fra katalogen):

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Enhetsatferd

### Releyer

En delt koordinator spør relesituasjonen en gang per fysisk modul og distribuerer svaret til alle aktiverte kanalenheter. Deaktiverte kanaler abonnerer ikke eller spør ikke bussen.

### Paneler

Kjente knappepaneler lager en `event`-enhet per fysisk knapp, en `Action`-hendelse og en `Last action`-sensor. UI-knappehendelsesenheter representerer mottatte fysiske Buspro-knapptelegrammar; de simulerer ikke et hardwaretrykk.

### Dimmere

Støttede dimmere kan avgi tilkobling, maksimal lysstyrke per kanal, belastningstype og minimumslysstyrke rapportert av protokoll. `Not reported` betyr at enheten returnerte protokollsentinelen i stedet for en brukbar verdi.

### Logikkontroller

`HDL-MCLog.431` avslører skrivebeskyttet tilkobling, fastvareversjonen, sist sett og logikhendelsesenheter. Noen fastvare svarer ikke på standard fastvarespørsmål; i så fall forblir fastvareenheten utilgjengelig. Logikkblokker kan ikke skrives fordi endring av dem kan overskrive kontrollerprogrammeringen.

## Tjenester

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` sender en rå protokollkommando og bør bare brukes med en verifisert HDL-operasjonskode og nyttelast.

## Utvikling

### Kjøre testpakker

Fra Home Assistant-konfigurasjonsmappe:

```bash
# Kjør alle protokolltester (19 tester)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v

# Kjør alle integrasjonstester (18 tester)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v

# Eller kjør enkelttest-filer
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

Protokolltester dekker telegrammanalyse, enhetkoordinering og sikkerhet for
kjerne-oppgaver/tilbakekall. Integrasjonstester dekker enhetskatalog,
administrert-enhet-logikk, YAML-normalisering og modellstøttesporing.
