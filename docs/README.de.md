# HDL Buspro für Home Assistant

[English](../README.md) | **Deutsch**

Die Integration verwaltet das Gateway und physische HDL-Buspro-Geräte über
die Home-Assistant-Oberfläche. Eine vollständige Liste der Modelle, Entitäten
und Dienste steht in der [englischen Dokumentation](../README.md).

> **Hinweis**: Für detaillierte Anleitungen zur Gerätekonfiguration, YAML-Beispiele, Dienste und Entwicklung siehe die [englische README](../README.md). Diese Seite enthält grundlegende Installations- und Konfigurationsinformationen.

## Installation

### HACS (empfohlen)

1. **HACS > Integrationen** öffnen.
2. Das Drei-Punkte-Menü öffnen und **Benutzerdefinierte Repositories** wählen.
3. `https://github.com/Frequencies/home_assistant_buspro` mit der Kategorie
   **Integration** hinzufügen.
4. Nach **HDL Buspro** suchen, den Eintrag öffnen und **Herunterladen** wählen.
5. Home Assistant neu starten, wenn HACS dazu auffordert.

Weitere Versionen können danach über **HACS > Integrationen** installiert
werden. Home Assistant nach jedem Integrationsupdate neu starten.

### Manuelle Installation

1. Das Repository der Integration herunterladen.
2. Dessen Verzeichnis `custom_components/buspro` nach
   `/config/custom_components/buspro` in Home Assistant kopieren.
3. Home Assistant neu starten.

## Ersteinrichtung

### Gateway-Konfiguration
1. **Einstellungen > Geräte & Dienste > Integration hinzufügen** öffnen und
   **HDL Buspro** auswählen.
2. Gateway-Host und UDP-Ports eingeben. Der Standardport ist normalerweise `6000`.
3. Eine freie Home-Assistant-Buspro-Adresse im Format `Subnetz.Gerät` eingeben.
   Der Standard `200.200` darf keinem anderen Buspro-Gerät gehören.

### Geräte hinzufügen
Nach der Gateway-Konfiguration:

1. **Einstellungen > Geräte & Dienste > HDL Buspro > Konfigurieren** öffnen.
2. **Gerät hinzufügen** auswählen, um ein physisches Buspro-Modul hinzuzufügen.
3. **Gerätetyp auswählen**: wählen Sie die Funktion (Relais, Dimmer, Ventilator, Jalousie, Multisensor usw.).
4. **Genaues Modell auswählen**: wählen Sie das Modell Ihrer Hardware. Dies bestimmt die Kanalanzahl.
   - Für unbekannte Modelle wählen Sie das Profil **Generisch** und geben Sie die Kanalanzahl an.
5. **Buspro-Adresse eingeben**: die physische Subnetz.Gerät-Adresse des Moduls (z. B. `1.5`).
6. **Gerätenamen eingeben**: einen Anzeigenamen für das Gerät (z. B. "Wohnzimmerlichter").
7. **Jeden Kanal benennen**: weisen Sie jedem Kanal oder jeder Funktion einen Namen zu, den Sie nutzen möchten.
   - Beispiel: für ein 4-Kanal-Relais: "Deckenleuchte", "Tischlampe" usw.
   - **Lassen Sie einen Namen leer, um diesen Kanal zu deaktivieren** — es wird keine Entität erstellt.
8. **Speichern** auswählen, um das Gerät und seine Entitäten zu erstellen.

Home Assistant gruppiert automatisch alle Entitäten eines physischen Moduls unter einem Geräteregistereintrag und lädt den Konfigurationseintrag neu.

### Geräte bearbeiten

Zum Ändern eines bestehenden Geräts **Konfigurieren > Gerät bearbeiten** öffnen. Sie können:
- Das Gerät umbenennen
- Einzelne Kanäle umbenennen, aktivieren oder deaktivieren
- Das Modell ändern (kann die Kanalanzahl verändern)
- Das Gerät vollständig entfernen

UI-verwaltete Geräte unterstützen vollständige Bearbeitung. Bei älteren YAML-Geräten können Änderungen im Geräteregister vorgenommen werden, aber die Protokollkonfiguration muss in YAML geändert werden. Home Assistant nach YAML-Änderungen neu starten.

### Beispiel: 4-Kanal-Relaismodul hinzufügen

1. Modell: `HDL-MR0410.431` (4 Relaiskanäle)
2. Buspro-Adresse: `1.10`
3. Gerätenamen: "Raumrelais"
4. Kanalnamen:
   - Kanal 1: "Deckenleuchte"
   - Kanal 2: "Wandlampe"
   - Kanal 3: "" (deaktiviert)
   - Kanal 4: "Ventilator"

Nach dem Speichern erstellt Home Assistant:
- `light.room_relays_ceiling_light`
- `light.room_relays_wall_lamp`
- `switch.room_relays_fan`

## Wichtige Änderungen in 2.2.0

- Adressen, Namen, Geräteanzahl und Kanalzuordnungen sind nicht mehr in der
  Integration fest hinterlegt. Sie werden in den Optionen des
  Konfigurationseintrags gespeichert.
- Das genaue Modell bestimmt die physische Kanalanzahl und die erzeugten
  Entitäten.
- Ein Kanal mit leerem Namen ist deaktiviert und wird nicht erzeugt.
- Die Buspro-Adresse von Home Assistant wird standardmäßig auf `200.200`
  migriert. Diese Adresse muss im Netzwerk frei sein.
- Panel-Ereignisse werden jetzt als `channel_on`, `channel_off`,
  `channel_level`, `scene` und Universal-Switch-Ereignisse dekodiert.
- Der eingebettete `Buspro`-Konstruktor benötigt jetzt `client_address`.

## Aktualisierung

1. Home Assistant nach dem Ersetzen der Komponente neu starten.
2. **Einstellungen > Geräte & Dienste > HDL Buspro > Konfigurieren** öffnen.
3. Gateway, UDP-Ports und die freie Buspro-Adresse von Home Assistant prüfen.
4. Für jedes Gerät das genaue Modell auswählen und die Kanalnamen prüfen.
5. Automatisierungen prüfen, die Panel-Ereignisse verwenden.
6. Alte YAML-Entitäten erst entfernen oder auskommentieren, nachdem die über
   die UI erstellten Ersatzentitäten geprüft wurden.

Derselbe physische Kanal darf nicht gleichzeitig in YAML und über die UI
konfiguriert sein. Andernfalls entstehen doppelte Entitäten und
Protokollabonnements.

## YAML-Konfiguration (veraltet)

YAML-Gerätekonfiguration wird vollständig unterstützt neben der Config-Entry-Gateway-Verwaltung. Sie können Lichter, Jalousien, Schalter, Ventilatoren, Klima, Sensoren und binäre Sensoren über YAML definieren, während das Gateway über die Integration-UI verwaltet wird.

**Hinweis**: Neue Geräte sollten die UI-Konfiguration **Konfigurieren > Gerät hinzufügen** verwenden, da sie Gerätegruppen, modellgesteuerte Funktionen und Kanalstatusspeicherung bietet. YAML wird empfohlen für:
- Geräte mit nicht standardisierten oder älteren Profilen
- Migration von älteren Buspro-Integrationen
- Komplexe Automatisierungen oder Sensortemplates

### YAML-Syntaxbeispiel

Zu Ihrer `configuration.yaml` hinzufügen:

```yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Deckenleuchte"
        dimmable: true
      "1.5.2":
        name: "Wandlampe"
        dimmable: false

cover:
  - platform: buspro
    devices:
      "2.10.1":
        name: "Wohnzimmergardinen"
        running_time: 45

climate:
  - platform: buspro
    devices:
      "3.1":
        name: "Schlafzimmerklima"
        profile: "ac"
```

### Plattformkonfiguration

Jede Plattform (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`, `switch`) akzeptiert:

| Schlüssel | Typ | Beschreibung |
| --- | --- | --- |
| `devices` | dict | Erforderlich. Zuordnung von Buspro-Adressen zu Gerätekonfigurationen. |
| `running_time` | int | Standardübergangszeit in Sekunden (0 = kein Übergang). Pro Gerät überschreibbar. |
| `ack_retry_enabled` | bool | Wiederholung bei keinem ACK (Plattform-Standard; pro Gerät überschreibbar). |

Jeder Geräteschlüssel ist die **Buspro-Adresse** im Format:
- **Licht, Jalousie, Ventilator, Schalter**: `subnetz.gerät.kanal` (z. B. `1.5.2`)
- **Klima, Sensor, Binärsensor**: `subnetz.gerät` (z. B. `3.1`)

Jede Gerätekonfiguration unterstützt:
- `name` (erforderlich): Anzeigename
- `running_time`, `dimmable`, `ack_retry_enabled` (plattformspezifisch, optional)
- `profile` (optional, für Klimasensoren — z. B. `"ac"`, `"floor_heating"`)
- `object_id` (optional): Entity-ID-Slug
- `unique_id` (optional): Zur manuellen Geräteregisterkontrolle

## Entwicklung

### Test-Suites ausführen

Aus dem Home-Assistant-Konfigurationsverzeichnis:

```bash
# Alle Protokolltests ausführen (19 Tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v

# Alle Integrationstests ausführen (18 Tests)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v

# Oder einzelne Testdateien ausführen
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

Protokolltests decken Telegrammanalyse, Gerätekoordination und Kernaufgaben-/Callback-Sicherheit ab. Integrationstests decken Gerätekatalog, verwaltete Gerätelogik, YAML-Normalisierung und Modellunterstützungsverfolgung ab.
