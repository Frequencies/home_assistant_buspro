# HDL Buspro

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

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

# Інтэграцыя HDL Buspro дазваляе вам кіраваць сістэмай HDL Buspro з Home Assistant.

## Ўстаноўка

### Усталяванне ў адзін клік (HACS)

[![Адкрыйце свой асобнік Home Assistant і адкрыйце рэпазіторый у Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Frequencies&repository=home_assistant_buspro&category=integration)

### Ручная ўстаноўка

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
        ack_retry_enabled: True
```
+ **час_працы** _(цэлае) (неабавязкова)_: час працы па змаўчанні ў секундах для ўсіх прылад. Час працы складае 0 секунд, калі не ўстаноўлена.
+ **ack_retry_enabled** _(boolean) (неабавязкова)_: Уключае аднаразовы паўтор адпраўкі каманды, калі ACK не атрыманы за 0,8 с. Па змаўчанні: `True`.
+ **прылады** _(абавязкова)_: спіс прылад для наладжвання
  + **X.X.X** _(Абавязкова)_: Адрас прылады ў фармаце `<ID падсеткі>.<ID прылады>.<нумар канала>`
    + **імя** _(радок) (абавязкова)_: Імя прылады
    + **час_працы** _(int) (неабавязкова)_: час працы прылады ў секундах. Калі апусціць, выкарыстоўваецца час працы па змаўчанні для ўсіх прылад.
    + **ack_retry_enabled** _(boolean) (неабавязкова)_: Пераазначэнне паўтору ACK для канкрэтнай прылады.
    + **з магчымасцю зацямнення** _(лагічнае значэнне) (неабавязкова)_: Ці можна прыладу зацямняць? Па змаўчанні - True.
    + **object_id** _(радок) (неабавязкова)_: аб'ект_id прылады. Па змаўчанні аўтаматычна ствараецца з назвы прылады.
    + **unique_id** _(радок) (неабавязкова)_: Стабільны ўнікальны ідэнтыфікатар сутнасці для рэестра сутнасцей Home Assistant.

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
    + **unique_id** _(радок) (неабавязкова)_: Стабільны ўнікальны ідэнтыфікатар сутнасці для рэестра сутнасцей Home Assistant.

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
      - address: "1.75"
        name: Hall
        type: humidity
        unit_of_measurement: "%"
```
+ **прылады** _(абавязкова)_: спіс прылад для наладжвання
  + **address** _(радок) (абавязкова)_: Адрас прылады датчыка ў фармаце `<ID падсеткі>.<ID прылады>`
  + **імя** _(радок) (абавязкова)_: Імя прылады
  + **тып** _(радок) (абавязкова)_: тып датчыка для кантролю.
    + Даступныя датчыкі:
     + тэмпература
     + асветленасць
     + вільготнасць
  + **адзінка_вымярэння** _(радок) (неабавязкова)_: тэкст, які будзе адлюстроўвацца ў якасці адзінкі вымярэння
  + **object_id** _(радок) (неабавязкова)_: аб'ект_id прылады. Па змаўчанні аўтаматычна ствараецца з назвы прылады.
  + **unique_id** _(радок) (неабавязкова)_: Стабільны ўнікальны ідэнтыфікатар сутнасці для рэестра сутнасцей Home Assistant.
  + **device_class** _(радок) (неабавязкова)_: клас прылады HASS, напрыклад, "тэмпература"
  + **scan_interval** _(int) (Неабавязкова)_: Інтэрвал апытання ў секундах. Калі не пазначаны або `0`, абнаўленні выконваюцца толькі па паведамленнях Buspro.
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
  + **unique_id** _(радок) (неабавязкова)_: Стабільны ўнікальны ідэнтыфікатар сутнасці для рэестра сутнасцей Home Assistant.
  + **тып** _(радок) (абавязкова)_: тып датчыка для кантролю.
    + Даступныя датчыкі:
      + рух
      + сухі_кантакт_1
      + сухі_кантакт_2
      + універсальны_выключальнік
      + аднаканальны
      + dry_contact
    + Заўвагі па фармаце адраса:
      + `motion`, `dry_contact_1`, `dry_contact_2`: `<subnet ID>.<device ID>`
      + `universal_switch`, `single_channel`, `dry_contact`: `<subnet ID>.<device ID>.<number>`
  + **device_class** _(радок) (неабавязкова)_: клас прылады HASS, напрыклад, "рух"
  + **scan_interval** _(int) (Неабавязкова)_: Інтэрвал апытання ў секундах. Калі не пазначаны або `0`, абнаўленні выконваюцца толькі па паведамленнях Buspro.
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
        unique_id: "hdl_climate_floorheat_zone_1"
        min_temp: 22
        max_temp: 32
        precision: 1
        name: Floor Heating Zone 1
```
+ **прылады** _(абавязкова)_: спіс прылад для наладжвання
  + **address** _(радок) (абавязкова)_: Адрас прылады датчыка ў фармаце `<ID падсеткі>.<ID прылады>`
  + **імя** _(радок) (абавязкова)_: Імя прылады
  + **тып** _(радок) (неабавязкова)_: `ac` або `floor_heating`. Па змаўчанні гэта `floor_heating`.
  + **floor_heating_device_type** _(радок) (неабавязкова)_: `dlp` або `module`.
Калі прапушчана, "модуль" выбіраецца аўтаматычна, калі пазначаны "канал", інакш - "dlp".
  + **relay_address** _(string) (Неабавязкова)_: Адрас канала рэле ў фармаце `<subnet ID>.<device ID>.<channel>`. Выкарыстоўваецца як знешняя зваротная сувязь стану рэле для HVAC-дзеяння.
  + **object_id** _(радок) (неабавязкова)_: аб'ект_id прылады. Па змаўчанні аўтаматычна ствараецца з назвы прылады.
  + **unique_id** _(радок) (неабавязкова)_: Стабільны ўнікальны ідэнтыфікатар сутнасці для рэестра сутнасцей Home Assistant.
  + **preset_modes** _(спіс) (неабавязкова)_: Спіс падтрымоўваных прадусталяваных рэжымаў. Выбар прадусталяванага рэжыму адключаны, калі ён не ўсталяваны. Магчымыя значэнні паказаны ў табліцы ніжэй. Адпаведныя рэжымы павінны быць уключаны ў HDL (Ацяпленне падлогі > Працоўныя налады > Рэжым).
  + **channel** _(int) (Неабавязкова)_: Канал модуля ацяплення падлогі (`1..6`) для `floor_heating_device_type: module`.
  + **min_temp** _(float) (Неабавязкова)_: Мінімальная мэтавая тэмпература, якая паказваецца ў інтэрфейсе Home Assistant.
  + **max_temp** _(float) (Неабавязкова)_: Максімальная мэтавая тэмпература, якая паказваецца ў інтэрфейсе Home Assistant.
  + **precision** _(float) (Неабавязкова)_: Крок змены мэтавай тэмпературы ў інтэрфейсе Home Assistant. Дапушчальныя значэнні: `1`, `0.5`, `0.1`.
    
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
  + **unique_id** _(радок) (неабавязкова)_: Стабільны ўнікальны ідэнтыфікатар сутнасці для рэестра сутнасцей Home Assistant.

Падтрымліваюцца функцыі:
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

---
## Заўвагі Па Міграцыі

Калі вы абнаўляецеся са старэйшай версіі гэтай інтэграцыі, праверце наступнае:

- **Ломаючыя змены climate v1.7.1 -> v2.0.0**
  - Мадэль climate была падзелена:
    - `type: ac` цяпер стварае climate-паводзіны для AC.
    - `type: floor_heating` цяпер стварае паводзіны цёплай падлогі.
    - Калі `type` не пазначаны, значэнне па змаўчанні — `floor_heating`.
  - Новая тыпізацыя цёплай падлогі:
    - Дададзены `floor_heating_device_type: dlp | module`.
    - Калі зададзены `channel`, а `floor_heating_device_type` не пазначаны, тып аўтаматычна становіцца `module`.
    - Для `floor_heating_device_type: module` абавязковы `channel` (`1..6`), інакш сутнасць не будзе створана.
  - Зменена паводзіны HVAC-рэжымаў:
    - AC-сутнасці маюць `COOL/OFF`.
    - Сутнасці цёплай падлогі маюць `HEAT/OFF` (`COOL` дадаткова даступны для `module`).
  - Неабходныя дзеянні:
    - Яўна пазначце `type` для кожнай climate-сутнасці.
    - Дадайце `floor_heating_device_type` і `channel` для модуляў цёплай падлогі.
    - Праверце аўтаматызацыі/скрыпты, якія абапіраюцца на старую семантыку climate-рэжымаў.

---

#### Платформа Вентылятара

Каб выкарыстоўваць вентылятар Buspro, дадайце ў `configuration.yaml`:

```yaml
fan:
  - platform: buspro
    running_time: 3
    ack_retry_enabled: true
    devices:
      1.89.3:
        name: Вентылятар Спальні
        dimmable: true
      1.89.4:
        name: Вентылятар Ваннай
        dimmable: false
```
+ **running_time** _(int) (Неабавязкова)_: Стандартны час выканання ў секундах.
+ **ack_retry_enabled** _(boolean) (Неабавязкова)_: Адзіны паўтор без ACK праз 0,8с.
+ **devices** _(Абавязкова)_: Спіс прылад у фармаце `<subnet>.<device>.<channel>`.


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
