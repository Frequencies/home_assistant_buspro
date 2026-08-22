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

1. Åpne **Innstillinger > Enheter og tjenester > Legg til integrasjon** og velg
   **HDL Buspro**.
2. Skriv inn gatewayadressen og UDP-portene. Vanlig standardport er `6000`.
3. Skriv inn en ledig Buspro-adresse for Home Assistant på formatet
   `subnett.enhet`. Standardverdien `200.200` må ikke tilhøre en annen
   Buspro-enhet.
4. Åpne **Konfigurer > Legg til enhet**, velg type og nøyaktig modell, og skriv
   inn den fysiske Buspro-adressen og et navn.
5. Gi nødvendige kanaler eller funksjoner navn. Et tomt navn holder kanalen
   deaktivert og hindrer at entiteten opprettes.

Kjente modeller bruker fast kanalantall eller funksjonslisten fra
enhetskatalogen. For generiske profiler angir brukeren et kanalantall innenfor
den støttede grensen. Etter lagring lastes konfigurasjonsoppføringen på nytt,
og entitetene grupperes under én fysisk enhet.

Åpne **Konfigurer > Rediger enhet** for å gjøre endringer. For enheter som
administreres i grensesnittet, kan modell, navn og kanaler endres, eller enheten
kan fjernes. Protokollkonfigurasjonen for eldre YAML-enheter må fortsatt endres
i YAML; start Home Assistant på nytt etterpå.

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

## Katalogsjekk og tester

For å sammenligne modellkatalogen med den vedlikeholdte offisielle HDL-listen:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

For eldre YAML-enheter normaliserer integrasjonen nå manglende profiler ved
hjelp av modellmetadata. Ukjente modeller eller ugyldige profiler logges som
advarsler og faller tilbake til `sensor_status`.

Målrettede tester for integrasjonen:

```bash
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -p 'test_*.py'
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -p 'test_*.py'
```
