# HDL Buspro
## Языки

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

Интеграция HDL Buspro позволяет вам управлять системой HDL Buspro из Home Assistant.

## Установка
В разделе HACS -> Интеграции добавьте пользовательский репозиторий "https://github.com/Frequencies/home_assistant_buspro" с категорией "Интеграция". Выберите интеграцию с именем "HDL Buspro" и загрузите ее.

Перезапустите Домашний помощник.

Перейдите в «Настройки» > «Интеграции» и добавьте интеграцию «HDL Buspro». Введите IP-адрес и номер порта шлюза.

## Конфигурация

#### Легкая платформа
   
Чтобы использовать индикатор Buspro в вашей установке, добавьте следующее в файл Configuration.yaml:

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
+ **running_time** _(int) (необязательно)_: время работы по умолчанию в секундах для всех устройств. Время работы составляет 0 секунд, если не установлено.
+ **ack_retry_enabled** _(boolean) (необязательно)_: Включает однократную повторную отправку команды, если ACK не получен в течение 0,8 с. По умолчанию: `True`.
+ **устройства** _(обязательно)_: список устройств для настройки.
  + **X.X.X** _(Обязательно)_: адрес устройства в формате `<идентификатор подсети>.<идентификатор устройства>.<номер канала>`
    + **имя** _(строка) (обязательно)_: имя устройства.
    + **running_time** _(int) (необязательно)_: время работы устройства в секундах. Если этот параметр опущен, используется время работы по умолчанию для всех устройств.
    + **ack_retry_enabled** _(boolean) (необязательно)_: Переопределение повтора ACK для конкретного устройства.
    + **диммируемая** _(логическое значение) (необязательно)_: регулируется ли яркость устройства? По умолчанию — Истина.
    + **object_id** _(строка) (необязательно)_: object_id устройства. Значение по умолчанию генерируется автоматически на основе имени устройства.

#### Переключить платформу

Чтобы использовать коммутатор Buspro в вашей установке, добавьте следующее в файл Configuration.yaml:

```yaml
switch:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Switch
      1.89.2:
        name: Front Door Switch
```
+ **устройства** _(обязательно)_: список устройств для настройки.
  + **X.X.X** _(Обязательно)_: адрес устройства в формате `<идентификатор подсети>.<идентификатор устройства>.<номер канала>`
    + **имя** _(строка) (обязательно)_: имя устройства.
    + **object_id** _(строка) (необязательно)_: object_id устройства. Значение по умолчанию генерируется автоматически на основе имени устройства.

#### Сенсорная платформа

Чтобы использовать датчик Buspro в вашей установке, добавьте следующее в файл Configuration.yaml:

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
+ **устройства** _(обязательно)_: список устройств для настройки.
  + **адрес** _(строка) (обязательно)_: адрес сенсорного устройства в формате `<идентификатор подсети>.<идентификатор устройства>`
  + **имя** _(строка) (обязательно)_: имя устройства.
  + **type** _(строка) (Обязательно)_: тип датчика для мониторинга.
    + Доступные датчики:
     + температура
     + освещенность
     + влажность
  + **единица_измерения** _(строка) (Необязательно)_: текст, который будет отображаться в качестве единицы измерения.
  + **object_id** _(строка) (необязательно)_: object_id устройства. Значение по умолчанию генерируется автоматически на основе имени устройства.
  + **device_class** _(строка) (Необязательно)_: класс устройства HASS, например, «температура».
(https://www.home-assistant.io/components/sensor/)
  + **устройство** _(строка) (Необязательно)_: Тип сенсорного устройства:
    + DLP

#### Бинарная сенсорная платформа

Чтобы использовать двоичный датчик Buspro в вашей установке, добавьте следующее в файл Configuration.yaml:

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
+ **устройства** _(обязательно)_: список устройств для настройки.
  + **адрес** _(строка) (обязательно)_: адрес сенсорного устройства в формате `<идентификатор подсети>.<идентификатор устройства>`. Если
'type' = 'universal_switch' К адресу должен быть добавлен номер универсального коммутатора.
  + **имя** _(строка) (обязательно)_: имя устройства.
  + **object_id** _(строка) (необязательно)_: object_id устройства. Значение по умолчанию генерируется автоматически на основе имени устройства.
  + **type** _(строка) (Обязательно)_: тип датчика для мониторинга.
    + Доступные датчики:
      + движение
      + Dry_contact_1
      + Dry_contact_2
      + Universal_switch
      + один_канал
  + **device_class** _(строка) (Необязательно)_: класс устройства HASS, например, «движение».
(https://www.home-assistant.io/components/binary_sensor/)

#### Климатическая платформа

Чтобы использовать панель климат-контроля Buspro в вашей установке, добавьте следующее в файл Configuration.yaml:

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
+ **устройства** _(обязательно)_: список устройств для настройки.
  + **адрес** _(строка) (обязательно)_: адрес сенсорного устройства в формате `<идентификатор подсети>.<идентификатор устройства>`
  + **имя** _(строка) (обязательно)_: имя устройства.
  + **type** _(строка) (Необязательно)_: `ac` или `floor_heating`. По умолчанию используется «floor_heating».
  + **floor_heating_device_type** _(строка) (Необязательно)_: `dlp` или `module`.
Если этот параметр опущен, модуль выбирается автоматически, если указан канал, в противном случае — dlp.
  + **object_id** _(строка) (необязательно)_: object_id устройства. Значение по умолчанию генерируется автоматически на основе имени устройства.
  + **preset_modes** _(список) (необязательно)_: список поддерживаемых предустановленных режимов. Выбор предустановленного режима отключен, если он не установлен. Возможные значения показаны в таблице ниже. Соответствующие режимы должны быть включены в HDL (Подогрев пола > Рабочие настройки > Режим).
  + **channel** _(int) (Необязательно)_: канал модуля подогрева пола (`1..6`) для `floor_heating_device_type: mod`.
    
| HA preset mode | HDL mode |
|:--------------:|:--------:|
|      none      |  Normal  |
|      away      |   Away   |
|      home      |   Day    |
|     sleep      |  Night   |


#### Платформа штор (Cover)

Чтобы использовать шторы Buspro в вашей установке, добавьте следующее в файл `configuration.yaml`:

```yaml
cover:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Curtain
        invert: false
        object_id: living_room_curtain
```
+ **devices** _(обязательно)_: сопоставление каналов штор Buspro
  + **ключ** _(string)_: `<ID подсети>.<ID устройства>.<канал>`
  + **name** _(string) (обязательно)_: отображаемое имя
  + **invert** _(bool) (необязательно)_: инвертировать направление открытия/закрытия. По умолчанию `false`.
  + **object_id** _(string) (необязательно)_: `object_id` сущности. По умолчанию генерируется из имени.

Поддерживаемые функции:
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

---
## Услуги

#### Отправка произвольного сообщения:
```
Domain: buspro
Service: send_message
Service Data: {"address": [1,74], "operate_code": [4,78], "payload": [1,100,0,3]}
```
#### Активация сцены:
```
Domain: buspro
Service: activate_scene
Service Data: {"address": [1,74], "scene_address": [3,5]}
```
#### Настройка универсального переключателя:
```
Domain: buspro
Service: set_universal_switch
Service Data: {"address": [1,74], "switch_number": 100, "status": 1}
```
