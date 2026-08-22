# HDL Buspro for Home Assistant

[English](../README.md) | **Norsk**

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
2. Velg **Legg til enhet** for å legge til en fysisk Buspro-modul.
3. **Velg enhettype**: velg funksjonen (Relé, Dimmer, Vifte, Gardin,
   Multisensor, osv.).
4. **Velg nøyaktig modell**: velg modellen som samsvarer med maskinvaren din.
   Dette bestemmer antallet kanaler.
   - For ukjente modeller, velg profilen **Generisk** og angi antallet kanaler.
5. **Skriv inn Buspro-adresse**: den fysiske subnett.enhet-adressen til modulen
   (f.eks. `1.5`).
6. **Skriv inn enhetsnavn**: et visningsnavn (f.eks. "Stuelyser").
7. **Gi navn til hver kanal**: tildel et navn til hver kanal eller funksjon du
   ønsker å bruke.
   - Eksempel: for et 4-kanals relé, navngi kanaler som "Taklampe",
     "Bordlampe", osv.
   - **La et navn være tomt for å deaktivere den kanalen** — ingen enhet vil
     bli opprettet.
8. Velg **Lagre** for å opprette enheten og entitetene.

Home Assistant grupperer automatisk alle entiteter fra en fysisk modul under
en enkelt enhetregistreringspost og laster inn konfigurasjonsoppføringen på
nytt.

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
