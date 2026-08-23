# HDL Buspro para Home Assistant

[🇧🇾 Беларуская](../be/README.md) | [🇩🇪 Deutsch](../de/README.md) | [🇬🇧 English](../../README.md) | 🇪🇸 Español | [🇫🇷 Français](../fr/README.md) | [🇮🇹 Italiano](../it/README.md) | [🇳🇱 Nederlands](../nl/README.md) | [🇳🇴 Norsk](../no/README.md) | [🇷🇺 Русский](../ru/README.md) | [🇺🇦 Українська](../uk/README.md)

La integración administra la pasarela y los dispositivos físicos HDL Buspro
desde la interfaz de Home Assistant. La lista completa de modelos, entidades y
servicios está en la [documentación en inglés](../README.md).

> **Nota importante**: Para configuración detallada de dispositivos, ejemplos de YAML, servicios disponibles y guía de desarrollo, consulte la [documentación en inglés](../README.md). Esta página proporciona información básica de instalación y configuración inicial.

## Confirmación de Comando (¡NUEVO!)

La integración ahora admite confirmación opcional de comandos para garantizar que los cambios de estado del dispositivo se reflejen en Home Assistant solo después de que el dispositivo físico confirme la recepción y ejecución.

### ¿Qué es?

- **Sin confirmación:** Los comandos se envían y la interfaz se actualiza inmediatamente (~5ms), pero si el dispositivo no recibe el comando debido a interferencia de red, el estado de la interfaz será incorrecto.
- **Con confirmación:** El sistema espera la confirmación del dispositivo (100-500ms), asegurando una sincronización perfecta entre Home Assistant y el dispositivo físico.

### ¿Cuándo usarlo?

Habilite la confirmación para:
- **Dispositivos críticos** — Relés de emergencia, interruptores principales
- **Redes no confiables** — Alta interferencia, pérdida de paquetes
- **Dependencias de automatización** — Cuando las automatizaciones dependen del estado exacto
- **Sistemas críticos para la seguridad** — HVAC, calefacción radiante, cargas importantes

### Configuración

Agregue confirmación a cualquier dispositivo en YAML:

```yaml
light:
  - platform: buspro
    devices:
      "1.10.1":
        name: "Luz Crítica"
        enable_confirmation: true
        confirmation_timeout: 5.0        # segundos
        confirmation_retries: 3          # intentos de reintento
```

**Parámetros:**
- `enable_confirmation` (boolean, predeterminado: `false`) — Habilitar/deshabilitar confirmación
- `confirmation_timeout` (float, predeterminado: `5.0`) — Tiempo agotado en segundos (0.1-60)
- `confirmation_retries` (integer, predeterminado: `3`) — Conteo de reintentos (0-10)

**Configuraciones recomendadas por tipo de dispositivo:**
- Relé/Interruptor/Luz: `timeout: 5.0`, `retries: 3`
- Cubierta/Cortina: `timeout: 10.0`, `retries: 2` (mecánico, más lento)
- Clima: `timeout: 5.0`, `retries: 3`
- Ventilador: `timeout: 5.0`, `retries: 3`

Para ejemplos completos y mejores prácticas, consulte **[DEVICE_EXAMPLES.md](docs/es/DEVICE_EXAMPLES.md)**.

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
2. Seleccione **Añadir dispositivo** y elija el tipo (Relé, Regulador, Ventilador, Cortina, etc.).
3. Seleccione el modelo (o **Genérico** para modelos desconocidos con cantidad de canales).
4. Introduzca la dirección Buspro, el nombre del dispositivo y los nombres de los canales (nombres vacíos desactivan canales).
5. Seleccione **Guardar**.

Home Assistant agrupa automáticamente todas las entidades bajo una entrada del Registro.

**Para ejemplos detallados de configuración UI y YAML para todos los tipos de dispositivos, ver [../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md).**

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

Para ejemplos completos de interfaz de usuario y YAML para todos los tipos de dispositivos, consulte **[../en/DEVICE_EXAMPLES.md](../en/DEVICE_EXAMPLES.md)**.

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

## Configuración de la pasarela

Agregue **HDL Buspro** desde **Configuración > Dispositivos y servicios** y configure:

- **Host**: nombre de host o dirección IPv4 de la pasarela HDL.
- **Puerto**: puerto UDP principal, generalmente `6000`.
- **Puertos de envío/recepción UDP**: solo cámbielos para una pasarela no estándar.
- **Dirección Buspro de Home Assistant**: una identidad `subnet.device` no utilizada, como la migración predeterminada `200.200`.

UDP no tiene un protocolo de enlace de conexión. La configuración valida la resolución de direcciones, el enrutamiento y la creación del socket de recepción local sin asumir que existe un dispositivo en una dirección Buspro codificada de forma permanente.

## Gestión de dispositivos

Abra **Configurar** en la integración y elija:

- **Configuración de pasarela** para actualizar la configuración de red e identidad de cliente.
- **Agregar dispositivo** para seleccionar un tipo de dispositivo, modelo, dirección Buspro y nombres de canales o capacidades.
- **Editar dispositivo** para renombrar canales, habilitar o deshabilitar canales, eliminar un dispositivo administrado por la interfaz de usuario o corregir el modelo de una entrada de registro existente.

Las direcciones físicas se muestran en Home Assistant como el número de serie del dispositivo. Las entidades que pertenecen a un módulo físico están conectadas a una única entrada del Registro de dispositivos.

## Modelos admitidos

| Modelo | Compatibilidad con Home Assistant |
| --- | --- |
| `HDL-MBUS01IP.431` | Metadatos del dispositivo de pasarela |
| `HDL-MCLog.431` | Conectividad, consulta de firmware, última sesión, eventos de lógica |
| `HDL-MR0410.431` | 4 canales de relé |
| `HDL-MR0810.432` | 8 canales de relé |
| `HDL-MR1210.433` | 12 canales de relé |
| `HDL-MR1610.433` | 16 canales de relé |
| `HDL-MR0416.431` | 4 canales de relé de alta potencia |
| `HDL-MR0416C.431` | 4 canales de relé de alta potencia |
| `HDL-MR0416D.431` | 4 canales de relé de alta potencia |
| `HDL-MR0816.432` | 8 canales de relé de alta potencia |
| `HDL-MR0816C.232` | 8 canales de relé de alta potencia |
| `HDL-MR0816D.432` | 8 canales de relé de alta potencia |
| `HDL-MR1216.433` | 12 canales de relé de alta potencia |
| `HDL-MR1616.434` | 16 canales de relé de alta potencia |
| `HDL-MR1216D.433` | 12 canales de relé de alta potencia |
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | 4/8/12 canales de relé de alta corriente |
| `HDL-MD0206.432` | 2 canales atenuadores |
| `HDL-MD0403.432` | 4 canales atenuadores |
| `HDL-MD0602.432` | 6 canales atenuadores |
| `HDL-MDT0203.433` | 2 canales atenuadores de borde trasero |
| `HDL-MDT0203.532` | 2 canales atenuadores de borde trasero |
| `HDL-MDT04015.433` | 4 canales atenuadores de borde trasero |
| `HDL-MDT04015.532` | 4 canales atenuadores de borde trasero |
| `HDL-MDT06015.433` | 6 canales atenuadores de borde trasero |
| `HDL-MDT06015.533` | 6 canales atenuadores de borde trasero |
| `HDL-MDLED0605.432` | 6 canales atenuadores y diagnóstico |
| `HDL-MRDA0610.432` | 6 canales atenuadores de control de balastro |
| `HDL-MRDA0610.433` | 6 canales atenuadores de control de balastro |
| `SB-DN-DALI64` | Hasta 64 canales DALI |
| `HDL-MS04.432` | 4 canales de contacto seco |
| `HDL-MS24.232` | 24 canales de contacto seco |
| `HDL-MSP02.4C` | Temperatura, iluminancia, movimiento |
| `HDL-MSP07M.4C` | Temperatura, iluminancia, humedad, movimiento, dos contactos |
| `HDL-MS08M.4C` | Temperatura, iluminancia, movimiento |
| `HDL-MS12M.4C` | Temperatura, iluminancia, humedad, movimiento, dos contactos |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Temperatura y acciones de panel |
| `HDL-MPTL4.460` | Temperatura y acciones de panel |
| `HDL-MP4S/TILE.48` | Temperatura, cuatro eventos de botón, acciones de panel |
| `HDL-MP2B/TILE.48` | Temperatura, dos eventos de botón, acciones de panel |
| `HDL-MP4B-A/TILE.48` | Temperatura, cuatro eventos de botón, acciones de panel |
| `HDL-MP4B/TILE.48` | Temperatura, cuatro eventos de botón, acciones de panel |
| `HDL-MP2B.480` | Temperatura, dos eventos de botón, acciones de panel |
| `HDL-MP4B.480` | Temperatura, cuatro eventos de botón, acciones de panel |
| `HDL-MPL8.431` | Temperatura, ocho eventos de botón, acciones de panel |
| `HDL-M/PT4.1` | Temperatura, cuatro eventos de botón, acciones de panel |
| `HDL-MFH04.432` | 4 canales de calefacción por suelo radiante |
| `HDL-MFH06.432` | 6 canales de calefacción por suelo radiante |
| `HDL-M/HVAC8.1` | Entidades climáticas de CA |
| `HDL-MPED4.431` | Entidades climáticas de CA |
| `HDL-MW02.431` | 2 canales de cortina / cubierta |
| `HDL-MWM45.431` | Entidades de cortina / cubierta (canales configurables) |

También están disponibles perfiles genéricos de CA, cortina, ventilador de velocidad variable, ventilador de encendido/apagado, interruptor universal y panel. Su dirección física y cualquier recuento de salida configurable son proporcionados por el usuario; no son inventario de instalación.

Algunos modelos se agregan mediante asignación de familia o compatibilidad de protocolo genérica. Durante el inicio de la integración, Buspro registra notas de soporte de modelo explícito para estos modelos (por ejemplo, comportamiento validado por el modelo en comparación con el comportamiento asignado por la familia) junto con direcciones físicas detectadas.

Para dispositivos YAML heredados, la integración ahora normaliza perfiles faltantes utilizando metadatos del catálogo de modelos. Los modelos desconocidos y las cadenas de perfil no admitidas se informan como advertencias de inicio y luego vuelven al comportamiento genérico `sensor_status` para mantener la funcionalidad de la configuración.

## Asistente de mantenimiento del catálogo

Para comparar el catálogo de integración con la lista de modelos HDL oficial mantenida, ejecute:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

El asistente lee `custom_components/buspro/devices/official_models.json` e imprime:

- modelos oficiales faltantes en `DEVICE_CATALOG`
- modelos de catálogo no presentes en la lista oficial
- modelos genéricos virtuales solo para integración

Utilice el modo estricto para verificaciones de estilo CI (salida distinta de cero cuando faltan modelos oficiales en el catálogo):

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Comportamiento de la entidad

### Relés

Un coordinador compartido consulta el estado del relé una vez por módulo físico y distribuye la respuesta a todas las entidades de canal habilitadas. Los canales deshabilitados no se suscriben ni consultan el bus.

### Paneles

Los paneles de botones conocidos crean una entidad `event` por botón físico, un evento `Action` y un sensor `Last action`. Las entidades de eventos de botón de la interfaz de usuario representan telegramas de botón Buspro físicos recibidos; no simulan una pulsación de hardware.

### Atenuadores

Los atenuadores soportados pueden exponer conectividad, brillo máximo por canal, tipo de carga y brillo mínimo informado por protocolo. `Not reported` significa que el dispositivo devolvió la centinela del protocolo en lugar de un valor utilizable.

### Controlador de lógica

`HDL-MCLog.431` expone conectividad de solo lectura, versión de firmware, última sesión y entidades de eventos de lógica. Algunos firmware no responden a la consulta de firmware estándar; en ese caso, la entidad de firmware permanece no disponible. Los bloques lógicos no son escribibles porque cambiarlos puede sobrescribir la programación del controlador.

## Servicios

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` envía un comando de protocolo sin procesar y solo debe usarse con un código de operación HDL y una carga útil verificados.

## Configuración YAML (heredado)

La configuración de dispositivos YAML es totalmente compatible junto con la gestión de puertas de enlace de entrada de configuración. Puede definir luces, cubiertas, interruptores, ventiladores, clima, sensores y sensores binarios a través de YAML mientras la puerta de enlace se gestiona mediante la interfaz de usuario de integración.

**Nota**: Los nuevos dispositivos deben utilizar la interfaz de usuario de integración **Configurar > Agregar dispositivo** en lugar de YAML, ya que proporciona agrupación de dispositivos, capacidades controladas por modelo y gestión del estado del canal. Se recomienda YAML para:
- Dispositivos con perfiles no estándar o heredados
- Migración desde integraciones Buspro más antiguas
- Automatización compleja o plantillas de sensores

### Ejemplo de sintaxis YAML

Agregue a su `configuration.yaml`:

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

### Configuración de plataforma

Cada plataforma (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`, `switch`) acepta:

| Clave | Tipo | Descripción |
| --- | --- | --- |
| `devices` | dict | Requerido. Mapeo de direcciones Buspro a configuraciones de dispositivos. |
| `running_time` | int | Tiempo de transición predeterminado en segundos (0 = sin transición). Anulado por dispositivo. |
| `ack_retry_enabled` | bool | Reintentar envíos sin ACK (valor predeterminado de plataforma; anulaciones por dispositivo). |

Cada clave de dispositivo es la **dirección Buspro** en formato:
- **Luz, cubierta, ventilador, interruptor**: `subnet.device.channel` (p. ej. `1.5.2`)
- **Clima, sensor, sensor binario**: `subnet.device` (p. ej. `3.1`)

Cada configuración de dispositivo admite:
- `name` (requerido): Nombre para mostrar
- `running_time`, `dimmable`, `ack_retry_enabled` (específico de la plataforma, opcional)
- `profile` (opcional, para sensores climáticos — p. ej. `"ac"`, `"floor_heating"`)
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
