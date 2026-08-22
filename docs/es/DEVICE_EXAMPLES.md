# Ejemplos de Configuración de Dispositivos HDL Buspro

**Idiomas disponibles:** [🇧🇾 Беларуская](../be/DEVICE_EXAMPLES.md) | [🇩🇪 Deutsch](../de/DEVICE_EXAMPLES.md) | [🇬🇧 English](../en/DEVICE_EXAMPLES.md) | 🇪🇸 Español | [🇫🇷 Français](../fr/DEVICE_EXAMPLES.md) | [🇮🇹 Italiano](../it/DEVICE_EXAMPLES.md) | [🇳🇱 Nederlands](../nl/DEVICE_EXAMPLES.md) | [🇳🇴 Norsk](../no/DEVICE_EXAMPLES.md) | [🇷🇺 Русский](../ru/DEVICE_EXAMPLES.md) | [🇺🇦 Українська](../uk/DEVICE_EXAMPLES.md)

---

Esta guía proporciona ejemplos de configuración prácticos de interfaz de usuario y YAML para todos los tipos de dispositivos compatibles en la integración HDL Buspro.

**Tabla de contenidos:**
- [Dispositivos de relé](#dispositivos-de-relé)
- [Dispositivos atenuadores](#dispositivos-atenuadores)
- [Dispositivos de cobertura (persianas/contraventanas)](#dispositivos-de-cobertura)
- [Dispositivos ventiladores](#dispositivos-ventiladores)
- [Dispositivos climáticos](#dispositivos-climáticos)
- [Dispositivos sensores](#dispositivos-sensores)
- [Dispositivos sensores binarios](#dispositivos-sensores-binarios)

---

## Dispositivos de relé

Los dispositivos de relé son interruptores simples encendido/apagado utilizados para iluminación, ventiladores y otras cargas binarias.

**Modelos compatibles:**
- `HDL-MR0410.431` - 4 canales de relé
- `HDL-MR0810.432` - 8 canales de relé
- `HDL-MR1210.433` - 12 canales de relé
- `HDL-MR1610.433` - 16 canales de relé
- Variantes de relé de alta potencia HDL (MR0416, MR0816, MR1216, MR1616, MR0420C, etc.)

### Ejemplo de configuración de interfaz de usuario

**Pasos:**
1. Vaya a **Configuración > Dispositivos y servicios > HDL Buspro > Configurar**
2. Haga clic en **Agregar dispositivo**
3. Seleccione el tipo de dispositivo: **Relé**
4. Seleccione el modelo exacto: **HDL-MR0410.431** (4 canales)
5. Ingrese la dirección Buspro: `1.10`
6. Ingrese el nombre del dispositivo: "Luces de la sala de estar"
7. Nombre los canales:
   - Canal 1: "Luz de techo"
   - Canal 2: "Lámpara de mesa"
   - Canal 3: "Lámpara de pared"
   - Canal 4: "" (dejar vacío para desactivar)
8. Haga clic en **Guardar**

**Resultado:**
- `light.luces_de_la_sala_de_estar_luz_de_techo`
- `light.luces_de_la_sala_de_estar_lámpara_de_mesa`
- `light.luces_de_la_sala_de_estar_lámpara_de_pared`

### Ejemplo de configuración YAML

**Centrado en entidades (archivos individuales):**

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.10.1":
        name: "Living Room Ceiling Light"
        object_id: "ceiling_light"
      "1.10.2":
        name: "Living Room Table Lamp"
        object_id: "table_lamp"
      "1.10.3":
        name: "Living Room Wall Sconce"
        object_id: "wall_sconce"
```

**Centrado en dispositivo (definición completa del dispositivo):**

```yaml
# configuration.yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 200.200
  devices:
    - address: "1.10"
      name: "Living Room Relays"
      model: "HDL-MR0410.431"
      device_type: "relay"
      channels:
        - number: 1
          name: "Ceiling Light"
          enabled: true
          object_id: "hdl_light_ceiling"
        - number: 2
          name: "Table Lamp"
          enabled: true
          object_id: "hdl_light_table"
        - number: 3
          name: "Wall Sconce"
          enabled: true
          object_id: "hdl_light_sconce"
        - number: 4
          enabled: false
```

---

## Dispositivos atenuadores

Los dispositivos atenuadores controlan los niveles de brillo (0-255) para luces regulables.

**Modelos compatibles:**
- `HDL-MD0206.432` - 2 canales atenuadores
- `HDL-MD0403.432` - 4 canales atenuadores
- `HDL-MD0602.432` - 6 canales atenuadores
- Atenuadores de borde de cola HDL (MDT0203, MDT04015, MDT06015, etc.)
- `HDL-MDLED0605.432` - 6 canales atenuadores con diagnósticos

### Ejemplo de configuración de interfaz de usuario

**Pasos:**
1. Vaya a **Configuración > Dispositivos y servicios > HDL Buspro > Configurar**
2. Haga clic en **Agregar dispositivo**
3. Seleccione el tipo de dispositivo: **Atenuador**
4. Seleccione el modelo exacto: **HDL-MD0602.432** (6 canales)
5. Ingrese la dirección Buspro: `1.5`
6. Ingrese el nombre del dispositivo: "Atenuadores de dormitorio"
7. Nombre los canales:
   - Canal 1: "Luz principal"
   - Canal 2: "Lámpara de noche izquierda"
   - Canal 3: "Lámpara de noche derecha"
   - Canales 4-6: dejar vacíos
8. Haga clic en **Guardar**

**Resultado:**
- `light.atenuadores_de_dormitorio_luz_principal` (regulable 0-255)
- `light.atenuadores_de_dormitorio_lámpara_de_noche_izquierda` (regulable 0-255)
- `light.atenuadores_de_dormitorio_lámpara_de_noche_derecha` (regulable 0-255)

### Ejemplo de configuración YAML

**Centrado en entidades:**

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Bedroom Main Light"
        dimmable: true
      "1.5.2":
        name: "Bedroom Bedside Left"
        dimmable: true
      "1.5.3":
        name: "Bedroom Bedside Right"
        dimmable: true
```

**Centrado en dispositivo:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "1.5"
      name: "Bedroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
          object_id: "hdl_dimmer_main"
        - number: 2
          name: "Bedside Left"
          enabled: true
          object_id: "hdl_dimmer_left"
        - number: 3
          name: "Bedside Right"
          enabled: true
          object_id: "hdl_dimmer_right"
        - number: 4
          enabled: false
        - number: 5
          enabled: false
        - number: 6
          enabled: false
```

---

## Dispositivos de cobertura

Los dispositivos de cobertura controlan persianas motorizadas, contraventanas y cortinas.

**Modelos compatibles:**
- `HDL-MW02.431` - 2 canales de cortina/cobertura
- `HDL-MWM45.431` - Entidades de cortina/cobertura (canales configurables)

### Ejemplo de configuración de interfaz de usuario

**Pasos:**
1. Vaya a **Configuración > Dispositivos y servicios > HDL Buspro > Configurar**
2. Haga clic en **Agregar dispositivo**
3. Seleccione el tipo de dispositivo: **Cobertura**
4. Seleccione el modelo exacto: **HDL-MW02.431** (2 canales)
5. Ingrese la dirección Buspro: `2.10`
6. Ingrese el nombre del dispositivo: "Persianas de la sala de estar"
7. Nombre los canales:
   - Canal 1: "Ventanas"
   - Canal 2: "Puerta del patio"
8. Haga clic en **Guardar**

**Resultado:**
- `cover.persianas_de_la_sala_de_estar_ventanas`
- `cover.persianas_de_la_sala_de_estar_puerta_del_patio`

### Ejemplo de configuración YAML

**Centrado en dispositivo:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "2.10"
      name: "Living Room Blinds"
      model: "HDL-MW02.431"
      device_type: "cover"
      channels:
        - number: 1
          name: "Windows"
          enabled: true
          object_id: "hdl_cover_windows"
        - number: 2
          name: "Patio Door"
          enabled: true
          object_id: "hdl_cover_patio"
```

---

## Dispositivos ventiladores

Los dispositivos ventiladores controlan ventiladores de velocidad variable.

**Modelos compatibles:**
- Perfil de ventilador genérico (ventiladores de velocidad variable)

### Ejemplo de configuración de interfaz de usuario

**Pasos:**
1. Vaya a **Configuración > Dispositivos y servicios > HDL Buspro > Configurar**
2. Haga clic en **Agregar dispositivo**
3. Seleccione el tipo de dispositivo: **Ventilador**
4. Seleccione el modelo exacto: **Genérico** (especifique el número de canales)
5. Ingrese la dirección Buspro: `3.5`
6. Ingrese el nombre del dispositivo: "Ventilador de extracción del baño"
7. Nombre el canal: "Ventilador principal"
8. Haga clic en **Guardar**

**Resultado:**
- `fan.ventilador_de_extracción_del_baño_ventilador_principal` (control de velocidad 0-255)

### Ejemplo de configuración YAML

**Centrado en dispositivo:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "3.5"
      name: "Bathroom Exhaust Fan"
      device_type: "fan"
      channels:
        - number: 1
          name: "Main Fan"
          enabled: true
          object_id: "hdl_fan_exhaust"
```

---

## Dispositivos climáticos

Los dispositivos climáticos controlan la temperatura y los sistemas HVAC.

**Modelos compatibles:**
- `HDL-MFH04.432` - 4 canales de calefacción radiante
- `HDL-MFH06.432` - 6 canales de calefacción radiante
- `HDL-M/HVAC8.1` - Control climático CA
- `HDL-MPED4.431` - Control climático CA
- Perfil CA genérico
- Perfil de calefacción radiante genérico

### Ejemplo de configuración de interfaz de usuario - Unidad CA

**Pasos:**
1. Vaya a **Configuración > Dispositivos y servicios > HDL Buspro > Configurar**
2. Haga clic en **Agregar dispositivo**
3. Seleccione el tipo de dispositivo: **Clima**
4. Seleccione el modelo exacto: **HDL-M/HVAC8.1** (CA)
5. Ingrese la dirección Buspro: `3.1`
6. Ingrese el nombre del dispositivo: "AC de la sala de estar"
7. Haga clic en **Guardar**

**Resultado:**
- `climate.ac_de_la_sala_de_estar` (temperatura objetivo, modo, control de energía)

### Ejemplo de configuración YAML

**Centrado en dispositivo:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "3.1"
      name: "Living Room AC"
      model: "HDL-M/HVAC8.1"
      device_type: "ac"
      object_id: "hdl_climate_ac"

    - address: "4.2"
      name: "Master Bedroom Floor Heating"
      model: "HDL-MFH06.432"
      device_type: "floor_heating"
      channels:
        - number: 1
          name: "Zone 1"
          enabled: true
        - number: 2
          name: "Zone 2"
          enabled: true
        - number: 3
          enabled: false
```

---

## Dispositivos sensores

Los dispositivos sensores proporcionan datos de temperatura, humedad, iluminancia y movimiento.

**Modelos compatibles:**
- `HDL-MSP02.4C` - Temperatura, iluminancia, movimiento
- `HDL-MSP07M.4C` - Temperatura, iluminancia, humedad, movimiento, 2 contactos
- `HDL-MS08M.4C` - Temperatura, iluminancia, movimiento
- `HDL-MS12M.4C` - Temperatura, iluminancia, humedad, movimiento, 2 contactos
- `HDL-MCLog.431` - Controlador lógico (solo lectura)
- Sensores de temperatura de panel (MPTL, MP2B, MP4B, MPL8, etc.)

### Ejemplo de configuración de interfaz de usuario

**Pasos:**
1. Vaya a **Configuración > Dispositivos y servicios > HDL Buspro > Configurar**
2. Haga clic en **Agregar dispositivo**
3. Seleccione el tipo de dispositivo: **Multisensor**
4. Seleccione el modelo exacto: **HDL-MSP07M.4C**
5. Ingrese la dirección Buspro: `2.5`
6. Ingrese el nombre del dispositivo: "Sensor de la sala de estar"
7. Haga clic en **Guardar**

**Resultado:**
- `sensor.sensor_de_la_sala_de_estar_temperatura`
- `sensor.sensor_de_la_sala_de_estar_iluminancia`
- `sensor.sensor_de_la_sala_de_estar_humedad`
- `binary_sensor.sensor_de_la_sala_de_estar_movimiento`
- 2 contactos secos adicionales

### Ejemplo de configuración YAML

**Centrado en entidades:**

```yaml
# configuration.yaml
sensor:
  - platform: buspro
    devices:
      "2.5":
        name: "Living Room Sensor"
        model: "HDL-MSP07M.4C"
        profile: "12in1"
        entities:
          - type: temperature
            name: "Temperature"
            object_id: "hdl_temp_living_room"
          - type: illuminance
            name: "Light Level"
            object_id: "hdl_lux_living_room"
          - type: humidity
            name: "Humidity"
            object_id: "hdl_humidity_living_room"

binary_sensor:
  - platform: buspro
    devices:
      "2.5":
        name: "Living Room Sensor"
        model: "HDL-MSP07M.4C"
        profile: "12in1"
        entities:
          - type: motion
            name: "Motion"
            object_id: "hdl_motion_living_room"
          - type: dry_contact
            number: 1
            name: "Door Contact"
            object_id: "hdl_door_living_room"
          - type: dry_contact
            number: 2
            name: "Window Contact"
            object_id: "hdl_window_living_room"
```

**Centrado en dispositivo:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "2.5"
      name: "Living Room Sensor"
      model: "HDL-MSP07M.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Temperature"
          object_id: "hdl_temp_living_room"
        - type: illuminance
          name: "Illuminance"
          object_id: "hdl_lux_living_room"
        - type: humidity
          name: "Humidity"
          object_id: "hdl_humidity_living_room"
        - type: motion
          name: "Motion"
          object_id: "hdl_motion_living_room"
        - type: dry_contact
          number: 1
          name: "Door Contact"
          object_id: "hdl_door_contact"
        - type: dry_contact
          number: 2
          name: "Window Contact"
          object_id: "hdl_window_contact"
```

---

## Dispositivos sensores binarios

Los dispositivos sensores binarios proporcionan estado encendido/apagado de contactos secos y sensores de puerta/ventana.

**Modelos compatibles:**
- `HDL-MS04.432` - 4 canales de contacto seco
- `HDL-MS24.232` - 24 canales de contacto seco
- Multisensores con contactos integrados (MSP07M, MS12M, etc.)

### Ejemplo de configuración de interfaz de usuario

**Pasos:**
1. Vaya a **Configuración > Dispositivos y servicios > HDL Buspro > Configurar**
2. Haga clic en **Agregar dispositivo**
3. Seleccione el tipo de dispositivo: **Contacto seco**
4. Seleccione el modelo exacto: **HDL-MS04.432** (4 canales)
5. Ingrese la dirección Buspro: `1.20`
6. Ingrese el nombre del dispositivo: "Sensores de puerta y ventana"
7. Nombre los canales:
   - Canal 1: "Puerta de entrada"
   - Canal 2: "Puerta de garaje"
   - Canal 3: "Ventana de la sala de estar"
   - Canal 4: dejar vacío
8. Haga clic en **Guardar**

**Resultado:**
- `binary_sensor.sensores_de_puerta_y_ventana_puerta_de_entrada`
- `binary_sensor.sensores_de_puerta_y_ventana_puerta_de_garaje`
- `binary_sensor.sensores_de_puerta_y_ventana_ventana_de_la_sala_de_estar`

### Ejemplo de configuración YAML

**Centrado en dispositivo:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "1.20"
      name: "Door & Window Sensors"
      model: "HDL-MS04.432"
      device_type: "dry_contact"
      channels:
        - number: 1
          name: "Front Door"
          enabled: true
          object_id: "hdl_door_front"
        - number: 2
          name: "Garage Door"
          enabled: true
          object_id: "hdl_door_garage"
        - number: 3
          name: "Living Room Window"
          enabled: true
          object_id: "hdl_window_living_room"
        - number: 4
          enabled: false
```

---

## Ejemplo complejo multi-dispositivo

Aquí hay un archivo de configuración completo que muestra múltiples tipos de dispositivos trabajando juntos:

```yaml
# configuration.yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 200.200
  devices:
    # Relay devices
    - address: "1.10"
      name: "Living Room Lights"
      model: "HDL-MR0410.431"
      device_type: "relay"
      channels:
        - number: 1
          name: "Ceiling Light"
          enabled: true
        - number: 2
          name: "Table Lamp"
          enabled: true
        - number: 3
          name: "Wall Sconce"
          enabled: true
        - number: 4
          enabled: false

    # Dimmer devices
    - address: "1.5"
      name: "Bedroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
        - number: 2
          name: "Bedside Left"
          enabled: true
        - number: 3
          name: "Bedside Right"
          enabled: true
        - number: 4
          enabled: false
        - number: 5
          enabled: false
        - number: 6
          enabled: false

    # Cover devices (blinds)
    - address: "2.10"
      name: "Blinds"
      model: "HDL-MW02.431"
      device_type: "cover"
      channels:
        - number: 1
          name: "Living Room"
          enabled: true
        - number: 2
          name: "Patio"
          enabled: true

    # Climate
    - address: "3.1"
      name: "AC Unit"
      model: "HDL-M/HVAC8.1"
      device_type: "ac"

    # Sensors
    - address: "2.5"
      name: "Living Room Sensor"
      model: "HDL-MSP07M.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Temperature"
        - type: illuminance
          name: "Illuminance"
        - type: humidity
          name: "Humidity"
        - type: motion
          name: "Motion"
        - type: dry_contact
          number: 1
          name: "Door"
        - type: dry_contact
          number: 2
          name: "Window"

    # Dry contacts
    - address: "1.20"
      name: "Door Sensors"
      model: "HDL-MS04.432"
      device_type: "dry_contact"
      channels:
        - number: 1
          name: "Front Door"
          enabled: true
        - number: 2
          name: "Garage Door"
          enabled: true
        - number: 3
          enabled: false
        - number: 4
          enabled: false
```

---

## Consejos y mejores prácticas

1. **Usar la interfaz de usuario para configuraciones simples** - La interfaz de usuario proporciona una forma intuitiva de agregar y administrar dispositivos sin necesidad de escribir YAML.

2. **Usar YAML para configuraciones complejas o programáticas** - YAML es mejor para instalaciones grandes o cuando necesita control de versiones.

3. **Nombres de dirección** - Siempre use el formato `subnet.device` para direcciones (por ejemplo, `1.5`, `2.10`). Los valores `subnet` y `device` deben ser direcciones Buspro válidas en su red.

4. **Numeración de canales** - Los canales se numeran comenzando en 1. Deje el nombre de un canal vacío en la interfaz de usuario para desactivarlo, lo que evita la creación de entidades para canales no utilizados.

5. **Nombres de dispositivos** - Use nombres descriptivos basados en la ubicación (por ejemplo, "Luces de la sala de estar" en lugar de "Relés"). Esto hace que las automatizaciones y escenas sean más fáciles de entender.

6. **IDs de objeto** - En YAML, `object_id` es opcional pero recomendado. Controla el slug de ID de entidad. Si se omite, Home Assistant genera uno a partir del nombre del canal.

7. **IDs únicos** - Para casos avanzados donde necesite controlar manualmente las entradas del registro de entidades, use `unique_id` en la configuración YAML. Esto permite que Home Assistant rastrear la entidad de manera confiable incluso si el nombre del dispositivo cambia.

Para más información sobre formatos de configuración YAML, consulte [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md).
