# Прыклады канфігурацыі прыладаў HDL Buspro

[English](../en/DEVICE_EXAMPLES.md) | [Русский](../ru/DEVICE_EXAMPLES.md) | [Українська](../uk/DEVICE_EXAMPLES.md) | [Беларуская](../be/DEVICE_EXAMPLES.md) | [Deutsch](../de/DEVICE_EXAMPLES.md) | [Français](../fr/DEVICE_EXAMPLES.md) | [Español](../es/DEVICE_EXAMPLES.md) | [Italiano](../it/DEVICE_EXAMPLES.md) | [Nederlands](../nl/DEVICE_EXAMPLES.md) | [Norsk](../no/DEVICE_EXAMPLES.md)

Гэты кіраўнік змяшчае практычныя прыклады канфігурацыі інтэрфейса і YAML для ўсіх падтрымліваемых тыпаў прыладаў у інтэграцыі HDL Buspro.

**Змест:**
- [Рэле прыладаў](#рэле-прыладаў)
- [Дыммерныя прыладаў](#дыммерныя-прыладаў)
- [Прыладаў кіравання жалюзі](#прыладаў-кіравання-жалюзі)
- [Вентылятары](#вентылятары)
- [Кліматычныя прыладаў](#кліматычныя-прыладаў)
- [Датчыкі](#датчыкі)
- [Двойковыя датчыкі](#двойковыя-датчыкі)

---

## Рэле прыладаў

Рэле прыладаў - гэта простыя вімыкачы вкл./откл., якія выкарыстоўваюцца для асвятлення, вентылятораў і іншых двойковых нагрузак.

**Падтрымліваемыя мадэлі:**
- `HDL-MR0410.431` - 4 канала рэле
- `HDL-MR0810.432` - 8 каналаў рэле
- `HDL-MR1210.433` - 12 каналаў рэле
- `HDL-MR1610.433` - 16 каналаў рэле
- Варыянты магутных рэле HDL (MR0416, MR0816, MR1216, MR1616, MR0420C і т.д.)

### Прыклад канфігурацыі праз інтэрфейс

**Кроки:**
1. Перайдзіце ў **Параметры > Прыладаў і сервісы > HDL Buspro > Наладзіць**
2. Нажміце **Дадаць прыладу**
3. Выберыце тып прылады: **Рэле**
4. Выберыце дакладную мадэль: **HDL-MR0410.431** (4 канала)
5. Введзіце адрас Buspro: `1.10`
6. Введзіце назву прылады: "Асвятлення вітальні"
7. Назовіце канала:
   - Канал 1: "Потолковы светильнік"
   - Канал 2: "Настольная лампа"
   - Канал 3: "Настенны светильнік"
   - Канал 4: "" (пакіньце пусцім, каб выключыць)
8. Нажміце **Сахаваць**

**Вынік:**
- `light.living_room_lights_ceiling_light`
- `light.living_room_lights_table_lamp`
- `light.living_room_lights_wall_sconce`

### Прыклад канфігурацыі YAML

**Арыентаваны на сутнасці (асобныя файлы):**

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.10.1":
        name: "Living Room Ceiling Light"
        object_id: "ceiling_light"
      "1.10.2":
        name: "Living Room Table Lamp"
        object_id: "table_lamp"
      "1.10.3":
        name: "Living Room Wall Sconce"
        object_id: "wall_sconce"
```

**Арыентаваны на прыладу (поўнае вызначэнне прылады):**

```yaml
# configuration.yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 200.200
  devices:
    - address: "1.10"
      name: "Living Room Relays"
      model: "HDL-MR0410.431"
      device_type: "relay"
      channels:
        - number: 1
          name: "Ceiling Light"
          enabled: true
          object_id: "hdl_light_ceiling"
        - number: 2
          name: "Table Lamp"
          enabled: true
          object_id: "hdl_light_table"
        - number: 3
          name: "Wall Sconce"
          enabled: true
          object_id: "hdl_light_sconce"
        - number: 4
          enabled: false
```

---

## Дыммерныя прыладаў

Дыммерныя прыладаў кіруюць узроўнем яркасці (0-255) для дыммеруемых светільнікаў.

**Падтрымліваемыя мадэлі:**
- `HDL-MD0206.432` - 2 канала дыммера
- `HDL-MD0403.432` - 4 канала дыммера
- `HDL-MD0602.432` - 6 каналаў дыммера
- Дыммеры HDL з задняй фронтам (MDT0203, MDT04015, MDT06015 і т.д.)
- `HDL-MDLED0605.432` - 6 каналаў дыммера з дыагностыкай

### Прыклад канфігурацыі праз інтэрфейс

**Кроки:**
1. Перайдзіце ў **Параметры > Прыладаў і сервісы > HDL Buspro > Наладзіць**
2. Нажміце **Дадаць прыладу**
3. Выберыце тып прылады: **Дыммер**
4. Выберыце дакладную мадэль: **HDL-MD0602.432** (6 каналаў)
5. Введзіце адрас Buspro: `1.5`
6. Введзіце назву прылады: "Спальня дыммеры"
7. Назовіце канала:
   - Канал 1: "Асноўнае асвятлення"
   - Канал 2: "Прыкроватны левы"
   - Канал 3: "Прыкроватны правы"
   - Канала 4-6: пакіньце пусцімі
8. Нажміце **Сахаваць**

**Вынік:**
- `light.bedroom_dimmers_main_light` (дыммеруемы 0-255)
- `light.bedroom_dimmers_bedside_left` (дыммеруемы 0-255)
- `light.bedroom_dimmers_bedside_right` (дыммеруемы 0-255)

### Прыклад канфігурацыі YAML

**Арыентаваны на сутнасці:**

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Bedroom Main Light"
        dimmable: true
      "1.5.2":
        name: "Bedroom Bedside Left"
        dimmable: true
      "1.5.3":
        name: "Bedroom Bedside Right"
        dimmable: true
```

**Арыентаваны на прыладу:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "1.5"
      name: "Bedroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
          object_id: "hdl_dimmer_main"
        - number: 2
          name: "Bedside Left"
          enabled: true
          object_id: "hdl_dimmer_left"
        - number: 3
          name: "Bedside Right"
          enabled: true
          object_id: "hdl_dimmer_right"
        - number: 4
          enabled: false
        - number: 5
          enabled: false
        - number: 6
          enabled: false
```

---

## Прыладаў кіравання жалюзі

Прыладаў кіравання жалюзі кіруюць механізаванымі жалюзі, ставнямі і шторамі.

**Падтрымліваемыя мадэлі:**
- `HDL-MW02.431` - 2 канала штор/жалюзі
- `HDL-MWM45.431` - Сутнасці штор/жалюзі (наладжвальныя канала)

### Прыклад канфігурацыі праз інтэрфейс

**Кроки:**
1. Перайдзіце ў **Параметры > Прыладаў і сервісы > HDL Buspro > Наладзіць**
2. Нажміце **Дадаць прыладу**
3. Выберыце тып прылады: **Жалюзі**
4. Выберыце дакладную мадэль: **HDL-MW02.431** (2 канала)
5. Введзіце адрас Buspro: `2.10`
6. Введзіце назву прылады: "Жалюзі вітальні"
7. Назовіце канала:
   - Канал 1: "Акны"
   - Канал 2: "Дзверы патыё"
8. Нажміце **Сахаваць**

**Вынік:**
- `cover.living_room_blinds_windows`
- `cover.living_room_blinds_patio_door`

### Прыклад канфігурацыі YAML

**Арыентаваны на прыладу:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "2.10"
      name: "Living Room Blinds"
      model: "HDL-MW02.431"
      device_type: "cover"
      channels:
        - number: 1
          name: "Windows"
          enabled: true
          object_id: "hdl_cover_windows"
        - number: 2
          name: "Patio Door"
          enabled: true
          object_id: "hdl_cover_patio"
```

---

## Вентылятары

Вентылятары кіруюць вентылятарамі з зменнай хуткасцю.

**Падтрымліваемыя мадэлі:**
- Універсальны профіль вентылятара (вентылятары з зменнай хуткасцю)

### Прыклад канфігурацыі праз інтэрфейс

**Кроки:**
1. Перайдзіце ў **Параметры > Прыладаў і сервісы > HDL Buspro > Наладзіць**
2. Нажміце **Дадаць прыладу**
3. Выберыце тып прылады: **Вентылятар**
4. Выберыце дакладную мадэль: **Універсальны** (укажыце кількасць каналаў)
5. Введзіце адрас Buspro: `3.5`
6. Введзіце назву прылады: "Вытягоны вентылятар у ванній"
7. Назовіце канал: "Асноўны вентылятар"
8. Нажміце **Сахаваць**

**Вынік:**
- `fan.bathroom_exhaust_fan_main_fan` (кіраванне хуткасцю 0-255)

### Прыклад канфігурацыі YAML

**Арыентаваны на прыладу:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "3.5"
      name: "Bathroom Exhaust Fan"
      device_type: "fan"
      channels:
        - number: 1
          name: "Main Fan"
          enabled: true
          object_id: "hdl_fan_exhaust"
```

---

## Кліматычныя прыладаў

Кліматычныя прыладаў кіруюць тэмпературай і сістэмамі HVAC.

**Падтрымліваемыя мадэлі:**
- `HDL-MFH04.432` - 4 канала цёплай падлогі
- `HDL-MFH06.432` - 6 каналаў цёплай падлогі
- `HDL-M/HVAC8.1` - Кіраванне кліматам AC
- `HDL-MPED4.431` - Кіраванне кліматам AC
- Універсальны профіль AC
- Універсальны профіль цёплай падлогі

### Прыклад канфігурацыі праз інтэрфейс - AC

**Кроки:**
1. Перайдзіце ў **Параметры > Прыладаў і сервісы > HDL Buspro > Наладзіць**
2. Нажміце **Дадаць прыладу**
3. Выберыце тып прылады: **Клімат**
4. Выберыце дакладную мадэль: **HDL-M/HVAC8.1** (AC)
5. Введзіце адрас Buspro: `3.1`
6. Введзіце назву прылады: "AC вітальні"
7. Нажміце **Сахаваць**

**Вынік:**
- `climate.living_room_ac` (мэтавая тэмпература, режым, кіраванне жыванням)

### Прыклад канфігурацыі YAML

**Арыентаваны на прыладу:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "3.1"
      name: "Living Room AC"
      model: "HDL-M/HVAC8.1"
      device_type: "ac"
      object_id: "hdl_climate_ac"

    - address: "4.2"
      name: "Master Bedroom Floor Heating"
      model: "HDL-MFH06.432"
      device_type: "floor_heating"
      channels:
        - number: 1
          name: "Zone 1"
          enabled: true
        - number: 2
          name: "Zone 2"
          enabled: true
        - number: 3
          enabled: false
```

---

## Датчыкі

Датчыкі прадаставляюць дадзеныя тэмпературы, вільгаці, асвятлення і руху.

**Падтрымліваемыя мадэлі:**
- `HDL-MSP02.4C` - Тэмпература, асвятлення, рух
- `HDL-MSP07M.4C` - Тэмпература, асвятлення, вільгаць, рух, 2 кантакты
- `HDL-MS08M.4C` - Тэмпература, асвятлення, рух
- `HDL-MS12M.4C` - Тэмпература, асвятлення, вільгаць, рух, 2 кантакты
- `HDL-MCLog.431` - Логічны контролер (толькі чытанне)
- Датчыкі тэмпературы панэлі (MPTL, MP2B, MP4B, MPL8 і т.д.)

### Прыклад канфігурацыі праз інтэрфейс

**Кроки:**
1. Перайдзіце ў **Параметры > Прыладаў і сервісы > HDL Buspro > Наладзіць**
2. Нажміце **Дадаць прыладу**
3. Выберыце тып прылады: **Мультыдатчык**
4. Выберыце дакладную мадэль: **HDL-MSP07M.4C**
5. Введзіце адрас Buspro: `2.5`
6. Введзіце назву прылады: "Датчык вітальні"
7. Нажміце **Сахаваць**

**Вынік:**
- `sensor.living_room_sensor_temperature`
- `sensor.living_room_sensor_illuminance`
- `sensor.living_room_sensor_humidity`
- `binary_sensor.living_room_sensor_motion`
- 2 дадатковыя сухія кантакты

### Прыклад канфігурацыі YAML

**Арыентаваны на сутнасці:**

```yaml
# configuration.yaml
sensor:
  - platform: buspro
    devices:
      "2.5":
        name: "Living Room Sensor"
        model: "HDL-MSP07M.4C"
        profile: "12in1"
        entities:
          - type: temperature
            name: "Temperature"
            object_id: "hdl_temp_living_room"
          - type: illuminance
            name: "Light Level"
            object_id: "hdl_lux_living_room"
          - type: humidity
            name: "Humidity"
            object_id: "hdl_humidity_living_room"

binary_sensor:
  - platform: buspro
    devices:
      "2.5":
        name: "Living Room Sensor"
        model: "HDL-MSP07M.4C"
        profile: "12in1"
        entities:
          - type: motion
            name: "Motion"
            object_id: "hdl_motion_living_room"
          - type: dry_contact
            number: 1
            name: "Door Contact"
            object_id: "hdl_door_living_room"
          - type: dry_contact
            number: 2
            name: "Window Contact"
            object_id: "hdl_window_living_room"
```

**Арыентаваны на прыладу:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "2.5"
      name: "Living Room Sensor"
      model: "HDL-MSP07M.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Temperature"
          object_id: "hdl_temp_living_room"
        - type: illuminance
          name: "Illuminance"
          object_id: "hdl_lux_living_room"
        - type: humidity
          name: "Humidity"
          object_id: "hdl_humidity_living_room"
        - type: motion
          name: "Motion"
          object_id: "hdl_motion_living_room"
        - type: dry_contact
          number: 1
          name: "Door Contact"
          object_id: "hdl_door_contact"
        - type: dry_contact
          number: 2
          name: "Window Contact"
          object_id: "hdl_window_contact"
```

---

## Двойковыя датчыкі

Двойковыя датчыкі прадаставляюць статус вкл./откл. ад сухіх кантактаў і датчыкаў дзвярэй/акон.

**Падтрымліваемыя мадэлі:**
- `HDL-MS04.432` - 4 канала сухіх кантактаў
- `HDL-MS24.232` - 24 канала сухіх кантактаў
- Мультыдатчыкі з інтэграванымі кантактамі (MSP07M, MS12M і т.д.)

### Прыклад канфігурацыі праз інтэрфейс

**Кроки:**
1. Перайдзіце ў **Параметры > Прыладаў і сервісы > HDL Buspro > Наладзіць**
2. Нажміце **Дадаць прыладу**
3. Выберыце тып прылады: **Суходы кантакт**
4. Выберыце дакладную мадэль: **HDL-MS04.432** (4 канала)
5. Введзіце адрас Buspro: `1.20`
6. Введзіце назву прылады: "Датчыкі дзвярэй і акон"
7. Назовіце канала:
   - Канал 1: "Входная дзвер"
   - Канал 2: "Дзвер гаража"
   - Канал 3: "Акно вітальні"
   - Канал 4: пакіньце пусцім
8. Нажміце **Сахаваць**

**Вынік:**
- `binary_sensor.door_window_sensors_front_door`
- `binary_sensor.door_window_sensors_garage_door`
- `binary_sensor.door_window_sensors_living_room_window`

### Прыклад канфігурацыі YAML

**Арыентаваны на прыладу:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "1.20"
      name: "Door & Window Sensors"
      model: "HDL-MS04.432"
      device_type: "dry_contact"
      channels:
        - number: 1
          name: "Front Door"
          enabled: true
          object_id: "hdl_door_front"
        - number: 2
          name: "Garage Door"
          enabled: true
          object_id: "hdl_door_garage"
        - number: 3
          name: "Living Room Window"
          enabled: true
          object_id: "hdl_window_living_room"
        - number: 4
          enabled: false
```

---

## Комплексны прыклад з кількасцю прыладаў

Вось поўны файл конфігурацыі, які паказвае кількасць тыпаў прыладаў, што працуюць разам:

```yaml
# configuration.yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 200.200
  devices:
    # Relay devices
    - address: "1.10"
      name: "Living Room Lights"
      model: "HDL-MR0410.431"
      device_type: "relay"
      channels:
        - number: 1
          name: "Ceiling Light"
          enabled: true
        - number: 2
          name: "Table Lamp"
          enabled: true
        - number: 3
          name: "Wall Sconce"
          enabled: true
        - number: 4
          enabled: false

    # Dimmer devices
    - address: "1.5"
      name: "Bedroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
        - number: 2
          name: "Bedside Left"
          enabled: true
        - number: 3
          name: "Bedside Right"
          enabled: true
        - number: 4
          enabled: false
        - number: 5
          enabled: false
        - number: 6
          enabled: false

    # Cover devices (blinds)
    - address: "2.10"
      name: "Blinds"
      model: "HDL-MW02.431"
      device_type: "cover"
      channels:
        - number: 1
          name: "Living Room"
          enabled: true
        - number: 2
          name: "Patio"
          enabled: true

    # Climate
    - address: "3.1"
      name: "AC Unit"
      model: "HDL-M/HVAC8.1"
      device_type: "ac"

    # Sensors
    - address: "2.5"
      name: "Living Room Sensor"
      model: "HDL-MSP07M.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Temperature"
        - type: illuminance
          name: "Illuminance"
        - type: humidity
          name: "Humidity"
        - type: motion
          name: "Motion"
        - type: dry_contact
          number: 1
          name: "Door"
        - type: dry_contact
          number: 2
          name: "Window"

    # Dry contacts
    - address: "1.20"
      name: "Door Sensors"
      model: "HDL-MS04.432"
      device_type: "dry_contact"
      channels:
        - number: 1
          name: "Front Door"
          enabled: true
        - number: 2
          name: "Garage Door"
          enabled: true
        - number: 3
          enabled: false
        - number: 4
          enabled: false
```

---

## Даводы і лепшыя практыкі

1. **Выкарыстоўвайце інтэрфейс для простых установак** - Інтэрфейс прадаставляе інтуітыўны спосаб дадання і кіравання прыладамі без неабходнасці напісання YAML.

2. **Выкарыстоўвайце YAML для комплексных або програмных конфігурацыі** - YAML лепш падыходзіць для вялікіх установак або коль трэба кіраванне версіямі.

3. **Адрасы** - Заўсёды выкарыстоўвайце формат `subnet.device` для адрасаў (напрыклад, `1.5`, `2.10`). Значэнні `subnet` і `device` мусяць быць дзейсны адрасамі Buspro у вашай сеце.

4. **Нумерацыя каналаў** - Канала нумеруюцца пачынаючы з 1. Пакіньце назву канала пусцім у інтэрфейсе, каб выключыць яго, што прадухінаць стварэнне сутнасці для невыкарыстаных каналаў.

5. **Назвы прыладаў** - Выкарыстоўвайце апісальныя імёны на аснове месцазнаходжання (напрыклад, "Асвятлення вітальні" замест "Рэле"). Гэта палегчае разуменне аўтаматызацыі і сцэн.

6. **Object IDs** - У YAML `object_id` з'яўляецца опцыянальным, але рекамендуецца. Гэта кіруе слагом ID сутнасці. Калі апушчана, Home Assistant генеруе яго з назвы канала.

7. **Унікальныя ID** - Для развітыя выпадкаў, калі патрэбна ручное кіраванне запісамі рэестра сутнасцей, выкарыстоўвайце `unique_id` у конфігурацыі YAML. Гэта дазваляе Home Assistant надзейна адсачліваць сутнасць нават пры змене назвы прылады.

Для атрымання больш дэтальнай інфармацыі аб форматах конфігурацыі YAML гл. [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md).
