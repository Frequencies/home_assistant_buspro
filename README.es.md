# HDL Buspro
## Idiomas

[![English](https://flagcdn.com/24x18/gb.png) English](README.md) |
[![Deutsch](https://flagcdn.com/24x18/de.png) Deutsch](README.de.md) |
[![Français](https://flagcdn.com/24x18/fr.png) Français](README.fr.md) |
[![Nederlands](https://flagcdn.com/24x18/nl.png) Nederlands](README.nl.md) |
[![Español](https://flagcdn.com/24x18/es.png) Español](README.es.md) |
[![Italiano](https://flagcdn.com/24x18/it.png) Italiano](README.it.md) |
[![Русский](https://flagcdn.com/24x18/ru.png) Русский](README.ru.md) |
[![Українська](https://flagcdn.com/24x18/ua.png) Українська](README.uk.md) |
[![Беларуская](https://flagcdn.com/24x18/by.png) Беларуская](README.be.md)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

La integración de HDL Buspro le permite controlar su sistema HDL Buspro desde Home Assistant.

## Instalación
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
```
+ **running_time** _(int) (Opcional)_: tiempo de ejecución predeterminado en segundos para todos los dispositivos. El tiempo de ejecución es de 0 segundos si no se configura.
+ **dispositivos** _(Obligatorio)_: una lista de dispositivos para configurar
  + **X.X.X** _(Obligatorio)_: La dirección del dispositivo en el formato `<ID de subred>.<ID de dispositivo>.<número de canal>`
    + **nombre** _(cadena) (Obligatorio)_: El nombre del dispositivo
    + **running_time** _(int) (Opcional)_: El tiempo de ejecución en segundos para el dispositivo. Si se omite, se utiliza el tiempo de ejecución predeterminado para todos los dispositivos.
    + **regulable** _(booleano) (Opcional)_: ¿El dispositivo es regulable? El valor predeterminado es Verdadero.
    + **object_id** _(cadena) (Opcional)_: dispositivo object_id. El valor predeterminado se genera automáticamente a partir del nombre del dispositivo.

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
  + **device_class** _(cadena) (Opcional)_: clase de dispositivo HASS, por ejemplo, "temperatura"
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
  + **tipo** _(cadena) (Obligatorio)_: Tipo de sensor a monitorear.
    + Sensores disponibles:
      + movimiento
      + contacto_seco_1
      + contacto_seco_2
      + interruptor_universal
      + canal único
  + **device_class** _(cadena) (Opcional)_: clase de dispositivo HASS, por ejemplo, "movimiento"
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
        name: Floor Heating Zone 1
```
+ **dispositivos** _(Obligatorio)_: una lista de dispositivos para configurar
  + **dirección** _(cadena) (Obligatorio)_: La dirección del dispositivo sensor en el formato `<ID de subred>.<ID de dispositivo>`
  + **nombre** _(cadena) (Obligatorio)_: El nombre del dispositivo
  + **tipo** _(cadena) (Opcional)_: `ac` o `floor_heating`. El valor predeterminado es `floor_heating`.
  + **tipo_de_dispositivo_de_calefacción_de_piso** _(cadena) (Opcional)_: `dlp` o `módulo`.
Si se omite, "módulo" se selecciona automáticamente cuando se proporciona "canal", en caso contrario, "dlp".
  + **object_id** _(cadena) (Opcional)_: dispositivo object_id. El valor predeterminado se genera automáticamente a partir del nombre del dispositivo.
  + **preset_modes** _(lista) (Opcional)_: Lista de modos preestablecidos admitidos. La selección del modo preestablecido está deshabilitada si no está configurada. Los valores posibles se muestran en la siguiente tabla. Los modos correspondientes deben estar habilitados en HDL (Calefacción por suelo radiante > Configuración de trabajo > Modo).
  + **canal** _(int) (Opcional)_: Canal del módulo de calefacción por suelo radiante (`1..6`) para `floor_heating_device_type: module`.
    
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

Funciones compatibles:
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

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
