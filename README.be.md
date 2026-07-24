# HDL Buspro
## Мовы

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

Інтэграцыя HDL Buspro дазваляе вам кіраваць сістэмай HDL Buspro з Home Assistant.

## Ўстаноўка
У HACS -> Інтэграцыі дадайце карыстальніцкі рэпазіторый "https://github.com/Frequencies/home_assistant_buspro" з катэгорыяй "Інтэграцыя". Абярыце інтэграцыю з назвай "HDL Buspro" і загрузіце яе.

Перазапусціце Home Assistant.

Перайдзіце ў Налады > Інтэграцыі і Дадайце інтэграцыю «HDL Buspro». Увядзіце IP-адрас і нумар порта шлюза.

## Канфігурацыя

#### Лёгкая платформа
   
Каб выкарыстоўваць святло Buspro пры ўсталёўцы, дадайце наступнае ў файл configuration.yaml:

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
+ **час_працы** _(цэлае) (неабавязкова)_: час працы па змаўчанні ў секундах для ўсіх прылад. Час працы складае 0 секунд, калі не ўстаноўлена.
+ **прылады** _(абавязкова)_: спіс прылад для наладжвання
  + **X.X.X** _(Абавязкова)_: Адрас прылады ў фармаце `<ID падсеткі>.<ID прылады>.<нумар канала>`
    + **імя** _(радок) (абавязкова)_: Імя прылады
    + **час_працы** _(int) (неабавязкова)_: час працы прылады ў секундах. Калі апусціць, выкарыстоўваецца час працы па змаўчанні для ўсіх прылад.
    + **з магчымасцю зацямнення** _(лагічнае значэнне) (неабавязкова)_: Ці можна прыладу зацямняць? Па змаўчанні - True.
    + **object_id** _(радок) (неабавязкова)_: аб'ект_id прылады. Па змаўчанні аўтаматычна ствараецца з назвы прылады.

#### Пераключыць платформу

Каб выкарыстоўваць пераключальнік Buspro пры ўсталёўцы, дадайце ў файл configuration.yaml наступнае:

```yaml
switch:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Switch
      1.89.2:
        name: Front Door Switch
```
+ **прылады** _(абавязкова)_: спіс прылад для наладжвання
  + **X.X.X** _(Абавязкова)_: Адрас прылады ў фармаце `<ID падсеткі>.<ID прылады>.<нумар канала>`
    + **імя** _(радок) (абавязкова)_: Імя прылады
    + **object_id** _(радок) (неабавязкова)_: аб'ект_id прылады. Па змаўчанні аўтаматычна ствараецца з назвы прылады.

#### Сэнсарная платформа

Каб выкарыстоўваць датчык Buspro пры ўсталёўцы, дадайце наступнае ў файл configuration.yaml:

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
```
+ **прылады** _(абавязкова)_: спіс прылад для наладжвання
  + **address** _(радок) (абавязкова)_: Адрас прылады датчыка ў фармаце `<ID падсеткі>.<ID прылады>`
  + **імя** _(радок) (абавязкова)_: Імя прылады
  + **тып** _(радок) (абавязкова)_: тып датчыка для кантролю.
    + Даступныя датчыкі:
     + тэмпература
     + асветленасць
  + **адзінка_вымярэння** _(радок) (неабавязкова)_: тэкст, які будзе адлюстроўвацца ў якасці адзінкі вымярэння
  + **object_id** _(радок) (неабавязкова)_: аб'ект_id прылады. Па змаўчанні аўтаматычна ствараецца з назвы прылады.
  + **device_class** _(радок) (неабавязкова)_: клас прылады HASS, напрыклад, "тэмпература"
(https://www.home-assistant.io/components/sensor/)
  + **прылада** _(радок) (неабавязкова)_: тып датчыка:
    + DLP

#### Двайковая сэнсарная платформа

Каб выкарыстоўваць двайковы датчык Buspro пры ўсталёўцы, дадайце наступнае ў файл configuration.yaml:

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
+ **прылады** _(абавязкова)_: спіс прылад для наладжвання
  + **address** _(радок) (абавязкова)_: Адрас прылады датчыка ў фармаце `<ID падсеткі>.<ID прылады>`. Калі
'type' = 'universal_switch' нумар універсальнага камутатара павінен быць дададзены да адраса.
  + **імя** _(радок) (абавязкова)_: Імя прылады
  + **object_id** _(радок) (неабавязкова)_: аб'ект_id прылады. Па змаўчанні аўтаматычна ствараецца з назвы прылады.
  + **тып** _(радок) (абавязкова)_: тып датчыка для кантролю.
    + Даступныя датчыкі:
      + рух
      + сухі_кантакт_1
      + сухі_кантакт_2
      + універсальны_выключальнік
      + аднаканальны
  + **device_class** _(радок) (неабавязкова)_: клас прылады HASS, напрыклад, "рух"
(https://www.home-assistant.io/components/binary_sensor/)

#### Кліматычная платформа

Каб выкарыстоўваць панэльны клімат-кантроль Buspro ў вашай ўстаноўцы, дадайце наступнае ў файл configuration.yaml:

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
+ **прылады** _(абавязкова)_: спіс прылад для наладжвання
  + **address** _(радок) (абавязкова)_: Адрас прылады датчыка ў фармаце `<ID падсеткі>.<ID прылады>`
  + **імя** _(радок) (абавязкова)_: Імя прылады
  + **тып** _(радок) (неабавязкова)_: `ac` або `floor_heating`. Па змаўчанні гэта `floor_heating`.
  + **floor_heating_device_type** _(радок) (неабавязкова)_: `dlp` або `module`.
Калі прапушчана, "модуль" выбіраецца аўтаматычна, калі пазначаны "канал", інакш - "dlp".
  + **object_id** _(радок) (неабавязкова)_: аб'ект_id прылады. Па змаўчанні аўтаматычна ствараецца з назвы прылады.
  + **preset_modes** _(спіс) (неабавязкова)_: Спіс падтрымоўваных прадусталяваных рэжымаў. Выбар прадусталяванага рэжыму адключаны, калі ён не ўсталяваны. Магчымыя значэнні паказаны ў табліцы ніжэй. Адпаведныя рэжымы павінны быць уключаны ў HDL (Ацяпленне падлогі > Працоўныя налады > Рэжым).
  + **channel** _(int) (Неабавязкова)_: Канал модуля ацяплення падлогі (`1..6`) для `floor_heating_device_type: module`.
    
| HA preset mode | HDL mode |
|:--------------:|:--------:|
|      none      |  Normal  |
|      away      |   Away   |
|      home      |   Day    |
|     sleep      |  Night   |


#### Платформа штор (Cover)

Каб выкарыстоўваць шторы Buspro у вашай устаноўцы, дадайце наступнае ў файл `configuration.yaml`:

```yaml
cover:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Curtain
        invert: false
        object_id: living_room_curtain
```
+ **devices** _(абавязкова)_: адпаведнасць каналаў штор Buspro
  + **ключ** _(string)_: `<ID падсеткі>.<ID прылады>.<канал>`
  + **name** _(string) (абавязкова)_: адлюстраваная назва
  + **invert** _(bool) (неабавязкова)_: інвертаваць напрамак адкрыцця/закрыцця. Па змаўчанні `false`.
  + **object_id** _(string) (неабавязкова)_: `object_id` сутнасці. Па змаўчанні генеруецца з назвы.

Падтрымліваюцца функцыі:
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

---
## Паслугі

#### Адпраўка адвольнага паведамлення:
```
Domain: buspro
Service: send_message
Service Data: {"address": [1,74], "operate_code": [4,78], "payload": [1,100,0,3]}
```
#### Актывацыя сцэны:
```
Domain: buspro
Service: activate_scene
Service Data: {"address": [1,74], "scene_address": [3,5]}
```
#### Настройка універсальнага выключальніка:
```
Domain: buspro
Service: set_universal_switch
Service Data: {"address": [1,74], "switch_number": 100, "status": 1}
```
