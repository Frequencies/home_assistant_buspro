# HDL Buspro für Home Assistant

[English](../README.md) | **Deutsch**

Die Integration verwaltet das Gateway und physische HDL-Buspro-Geräte über
die Home-Assistant-Oberfläche. Eine vollständige Liste der Modelle, Entitäten
und Dienste steht in der [englischen Dokumentation](../README.md).

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

1. **Einstellungen > Geräte & Dienste > Integration hinzufügen** öffnen und
   **HDL Buspro** auswählen.
2. Gateway-Adresse und UDP-Ports eingeben. Der übliche Standardport ist `6000`.
3. Eine freie Home-Assistant-Buspro-Adresse im Format `Subnetz.Gerät` eingeben.
   Der Standard `200.200` darf keinem anderen Buspro-Gerät gehören.
4. **Konfigurieren > Gerät hinzufügen** öffnen, Gerätetyp und genaues Modell
   auswählen und die physische Buspro-Adresse sowie einen Namen eingeben.
5. Benötigte Kanäle oder Funktionen benennen. Ein leerer Name lässt den Kanal
   deaktiviert und verhindert die Erstellung seiner Entität.

Bekannte Modelle verwenden die feste Kanalanzahl oder Funktionsliste aus dem
Gerätekatalog. Bei generischen Profilen gibt der Benutzer die Kanalanzahl
innerhalb des unterstützten Limits an. Nach dem Speichern wird der
Konfigurationseintrag neu geladen und alle Entitäten werden unter einem
physischen Gerät gruppiert.

Zum Ändern **Konfigurieren > Gerät bearbeiten** öffnen. Bei UI-verwalteten
Geräten können Modell, Name und Kanäle geändert oder das Gerät entfernt
werden. Protokolleinstellungen älterer YAML-Geräte müssen weiterhin in YAML
geändert werden; danach Home Assistant neu starten.

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

## Katalogabgleich und Tests

Zum Prüfen des Modellkatalogs gegenüber der gepflegten offiziellen HDL-Liste:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

Bei Legacy-YAML-Geräten normalisiert die Integration fehlende Profile jetzt
anhand der Modellmetadaten. Unbekannte Modelle oder ungültige
Profil-Zeichenfolgen werden als Warnung protokolliert und fallen auf
`sensor_status` zurück.

Fokussierte Tests der Integration:

```bash
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -p 'test_*.py'
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -p 'test_*.py'
```
