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

# La integración de HDL Buspro le permite controlar su sistema HDL Buspro desde Home Assistant.

## Instalación

### Instalación con un clic (HACS)

[![Abra su instancia de Home Assistant y abra un repositorio en Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Frequencies&repository=home_assistant_buspro&category=integration)

### Instalación manual

En HACS -> Integraciones, agrega el repositorio personalizado "https://github.com/Frequencies/home_assistant_buspro" con la categoría "Integración". Selecciona la integración llamada "HDL Buspro" y descárgala.

Reinicie el Asistente de inicio.

Vaya a Configuración > Integraciones y agregue la integración "HDL Buspro". Escriba la dirección IP y el número de puerto de la puerta de enlace.

## Configuración

#### Plataforma ligera
   
Para usar su luz Buspro en su instalación, agregue lo siguiente a su archivo Configuration.yaml:

```yaml
light:
  - platform: buspro
    running_time: 3
    devices:
      1.89.1:
        name: Living Room Light
        running_time: 5
      1.89.2:
        name: Front Door Light
        dimmable: False
        ack_retry_enabled: True
```
+ **running_time** _(int) (Opcional)_: tiempo de ejecución predeterminado en segundos para todos los dispositivos. El tiempo de ejecución es de 0 segundos si no se configura.
+ **ack_retry_enabled** _(boolean) (Opcional)_: Habilita un reintento unico del comando si no se recibe ACK en 0,8 s. Valor predeterminado: `True`.
+ **dispositivos** _(Obligatorio)_: una lista de dispositivos para configurar
  + **X.X.X** _(Obligatorio)_: La dirección del dispositivo en el formato `<ID de subred>.<ID de dispositivo>.<número de canal>`
    + **nombre** _(cadena) (Obligatorio)_: El nombre del dispositivo
    + **running_time** _(int) (Opcional)_: El tiempo de ejecución en segundos para el dispositivo. Si se omite, se utiliza el tiempo de ejecución predeterminado para todos los dispositivos.
    + **ack_retry_enabled** _(boolean) (Opcional)_: Anulacion por dispositivo para el reintento ACK.
    + **regulable** _(booleano) (Opcional)_: ¿El dispositivo es regulable? El valor predeterminado es Verdadero.
    + **object_id** _(cadena) (Opcional)_: dispositivo object_id. El valor predeterminado se genera automáticamente a partir del nombre del dispositivo.
    + **unique_id** _(cadena) (Opcional)_: Identificador único estable de la entidad para el registro de entidades de Home Assistant.

#### Cambiar de plataforma

Para usar su conmutador Buspro en su instalación, agregue lo siguiente a su archivo Configuration.yaml:

```yaml
switch:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Switch
      1.89.2:
        name: Front Door Switch
```
+ **dispositivos** _(Obligatorio)_: una lista de dispositivos para configurar
  + **X.X.X** _(Obligatorio)_: La dirección del dispositivo en el formato `<ID de subred>.<ID de dispositivo>.<número de canal>`
    + **nombre** _(cadena) (Obligatorio)_: El nombre del dispositivo
    + **object_id** _(cadena) (Opcional)_: dispositivo object_id. El valor predeterminado se genera automáticamente a partir del nombre del dispositivo.
    + **unique_id** _(cadena) (Opcional)_: Identificador único estable de la entidad para el registro de entidades de Home Assistant.

#### Plataforma de sensores

Para usar su sensor Buspro en su instalación, agregue lo siguiente a su archivo Configuration.yaml:

```yaml
sensor:
  - platform: buspro
    devices:
      - address: "1.74"
        name: Living Room
        type: temperature
        unit_of_measurement: °C
        device_class: temperature
        device: dlp
      - address: "1.74"
        name: Front Door
        type: illuminance
        unit_of_measurement: lux
      - address: "1.75"
        name: Hall
        type: humidity
        unit_of_measurement: "%"
```
+ **dispositivos** _(Obligatorio)_: una lista de dispositivos para configurar
  + **dirección** _(cadena) (Obligatorio)_: La dirección del dispositivo sensor en el formato `<ID de subred>.<ID de dispositivo>`
  + **nombre** _(cadena) (Obligatorio)_: El nombre del dispositivo
  + **tipo** _(cadena) (Obligatorio)_: Tipo de sensor a monitorear.
    + Sensores disponibles:
     + temperatura
     + iluminancia
     + humedad
  + **unidad_de_medida** _(cadena) (Opcional)_: texto que se mostrará como unidad de medida
  + **object_id** _(cadena) (Opcional)_: dispositivo object_id. El valor predeterminado se genera automáticamente a partir del nombre del dispositivo.
  + **unique_id** _(cadena) (Opcional)_: Identificador único estable de la entidad para el registro de entidades de Home Assistant.
  + **device_class** _(cadena) (Opcional)_: clase de dispositivo HASS, por ejemplo, "temperatura"
  + **scan_interval** _(int) (Opcional)_: Intervalo de sondeo en segundos. Si se omite o es `0`, las actualizaciones dependen solo de mensajes Buspro.
(https://www.home-assistant.io/components/sensor/)
  + **dispositivo** _(cadena) (Opcional)_: El tipo de dispositivo sensor:
    + dlp

#### Plataforma de sensores binarios

Para usar su sensor binario Buspro en su instalación, agregue lo siguiente a su archivo Configuration.yaml:

```yaml
binary_sensor:
  - platform: buspro
    devices:
      - address: "1.74"
        name: Living Room
        type: motion
        device_class: motion
      - address: "1.74.100"
        name: Front Door
        type: universal_switch
      - address: "1.75.3"
        name: Kitchen switch
        type: single_channel
```
+ **dispositivos** _(Obligatorio)_: una lista de dispositivos para configurar
  + **dirección** _(cadena) (Obligatorio)_: La dirección del dispositivo sensor en el formato `<ID de subred>.<ID de dispositivo>`. Si
Se debe agregar el número de interruptor universal 'type' = 'universal_switch' a la dirección.
  + **nombre** _(cadena) (Obligatorio)_: El nombre del dispositivo
  + **object_id** _(cadena) (Opcional)_: dispositivo object_id. El valor predeterminado se genera automáticamente a partir del nombre del dispositivo.
  + **unique_id** _(cadena) (Opcional)_: Identificador único estable de la entidad para el registro de entidades de Home Assistant.
  + **tipo** _(cadena) (Obligatorio)_: Tipo de sensor a monitorear.
    + Sensores disponibles:
      + movimiento
      + contacto_seco_1
      + contacto_seco_2
      + interruptor_universal
      + canal único
      + dry_contact
    + Notas sobre formato de direccion:
      + `motion`, `dry_contact_1`, `dry_contact_2`: `<subnet ID>.<device ID>`
      + `universal_switch`, `single_channel`, `dry_contact`: `<subnet ID>.<device ID>.<number>`
  + **device_class** _(cadena) (Opcional)_: clase de dispositivo HASS, por ejemplo, "movimiento"
  + **scan_interval** _(int) (Opcional)_: Intervalo de sondeo en segundos. Si se omite o es `0`, las actualizaciones dependen solo de mensajes Buspro.
(https://www.home-assistant.io/components/binary_sensor/)

#### Plataforma climática

Para utilizar el control climático del panel Buspro en su instalación, agregue lo siguiente a su archivo Configuration.yaml:

```yaml
climate:
  - platform: buspro
    devices:
      - address: "1.74"
        name: Bedroom AC
        type: ac
      - address: "1.74"
        name: Living Room
        type: floor_heating
        floor_heating_device_type: dlp
        preset_modes: 
          - none
          - away
          - home
          - sleep
      - address: "1.90"
        type: floor_heating
        floor_heating_device_type: module
        channel: 1
        unique_id: "hdl_climate_floorheat_zone_1"
        min_temp: 22
        max_temp: 32
        precision: 1
        name: Floor Heating Zone 1
```
+ **dispositivos** _(Obligatorio)_: una lista de dispositivos para configurar
  + **dirección** _(cadena) (Obligatorio)_: La dirección del dispositivo sensor en el formato `<ID de subred>.<ID de dispositivo>`
  + **nombre** _(cadena) (Obligatorio)_: El nombre del dispositivo
  + **tipo** _(cadena) (Opcional)_: `ac` o `floor_heating`. El valor predeterminado es `floor_heating`.
  + **tipo_de_dispositivo_de_calefacción_de_piso** _(cadena) (Opcional)_: `dlp` o `módulo`.
Si se omite, "módulo" se selecciona automáticamente cuando se proporciona "canal", en caso contrario, "dlp".
  + **relay_address** _(string) (Opcional)_: Direccion del canal de rele en formato `<subnet ID>.<device ID>.<channel>`. Se usa como retroalimentacion externa del estado del rele para la accion HVAC.
  + **object_id** _(cadena) (Opcional)_: dispositivo object_id. El valor predeterminado se genera automáticamente a partir del nombre del dispositivo.
  + **unique_id** _(cadena) (Opcional)_: Identificador único estable de la entidad para el registro de entidades de Home Assistant.
  + **preset_modes** _(lista) (Opcional)_: Lista de modos preestablecidos admitidos. La selección del modo preestablecido está deshabilitada si no está configurada. Los valores posibles se muestran en la siguiente tabla. Los modos correspondientes deben estar habilitados en HDL (Calefacción por suelo radiante > Configuración de trabajo > Modo).
  + **canal** _(int) (Opcional)_: Canal del módulo de calefacción por suelo radiante (`1..6`) para `floor_heating_device_type: module`.
  + **min_temp** _(float) (Opcional)_: Temperatura objetivo mínima mostrada en la interfaz de Home Assistant.
  + **max_temp** _(float) (Opcional)_: Temperatura objetivo máxima mostrada en la interfaz de Home Assistant.
  + **precision** _(float) (Opcional)_: Paso de ajuste de la temperatura objetivo en la interfaz de Home Assistant. Valores permitidos: `1`, `0.5`, `0.1`.
    
| HA preset mode | HDL mode |
|:--------------:|:--------:|
|      none      |  Normal  |
|      away      |   Away   |
|      home      |   Day    |
|     sleep      |  Night   |


#### Plataforma de persianas

Para usar tus persianas Buspro en tu instalación, añade lo siguiente a tu archivo `configuration.yaml`:

```yaml
cover:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Curtain
        invert: false
        object_id: living_room_curtain
```
+ **devices** _(Obligatorio)_: Mapa de canales de cortina Buspro
  + **clave** _(string)_: `<ID de subred>.<ID de dispositivo>.<canal>`
  + **name** _(string) (Obligatorio)_: Nombre visible
  + **invert** _(bool) (Opcional)_: Invierte la dirección abrir/cerrar. Valor predeterminado `false`.
  + **object_id** _(string) (Opcional)_: `object_id` de la entidad. Se genera automáticamente a partir del nombre.
  + **unique_id** _(cadena) (Opcional)_: Identificador único estable de la entidad para el registro de entidades de Home Assistant.

Funciones compatibles:
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

---
## Notas De Migración

Si actualizas desde una versión anterior de esta integración, revisa lo siguiente:

- **Cambios incompatibles de climate v1.7.1 -> v2.0.0**
  - El modelo de climate se dividió:
    - `type: ac` ahora crea comportamiento de climate AC.
    - `type: floor_heating` ahora crea comportamiento de suelo radiante.
    - Si se omite `type`, el valor por defecto es `floor_heating`.
  - Nuevo tipado de suelo radiante:
    - Se introdujo `floor_heating_device_type: dlp | module`.
    - Si se define `channel` y se omite `floor_heating_device_type`, el tipo cambia automáticamente a `module`.
    - Para `floor_heating_device_type: module`, `channel` (`1..6`) es obligatorio; si falta, la entidad no se crea.
  - Cambio en el comportamiento de modos HVAC:
    - Las entidades AC exponen `COOL/OFF`.
    - Las entidades de suelo radiante exponen `HEAT/OFF` (`COOL` también disponible para `module`).
  - Acción requerida:
    - Define `type` explícitamente para cada entidad climate.
    - Agrega `floor_heating_device_type` y `channel` para módulos de suelo radiante.
    - Revisa automatizaciones/scripts que asuman la semántica antigua de modos climate.

---

#### Plataforma De Ventilador

Para usar su ventilador Buspro, agregue lo siguiente en `configuration.yaml`:

```yaml
fan:
  - platform: buspro
    running_time: 3
    ack_retry_enabled: true
    devices:
      1.89.3:
        name: Ventilador Dormitorio
        dimmable: true
      1.89.4:
        name: Ventilador Bano
        dimmable: false
```
+ **running_time** _(int) (Opcional)_: Tiempo de ejecucion por defecto en segundos.
+ **ack_retry_enabled** _(boolean) (Opcional)_: Reintento unico sin ACK tras 0,8s.
+ **devices** _(Obligatorio)_: Lista de dispositivos con formato `<subnet>.<device>.<channel>`.


---
## Servicios

#### Enviar un mensaje arbitrario:
```
Domain: buspro
Service: send_message
Service Data: {"address": [1,74], "operate_code": [4,78], "payload": [1,100,0,3]}
```
#### Activar una escena:
```
Domain: buspro
Service: activate_scene
Service Data: {"address": [1,74], "scene_address": [3,5]}
```
#### Configuración de un interruptor universal:
```
Domain: buspro
Service: set_universal_switch
Service Data: {"address": [1,74], "switch_number": 100, "status": 1}
```
