# HDL Buspro

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## Языки

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

# Интеграция HDL Buspro позволяет вам управлять системой HDL Buspro из Home Assistant.

## Установка

### Установка в один клик (HACS)

[![Откройте свой экземпляр Home Assistant и откройте репозиторий в Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Frequencies&repository=home_assistant_buspro&category=integration)

### Установка вручную

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
    + **unique_id** _(строка) (необязательно)_: Стабильный уникальный идентификатор сущности для реестра сущностей Home Assistant.

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
    + **unique_id** _(строка) (необязательно)_: Стабильный уникальный идентификатор сущности для реестра сущностей Home Assistant.

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
  + **unique_id** _(строка) (необязательно)_: Стабильный уникальный идентификатор сущности для реестра сущностей Home Assistant.
  + **device_class** _(строка) (Необязательно)_: класс устройства HASS, например, «температура».
  + **scan_interval** _(int) (Необязательно)_: Интервал опроса в секундах. Если не указан или `0`, обновления выполняются только по сообщениям Buspro.
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
  + **unique_id** _(строка) (необязательно)_: Стабильный уникальный идентификатор сущности для реестра сущностей Home Assistant.
  + **type** _(строка) (Обязательно)_: тип датчика для мониторинга.
    + Доступные датчики:
      + движение
      + Dry_contact_1
      + Dry_contact_2
      + Universal_switch
      + один_канал
      + dry_contact
    + Примечания по формату адреса:
      + `motion`, `dry_contact_1`, `dry_contact_2`: `<subnet ID>.<device ID>`
      + `universal_switch`, `single_channel`, `dry_contact`: `<subnet ID>.<device ID>.<number>`
  + **device_class** _(строка) (Необязательно)_: класс устройства HASS, например, «движение».
  + **scan_interval** _(int) (Необязательно)_: Интервал опроса в секундах. Если не указан или `0`, обновления выполняются только по сообщениям Buspro.
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
        unique_id: "hdl_climate_floorheat_zone_1"
        min_temp: 22
        max_temp: 32
        precision: 1
        name: Floor Heating Zone 1
```
+ **устройства** _(обязательно)_: список устройств для настройки.
  + **адрес** _(строка) (обязательно)_: адрес сенсорного устройства в формате `<идентификатор подсети>.<идентификатор устройства>`
  + **имя** _(строка) (обязательно)_: имя устройства.
  + **type** _(строка) (Необязательно)_: `ac` или `floor_heating`. По умолчанию используется «floor_heating».
  + **floor_heating_device_type** _(строка) (Необязательно)_: `dlp` или `module`.
Если этот параметр опущен, модуль выбирается автоматически, если указан канал, в противном случае — dlp.
  + **relay_address** _(string) (Необязательно)_: Адрес канала реле в формате `<subnet ID>.<device ID>.<channel>`. Используется как внешняя обратная связь по состоянию реле для действия HVAC.
  + **object_id** _(строка) (необязательно)_: object_id устройства. Значение по умолчанию генерируется автоматически на основе имени устройства.
  + **unique_id** _(строка) (необязательно)_: Стабильный уникальный идентификатор сущности для реестра сущностей Home Assistant.
  + **preset_modes** _(список) (необязательно)_: список поддерживаемых предустановленных режимов. Выбор предустановленного режима отключен, если он не установлен. Возможные значения показаны в таблице ниже. Соответствующие режимы должны быть включены в HDL (Подогрев пола > Рабочие настройки > Режим).
  + **channel** _(int) (Необязательно)_: канал модуля подогрева пола (`1..6`) для `floor_heating_device_type: mod`.
  + **min_temp** _(float) (Необязательно)_: Минимальная целевая температура, отображаемая в интерфейсе Home Assistant.
  + **max_temp** _(float) (Необязательно)_: Максимальная целевая температура, отображаемая в интерфейсе Home Assistant.
  + **precision** _(float) (Необязательно)_: Шаг изменения целевой температуры в интерфейсе Home Assistant. Допустимые значения: `1`, `0.5`, `0.1`.
    
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
  + **unique_id** _(строка) (необязательно)_: Стабильный уникальный идентификатор сущности для реестра сущностей Home Assistant.

Поддерживаемые функции:
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

---
## Примечания По Миграции

Если вы обновляетесь с более старой версии этой интеграции, проверьте следующее:

- **Ломающие изменения climate v1.7.1 -> v2.0.0**
  - Модель climate была разделена:
    - `type: ac` теперь создает поведение climate для AC.
    - `type: floor_heating` теперь создает поведение теплого пола.
    - Если `type` не указан, по умолчанию используется `floor_heating`.
  - Новая типизация теплого пола:
    - Добавлен `floor_heating_device_type: dlp | module`.
    - Если задан `channel`, а `floor_heating_device_type` не указан, тип автоматически становится `module`.
    - Для `floor_heating_device_type: module` обязателен `channel` (`1..6`), иначе сущность не создается.
  - Изменилось поведение HVAC-режимов:
    - AC-сущности используют `COOL/OFF`.
    - Сущности теплого пола используют `HEAT/OFF` (`COOL` дополнительно доступен для `module`).
  - Что нужно сделать:
    - Явно укажите `type` для каждой climate-сущности.
    - Добавьте `floor_heating_device_type` и `channel` для модулей теплого пола.
    - Проверьте автоматизации/скрипты, которые опираются на старую семантику climate-режимов.

---

#### Платформа Вентилятора

Чтобы использовать вентилятор Buspro, добавьте в `configuration.yaml`:

```yaml
fan:
  - platform: buspro
    running_time: 3
    ack_retry_enabled: true
    devices:
      1.89.3:
        name: Вентилятор Спальни
        dimmable: true
      1.89.4:
        name: Вентилятор Ванной
        dimmable: false
```
+ **running_time** _(int) (Необязательно)_: Время выполнения по умолчанию в секундах.
+ **ack_retry_enabled** _(boolean) (Необязательно)_: Однократный повтор без ACK через 0,8с.
+ **devices** _(Обязательно)_: Список устройств в формате `<subnet>.<device>.<channel>`.


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
