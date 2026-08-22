# HDL Buspro

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## Idiomas

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


## Primera configuración

### Configuración de la puerta de enlace
1. Abra **Settings > Devices & services > Add integration** y seleccione
   **HDL Buspro**.
2. Ingrese el host de la puerta de enlace y los puertos UDP. El puerto `6000` es el predeterminado normal.
3. Ingrese una dirección Buspro de Home Assistant no utilizada en formato `subnet.device`.
   El predeterminado es `200.200`; no debe pertenecer a otro dispositivo Buspro.

### Agregar dispositivos
Después de completar la configuración de la puerta de enlace:

1. Abra **Settings > Devices & services > HDL Buspro > Configure**.
2. Haga clic en **Add device** para agregar un módulo físico Buspro.
3. **Seleccione el tipo de dispositivo** (Relay, Dimmer, Cover, Climate, Sensor, etc.).
4. **Seleccione el modelo exacto** que coincida con su hardware.
5. **Ingrese la dirección Buspro** en formato `subnet.device` (p. ej., `1.5`).
6. **Ingrese el nombre del dispositivo** (p. ej., "Luces de la sala").
7. **Nombre cada canal** — déjelo vacío para desactivar un canal.
8. Haga clic en **Save**.

Home Assistant agrupa automáticamente las entidades por módulo físico en el Registro de dispositivos.

**Para obtener ejemplos de configuración de UI y YAML de todos los tipos de dispositivos, consulte [DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md).**

### Editar dispositivos

Para cambiar un dispositivo existente, abra **Configure > Edit device**. Puede:
- Cambiar el nombre del dispositivo
- Cambiar el nombre, habilitar o deshabilitar canales individuales
- Cambiar el modelo (lo que puede cambiar el número de canales)
- Eliminar el dispositivo completamente

Los dispositivos gestionados por UI admiten edición completa. Los dispositivos YAML heredados pueden exponer controles de nomenclatura del registro, pero su configuración de protocolo aún debe cambiarse en YAML. Reinicie Home Assistant después de cambiar YAML.

### Ejemplo rápido: Agregar un módulo de relé de 4 canales

1. Modelo: `HDL-MR0410.431` (4 canales de relé)
2. Dirección Buspro: `1.10`
3. Nombre del dispositivo: "Relés de la habitación"
4. Nombres de canales: "Luz de techo", "Lámpara de pared", "", "Ventilador"
5. Haga clic en **Save**

Home Assistant crea automáticamente las entidades: `light.room_relays_ceiling_light`, `light.room_relays_wall_lamp`, `switch.room_relays_fan`

Para obtener ejemplos completos de UI y YAML para todos los tipos de dispositivos, consulte **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)**.

## Opciones de configuración

La integración buspro admite tanto **configuración basada en UI** como **configuración YAML**:

### Configuración de UI
La forma más fácil de agregar dispositivos — consulte **[DEVICE_EXAMPLES.md](docs/en/DEVICE_EXAMPLES.md)** para obtener ejemplos paso a paso de todos los tipos de dispositivos.

### Configuración YAML  
La integración admite dos enfoques YAML complementarios:
- **Entity-Centric** (Heredado) — archivos de entidad individuales organizados por dominio
- **Device-Centric** (Moderno) — definiciones completas de dispositivos con todos los canales

**Para obtener documentación completa de YAML, ejemplos y mejores prácticas, consulte [DUAL_MODE_YAML.md](docs/en/DUAL_MODE_YAML.md)** (también disponible en [Беларуская](docs/be/DUAL_MODE_YAML.md) | [Deutsch](docs/de/DUAL_MODE_YAML.md) | [Español](docs/es/DUAL_MODE_YAML.md) | [Français](docs/fr/DUAL_MODE_YAML.md) | [Italiano](docs/it/DUAL_MODE_YAML.md) | [Nederlands](docs/nl/DUAL_MODE_YAML.md) | [Norsk](docs/no/DUAL_MODE_YAML.md) | [Русский](docs/ru/DUAL_MODE_YAML.md) | [Українська](docs/uk/DUAL_MODE_YAML.md))

## Cambios importantes en 2.2.0

Lea esta sección antes de actualizar desde 2.1.x.

> [!WARNING]
> Esta versión cambia la propiedad del dispositivo, la creación de canales,
> la semántica de eventos del panel y el constructor Python incrustado. Complete la lista de verificación de actualización antes de eliminar YAML heredado.

1. **Los dispositivos específicos de la instalación ya no están integrados en la integración.**
   Las direcciones de dispositivos, nombres, asignaciones de canales y recuentos de dispositivos ahora pertenecen
   a las opciones de entrada de configuración o al Registro de dispositivos de Home Assistant. El catálogo de dispositivos
   contiene solo capacidades de hardware.

2. **Los módulos de relé gestionados por UI utilizan su recuento de canales físicos.**
   `HDL-MR1210.433` siempre expone 12 espacios de canal y
   `HDL-MR1610.433` siempre expone 16. Un dispositivo existente no puede reducirse
   por debajo del recuento de canales físicos de su modelo.

3. **Un nombre de canal vacío desactiva el canal.**
   Los canales desactivados no se instancian, no crean objetos de protocolo y
   están marcados como desactivados por la integración en el Registro de entidades. Ingresar un
   nombre habilita el canal nuevamente.

4. **El modelo exacto controla las entidades generadas.**
   Un `panel HDL` genérico no tiene un recuento de botones conocido. Seleccione el modelo físico
   para crear eventos de botón. Cambiar un modelo recarga la entrada de configuración.

5. **Home Assistant tiene su propia dirección Buspro.**
   Las entradas de configuración existentes se migran a `200.200`. Esta dirección debe estar sin usar en
   la red Buspro y se puede cambiar en **Configure > Gateway settings**.

6. **La IP de origen del paquete ya no está codificada.**
   La integración la deriva de la ruta a la puerta de enlace configurada. Un
   host de Home Assistant multi-interfaz debe enrutar la puerta de enlace a través de la
   interfaz LAN prevista.

7. **Los eventos de acción del panel ahora están decodificados.**
   Las automatizaciones que consumen valores de acción sin procesar antiguos deben verificarse. Los eventos utilizan
   `channel_on`, `channel_off`, `channel_level`, `scene`,
   `universal_switch_on` o `universal_switch_off`, con atributos de destino y resumen
   donde se puedan resolver.

8. **La API de Python incrustada cambió.**
   Los usuarios directos de `pybuspro.Buspro` deben proporcionar `client_address`; consulte
   [pybuspro/README.md](pybuspro/README.md).

La integración aún lee entidades YAML heredadas durante la migración. No mantenga
el mismo canal físico en configuración tanto YAML como gestionada por UI, porque
eso puede crear entidades duplicadas y suscripciones de protocolo duplicadas.

## Lista de verificación de actualización

1. Reinicie Home Assistant después de reemplazar el componente personalizado.
2. Abra **Settings > Devices & services > HDL Buspro > Configure**.
3. Verifique el host de la puerta de enlace, los puertos y la dirección Buspro de Home Assistant sin usar.
4. Abra cada dispositivo físico y seleccione su modelo exacto.
5. Verifique cada nombre de canal de relé. Los canales vacíos intencionalmente permanecen desactivados.
6. Verifique las automatizaciones que consumen eventos de acción del panel.
7. Elimine o comente las entidades YAML migradas solo después de que sus
   reemplazos gestionados por UI hayan retenido los ID de entidad esperados.

## Configuración de la puerta de enlace

Agregue **HDL Buspro** de **Settings > Devices & services** y configure:

- **Host**: nombre de host de la puerta de enlace IP de HDL o dirección IPv4.
- **Puerto**: puerto UDP primario, normalmente `6000`.
- **Puertos de envío/recepción UDP**: solo cambie estos para una puerta de enlace no estándar.
- **Dirección Buspro de Home Assistant**: una identidad `subnet.device` sin usar, tal como
  el predeterminado de migración `200.200`.

UDP no tiene un apretón de manos de conexión. La configuración valida la resolución de direcciones, el enrutamiento,
y la creación del socket de recepción local sin asumir que existe un dispositivo
en una dirección Buspro codificada.

## Gestión de dispositivos

Abra **Configure** en la integración y elija:

- **Gateway settings** para actualizar la configuración de red e identidad del cliente.
- **Add device** para seleccionar un tipo de dispositivo, modelo, dirección Buspro y canal o
  nombres de capacidad.
- **Edit device** para cambiar el nombre de los canales, habilitar o deshabilitar canales, eliminar un
  dispositivo gestionado por UI o corregir el modelo de un dispositivo de registro existente.

Las direcciones físicas se muestran en Home Assistant como el número de serie del dispositivo.
Las entidades pertenecientes a un módulo físico están adjuntas al mismo
entrada del Registro de dispositivos.

## Modelos compatibles

| Modelo | Soporte de Home Assistant |
| --- | --- |
| `HDL-MBUS01IP.431` | Metadatos del dispositivo de puerta de enlace |
| `HDL-MCLog.431` | Conectividad, consulta de firmware, último visto, eventos de lógica |
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
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | 4/8/12 canales de relé de corriente alta |
| `HDL-MD0206.432` | 2 canales de atenuador |
| `HDL-MD0403.432` | 4 canales de atenuador |
| `HDL-MD0602.432` | 6 canales de atenuador |
| `HDL-MDT0203.433` | 2 canales de atenuador de borde trasero |
| `HDL-MDT0203.532` | 2 canales de atenuador de borde trasero |
| `HDL-MDT04015.433` | 4 canales de atenuador de borde trasero |
| `HDL-MDT04015.532` | 4 canales de atenuador de borde trasero |
| `HDL-MDT06015.433` | 6 canales de atenuador de borde trasero |
| `HDL-MDT06015.533` | 6 canales de atenuador de borde trasero |
| `HDL-MDLED0605.432` | 6 canales de atenuador y diagnósticos |
| `HDL-MRDA0610.432` | 6 canales de atenuador de control de balasto |
| `HDL-MRDA0610.433` | 6 canales de atenuador de control de balasto |
| `SB-DN-DALI64` | Hasta 64 canales DALI |
| `HDL-MS04.432` | 4 canales de contacto seco |
| `HDL-MS24.232` | 24 canales de contacto seco |
| `HDL-MSP02.4C` | Temperatura, iluminancia, movimiento |
| `HDL-MSP07M.4C` | Temperatura, iluminancia, humedad, movimiento, dos contactos |
| `HDL-MS08M.4C` | Temperatura, iluminancia, movimiento |
| `HDL-MS12M.4C` | Temperatura, iluminancia, humedad, movimiento, dos contactos |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Temperatura y acciones del panel |
| `HDL-MPTL4.460` | Temperatura y acciones del panel |
| `HDL-MP4S/TILE.48` | Temperatura, cuatro eventos de botón, acciones del panel |
| `HDL-MP2B/TILE.48` | Temperatura, dos eventos de botón, acciones del panel |
| `HDL-MP4B-A/TILE.48` | Temperatura, cuatro eventos de botón, acciones del panel |
| `HDL-MP4B/TILE.48` | Temperatura, cuatro eventos de botón, acciones del panel |
| `HDL-MP2B.480` | Temperatura, dos eventos de botón, acciones del panel |
| `HDL-MP4B.480` | Temperatura, cuatro eventos de botón, acciones del panel |
| `HDL-MPL8.431` | Temperatura, ocho eventos de botón, acciones del panel |
| `HDL-M/PT4.1` | Temperatura, cuatro eventos de botón, acciones del panel |
| `HDL-MFH04.432` | 4 canales de calefacción de piso |
| `HDL-MFH06.432` | 6 canales de calefacción de piso |
| `HDL-M/HVAC8.1` | Entidades de clima AC |
| `HDL-MPED4.431` | Entidades de clima AC |
| `HDL-MW02.431` | 2 canales de cortina / cobertura |
| `HDL-MWM45.431` | Entidades de cortina / cobertura (canales configurables) |

AC genérico, cortina, ventilador de velocidad variable, ventilador de encendido/apagado, conmutador universal y
perfiles de panel también están disponibles. Su dirección física y cualquier recuento de salida configurable
son proporcionados por el usuario; no son inventario de instalación.

Algunos modelos se agregan a través de asignación de familia o compatibilidad de protocolo genérico.
Durante el inicio de la integración, Buspro registra notas explícitas de compatibilidad de modelos para esos
modelos (por ejemplo, comportamiento validado por modelo frente a asignado por familia) junto con
direcciones físicas detectadas.

Para dispositivos YAML heredados, la integración ahora normaliza perfiles faltantes utilizando
metadatos del modelo de catálogo. Los modelos desconocidos y las cadenas de perfil no admitidas se
informan como advertencias de inicio, luego se devuelven al comportamiento genérico `sensor_status`
para mantener la configuración funcional.

## Asistente de mantenimiento del catálogo

Para comparar el catálogo de integración con la lista oficial de modelos HDL mantenida,
ejecute:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

El asistente lee `custom_components/buspro/devices/official_models.json` e
imprime:

- modelos oficiales faltantes en `DEVICE_CATALOG`
- modelos de catálogo no presentes en la lista oficial
- modelos genéricos virtuales solo para integración

Utilice el modo estricto para comprobaciones de estilo CI (salida distinta de cero cuando faltan modelos oficiales
en el catálogo):

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Comportamiento de la entidad

### Relés

Un coordinador compartido consulta el estado del relé una vez por módulo físico y
distribuye la respuesta a todas las entidades de canal habilitadas. Los canales desactivados no
se suscriben ni consultan el bus.

### Paneles

Los paneles de botones conocidos crean una entidad `event` por botón físico, un
evento `Action` y un sensor `Last action`. Las entidades de evento de botón de UI representan telegrama Buspro
de botón físico recibido; no simulan una pulsación de hardware.

### Atenuadores

Los atenuadores compatibles pueden exponer conectividad, brillo máximo por canal,
tipo de carga y brillo mínimo reportado por protocolo. `Not reported` significa que el
dispositivo devolvió la centinela de protocolo en lugar de un valor utilizable.

### Controlador de lógica

`HDL-MCLog.431` expone conectividad de solo lectura, versión de firmware, último visto,
y entidades de eventos de lógica. Algún firmware no responde a la consulta estándar de firmware;
en ese caso, la entidad de firmware permanece no disponible. Los bloques de lógica no
se pueden escribir porque cambiarlos puede sobrescribir la programación del controlador.

## Servicios

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` envía un comando de protocolo sin procesar y solo debe usarse con
un código de operación HDL verificado y carga útil.

## Configuración YAML (heredada)

La configuración de dispositivos YAML es totalmente compatible con la administración de entrada de configuración de la puerta de enlace. Puede definir luces, coberturas, conmutadores, ventiladores, clima, sensores y sensores binarios a través de YAML mientras la puerta de enlace es administrada por la interfaz de usuario de la integración.

**Nota**: Los nuevos dispositivos deben usar la interfaz de usuario **Configure > Add device** de la integración en lugar de YAML, ya que proporciona agrupación de dispositivos, capacidades impulsadas por modelos y administración del estado del canal. YAML se recomienda para:
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

### Configuración de la plataforma

Cada plataforma (`light`, `cover`, `fan`, `climate`, `sensor`, `binary_sensor`, `switch`) acepta:

| Clave | Tipo | Descripción |
| --- | --- | --- |
| `devices` | dict | Requerido. Asignación de direcciones Buspro a configuraciones de dispositivos. |
| `running_time` | int | Tiempo de transición predeterminado en segundos (0 = sin transición). Se anula por dispositivo. |
| `ack_retry_enabled` | bool | Reintenta envíos sin ACK (predeterminado de plataforma; anulaciones por dispositivo). |

Cada clave de dispositivo es la **dirección Buspro** en formato:
- **Light, cover, fan, switch**: `subnet.device.channel` (p. ej., `1.5.2`)
- **Climate, sensor, binary_sensor**: `subnet.device` (p. ej., `3.1`)

Cada configuración de dispositivo admite:
- `name` (requerido): Nombre para mostrar
- `running_time`, `dimmable`, `ack_retry_enabled` (específico de plataforma, opcional)
- `profile` (opcional, para sensores de clima — p. ej., `"ac"`, `"floor_heating"`)
- `object_id` (opcional): Slug de ID de entidad
- `unique_id` (opcional): Para control manual del registro de entidades

## Desarrollo

### Ejecutar los conjuntos de pruebas

Desde la raíz de configuración de Home Assistant:

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

Las pruebas de protocolo cubren análisis de telegrama, coordinación de dispositivos y seguridad de tareas/devoluciones de llamadas principales. Las pruebas de integración cubren catálogo de dispositivos, lógica de dispositivos administrados, normalización de YAML y seguimiento de compatibilidad de modelos.
