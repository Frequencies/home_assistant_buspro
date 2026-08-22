# HDL Buspro

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## Språk

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


## Første oppsett

### Gateway-konfigurasjon
1. Åpne **Innstillinger > Enheter og tjenester > Legg til integrasjon** og velg
   **HDL Buspro**.
2. Angi gateway-verten og UDP-portene. Port `6000` er standard standard.
3. Angi en ubrukt Home Assistant Buspro-adresse i `subnet.device`-format.
   Standarden er `200.200`; den må ikke tilhøre en annen Buspro-enhet.

### Legge til enheter
Etter at gateway-oppsettet er fullført:

1. Åpne **Innstillinger > Enheter og tjenester > HDL Buspro > Konfigurer**.
2. Klikk **Legg til enhet** for å legge til en Buspro fysisk modul.
3. **Velg enhetstype** (Relé, Dimmer, Persienne, Klima, Sensor osv.).
4. **Velg nøyaktig modell** som samsvarer med maskinvaren din.
5. **Angi Buspro-adresse** i `subnet.device`-format (f.eks. `1.5`).
6. **Angi enhetsnavn** (f.eks. "Stuelamper").
7. **Gi navn til hver kanal** — la feltet stå tomt for å deaktivere en kanal.
8. Klikk **Lagre**.

Home Assistant grupperer enheter automatisk etter fysisk modul i enhetregisteret.

**For eksempler på UI- og YAML-konfigurasjon for alle enhetstyper, se [DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md).**

### Redigering av enheter

For å endre en eksisterende enhet, åpne **Konfigurer > Rediger enhet**. Du kan:
- Gi nytt navn til enheten
- Gi nytt navn til, aktivere eller deaktivere individuelle kanaler
- Endre modellen (som kan endre antall kanaler)
- Fjerne enheten helt

UI-administrerte enheter støtter full redigering. Eldre YAML-enheter kan eksponere registreringskontroller for navn, men protokollkonfigurasjonen må fortsatt endres i YAML. Start Home Assistant på nytt etter å ha endret YAML.

### Raskt eksempel: Legge til en 4-kanals relé-modul

1. Modell: `HDL-MR0410.431` (4 relé-kanaler)
2. Buspro-adresse: `1.10`
3. Enhetsnavn: "Stuerelé"
4. Kanalnavn: "Taklampe", "Vegglampe", "", "Vifte"
5. Klikk **Lagre**

Home Assistant oppretter automatisk enheter: `light.room_relays_ceiling_light`, `light.room_relays_wall_lamp`, `switch.room_relays_fan`

For komplette UI- og YAML-eksempler for alle enhetstyper, se **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)**.

## Konfigurasjonsalternativer

Buspro-integrasjonen støtter både **UI-basert oppsett** og **YAML-konfigurasjon**:

### UI-oppsett
Den enkleste måten å legge til enheter på — se **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)** for trinn-for-trinn eksempler på alle enhetstyper.

### YAML-konfigurasjon  
Integrasjonen støtter to komplementære YAML-tilnærminger:
- **Entity-sentrert** (Eldre) — individuelle entityfiler organisert etter domene
- **Enhet-sentrert** (Moderne) — komplette enhetsdefinisjonerer med alle kanaler

**For fullstendig YAML-dokumentasjon, eksempler og beste praksis, se [DUAL_MODE_YAML.md](docs/en/DUAL_MODE_YAML.md)** (også tilgjengelig på [Беларуская](docs/be/DUAL_MODE_YAML.md) | [Deutsch](docs/de/DUAL_MODE_YAML.md) | [Español](docs/es/DUAL_MODE_YAML.md) | [Français](docs/fr/DUAL_MODE_YAML.md) | [Italiano](docs/it/DUAL_MODE_YAML.md) | [Nederlands](docs/nl/DUAL_MODE_YAML.md) | [Norsk](docs/no/DUAL_MODE_YAML.md) | [Русский](docs/ru/DUAL_MODE_YAML.md) | [Українська](docs/uk/DUAL_MODE_YAML.md))

## Brytende endringer i 2.2.0

Les denne delen før du oppgraderer fra 2.1.x.

> [!WARNING]
> Denne versjonen endrer enhetseierskap, kanalopprettelse, panelhendelsessemantikk
> og den innebygde Python-konstruktøren. Fullfør oppgraderingsjekklisten
> før du fjerner eldre YAML.

1. **Installasjonsspesifikke enheter er ikke lenger bygget inn i integrasjonen.**
   Enhetadresser, navn, kanaltildelinger og enhetantall tilhører nå
   konfigurasjonsoppføringer eller Home Assistant-enhetregisteret. Enhetskatalogen
   inneholder bare maskinvareegenskaper.

2. **UI-administrerte relé-moduler bruker sitt fysiske kanaltall.**
   `HDL-MR1210.433` eksponerer alltid 12 kanalplasser og
   `HDL-MR1610.433` eksponerer alltid 16. En eksisterende enhet kan ikke reduseres
   under modellens fysiske kanaltall.

3. **Et tomt kanalnavn deaktiverer kanalen.**
   Deaktiverte kanaler blir ikke instansiert, oppretter ikke protokollobjekter og
   er merket som deaktiverte av integrasjonen i Entity Registry. Hvis du angir et
   navn, aktiveres kanalen igjen.

4. **Den nøyaktige modellen kontrollerer opprettede enheter.**
   Et generisk `HDL-panel` har ingen kjent knappantall. Velg den fysiske modellen
   for å opprette knappehendelser. Endring av modell laster inn konfigurasjonsoppføringen på nytt.

5. **Home Assistant har sin egen Buspro-adresse.**
   Eksisterende konfigurasjonsoppføringer migreres til `200.200`. Denne adressen må være
   ubrukt på Buspro-nettverket og kan endres under **Konfigurer > Gateway-innstillinger**.

6. **IP-pakkekilden er ikke lenger hard-kodet.**
   Integrasjonen henter den fra ruten til den konfigurerte gateway'en. En
   Home Assistant-vert med flere grensesnitt må dirigere gatewayen gjennom det
   tiltenkte LAN-grensesnittet.

7. **Panelhendelser er nå dekodert.**
   Automatiksering som bruker gamle råhandlingsverdier bør sjekkes. Hendelser bruker
   `channel_on`, `channel_off`, `channel_level`, `scene`,
   `universal_switch_on` eller `universal_switch_off`, med mål- og sammenfattingsattributter
   der de kan løses.

8. **Det innebygde Python-APIet endret seg.**
   Direkte `pybuspro.Buspro`-brukere må oppgi `client_address`; se
   [pybuspro/README.md](pybuspro/README.md).

Integrasjonen leser fortsatt eldre YAML-enheter under migrering. Ikke hold
samme fysiske kanal i både YAML og UI-administrert konfigurasjon, da det
kan skape dupliserte enheter og dupliserte protokollabonnementer.

## Oppgraderingsjekkliste

1. Start Home Assistant på nytt etter å ha erstattet den egendefinerte komponenten.
2. Åpne **Innstillinger > Enheter og tjenester > HDL Buspro > Konfigurer**.
3. Sjekk gateway-verten, portene og ubrukt Home Assistant Buspro-adresse.
4. Åpne hver fysiske enhet og velg dens nøyaktige modell.
5. Sjekk alle relé-kanalnavn. Tomme kanaler forblir med vilje deaktiverte.
6. Bekreft automatiksering som bruker panelhendelser.
7. Fjern eller kommenter migrerte YAML-enheter bare etter at deres UI-administrerte
   erstatninger har beholdt forventet entity ID-er.

## Gateway-oppsett

Legg til **HDL Buspro** fra **Innstillinger > Enheter og tjenester** og konfigurer:

- **Vert**: HDL IP-gateway-vertsnavn eller IPv4-adresse.
- **Port**: primær UDP-port, normalt `6000`.
- **UDP-send/mottaksporter**: endre disse bare for en ikke-standard gateway.
- **Home Assistant Buspro-adresse**: en ubrukt `subnet.device`-identitet, for eksempel
  migreringsstandarden `200.200`.

UDP har ingen tilkoblingshåndtrykk. Oppsettet validerer adresseoppløsning, ruting
og opprettelse av den lokale mottakssokelen uten å anta at en enhet eksisterer
ved en hard-kodet Buspro-adresse.

## Enhetsstyring

Åpne **Konfigurer** på integrasjonen og velg:

- **Gateway-innstillinger** for å oppdatere nettverksinnstillinger og klientidentitet.
- **Legg til enhet** for å velge enhetstype, modell, Buspro-adresse og kanal- eller
  mulighetsnavn.
- **Rediger enhet** for å gi nye navn til kanaler, aktivere eller deaktivere kanaler, fjerne en
  UI-administrert enhet eller korrigere modellen på en eksisterende registreringsenhet.

Fysiske adresser vises i Home Assistant som enhetens serienummer.
Enheter som tilhører en fysisk modul er vedlagt samme Device
Registry-oppføring.

## Støttede modeller

| Modell | Home Assistant-støtte |
| --- | --- |
| `HDL-MBUS01IP.431` | Gateway-enhetmetadata |
| `HDL-MCLog.431` | Tilkoblingsevne, firmwareforespørsel, sist sett, logikkhendelser |
| `HDL-MR0410.431` | 4 relé-kanaler |
| `HDL-MR0810.432` | 8 relé-kanaler |
| `HDL-MR1210.433` | 12 relé-kanaler |
| `HDL-MR1610.433` | 16 relé-kanaler |
| `HDL-MR0416.431` | 4 høyeffekt-relé-kanaler |
| `HDL-MR0416C.431` | 4 høyeffekt-relé-kanaler |
| `HDL-MR0416D.431` | 4 høyeffekt-relé-kanaler |
| `HDL-MR0816.432` | 8 høyeffekt-relé-kanaler |
| `HDL-MR0816C.232` | 8 høyeffekt-relé-kanaler |
| `HDL-MR0816D.432` | 8 høyeffekt-relé-kanaler |
| `HDL-MR1216.433` | 12 høyeffekt-relé-kanaler |
| `HDL-MR1616.434` | 16 høyeffekt-relé-kanaler |
| `HDL-MR1216D.433` | 12 høyeffekt-relé-kanaler |
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | 4/8/12 høystrøm-relé-kanaler |
| `HDL-MD0206.432` | 2 dimmer-kanaler |
| `HDL-MD0403.432` | 4 dimmer-kanaler |
| `HDL-MD0602.432` | 6 dimmer-kanaler |
| `HDL-MDT0203.433` | 2 trailing-edge dimmer-kanaler |
| `HDL-MDT0203.532` | 2 trailing-edge dimmer-kanaler |
| `HDL-MDT04015.433` | 4 trailing-edge dimmer-kanaler |
| `HDL-MDT04015.532` | 4 trailing-edge dimmer-kanaler |
| `HDL-MDT06015.433` | 6 trailing-edge dimmer-kanaler |
| `HDL-MDT06015.533` | 6 trailing-edge dimmer-kanaler |
| `HDL-MDLED0605.432` | 6 dimmer-kanaler og diagnostikk |
| `HDL-MRDA0610.432` | 6 ballast-kontroll dimmer-kanaler |
| `HDL-MRDA0610.433` | 6 ballast-kontroll dimmer-kanaler |
| `SB-DN-DALI64` | Opptil 64 DALI-kanaler |
| `HDL-MS04.432` | 4 tørt-kontakt-kanaler |
| `HDL-MS24.232` | 24 tørt-kontakt-kanaler |
| `HDL-MSP02.4C` | Temperatur, belysningsstyrke, bevegelse |
| `HDL-MSP07M.4C` | Temperatur, belysningsstyrke, fuktighet, bevegelse, to kontakter |
| `HDL-MS08M.4C` | Temperatur, belysningsstyrke, bevegelse |
| `HDL-MS12M.4C` | Temperatur, belysningsstyrke, fuktighet, bevegelse, to kontakter |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Temperatur og paneelhandlinger |
| `HDL-MPTL4.460` | Temperatur og paneelhandlinger |
| `HDL-MP4S/TILE.48` | Temperatur, fire knappehendelser, paneelhandlinger |
| `HDL-MP2B/TILE.48` | Temperatur, to knappehendelser, paneelhandlinger |
| `HDL-MP4B-A/TILE.48` | Temperatur, fire knappehendelser, paneelhandlinger |
| `HDL-MP4B/TILE.48` | Temperatur, fire knappehendelser, paneelhandlinger |
| `HDL-MP2B.480` | Temperatur, to knappehendelser, paneelhandlinger |
| `HDL-MP4B.480` | Temperatur, fire knappehendelser, paneelhandlinger |
| `HDL-MPL8.431` | Temperatur, åtte knappehendelser, paneelhandlinger |
| `HDL-M/PT4.1` | Temperatur, fire knappehendelser, paneelhandlinger |
| `HDL-MFH04.432` | 4 gulvvarmekanaler |
| `HDL-MFH06.432` | 6 gulvvarmekanaler |
| `HDL-M/HVAC8.1` | AC klimaenheter |
| `HDL-MPED4.431` | AC klimaenheter |
| `HDL-MW02.431` | 2 persienne/dekkerkanaler |
| `HDL-MWM45.431` | Persienne/dekkerentiteter (konfigurerbare kanaler) |

Generiske AC, persienne, variabel hastighet vifte, av/på vifte, universal-svitsj og
panelerprofiler er også tilgjengelige. Deres fysiske adresse og eventuelle konfigurerbare
utgangsantall leveres av brukeren; de er ikke installasjonslager.

Noen modeller legges til via familiemapping eller generisk protokollkompatibilitet.
Under integrasjonsstart logger Buspro eksplisitt modellstøttedokumenter for disse
modellene (for eksempel modellvalidert vs. familje-kartlagt oppførsel) sammen med
oppdagede fysiske adresser.

For eldre YAML-enheter normaliserer integrasjonen nå manglende profiler ved hjelp av
katalogmodellmetadata. Ukjente modeller og ustøttede profilstrenger
rapporteres som oppstartadvarsler, deretter faller tilbake til generisk `sensor_status`
oppførsel for å holde oppsettet funksjonelt.

## Hjelpemiddel for katalogvedlikehold

For å sammenligne integrasjonskatalogen med den vedlikeholdt offisielle HDL-modellisten,
kjør:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

Hjelpemiddelet leser `custom_components/buspro/devices/official_models.json` og
skriver ut:

- offisielle modeller som mangler i `DEVICE_CATALOG`
- katalogmodeller som ikke finnes i den offisielle listen
- virtuelle integrasjonsonly generiske modeller

Bruk streng modus for CI-stil sjekker (ikke-null avslutning når offisielle modeller
mangler i katalogen):

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Entitetsoppførsel

### Relé

En delt koordinator spør relestatus en gang per fysisk modul og
distribuerer responsen til alle aktiverte kanalenheter. Deaktiverte kanaler
abonnerer ikke på eller spør bussen.

### Paneler

Kjente knappepaneler oppretter en `event`-enhet per fysisk knapp, en `Action`-hendelse
og en `Last action`-sensor. UI-knapphendelsesenheter representerer mottatt
fysiske Buspro-knapptelegrammar; de simulerer ikke et maskinvaretrykk.

### Dimmer

Støttede dimmer-enheter kan eksponere tilkoblingsevne, maksimal lysstyrke per kanal,
belastningstype og protokollrapportert minimum lyssterke. `Ikke rapportert` betyr at
enheten returnerte protokollsentinelen i stedet for en brukbar verdi.

### Logikk-styringsenhet

`HDL-MCLog.431` eksponerer skrivebeskyttet tilkoblingsevne, firmwareversjon, sist sett
og logikkhendelsesenheter. Noe firmware svarer ikke på standardfirmwareforespørselen;
i så fall forblir firmwareenheten utilgjengelig. Logikkblokker kan ikke skrives til
fordi endring av dem kan overskrive styringsenhetsprogrammering.

## Tjenester

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` sender en rå protokollkommando og bør kun brukes med
en verifisert HDL-operasjonskode og last.

## YAML-konfigurasjon (eldre)

YAML-enhetskonfigurasjon støttes fullstendig sammen med config-entry gateway-administrasjon. Du kan definere lys, persienner, svitsjer, vifter, klima, sensorer og binærsensorer via YAML mens gatewayen administreres av integrasjons-UI-et.

**Merk**: Nye enheter bør bruke integrasjons **Konfigurer > Legg til enhet** UI i stedet for YAML, da den gir enhetgruppering, modellstyrt kapabilitet og kanaltilstandsstyring. YAML anbefales for:
- Enheter med ikke-standard eller eldre profiler
- Migrering fra eldre Buspro-integrasjoner
- Kompleks automatiksering eller sensormaler

### YAML syntakseksempel

Legg til i `configuration.yaml`:

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

### Plattformkonfigurasjon

Hver plattform (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`, `switch`) aksepterer:

| Nøkkel | Type | Beskrivelse |
| --- | --- | --- |
| `devices` | dict | Obligatorisk. Kartlegging av Buspro-adresser til enhetskonfigurasjoner. |
| `running_time` | int | Standard overgangstid i sekunder (0 = ingen overgang). Overstyrt per enhet. |
| `ack_retry_enabled` | bool | Forsøk sending på ingen ACK (plattformstandard; per-enhet overstyringer). |

Hver enhetsnøkkel er **Buspro-adressen** i format:
- **Lys, persienne, vifte, svitsj**: `subnet.device.channel` (f.eks. `1.5.2`)
- **Klima, sensor, binærsensor**: `subnet.device` (f.eks. `3.1`)

Hver enhetskonfigurasjon støtter:
- `name` (obligatorisk): Visningsnavn
- `running_time`, `dimmable`, `ack_retry_enabled` (plattformspesifikk, valgfritt)
- `profile` (valgfritt, for klimasensorer — f.eks. `"ac"`, `"floor_heating"`)
- `object_id` (valgfritt): Entity ID-slug
- `unique_id` (valgfritt): For manuell entity registry-kontroll

## Utvikling

### Kjør testsamlingene

Fra Home Assistant-konfigurasjonroten:

```bash
# Run all protocol tests (19 tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v

# Run all integration tests (18 tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v

# Or run individual test files
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

Protokolltester dekker telegramparsing, enhetkoordinasjon og sikkerhet for kjerne-oppgaver/tilbakekallinger. Integrasjonsprøver dekker enhetskatalog, administrert-enhet logikk, YAML-normalisering og modellstøttesporing.
