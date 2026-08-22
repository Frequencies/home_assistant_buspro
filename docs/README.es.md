# HDL Buspro para Home Assistant

[English](../README.md) | **Español**

La integración administra la pasarela y los dispositivos físicos HDL Buspro
desde la interfaz de Home Assistant. La lista completa de modelos, entidades y
servicios está en la [documentación en inglés](../README.md).

> **Nota importante**: Para configuración detallada de dispositivos, ejemplos de YAML, servicios disponibles y guía de desarrollo, consulte la [documentación en inglés](../README.md). Esta página proporciona información básica de instalación y configuración inicial.

## Instalación

### HACS (recomendado)

1. Abra **HACS > Integraciones**.
2. Abra el menú de tres puntos y seleccione **Repositorios personalizados**.
3. Añada `https://github.com/Frequencies/home_assistant_buspro` con la categoría
   **Integración**.
4. Busque **HDL Buspro**, ábralo y seleccione **Descargar**.
5. Reinicie Home Assistant cuando HACS lo solicite.

Las versiones futuras se podrán instalar desde **HACS > Integraciones**.
Reinicie Home Assistant después de cada actualización de la integración.

### Instalación manual

1. Descargue el repositorio de la integración.
2. Copie su directorio `custom_components/buspro` en
   `/config/custom_components/buspro` de Home Assistant.
3. Reinicie Home Assistant.

## Primera configuración

### Configuración de la pasarela
1. Abra **Ajustes > Dispositivos y servicios > Añadir integración** y
   seleccione **HDL Buspro**.
2. Introduzca el host de la pasarela y los puertos UDP. El puerto normal es `6000`.
3. Introduzca una dirección Buspro libre para Home Assistant en formato
   `subred.dispositivo`. El valor predeterminado es `200.200`; no debe
   pertenecer a otro dispositivo Buspro.

### Añadir dispositivos
Después de completar la configuración de la pasarela:

1. Abra **Ajustes > Dispositivos y servicios > HDL Buspro > Configurar**.
2. Seleccione **Añadir dispositivo** para añadir un módulo Buspro físico.
3. **Seleccione el tipo de dispositivo**: elija la capacidad (Relé, Regulador,
   Ventilador, Cortina, Multisensor, etc.).
4. **Seleccione el modelo exacto**: elija el modelo que coincida con su hardware.
   Esto determina la cantidad de canales.
   - Para modelos desconocidos, elija el perfil **Genérico** e indique la cantidad de canales.
5. **Introduzca la dirección Buspro**: la dirección física subred.dispositivo del
   módulo (p. ej., `1.5`).
6. **Introduzca el nombre del dispositivo**: un nombre para mostrar (p. ej.,
   "Luces de la sala").
7. **Nombre cada canal**: asigne un nombre a cada canal o capacidad que desee usar.
   - Ejemplo: para un relé de 4 canales, nombre los canales como "Luz del techo",
     "Lámpara de mesa", etc.
   - **Deje un nombre vacío para desactivar ese canal** — no se creará una entidad.
8. Seleccione **Guardar** para crear el dispositivo y sus entidades.

Home Assistant agrupa automáticamente todas las entidades de un módulo físico bajo
una entrada del Registro de dispositivos y recarga la entrada de configuración.

### Editar dispositivos

Para cambiar un dispositivo existente, abra **Configurar > Editar dispositivo**. Puede:
- Renombrar el dispositivo
- Renombrar, activar o desactivar canales individuales
- Cambiar el modelo (puede cambiar la cantidad de canales)
- Eliminar el dispositivo completamente

Los dispositivos administrados desde la interfaz soportan edición completa. Los
dispositivos YAML heredados pueden exponer controles de nomenclatura del registro,
pero su configuración de protocolo debe modificarse en YAML. Reinicie Home
Assistant después de cambios en YAML.

### Ejemplo: Añadir un módulo relé de 4 canales

1. Modelo: `HDL-MR0410.431` (4 canales relé)
2. Dirección Buspro: `1.10`
3. Nombre del dispositivo: "Relés de la sala"
4. Nombres de canales:
   - Canal 1: "Luz del techo"
   - Canal 2: "Lámpara de pared"
   - Canal 3: "" (desactivado)
   - Canal 4: "Ventilador"

Después de guardar, Home Assistant crea:
- `light.room_relays_ceiling_light`
- `light.room_relays_wall_lamp`
- `switch.room_relays_fan`

## Cambios incompatibles en 2.2.0

- Las direcciones, los nombres, la cantidad de dispositivos y las asignaciones
  de canales ya no están integrados en el componente. Se guardan en las
  opciones de la entrada de configuración.
- El modelo exacto determina la cantidad física de canales y las entidades que
  se crean.
- Un canal sin nombre queda deshabilitado y no se crea.
- La dirección Buspro de Home Assistant se migra a `200.200` de forma
  predeterminada. Debe estar libre en la red.
- Los eventos de panel ahora se decodifican como `channel_on`, `channel_off`,
  `channel_level`, `scene` y eventos de interruptor universal.
- El constructor `Buspro` integrado ahora requiere `client_address`.

## Actualización

1. Reinicie Home Assistant después de reemplazar el componente.
2. Abra **Ajustes > Dispositivos y servicios > HDL Buspro > Configurar**.
3. Compruebe la pasarela, los puertos UDP y una dirección Buspro libre para
   Home Assistant.
4. Seleccione el modelo exacto de cada dispositivo y revise los nombres de los
   canales.
5. Revise las automatizaciones que usan eventos de panel.
6. Elimine o comente las entidades YAML antiguas solo después de comprobar sus
   reemplazos administrados desde la interfaz.

No configure el mismo canal físico en YAML y en la interfaz al mismo tiempo:
se crearán entidades y suscripciones de protocolo duplicadas.

## Configuración YAML (heredada)

La configuración de dispositivos YAML es completamente compatible junto con la
gestión de la pasarela por entrada de configuración. Puede definir luces,
cortinas, interruptores, ventiladores, clima, sensores y sensores binarios a través
de YAML mientras la pasarela se gestiona desde la interfaz de la integración.

**Nota**: Los nuevos dispositivos deben usar la interfaz de usuario **Configurar >
Añadir dispositivo** en lugar de YAML, ya que proporciona agrupación de dispositivos,
capacidades controladas por modelo y gestión del estado de canales. YAML se
recomienda para:
- Dispositivos con perfiles no estándar o heredados
- Migración desde integraciones Buspro antiguas
- Automatizaciones complejas o plantillas de sensores

### Ejemplo de sintaxis YAML

Añada a su `configuration.yaml`:

```yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Luz del techo"
        dimmable: true
      "1.5.2":
        name: "Lámpara de pared"
        dimmable: false

cover:
  - platform: buspro
    devices:
      "2.10.1":
        name: "Cortina de la sala"
        running_time: 45

climate:
  - platform: buspro
    devices:
      "3.1":
        name: "Clima del dormitorio"
        profile: "ac"
```

### Configuración de plataforma

Cada plataforma (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`,
`switch`) acepta:

| Clave | Tipo | Descripción |
| --- | --- | --- |
| `devices` | dict | Requerido. Asignación de direcciones Buspro a configuraciones de dispositivos. |
| `running_time` | int | Tiempo de transición predeterminado en segundos (0 = sin transición). Se anula por dispositivo. |
| `ack_retry_enabled` | bool | Reintentar envíos sin ACK (predeterminado de plataforma; se anula por dispositivo). |

Cada clave de dispositivo es la **dirección Buspro** en formato:
- **Luz, cortina, ventilador, interruptor**: `subred.dispositivo.canal` (p. ej., `1.5.2`)
- **Clima, sensor, sensor binario**: `subred.dispositivo` (p. ej., `3.1`)

Cada configuración de dispositivo soporta:
- `name` (requerido): Nombre para mostrar
- `running_time`, `dimmable`, `ack_retry_enabled` (específico de plataforma, opcional)
- `profile` (opcional, para sensores de clima — p. ej., `"ac"`, `"floor_heating"`)
- `object_id` (opcional): Slug de ID de entidad
- `unique_id` (opcional): Para control manual del registro de entidades

## Desarrollo

### Ejecutar los juegos de pruebas

Desde el directorio de configuración de Home Assistant:

```bash
# Ejecutar todas las pruebas de protocolo (19 pruebas)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v

# Ejecutar todas las pruebas de integración (18 pruebas)
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v

# O ejecutar archivos de prueba individuales
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

Las pruebas de protocolo cubren análisis de telegramas, coordinación de dispositivos
y seguridad de tareas/callbacks principales. Las pruebas de integración cubren
catálogo de dispositivos, lógica de dispositivos administrados, normalización YAML
y seguimiento de soporte de modelos.
