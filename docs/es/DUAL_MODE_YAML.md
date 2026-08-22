# Configuración YAML Dual-Mode

**Documentation:** [English](../en/DUAL_MODE_YAML.md) | [Русский](../ru/DUAL_MODE_YAML.md) | [Беларуская](../be/DUAL_MODE_YAML.md) | [Deutsch](../de/DUAL_MODE_YAML.md) | **Español** | [Français](../fr/DUAL_MODE_YAML.md) | [Italiano](../it/DUAL_MODE_YAML.md) | [Nederlands](../nl/DUAL_MODE_YAML.md) | [Norsk](../no/DUAL_MODE_YAML.md) | [Українська](../uk/DUAL_MODE_YAML.md)

El componente personalizado buspro admite dos enfoques complementarios de configuración YAML:

1. **Centrado en entidad** (Legacy) - Definiciones de entidades individuales
2. **Centrado en dispositivo** (Modern) - Definiciones completas de dispositivo con todos los canales

Puedes usar **uno u otro enfoque o ambos simultáneamente** en tu configuración de Home Assistant.

## Formato centrado en entidad (Legacy)

Define entidades individualmente. Útil para organizar entidades por dominio (luces, interruptores, sensores).

### Características
- Una entidad por entrada YAML
- Enfoque en tipos específicos de sensores o salidas
- Agrupación automática de dispositivos por prefijo de dirección
- Adecuado para la organización de entidades individuales

### Ejemplo
```yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 1.1
  devices:
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"
        - type: illuminance
          name: "Kitchen Illuminance"
          object_id: "hdl_sensor_illuminance_kitchen_ceiling"
```

### Organización de archivos

```
entities/
├── buspro_devices/
│   └── kitchen/
│       └── multisensor_2_10.yaml    # Configuración de entidad centrada en dispositivo
```

## Formato centrado en dispositivo (Modern)

Define dispositivos completos con todos sus canales/entidades. Útil para gestionar todos los aspectos de un dispositivo en un solo lugar.

### Características
- Un dispositivo = un archivo YAML
- Todos los canales definidos juntos
- Agrupación y estructura clara del dispositivo
- Adecuado para la gestión integral de dispositivos
- Se asigna directamente al registro de dispositivos buspro

### Ejemplo
```yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 1.1
  devices:
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
          object_id: "hdl_switch_light_bathroom_main"
        - number: 2
          name: "Exhaust Fan"
          enabled: true
          object_id: "hdl_switch_fan_bathroom_exhaust"

    - address: "2.5"
      name: "Guestroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Bra Okno"
          enabled: true
          object_id: "hdl_switch_light_guestroom_bra_window"
        - number: 2
          name: "Bra Dver"
          enabled: true
          object_id: "hdl_switch_light_guestroom_bra_door"
```

### Organización de archivos

```
entities/
├── switches/
│   ├── light/
│   │   ├── guestroom/
│   │   │   ├── switch_light_guestroom_bra_window.yaml  # Centrado en dispositivo
│   │   │   └── switch_light_guestroom_bra_door.yaml
│   │   └── bathroom/
│   │       └── switch_light_bathroom_main.yaml
```

## Detalles del formato de canal centrado en dispositivo

### Campos obligatorios

```yaml
address: "2.5"                    # Dirección del dispositivo (subred.dispositivo)
name: "Device Name"               # Nombre legible del dispositivo
model: "HDL-MD0606.32"           # Modelo de dispositivo del catálogo
device_type: "relay|dimmer|..."  # Tipo de entidad
channels:                         # Lista de canales/entidades
  - number: 1                     # Número de canal (1-N) o nombre de capacidad
    name: "Channel Name"          # Nombre de pantalla del canal
    enabled: true                 # Crear entidad (predeterminado: true)
```

### Campos opcionales

```yaml
channels:
  - number: 1
    name: "Channel Name"
    enabled: true
    object_id: "hdl_switch_light_guestroom_bra_window"  # Sufijo de ID de entidad
    unique_id: "buspro-2.5-relay-1"                     # Identificador único
```

## Tipos de dispositivos soportados

**Iluminación:**
- `relay` - Interruptores simples de encendido/apagado
- `dimmer` - Luces ajustables (control de brillo 0-255)

**Sensores y entradas:**
- `dry_contact` - Sensores binarios (contactos de puertas/ventanas)
- `multisensor` - Sensores ambientales compuestos
- `universal_switch` - Entradas de interruptores universales con lógica día/noche

**Clima y HVAC:**
- `floor_heating` - Módulos de calefacción por suelo/control de temperatura
- `ac` - Controladores de aire acondicionado

**Motorizados:**
- `cover` - Motores de persianas/cierres con control de posición
- `fan` - Controladores de velocidad del ventilador

## Mezclar ambos enfoques

Puedes usar ambos formatos simultáneamente, siempre que no entren en conflicto:

```yaml
buspro:
  devices:
    # Centrado en entidad: multisensor
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"

    # Centrado en dispositivo: relé con canales
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          object_id: "hdl_switch_light_bathroom_main"
```

**Importante:** Cada dirección solo puede definirse una vez. No uses la misma dirección en ambos formatos.

## Agrupación del registro de dispositivos

Ambos formatos agrupan automáticamente las entidades bajo su dispositivo principal en el registro de dispositivos de Home Assistant:

- Los dispositivos se identifican por **dirección base** (por ejemplo, `2.5`)
- Todas las entidades con direcciones `2.5.1`, `2.5.2`, ... se agrupan bajo el dispositivo `2.5`
- Las propiedades del dispositivo (nombre, modelo, fabricante) se aplican a todas las entidades

### Ejemplo de jerarquía del registro de dispositivos

```
Dispositivo: Guestroom Relay (2.5)
├── Entidad: Bra Okno (2.5.1) [dimmer/switch]
└── Entidad: Bra Dver (2.5.2) [dimmer/switch]

Dispositivo: Bathroom Relay (2.4)
├── Entidad: Main Light (2.4.1) [relay/switch]
└── Entidad: Exhaust Fan (2.4.2) [relay/switch]
```

## Mejores prácticas

### Para centrado en entidad:
- Organiza archivos por dominio (`entities/sensors/`, `entities/lights/`)
- Una entidad por archivo
- Utiliza nombres de archivo descriptivos
- Adecuado para configuraciones orientadas a sensores

### Para centrado en dispositivo:
- Organiza archivos por habitación o grupo de dispositivos
- Todos los canales en un archivo
- Usa nombres consistentes en todos los canales
- Adecuado para la gestión organizada de dispositivos

### Para ambos:
- No dupliques direcciones entre formatos
- Usa el formato que se adapte a tu flujo de trabajo
- Considera las preferencias de tu equipo
- Documenta tu elección en CLAUDE.md o README
