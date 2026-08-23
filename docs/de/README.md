# HDL Buspro für Home Assistant

[🇧🇾 Беларуская](../be/README.md) | 🇩🇪 Deutsch | [🇬🇧 English](../../README.md) | [🇪🇸 Español](../es/README.md) | [🇫🇷 Français](../fr/README.md) | [🇮🇹 Italiano](../it/README.md) | [🇳🇱 Nederlands](../nl/README.md) | [🇳🇴 Norsk](../no/README.md) | [🇷🇺 Русский](../ru/README.md) | [🇺🇦 Українська](../uk/README.md)

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
2. **Gerät hinzufügen** auswählen und Gerätetyp (Relais, Dimmer, Ventilator, Jalousie, usw.) wählen.
3. Modell auswählen (oder **Generisch** für unbekannte Modelle mit Kanalanzahl).
4. Buspro-Adresse, Gerätename und Kanalnamen eingeben (leere Namen deaktivieren Kanäle).
5. **Speichern** auswählen.

Home Assistant gruppiert automatisch alle Entitäten unter einem Geräteregistereintrag.

**Für detaillierte UI- und YAML-Konfigurationsbeispiele für alle Gerätetypen siehe [../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md).**

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

Vollständige UI- und YAML-Beispiele für alle Gerätetypen finden Sie unter **[../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md)**.

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

## Konfigurationsoptionen

Die Buspro-Integration unterstützt sowohl **UI-basierte Konfiguration** als auch **YAML-Konfiguration**:

### UI-Konfiguration
Der einfachste Weg zum Hinzufügen von Geräten — siehe **[../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md)** für schrittweise Beispiele aller Gerätetypen.

### YAML-Konfiguration  
Die Integration unterstützt zwei ergänzende YAML-Ansätze:
- **Entity-Centric** (Legacy) — einzelne Entitätsdateien, nach Domänen organisiert
- **Device-Centric** (Modern) — komplette Gerätedefinitionen mit allen Kanälen

**Für vollständige YAML-Dokumentation, Beispiele und Best Practices siehe [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md)** (auch verfügbar auf [English](../en/DUAL_MODE_YAML.md) | [Беларуская](../en/DUAL_MODE_YAML.md) | [Español](../en/DUAL_MODE_YAML.md) | [Français](../en/DUAL_MODE_YAML.md) | [Italiano](../en/DUAL_MODE_YAML.md) | [Nederlands](../en/DUAL_MODE_YAML.md) | [Norsk](../en/DUAL_MODE_YAML.md) | [Русский](../en/DUAL_MODE_YAML.md) | [Українська](../en/DUAL_MODE_YAML.md))

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

## Gateway-Setup

Fügen Sie **HDL Buspro** aus **Einstellungen > Geräte und Dienste** hinzu und konfigurieren Sie:

- **Host**: Hostname oder IPv4-Adresse des HDL-Gateways.
- **Port**: primärer UDP-Port, normalerweise `6000`.
- **UDP-Sende-/Empfangsports**: ändern Sie diese nur für ein nicht standardisiertes Gateway.
- **Home Assistant Buspro-Adresse**: eine nicht verwendete `subnet.device`-Identität, wie z. B. die Migrationsvorgabe `200.200`.

UDP hat keinen Verbindungs-Handshake. Das Setup validiert Adressenauflösung, Routing und Erstellung des lokalen Empfängersockets, ohne anzunehmen, dass ein Gerät unter einer fest codierten Buspro-Adresse vorhanden ist.

## Geräteverwaltung

Öffnen Sie **Konfigurieren** in der Integration und wählen Sie:

- **Gateway-Einstellungen** zum Aktualisieren von Netzwerkeinstellungen und Client-Identität.
- **Gerät hinzufügen** zum Auswählen eines Gerätetyps, Modells, der Buspro-Adresse und der Kanal- oder Funktionsnamen.
- **Gerät bearbeiten** zum Umbenennen von Kanälen, Aktivieren oder Deaktivieren von Kanälen, Entfernen eines UI-verwalteten Geräts oder Korrigieren des Modells eines vorhandenen Registereintrags.

Physische Adressen werden in Home Assistant als Seriennummer des Geräts angezeigt. Entities, die zu einem physischen Modul gehören, sind an einen einzelnen Geräteregisters-Eintrag gebunden.

## Unterstützte Modelle

| Modell | Home Assistant-Unterstützung |
| --- | --- |
| `HDL-MBUS01IP.431` | Metadaten des Gateway-Geräts |
| `HDL-MCLog.431` | Konnektivität, Firmware-Abfrage, zuletzt gesehen, Logikereignisse |
| `HDL-MR0410.431` | 4 Relaiskanäle |
| `HDL-MR0810.432` | 8 Relaiskanäle |
| `HDL-MR1210.433` | 12 Relaiskanäle |
| `HDL-MR1610.433` | 16 Relaiskanäle |
| `HDL-MR0416.431` | 4 Hochleistungs-Relaiskanäle |
| `HDL-MR0416C.431` | 4 Hochleistungs-Relaiskanäle |
| `HDL-MR0416D.431` | 4 Hochleistungs-Relaiskanäle |
| `HDL-MR0816.432` | 8 Hochleistungs-Relaiskanäle |
| `HDL-MR0816C.232` | 8 Hochleistungs-Relaiskanäle |
| `HDL-MR0816D.432` | 8 Hochleistungs-Relaiskanäle |
| `HDL-MR1216.433` | 12 Hochleistungs-Relaiskanäle |
| `HDL-MR1616.434` | 16 Hochleistungs-Relaiskanäle |
| `HDL-MR1216D.433` | 12 Hochleistungs-Relaiskanäle |
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | 4/8/12 Hochstrom-Relaiskanäle |
| `HDL-MD0206.432` | 2 Dimmkanäle |
| `HDL-MD0403.432` | 4 Dimmkanäle |
| `HDL-MD0602.432` | 6 Dimmkanäle |
| `HDL-MDT0203.433` | 2 Trailing-Edge-Dimmkanäle |
| `HDL-MDT0203.532` | 2 Trailing-Edge-Dimmkanäle |
| `HDL-MDT04015.433` | 4 Trailing-Edge-Dimmkanäle |
| `HDL-MDT04015.532` | 4 Trailing-Edge-Dimmkanäle |
| `HDL-MDT06015.433` | 6 Trailing-Edge-Dimmkanäle |
| `HDL-MDT06015.533` | 6 Trailing-Edge-Dimmkanäle |
| `HDL-MDLED0605.432` | 6 Dimmkanäle und Diagnose |
| `HDL-MRDA0610.432` | 6 Ballaststeuerungs-Dimmkanäle |
| `HDL-MRDA0610.433` | 6 Ballaststeuerungs-Dimmkanäle |
| `SB-DN-DALI64` | Bis zu 64 DALI-Kanäle |
| `HDL-MS04.432` | 4 Trockenkontaktkanäle |
| `HDL-MS24.232` | 24 Trockenkontaktkanäle |
| `HDL-MSP02.4C` | Temperatur, Beleuchtungsstärke, Bewegung |
| `HDL-MSP07M.4C` | Temperatur, Beleuchtungsstärke, Feuchte, Bewegung, zwei Kontakte |
| `HDL-MS08M.4C` | Temperatur, Beleuchtungsstärke, Bewegung |
| `HDL-MS12M.4C` | Temperatur, Beleuchtungsstärke, Feuchte, Bewegung, zwei Kontakte |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Temperatur und Paneelaktionen |
| `HDL-MPTL4.460` | Temperatur und Paneelaktionen |
| `HDL-MP4S/TILE.48` | Temperatur, vier Schaltflächenereignisse, Paneelaktionen |
| `HDL-MP2B/TILE.48` | Temperatur, zwei Schaltflächenereignisse, Paneelaktionen |
| `HDL-MP4B-A/TILE.48` | Temperatur, vier Schaltflächenereignisse, Paneelaktionen |
| `HDL-MP4B/TILE.48` | Temperatur, vier Schaltflächenereignisse, Paneelaktionen |
| `HDL-MP2B.480` | Temperatur, zwei Schaltflächenereignisse, Paneelaktionen |
| `HDL-MP4B.480` | Temperatur, vier Schaltflächenereignisse, Paneelaktionen |
| `HDL-MPL8.431` | Temperatur, acht Schaltflächenereignisse, Paneelaktionen |
| `HDL-M/PT4.1` | Temperatur, vier Schaltflächenereignisse, Paneelaktionen |
| `HDL-MFH04.432` | 4 Fußbodenheizungskanäle |
| `HDL-MFH06.432` | 6 Fußbodenheizungskanäle |
| `HDL-M/HVAC8.1` | AC-Klimaentities |
| `HDL-MPED4.431` | AC-Klimaentities |
| `HDL-MW02.431` | 2 Vorhang-/Abdeckungskanäle |
| `HDL-MWM45.431` | Vorhang-/Abdeckungsentities (konfigurierbare Kanäle) |

Generische AC-, Vorhang-, Drehzahlregler-, Ein-/Aus-Gebläse-, Universal-Switch- und Panel-Profile sind ebenfalls verfügbar. Ihre physische Adresse und alle konfigurierbaren Ausgaben werden vom Benutzer bereitgestellt; sie sind kein Installationsinventar.

Einige Modelle werden über Familienmapping oder generische Protokollkompatibilität hinzugefügt. Bei der Integration startet Buspro explizite Modellunterstützungshinweise für diese Modelle (z. B. modellvalidiertes versus familiengekoppeltes Verhalten) zusammen mit erkannten physischen Adressen.

Für ältere YAML-Geräte normalisiert die Integration nun fehlende Profile mithilfe von Katalogmodell-Metadaten. Unbekannte Modelle und nicht unterstützte Profilzeichenfolgen werden als Startwarnungen gemeldet und fallen dann auf das generische `sensor_status`-Verhalten zurück, um die Funktionalität des Setups beizubehalten.

## Katalogwartungs-Helfer

Um den Integrationskatalog mit der verwalteten offiziellen HDL-Modellliste zu vergleichen, führen Sie aus:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

Der Helfer liest `custom_components/buspro/devices/official_models.json` und druckt:

- offizielle Modelle, die in `DEVICE_CATALOG` fehlen
- Katalogmodelle, die nicht in der offiziellen Liste vorhanden sind
- virtuelle nur für Integration verfügbare generische Modelle

Verwenden Sie den strikten Modus für CI-ähnliche Überprüfungen (Beendigung mit nicht null, wenn offizielle Modelle im Katalog fehlen):

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Entity-Verhalten

### Relais

Ein gemeinsamer Koordinator fragt den Relaiszustand einmal pro physischem Modul ab und verteilt die Antwort an alle aktivierten Kanalentities. Deaktivierte Kanäle abonnieren nicht oder fragen den Bus nicht ab.

### Paneele

Bekannte Tasten-Paneele erstellen pro physischer Taste ein `event`-Entity, ein `Action`-Ereignis und einen `Last action`-Sensor. UI-Tastenereigenisse-Entities stellen empfangene physische Buspro-Tastentelegrammdarstellen; sie simulieren nicht das physische Drücken von Tasten.

### Dimmer

Unterstützte Dimmer können Konnektivität, maximale Helligkeit pro Kanal, Lasttyp und vom Protokoll gemeldete Mindestkelligkeit offenlegen. `Not reported` bedeutet, dass das Gerät die Protokoll-Sentinel statt eines verwertbaren Wertes zurückgab.

### Logik-Controller

`HDL-MCLog.431` stellt schreibgeschützten Zugriff auf Konnektivität, Firmware-Version, Zuletzt gesehen und Logik-Event-Entities bereit. Einige Firmware antwortet nicht auf die Standard-Firmware-Abfrage; in diesem Fall bleibt die Firmware-Entity nicht verfügbar. Logikblöcke sind nicht schreibbar, da ihre Änderung die Controller-Programmierung überschreiben kann.

## Dienste

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` sendet einen rohen Protokollbefehl und sollte nur mit verifiziertem HDL-Betriebscode und Payload verwendet werden.

## YAML-Konfiguration (Vermächtnis)

Die YAML-Gerätekonfiguration wird vollständig neben der Verwaltung von Config-Entry-Gateways unterstützt. Sie können Lichter, Abdeckungen, Schalter, Lüfter, Klima, Sensoren und binäre Sensoren über YAML definieren, während das Gateway von der Integrations-Benutzeroberfläche verwaltet wird.

**Hinweis**: Neue Geräte sollten stattdessen die Integrations-Benutzeroberfläche **Konfigurieren > Gerät hinzufügen** verwenden, da sie Gerätegruppierung, modellgesteuerte Funktionen und Kanalstatusverwaltung bietet. YAML wird empfohlen für:
- Geräte mit nicht standardmäßigen oder Legacy-Profilen
- Migration von älteren Buspro-Integrationen
- Komplexe Automatisierung oder Sensorvorlagen

### YAML-Syntaxbeispiel

Fügen Sie dies zu Ihrer `configuration.yaml` hinzu:

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

### Plattformkonfiguration

Jede Plattform (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`, `switch`) akzeptiert:

| Schlüssel | Typ | Beschreibung |
| --- | --- | --- |
| `devices` | dict | Erforderlich. Zuordnung von Buspro-Adressen zu Gerätekonfigurationen. |
| `running_time` | int | Standard-Übergangsdauer in Sekunden (0 = kein Übergang). Wird pro Gerät überschrieben. |
| `ack_retry_enabled` | bool | Wiederholung beim Senden ohne ACK (Plattformstandard; pro-Gerät Außerkraftsetzungen). |

Jeder Geräteschlüssel ist die **Buspro-Adresse** im Format:
- **Licht, Abdeckung, Lüfter, Schalter**: `subnet.device.channel` (z.B. `1.5.2`)
- **Klima, Sensor, binärer Sensor**: `subnet.device` (z.B. `3.1`)

Jede Gerätekonfiguration unterstützt:
- `name` (erforderlich): Anzeigename
- `running_time`, `dimmable`, `ack_retry_enabled` (plattformspezifisch, optional)
- `profile` (optional, für Klimasensoren — z.B. `"ac"`, `"floor_heating"`)
- `object_id` (optional): Entity-ID-Slug
- `unique_id` (optional): Zur manuellen Steuerung der Entity-Registry

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

## Befehlsbestätigung (NEU!)

Die Integration unterstützt nun **optionale Befehlsbestätigung**, um sicherzustellen, dass Gerätzustandsänderungen in Home Assistant erst nach der physikalischen Bestätigung des Geräts widergespiegelt werden.

### Was ist es?

- **Ohne Bestätigung:** Befehle werden gesendet und die Benutzeroberfläche aktualisiert sich sofort (~5ms), aber wenn das Gerät den Befehl aufgrund von Netzwerkstörungen nicht empfängt, ist der Zustand der Benutzeroberfläche falsch.
- **Mit Bestätigung:** Das System wartet auf die Gerätebestätigung (100-500ms) und stellt so eine perfekte Synchronisierung zwischen Home Assistant und dem physischen Gerät sicher.

### Wann sollte ich es verwenden?

Aktivieren Sie die Bestätigung für:
- **Kritische Geräte** — Notfall-Relais, Hauptschalter
- **Unzuverlässige Netzwerke** — Hohe Störungen, Paketverluste
- **Automatisierungsabhängigkeiten** — Wenn Automatisierungen auf genauen Zustand angewiesen sind
- **Sicherheitskritische Systeme** — HVAC, Fußbodenheizung, wichtige Lasten

### Konfiguration

Fügen Sie die Bestätigung zu jedem Gerät in YAML hinzu:

```yaml
light:
  - platform: buspro
    devices:
      "1.10.1":
        name: "Kritisches Licht"
        enable_confirmation: true
        confirmation_timeout: 5.0        # Sekunden
        confirmation_retries: 3          # Wiederholungsversuche
```

**Parameter:**
- `enable_confirmation` (boolean, Standard: `false`) — Bestätigung aktivieren/deaktivieren
- `confirmation_timeout` (float, Standard: `5.0`) — Timeout in Sekunden (0.1-60)
- `confirmation_retries` (integer, Standard: `3`) — Wiederholungsanzahl (0-10)

**Empfohlene Einstellungen nach Gerätetyp:**
- Relais/Schalter/Licht: `timeout: 5.0`, `retries: 3`
- Abdeckung/Vorhang: `timeout: 10.0`, `retries: 2` (mechanisch, langsamer)
- Klima: `timeout: 5.0`, `retries: 3`
- Lüfter: `timeout: 5.0`, `retries: 3`

Für vollständige Beispiele und Best Practices siehe **[DEVICE_EXAMPLES.md](docs/de/DEVICE_EXAMPLES.md)**.

