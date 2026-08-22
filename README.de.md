# HDL Buspro

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## Sprachen

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


## Erste Einrichtung

### Gateway-Konfiguration
1. Öffnen Sie **Einstellungen > Geräte & Dienste > Integration hinzufügen** und wählen Sie
   **HDL Buspro**.
2. Geben Sie den Gateway-Host und UDP-Ports ein. Port `6000` ist die normale Standardeinstellung.
3. Geben Sie eine ungenutzte Home Assistant Buspro-Adresse im Format `subnet.device` ein.
   Der Standard ist `200.200`; sie darf nicht zu einem anderen Buspro-Gerät gehören.

### Geräte hinzufügen
Nach Abschluss der Gateway-Einrichtung:

1. Öffnen Sie **Einstellungen > Geräte & Dienste > HDL Buspro > Konfigurieren**.
2. Klicken Sie auf **Gerät hinzufügen**, um ein physisches Buspro-Modul hinzuzufügen.
3. **Wählen Sie den Gerätetyp** (Relais, Dimmer, Abdeckung, Klima, Sensor usw.).
4. **Wählen Sie das genaue Modell** aus, das Ihrer Hardware entspricht.
5. **Geben Sie die Buspro-Adresse** im Format `subnet.device` ein (z. B. `1.5`).
6. **Geben Sie den Gerätenamen** ein (z. B. "Wohnzimmerleuchten").
7. **Benennen Sie jeden Kanal** — lassen Sie die Einstellung leer, um einen Kanal zu deaktivieren.
8. Klicken Sie auf **Speichern**.

Home Assistant gruppiert Entitäten automatisch nach physischem Modul in der Geräteregistrierung.

**Beispiele für UI- und YAML-Konfigurationen für alle Gerätetypen finden Sie unter [DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md).**

### Geräte bearbeiten

Um ein vorhandenes Gerät zu ändern, öffnen Sie **Konfigurieren > Gerät bearbeiten**. Sie können:
- Das Gerät umbenennen
- Einzelne Kanäle umbenennen, aktivieren oder deaktivieren
- Das Modell ändern (was die Kanalanzahl ändern kann)
- Das Gerät vollständig entfernen

UI-verwaltete Geräte unterstützen die vollständige Bearbeitung. Legacy YAML-Geräte können Registrierungsnamen-Steuerelemente anzeigen, aber ihre Protokollkonfiguration muss weiterhin in YAML geändert werden. Starten Sie Home Assistant neu, nachdem Sie YAML geändert haben.

### Schnellbeispiel: Hinzufügen eines 4-Kanal-Relaismoduls

1. Modell: `HDL-MR0410.431` (4 Relaiskanäle)
2. Buspro-Adresse: `1.10`
3. Gerätename: "Room relays"
4. Kanalnamen: "Ceiling light", "Wall lamp", "", "Fan"
5. Klicken Sie auf **Speichern**

Home Assistant erstellt automatisch Entitäten: `light.room_relays_ceiling_light`, `light.room_relays_wall_lamp`, `switch.room_relays_fan`

Vollständige UI- und YAML-Beispiele für alle Gerätetypen finden Sie unter **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)**.

## Konfigurationsoptionen

Die Buspro-Integration unterstützt sowohl **UI-basierte Einrichtung** als auch **YAML-Konfiguration**:

### UI-Einrichtung
Die einfachste Möglichkeit, Geräte hinzuzufügen — siehe **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)** für schrittweise Beispiele für alle Gerätetypen.

### YAML-Konfiguration  
Die Integration unterstützt zwei komplementäre YAML-Ansätze:
- **Entitätsorientiert** (Legacy) — einzelne Entitätsdateien organisiert nach Domäne
- **Geräteorientiert** (Modern) — vollständige Gerätedefinitionen mit allen Kanälen

**Umfassende YAML-Dokumentation, Beispiele und Best Practices finden Sie unter [DUAL_MODE_YAML.md](docs/en/DUAL_MODE_YAML.md)** (auch verfügbar auf [Беларуская](docs/be/DUAL_MODE_YAML.md) | [Deutsch](docs/de/DUAL_MODE_YAML.md) | [Español](docs/es/DUAL_MODE_YAML.md) | [Français](docs/fr/DUAL_MODE_YAML.md) | [Italiano](docs/it/DUAL_MODE_YAML.md) | [Nederlands](docs/nl/DUAL_MODE_YAML.md) | [Norsk](docs/no/DUAL_MODE_YAML.md) | [Русский](docs/ru/DUAL_MODE_YAML.md) | [Українська](docs/uk/DUAL_MODE_YAML.md))

## Größere Änderungen in 2.2.0

Lesen Sie diesen Abschnitt vor dem Upgrade von 2.1.x.

> [!WARNING]
> Diese Version ändert die Gerätebesitzverhältnisse, die Kanalerstellung, die Semantik von Panel-Ereignissen
> und den eingebetteten Python-Konstruktor. Vervollständigen Sie die Upgrade-
> Checkliste, bevor Sie Legacy YAML entfernen.

1. **Installationsspezifische Geräte werden nicht mehr in die Integration integriert.**
   Geräteadressen, Namen, Kanalzuweisungen und Geräteanzahl gehören jetzt
   zu Konfigurationseintrag-Optionen oder zur Home Assistant-Geräteregistrierung. Der Gerätekatalog
   enthält nur Hardware-Funktionen.

2. **UI-verwaltete Relaismodule verwenden ihre physische Kanalanzahl.**
   `HDL-MR1210.433` zeigt immer 12 Kanalplätze an und
   `HDL-MR1610.433` zeigt immer 16 an. Ein vorhandenes Gerät kann nicht
   unter die physische Kanalanzahl seines Modells reduziert werden.

3. **Ein leerer Kanalname deaktiviert den Kanal.**
   Deaktivierte Kanäle werden nicht instanziiert, erstellen keine Protokollobjekte und
   sind in der Entity Registry durch die Integration als deaktiviert gekennzeichnet. Das Eingeben eines
   Namens aktiviert den Kanal erneut.

4. **Das genaue Modell steuert generierte Entitäten.**
   Ein generisches `HDL panel` hat keine bekannte Schaltflächenanzahl. Wählen Sie das physische Modell
   aus, um Schaltflächenereignisse zu erstellen. Das Ändern eines Modells lädt den Konfigurationseintrag neu.

5. **Home Assistant hat seine eigene Buspro-Adresse.**
   Vorhandene Konfigurationseinträge werden zu `200.200` migriert. Diese Adresse muss auf dem
   Buspro-Netzwerk nicht verwendet werden und kann unter **Konfigurieren > Gateway-Einstellungen** geändert werden.

6. **Die IP-Adresse der Paketquelle ist nicht mehr hartcodiert.**
   Die Integration leitet sie aus der Route zum konfigurierten Gateway ab. Ein
   Home Assistant-Host mit mehreren Schnittstellen muss das Gateway durch die
   vorgesehene LAN-Schnittstelle weiterleiten.

7. **Panel-Aktionsereignisse sind jetzt dekodiert.**
   Automationen, die alte Rohaktionswerte verwenden, sollten überprüft werden. Ereignisse verwenden
   `channel_on`, `channel_off`, `channel_level`, `scene`,
   `universal_switch_on` oder `universal_switch_off`, mit Ziel- und Zusammenfassungsattributen,
   wo sie aufgelöst werden können.

8. **Die eingebettete Python-API hat sich geändert.**
   Direkte `pybuspro.Buspro`-Benutzer müssen `client_address` angeben; siehe
   [pybuspro/README.md](pybuspro/README.md).

Die Integration liest während der Migration weiterhin Legacy YAML-Entitäten. Bewahren Sie nicht denselben
physischen Kanal sowohl in YAML- als auch in UI-verwalteter Konfiguration auf, da dies
doppelte Entitäten und doppelte Protokollabos erstellen kann.

## Upgrade-Checkliste

1. Starten Sie Home Assistant neu, nachdem Sie die benutzerdefinierte Komponente ersetzt haben.
2. Öffnen Sie **Einstellungen > Geräte & Dienste > HDL Buspro > Konfigurieren**.
3. Überprüfen Sie den Gateway-Host, die Ports und die ungenutzte Home Assistant Buspro-Adresse.
4. Öffnen Sie jedes physische Gerät und wählen Sie sein genaues Modell aus.
5. Überprüfen Sie jeden Relaiskanalnamen. Leere Kanäle bleiben absichtlich deaktiviert.
6. Überprüfen Sie Automationen, die Panel-Aktionsereignisse verwenden.
7. Entfernen oder kommentieren Sie migrierte YAML-Entitäten nur, nachdem ihre UI-verwalteten
   Ersatzkomponenten die erwarteten Entity IDs beibehalten haben.

## Gateway-Einrichtung

Fügen Sie **HDL Buspro** unter **Einstellungen > Geräte & Dienste** hinzu und konfigurieren Sie:

- **Host**: HDL IP Gateway-Hostname oder IPv4-Adresse.
- **Port**: primärer UDP-Port, normalerweise `6000`.
- **UDP-Send-/Empfangsports**: ändern Sie diese nur für ein nicht standardisiertes Gateway.
- **Home Assistant Buspro-Adresse**: eine ungenutzte `subnet.device`-Identität, z. B.
  der Migrations-Standard `200.200`.

UDP hat keinen Verbindungs-Handshake. Das Setup validiert die Adressauflösung, das Routing
und die Erstellung des lokalen Empfangssockets, ohne anzunehmen, dass ein Gerät
unter einer hartcodierten Buspro-Adresse vorhanden ist.

## Geräteverwaltung

Öffnen Sie **Konfigurieren** in der Integration und wählen Sie:

- **Gateway-Einstellungen**, um Netzwerkeinstellungen und Client-Identität zu aktualisieren.
- **Gerät hinzufügen**, um einen Gerätetyp, Modell, Buspro-Adresse und Kanal- oder
  Funktionsnamen auszuwählen.
- **Gerät bearbeiten**, um Kanäle umzubenennen, Kanäle zu aktivieren oder zu deaktivieren, ein
  UI-verwaltetes Gerät zu entfernen oder das Modell eines vorhandenen Registrierungsgeräts zu korrigieren.

Physische Adressen werden in Home Assistant als Geräteserienmummer angezeigt.
Entitäten, die zu einem physischen Modul gehören, sind an denselben Device
Registry-Eintrag gebunden.

## Unterstützte Modelle

| Modell | Home Assistant-Unterstützung |
| --- | --- |
| `HDL-MBUS01IP.431` | Gateway-Gerätemetadaten |
| `HDL-MCLog.431` | Verbindung, Firmware-Abfrage, zuletzt gesehen, Logic-Ereignisse |
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
| `HDL-MD0206.432` | 2 Dimmerkanäle |
| `HDL-MD0403.432` | 4 Dimmerkanäle |
| `HDL-MD0602.432` | 6 Dimmerkanäle |
| `HDL-MDT0203.433` | 2 Trailing-Edge-Dimmerkanäle |
| `HDL-MDT0203.532` | 2 Trailing-Edge-Dimmerkanäle |
| `HDL-MDT04015.433` | 4 Trailing-Edge-Dimmerkanäle |
| `HDL-MDT04015.532` | 4 Trailing-Edge-Dimmerkanäle |
| `HDL-MDT06015.433` | 6 Trailing-Edge-Dimmerkanäle |
| `HDL-MDT06015.533` | 6 Trailing-Edge-Dimmerkanäle |
| `HDL-MDLED0605.432` | 6 Dimmerkanäle und Diagnose |
| `HDL-MRDA0610.432` | 6 Vorschalt-Dimmerkanäle |
| `HDL-MRDA0610.433` | 6 Vorschalt-Dimmerkanäle |
| `SB-DN-DALI64` | Bis zu 64 DALI-Kanäle |
| `HDL-MS04.432` | 4 Trockenkonaktkanäle |
| `HDL-MS24.232` | 24 Trockenkonaktkanäle |
| `HDL-MSP02.4C` | Temperatur, Beleuchtungsstärke, Bewegung |
| `HDL-MSP07M.4C` | Temperatur, Beleuchtungsstärke, Luftfeuchtigkeit, Bewegung, zwei Kontakte |
| `HDL-MS08M.4C` | Temperatur, Beleuchtungsstärke, Bewegung |
| `HDL-MS12M.4C` | Temperatur, Beleuchtungsstärke, Luftfeuchtigkeit, Bewegung, zwei Kontakte |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Temperatur und Panel-Aktionen |
| `HDL-MPTL4.460` | Temperatur und Panel-Aktionen |
| `HDL-MP4S/TILE.48` | Temperatur, vier Schaltflächenereignisse, Panel-Aktionen |
| `HDL-MP2B/TILE.48` | Temperatur, zwei Schaltflächenereignisse, Panel-Aktionen |
| `HDL-MP4B-A/TILE.48` | Temperatur, vier Schaltflächenereignisse, Panel-Aktionen |
| `HDL-MP4B/TILE.48` | Temperatur, vier Schaltflächenereignisse, Panel-Aktionen |
| `HDL-MP2B.480` | Temperatur, zwei Schaltflächenereignisse, Panel-Aktionen |
| `HDL-MP4B.480` | Temperatur, vier Schaltflächenereignisse, Panel-Aktionen |
| `HDL-MPL8.431` | Temperatur, acht Schaltflächenereignisse, Panel-Aktionen |
| `HDL-M/PT4.1` | Temperatur, vier Schaltflächenereignisse, Panel-Aktionen |
| `HDL-MFH04.432` | 4 Flächenheizungskanäle |
| `HDL-MFH06.432` | 6 Flächenheizungskanäle |
| `HDL-M/HVAC8.1` | AC-Klimaentitäten |
| `HDL-MPED4.431` | AC-Klimaentitäten |
| `HDL-MW02.431` | 2 Vorhang-/Abdeckungskanäle |
| `HDL-MWM45.431` | Vorhang-/Abdeckungsentitäten (konfigurierbare Kanäle) |

Generische AC-, Vorhang-, Drehzahl-Lüfter-, Ein-/Aus-Lüfter-, Universal-Schalter- und
Panel-Profile sind ebenfalls verfügbar. Ihre physische Adresse und eine konfigurierbare
Ausgangsanzahl werden vom Benutzer bereitgestellt; sie sind kein Installationsinventar.

Einige Modelle werden über Familien-Mapping oder generische Protokollkompatibilität hinzugefügt.
Beim Start der Integration protokolliert Buspro explizite Modellunterstützungsnotizen für diese
Modelle (z. B. modellvalidiert vs. familien-zugeordnetes Verhalten) zusammen mit
erkannten physischen Adressen.

Für Legacy YAML-Geräte normalisiert die Integration nun fehlende Profile mithilfe von
Katalogmodellmetadaten. Unbekannte Modelle und nicht unterstützte Profilzeichenfolgen
werden als Startwarnungen gemeldet und fallen dann auf generisches `sensor_status`-Verhalten
zurück, um das Setup funktionsfähig zu halten.

## Katalogwartungs-Helfer

Um den Integrationskatalog mit der gepflegten offiziellen HDL-Modellliste zu vergleichen,
führen Sie Folgendes aus:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

Der Helfer liest `custom_components/buspro/devices/official_models.json` und
gibt aus:

- Offizielle Modelle, die in `DEVICE_CATALOG` fehlen
- Katalogmodelle, die nicht in der offiziellen Liste vorhanden sind
- Nur für die Integration verfügbare virtuelle generische Modelle

Verwenden Sie den Strict-Modus für CI-ähnliche Überprüfungen (Ausgang ungleich null, wenn offizielle Modelle
im Katalog fehlen):

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Entity-Verhalten

### Relais

Ein gemeinsamer Koordinator fragt den Relaisstatus einmal pro physischem Modul ab und
verteilt die Antwort an alle aktivierten Kanal-Entitäten. Deaktivierte Kanäle
abonnieren den Bus nicht und fragen ihn nicht ab.

### Panels

Bekannte Schaltflächenpanels erstellen eine `event`-Entität pro physischer Schaltfläche, ein `Action`-
Ereignis und einen `Last action`-Sensor. UI-Schaltflächenereignis-Entitäten stellen empfangene
physische Buspro-Schaltflächentelegramme dar; sie simulieren keinen Hardware-Druck.

### Dimmer

Unterstützte Dimmer können Konnektivität, maximale Helligkeit pro Kanal,
Lasttyp und vom Protokoll gemeldete Mindesthelligkeit anzeigen. `Not reported` bedeutet, dass das
Gerät die Protokollsentinel anstelle eines verwendbaren Werts zurückgegeben hat.

### Logic-Controller

`HDL-MCLog.431` zeigt schreibgeschützte Konnektivität, Firmware-Version, zuletzt gesehen,
und Logic-Ereignis-Entitäten an. Einige Firmware antwortet nicht auf die Standard-Firmware-
Abfrage; in diesem Fall bleibt die Firmware-Entität nicht verfügbar. Logic-Blöcke
sind nicht beschreibbar, da ihre Änderung die Controller-Programmierung überschreiben kann.

## Services

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` sendet einen Rohprotokoll-Befehl und sollte nur mit
einem verifizierten HDL-Operationscode und einer Nutzlast verwendet werden.

## YAML-Konfiguration (Legacy)

Die YAML-Gerätekonfiguration wird vollständig neben der Gateway-Verwaltung durch Konfigurationseintrag unterstützt. Sie können Lichter, Abdeckungen, Schalter, Lüfter, Klima, Sensoren und Binärsensoren via YAML definieren, während das Gateway durch die Integration UI verwaltet wird.

**Hinweis**: Neue Geräte sollten stattdessen die **Konfigurieren > Gerät hinzufügen**-UI der Integration verwenden, da sie Gerätegruppen, modellgesteuerte Funktionen und Kanalzustandsverwaltung bietet. YAML wird empfohlen für:
- Geräte mit nicht standardisierten oder Legacy-Profilen
- Migration von älteren Buspro-Integrationen
- Komplexe Automatisierungs- oder Sensorvorlagen

### YAML-Syntax-Beispiel

Fügen Sie zu Ihrer `configuration.yaml` hinzu:

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
| `ack_retry_enabled` | bool | Wiederholung sendet bei keinem ACK (Plattformstandard; pro Gerät überschrieben). |

Jeder Geräteschlüssel ist die **Buspro-Adresse** im Format:
- **Licht, Abdeckung, Lüfter, Schalter**: `subnet.device.channel` (z. B. `1.5.2`)
- **Klima, Sensor, Binärsensor**: `subnet.device` (z. B. `3.1`)

Jede Gerätekonfiguration unterstützt:
- `name` (erforderlich): Anzeigename
- `running_time`, `dimmable`, `ack_retry_enabled` (plattformspezifisch, optional)
- `profile` (optional, für Klimasensoren — z. B. `"ac"`, `"floor_heating"`)
- `object_id` (optional): Entity ID-Slug
- `unique_id` (optional): Für manuelle Entity-Registry-Steuerung

## Entwicklung

### Testsuites ausführen

Aus dem Home Assistant-Konfigurationsverzeichnis:

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

Protokolltests umfassen Telegramm-Parsing, Gerätekoordination und Kern-Task/Callback-Sicherheit. Integrationstests umfassen Gerätekatalog, verwaltete Gerätelogik, YAML-Normalisierung und Modellunterstützungsverfolgung.
