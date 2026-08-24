# Двухрэжымная канфігурацыя YAML

🇧🇾 Беларуская | [🇩🇪 Deutsch](../de/DUAL_MODE_YAML.md) | [🇬🇧 English](../en/DUAL_MODE_YAML.md) | [🇪🇸 Español](../es/DUAL_MODE_YAML.md) | [🇫🇷 Français](../fr/DUAL_MODE_YAML.md) | [🇮🇹 Italiano](../it/DUAL_MODE_YAML.md) | [🇳🇱 Nederlands](../nl/DUAL_MODE_YAML.md) | [🇳🇴 Norsk](../no/DUAL_MODE_YAML.md) | [🇷🇺 Русский](../ru/DUAL_MODE_YAML.md) | [🇺🇦 Українська](../uk/DUAL_MODE_YAML.md)

Карыстальніцкі кампанент buspro падтрымлівае два ўзаемадапаўняльныя падыходы да канфігурацыі YAML:

1. **На аснове сутнасці** (Legacy) - Вызначэнні асобных сутнасцей
2. **На аснове прыстасавання** (Modern) - Поўныя вызначэнні прыстасавання з усімі каналамі

Вы можаце выкарыстоўваць **або адзін падыход, або абодва адначасова** у канфігурацыі Home Assistant.

## Фармат на аснове сутнасці (Legacy)

Вызначайце сутнасці асобна. Карысна для арганізацыі сутнасцей па доменах (асвятленне, выключальнікі, датчыкі).

### Характарыстыкі
- Адна сутнасць на адзін запіс YAML
- Фокус на канкрэтныя тыпы датчыкаў або выхадаў
- Аўтаматычнае групаванне прыстасаванняў па префіксе адраса
- Прыдатна для арганізацыі асобных сутнасцей

### Прыклад
```yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 1.1
  devices:
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"
        - type: illuminance
          name: "Kitchen Illuminance"
          object_id: "hdl_sensor_illuminance_kitchen_ceiling"
```

### Арганізацыя файлаў

```
entities/
├── buspro_devices/
│   └── kitchen/
│       └── multisensor_2_10.yaml    # Конфігурацыя сутнасці на аснове прыстасавання
```

## Фармат на аснове прыстасавання (Modern)

Вызначайце поўныя прыстасаванні з усімі іх каналамі/сутнасцямі. Карысна для кіравання ўсімі аспектамі прыстасавання ў адным месцы.

### Характарыстыкі
- Адно прыстасаванне = адзін файл YAML
- Усе каналы вызначаны разам
- Ясная групіроўка і структура прыстасавання
- Прыдатна для комплекснага кіравання прыстасаваннем
- Непасрэдна адпавядае реестру прыстасаванняў buspro

### Прыклад
```yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 1.1
  devices:
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
          object_id: "hdl_switch_light_bathroom_main"
        - number: 2
          name: "Exhaust Fan"
          enabled: true
          object_id: "hdl_switch_fan_bathroom_exhaust"

    - address: "2.5"
      name: "Guestroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Bra Okno"
          enabled: true
          object_id: "hdl_switch_light_guestroom_bra_window"
        - number: 2
          name: "Bra Dver"
          enabled: true
          object_id: "hdl_switch_light_guestroom_bra_door"
```

### Арганізацыя файлаў

```
entities/
├── switches/
│   ├── light/
│   │   ├── guestroom/
│   │   │   ├── switch_light_guestroom_bra_window.yaml  # На аснове прыстасавання
│   │   │   └── switch_light_guestroom_bra_door.yaml
│   │   └── bathroom/
│   │       └── switch_light_bathroom_main.yaml
```

## Дэталі фармату каналаў на аснове прыстасавання

### Абавязковыя палі

```yaml
address: "2.5"                    # Адрас прыстасавання (падмережа.прыстасаванне)
name: "Device Name"               # Зразумелая назва прыстасавання
model: "HDL-MD0606.32"           # Мадэль прыстасавання з каталога
device_type: "relay|dimmer|..."  # Тып сутнасці
channels:                         # Спіс каналаў/сутнасцей
  - number: 1                     # Номар канала (1-N) або назва магчымасці
    name: "Channel Name"          # Адлюстраваемая назва канала
    enabled: true                 # Ствараць ли сутнасць (па змовчанню: true)
```

### Неабавязковыя палі

```yaml
channels:
  - number: 1
    name: "Channel Name"
    enabled: true
    object_id: "hdl_switch_light_guestroom_bra_window"  # Суфікс ID сутнасці
    unique_id: "buspro-2.5-relay-1"                     # Унікальны ідэнтыфікатар
```

## Падтрыманыя тыпы прыстасаванняў

**Асвятленне:**
- `relay` - Простыя выключальнікі (укл/выкл)
- `dimmer` - Дымаваныя асветлівы (кіраванне яркасцю 0-255)

**Датчыкі і ўваходы:**
- `dry_contact` - Бінарныя датчыкі (кантакты дзвяраў/вокнаў)
- `multisensor` - Комплексныя датчыкі навакольнага асяродзя
- `universal_switch` - Универсальныя ўваходы перамыкачоў з логікай дзень/ночь

**Клімат і HVAC:**
- `floor_heating` - Модулі кіравання падагрэвам паду/тэмпературай
- `ac` - Кантролеры кандыцыянавання

**Мотарызаваныя:**
- `cover` - Мотары жалюзі/ставняў з кіраваннем становішча
- `fan` - Кантролеры хуткасці вентылятараў

## Камбінаванне абоіх падыходаў

Вы можаце выкарыстоўваць абодва фарматы адначасова, калі яны не канфліктуюць:

```yaml
buspro:
  devices:
    # На аснове сутнасці: мультысенсор
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"

    # На аснове прыстасавання: рэле з каналамі
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          object_id: "hdl_switch_light_bathroom_main"
```

**Важна:** Кожны адрас можа быць вызначаны толькі адзін раз. Не выкарыстоўвайце адзін і той жа адрас у обух форматах.

## Групіроўка реестру прыстасаванняў

Абодва фарматы аўтаматычна групіруюць сутнасці пад іх бацькоўскім прыстасаваннем у рэестры прыстасаванняў Home Assistant:

- Прыстасаванні ідэнтыфікуюцца па **базавым адрасе** (напрыклад, `2.5`)
- Усе сутнасці з адрасамі `2.5.1`, `2.5.2`, ... групіруюцца пад прыстасаваннем `2.5`
- Ўласцівасці прыстасавання (назва, мадэль, вытворца) прымяняюцца да ўсіх сутнасцей

### Прыклад ієрархіі реестру прыстасаванняў

```
Прыстасаванне: Guestroom Relay (2.5)
├── Сутнасць: Bra Okno (2.5.1) [dimmer/switch]
└── Сутнасць: Bra Dver (2.5.2) [dimmer/switch]

Прыстасаванне: Bathroom Relay (2.4)
├── Сутнасць: Main Light (2.4.1) [relay/switch]
└── Сутнасць: Exhaust Fan (2.4.2) [relay/switch]
```

## Найлепшыя практыкі

### Для фармату на аснове сутнасці:
- Арганізуйце файлы па доменах (`entities/sensors/`, `entities/lights/`)
- Адна сутнасць у адным файле
- Выкарыстоўвайце апісальныя назвы файлаў
- Прыдатна для канфігурацый, арыентаваных на датчыкі

### Для фармату на аснове прыстасавання:
- Арганізуйце файлы па кімнатах або групах прыстасаванняў
- Усе каналы ў адным файле
- Выкарыстоўвайце ўзгоднены назвы для ўсіх каналаў
- Прыдатна для арганізаванага кіравання прыстасаваннямі

### Для абоіх:
- Не дублюйце адрасы паміж форматамі
- Выкарыстоўвайце фармат, які адпавядае вашаму рабочаму працэсу
- Разглядайце перавагі вашай каманды
- Дакументуйце свой выбар у CLAUDE.md або README
