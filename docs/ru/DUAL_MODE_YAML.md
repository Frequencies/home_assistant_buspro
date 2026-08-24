# Двухрежимная конфигурация YAML

[🇧🇾 Беларуская](../be/DUAL_MODE_YAML.md) | [🇩🇪 Deutsch](../de/DUAL_MODE_YAML.md) | [🇬🇧 English](../en/DUAL_MODE_YAML.md) | [🇪🇸 Español](../es/DUAL_MODE_YAML.md) | [🇫🇷 Français](../fr/DUAL_MODE_YAML.md) | [🇮🇹 Italiano](../it/DUAL_MODE_YAML.md) | [🇳🇱 Nederlands](../nl/DUAL_MODE_YAML.md) | [🇳🇴 Norsk](../no/DUAL_MODE_YAML.md) | 🇷🇺 Русский | [🇺🇦 Українська](../uk/DUAL_MODE_YAML.md)

---

Пользовательский компонент buspro поддерживает два дополнительных подхода к конфигурации YAML:

1. **На основе сущности** (Legacy) - Определения отдельных сущностей
2. **На основе устройства** (Modern) - Полные определения устройства со всеми каналами

Вы можете использовать **либо один подход, либо оба одновременно** в конфигурации Home Assistant.

## Формат на основе сущности (Legacy)

Определяйте сущности по отдельности. Полезно для организации сущностей по доменам (огни, выключатели, датчики).

### Характеристики
- Одна сущность на одну запись YAML
- Фокус на определённые типы датчиков или выходов
- Автоматическое группирование устройств по префиксу адреса
- Подходит для организации отдельных сущностей

### Пример
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

## Формат на основе устройства (Modern)

Определяйте полные устройства со всеми их каналами/сущностями. Полезно для управления всеми аспектами устройства в одном месте.

### Характеристики
- Одно устройство = один YAML файл
- Все каналы определены вместе
- Ясное группирование и структура устройства
- Подходит для комплексного управления устройством
- Напрямую соответствует реестру устройств buspro

### Пример
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

### Организация файлов

```
entities/
├── buspro_devices/
│   └── kitchen/
│       └── multisensor_2_10.yaml    # Конфигурация сущности на основе устройства
```

## Формат на основе устройства (Modern)

Определяйте полные устройства со всеми их каналами/сущностями. Полезно для управления всеми аспектами устройства в одном месте.

### Характеристики
- Одно устройство = один YAML файл
- Все каналы определены вместе
- Ясное группирование и структура устройства
- Подходит для комплексного управления устройством
- Напрямую соответствует реестру устройств buspro

### Пример
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

### Организация файлов

```
entities/
├── switches/
│   ├── light/
│   │   ├── guestroom/
│   │   │   ├── switch_light_guestroom_bra_window.yaml  # На основе устройства
│   │   │   └── switch_light_guestroom_bra_door.yaml
│   │   └── bathroom/
│   │       └── switch_light_bathroom_main.yaml
```

## Детали формата каналов на основе устройства

### Обязательные поля

```yaml
address: "2.5"                    # Адрес устройства (подсеть.устройство)
name: "Device Name"               # Понятное имя устройства
model: "HDL-MD0606.32"           # Модель устройства из каталога
device_type: "relay|dimmer|..."  # Тип сущности
channels:                         # Список каналов/сущностей
  - number: 1                     # Номер канала (1-N) или название возможности
    name: "Channel Name"          # Отображаемое имя канала
    enabled: true                 # Создавать ли сущность (по умолчанию: true)
```

### Необязательные поля

```yaml
channels:
  - number: 1
    name: "Channel Name"
    enabled: true
    object_id: "hdl_switch_light_guestroom_bra_window"  # Суффикс ID сущности
    unique_id: "buspro-2.5-relay-1"                     # Уникальный идентификатор
```

## Поддерживаемые типы устройств

**Освещение:**
- `relay` - Простые выключатели (вкл/выкл)
- `dimmer` - Диммируемые огни (управление яркостью 0-255)

**Датчики и входы:**
- `dry_contact` - Бинарные датчики (контакты дверей/окон)
- `multisensor` - Комплексные датчики окружающей среды
- `universal_switch` - Универсальные входы переключателей с логикой день/ночь

**Климат и HVAC:**
- `floor_heating` - Модули управления подогревом пола/температурой
- `ac` - Контроллеры кондиционирования

**Моторизованные:**
- `cover` - Моторы жалюзи/ставней с управлением положением
- `fan` - Контроллеры скорости вентиляторов

## Комбинирование обоих подходов

Вы можете использовать оба формата одновременно, если они не конфликтуют. Каждый адрес может быть определён только один раз.

## Группирование реестра устройств

Оба формата автоматически группируют сущности под их родительским устройством:
- Устройства идентифицируются по **базовому адресу** (например, `2.5`)
- Все сущности с адресами `2.5.1`, `2.5.2`, ... группируются под устройством `2.5`
- Свойства устройства применяются ко всем сущностям

## Лучшие практики

**Для формата на основе сущности:**
- Организуйте файлы по доменам
- Одна сущность в одном файле
- Используйте описательные имена файлов
- Подходит для конфигураций, ориентированных на датчики

**Для формата на основе устройства:**
- Организуйте файлы по комнатам или группам устройств
- Все каналы в одном файле
- Используйте согласованные имена для всех каналов
- Подходит для организованного управления устройствами
