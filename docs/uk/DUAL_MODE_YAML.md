# Двохрежимна конфігурація YAML

[🇧🇾 Беларуская](../be/DUAL_MODE_YAML.md) | [🇩🇪 Deutsch](../de/DUAL_MODE_YAML.md) | [🇬🇧 English](../en/DUAL_MODE_YAML.md) | [🇪🇸 Español](../es/DUAL_MODE_YAML.md) | [🇫🇷 Français](../fr/DUAL_MODE_YAML.md) | [🇮🇹 Italiano](../it/DUAL_MODE_YAML.md) | [🇳🇱 Nederlands](../nl/DUAL_MODE_YAML.md) | [🇳🇴 Norsk](../no/DUAL_MODE_YAML.md) | [🇷🇺 Русский](../ru/DUAL_MODE_YAML.md) | 🇺🇦 Українська

---

Користувацький компонент buspro підтримує два взаємодоповняльних підходи до конфігурації YAML:

1. **На основі сутності** (Legacy) - Визначення окремих сутностей
2. **На основі пристрою** (Modern) - Повні визначення пристрою з усіма каналами

Ви можете використовувати **або один підхід, або обидва одночасно** у конфігурації Home Assistant.

## Формат на основі сутності (Legacy)

Визначайте сутності окремо. Корисно для організації сутностей за доменами (вогні, вимикачі, датчики).

### Характеристики
- Одна сутність на один запис YAML
- Фокус на конкретні типи датчиків або виходів
- Автоматичне групування пристроїв за префіксом адреси
- Підходить для організації окремих сутностей

### Приклад
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

### Організація файлів

```
entities/
├── buspro_devices/
│   └── kitchen/
│       └── multisensor_2_10.yaml    # Конфігурація сутності на основі пристрою
```

## Формат на основі пристрою (Modern)

Визначайте повні пристрої з усіма їхніми каналами/сутностями. Корисно для управління всіма аспектами пристрою в одному місці.

### Характеристики
- Один пристрій = один файл YAML
- Усі канали визначені разом
- Чітке групування та структура пристрою
- Підходить для комплексного управління пристроєм
- Безпосередньо відповідає реєстру пристроїв buspro

### Приклад
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

### Організація файлів

```
entities/
├── switches/
│   ├── light/
│   │   ├── guestroom/
│   │   │   ├── switch_light_guestroom_bra_window.yaml  # На основі пристрою
│   │   │   └── switch_light_guestroom_bra_door.yaml
│   │   └── bathroom/
│   │       └── switch_light_bathroom_main.yaml
```

## Деталі формату каналів на основі пристрою

### Обов'язкові поля

```yaml
address: "2.5"                    # Адреса пристрою (підмережа.пристрій)
name: "Device Name"               # Зрозуміла назва пристрою
model: "HDL-MD0606.32"           # Модель пристрою з каталогу
device_type: "relay|dimmer|..."  # Тип сутності
channels:                         # Список каналів/сутностей
  - number: 1                     # Номер каналу (1-N) або назва можливості
    name: "Channel Name"          # Отображуване ім'я каналу
    enabled: true                 # Створювати ли сутність (по умовчанню: true)
```

### Необов'язкові поля

```yaml
channels:
  - number: 1
    name: "Channel Name"
    enabled: true
    object_id: "hdl_switch_light_guestroom_bra_window"  # Суфікс ID сутності
    unique_id: "buspro-2.5-relay-1"                     # Унікальний ідентифікатор
```

## Підтримувані типи пристроїв

**Освітлення:**
- `relay` - Прості вимикачи (вкл/вимк)
- `dimmer` - Диморовані вогні (управління яскравістю 0-255)

**Датчики та входи:**
- `dry_contact` - Бінарні датчики (контакти дверей/вікон)
- `multisensor` - Комплексні датчики навколишнього середовища
- `universal_switch` - Універсальні входи перемикачів з логікою день/ніч

**Клімат та HVAC:**
- `floor_heating` - Модулі управління підігрівом підлоги/температурою
- `ac` - Контролери кондиціонування

**Моторизовані:**
- `cover` - Мотори жалюзі/ставень з управлінням положенням
- `fan` - Контролери швидкості вентиляторів

## Комбінування обох підходів

Ви можете використовувати обидва формати одночасно, якщо вони не конфліктують:

```yaml
buspro:
  devices:
    # На основі сутності: мультисенсор
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"

    # На основі пристрою: реле з каналами
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          object_id: "hdl_switch_light_bathroom_main"
```

**Важливо:** Кожна адреса може бути визначена лише один раз. Не використовуйте одну і ту ж адресу в обох форматах.

## Групування реєстру пристроїв

Обидва формати автоматично групують сутності під їхнім батьківським пристроєм в реєстрі пристроїв Home Assistant:

- Пристрої ідентифікуються за **базовою адресою** (наприклад, `2.5`)
- Усі сутності з адресами `2.5.1`, `2.5.2`, ... групуються під пристроєм `2.5`
- Властивості пристрою (назва, модель, виробник) застосовуються до всіх сутностей

### Приклад ієрархії реєстру пристроїв

```
Пристрій: Guestroom Relay (2.5)
├── Сутність: Bra Okno (2.5.1) [dimmer/switch]
└── Сутність: Bra Dver (2.5.2) [dimmer/switch]

Пристрій: Bathroom Relay (2.4)
├── Сутність: Main Light (2.4.1) [relay/switch]
└── Сутність: Exhaust Fan (2.4.2) [relay/switch]
```

## Найкращі практики

### Для формату на основі сутності:
- Організуйте файли за доменами (`entities/sensors/`, `entities/lights/`)
- Одна сутність в одному файлі
- Використовуйте описові назви файлів
- Підходить для конфігурацій, орієнтованих на датчики

### Для формату на основі пристрою:
- Організуйте файли за кімнатами або групами пристроїв
- Усі канали в одному файлі
- Використовуйте узгоджені назви для всіх каналів
- Підходить для організованого управління пристроями

### Для обох:
- Не дублюйте адреси між форматами
- Використовуйте формат, який відповідає вашому робочому процесу
- Розглядайте переваги вашої команди
- Документуйте свій вибір у CLAUDE.md або README
