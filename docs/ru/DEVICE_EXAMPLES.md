# Примеры конфигурации устройств HDL Buspro

[🇧🇾 Беларуская](../be/DEVICE_EXAMPLES.md) | [🇩🇪 Deutsch](../de/DEVICE_EXAMPLES.md) | [🇬🇧 English](../en/DEVICE_EXAMPLES.md) | [🇪🇸 Español](../es/DEVICE_EXAMPLES.md) | [🇫🇷 Français](../fr/DEVICE_EXAMPLES.md) | [🇮🇹 Italiano](../it/DEVICE_EXAMPLES.md) | [🇳🇱 Nederlands](../nl/DEVICE_EXAMPLES.md) | [🇳🇴 Norsk](../no/DEVICE_EXAMPLES.md) | 🇷🇺 Русский | [🇺🇦 Українська](../uk/DEVICE_EXAMPLES.md)

Это руководство содержит практические примеры конфигурации интерфейса и YAML для всех поддерживаемых типов устройств в интеграции HDL Buspro.

**Содержание:**
- [Релейные устройства](#релейные-устройства)
- [Диммерные устройства](#диммерные-устройства)
- [Устройства управления жалюзи](#устройства-управления-жалюзи)
- [Вентиляторы](#вентиляторы)
- [Климатические устройства](#климатические-устройства)
- [Датчики](#датчики)
- [Бинарные датчики](#бинарные-датчики)

---

## Релейные устройства

Релейные устройства - это простые выключатели включения/выключения, используемые для освещения, вентиляторов и других двоичных нагрузок.

**Поддерживаемые модели:**
- `HDL-MR0410.431` - 4 релейных канала
- `HDL-MR0810.432` - 8 релейных каналов
- `HDL-MR1210.433` - 12 релейных каналов
- `HDL-MR1610.433` - 16 релейных каналов
- Варианты мощных реле HDL (MR0416, MR0816, MR1216, MR1616, MR0420C и т.д.)

### Пример конфигурации через интерфейс

**Шаги:**
1. Перейдите в **Параметры > Устройства и услуги > HDL Buspro > Настроить**
2. Нажмите **Добавить устройство**
3. Выберите тип устройства: **Реле**
4. Выберите точную модель: **HDL-MR0410.431** (4 канала)
5. Введите адрес Buspro: `1.10`
6. Введите название устройства: "Освещение гостиной"
7. Назовите каналы:
   - Канал 1: "Потолочный светильник"
   - Канал 2: "Настольная лампа"
   - Канал 3: "Настенный светильник"
   - Канал 4: "" (оставьте пустым, чтобы отключить)
8. Нажмите **Сохранить**

**Результат:**
- `light.living_room_lights_ceiling_light`
- `light.living_room_lights_table_lamp`
- `light.living_room_lights_wall_sconce`

### Пример конфигурации YAML

**Ориентированный на сущности (отдельные файлы):**

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

**Ориентированный на устройство (полное определение устройства):**

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

## Диммерные устройства

Диммерные устройства управляют уровнем яркости (0-255) для диммируемых светильников.

**Поддерживаемые модели:**
- `HDL-MD0206.432` - 2 диммерных канала
- `HDL-MD0403.432` - 4 диммерных канала
- `HDL-MD0602.432` - 6 диммерных каналов
- Диммеры HDL с тыльным фронтом (MDT0203, MDT04015, MDT06015 и т.д.)
- `HDL-MDLED0605.432` - 6 диммерных каналов с диагностикой

### Пример конфигурации через интерфейс

**Шаги:**
1. Перейдите в **Параметры > Устройства и услуги > HDL Buspro > Настроить**
2. Нажмите **Добавить устройство**
3. Выберите тип устройства: **Диммер**
4. Выберите точную модель: **HDL-MD0602.432** (6 каналов)
5. Введите адрес Buspro: `1.5`
6. Введите название устройства: "Спальня диммеры"
7. Назовите каналы:
   - Канал 1: "Основное освещение"
   - Канал 2: "Прикроватный левый"
   - Канал 3: "Прикроватный правый"
   - Каналы 4-6: оставьте пустыми
8. Нажмите **Сохранить**

**Результат:**
- `light.bedroom_dimmers_main_light` (диммируемый 0-255)
- `light.bedroom_dimmers_bedside_left` (диммируемый 0-255)
- `light.bedroom_dimmers_bedside_right` (диммируемый 0-255)

### Пример конфигурации YAML

**Ориентированный на сущности:**

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

**Ориентированный на устройство:**

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

## Устройства управления жалюзи

Устройства управления жалюзи управляют моторизованными жалюзи, ставнями и шторами.

**Поддерживаемые модели:**
- `HDL-MW02.431` - 2 канала штор/жалюзи
- `HDL-MWM45.431` - Сущности штор/жалюзи (настраиваемые каналы)

### Пример конфигурации через интерфейс

**Шаги:**
1. Перейдите в **Параметры > Устройства и услуги > HDL Buspro > Настроить**
2. Нажмите **Добавить устройство**
3. Выберите тип устройства: **Жалюзи**
4. Выберите точную модель: **HDL-MW02.431** (2 канала)
5. Введите адрес Buspro: `2.10`
6. Введите название устройства: "Жалюзи гостиной"
7. Назовите каналы:
   - Канал 1: "Окна"
   - Канал 2: "Дверь патио"
8. Нажмите **Сохранить**

**Результат:**
- `cover.living_room_blinds_windows`
- `cover.living_room_blinds_patio_door`

### Пример конфигурации YAML

**Ориентированный на устройство:**

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

## Вентиляторы

Вентиляторы управляют вентиляторами с переменной скоростью.

**Поддерживаемые модели:**
- Универсальный профиль вентилятора (вентиляторы с переменной скоростью)

### Пример конфигурации через интерфейс

**Шаги:**
1. Перейдите в **Параметры > Устройства и услуги > HDL Buspro > Настроить**
2. Нажмите **Добавить устройство**
3. Выберите тип устройства: **Вентилятор**
4. Выберите точную модель: **Универсальный** (укажите количество каналов)
5. Введите адрес Buspro: `3.5`
6. Введите название устройства: "Вытяжной вентилятор в ванной"
7. Назовите канал: "Основной вентилятор"
8. Нажмите **Сохранить**

**Результат:**
- `fan.bathroom_exhaust_fan_main_fan` (управление скоростью 0-255)

### Пример конфигурации YAML

**Ориентированный на устройство:**

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

## Климатические устройства

Климатические устройства управляют температурой и системами HVAC.

**Поддерживаемые модели:**
- `HDL-MFH04.432` - 4 канала теплого пола
- `HDL-MFH06.432` - 6 каналов теплого пола
- `HDL-M/HVAC8.1` - Управление климатом AC
- `HDL-MPED4.431` - Управление климатом AC
- Универсальный профиль AC
- Универсальный профиль теплого пола

### Пример конфигурации через интерфейс - AC

**Шаги:**
1. Перейдите в **Параметры > Устройства и услуги > HDL Buspro > Настроить**
2. Нажмите **Добавить устройство**
3. Выберите тип устройства: **Климат**
4. Выберите точную модель: **HDL-M/HVAC8.1** (AC)
5. Введите адрес Buspro: `3.1`
6. Введите название устройства: "AC гостиной"
7. Нажмите **Сохранить**

**Результат:**
- `climate.living_room_ac` (целевая температура, режим, управление питанием)

### Пример конфигурации YAML

**Ориентированный на устройство:**

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

## Датчики

Датчики предоставляют данные температуры, влажности, освещенности и движения.

**Поддерживаемые модели:**
- `HDL-MSP02.4C` - Температура, освещенность, движение
- `HDL-MSP07M.4C` - Температура, освещенность, влажность, движение, 2 контакта
- `HDL-MS08M.4C` - Температура, освещенность, движение
- `HDL-MS12M.4C` - Температура, освещенность, влажность, движение, 2 контакта
- `HDL-MCLog.431` - Логический контроллер (только чтение)
- Датчики температуры панели (MPTL, MP2B, MP4B, MPL8 и т.д.)

### Пример конфигурации через интерфейс

**Шаги:**
1. Перейдите в **Параметры > Устройства и услуги > HDL Buspro > Настроить**
2. Нажмите **Добавить устройство**
3. Выберите тип устройства: **Мультидатчик**
4. Выберите точную модель: **HDL-MSP07M.4C**
5. Введите адрес Buspro: `2.5`
6. Введите название устройства: "Датчик гостиной"
7. Нажмите **Сохранить**

**Результат:**
- `sensor.living_room_sensor_temperature`
- `sensor.living_room_sensor_illuminance`
- `sensor.living_room_sensor_humidity`
- `binary_sensor.living_room_sensor_motion`
- 2 дополнительных сухих контакта

### Пример конфигурации YAML

**Ориентированный на сущности:**

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

**Ориентированный на устройство:**

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

## Бинарные датчики

Бинарные датчики предоставляют статус включения/выключения сухих контактов и датчиков дверей/окон.

**Поддерживаемые модели:**
- `HDL-MS04.432` - 4 канала сухих контактов
- `HDL-MS24.232` - 24 канала сухих контактов
- Мультидатчики с интегрированными контактами (MSP07M, MS12M и т.д.)

### Пример конфигурации через интерфейс

**Шаги:**
1. Перейдите в **Параметры > Устройства и услуги > HDL Buspro > Настроить**
2. Нажмите **Добавить устройство**
3. Выберите тип устройства: **Сухой контакт**
4. Выберите точную модель: **HDL-MS04.432** (4 канала)
5. Введите адрес Buspro: `1.20`
6. Введите название устройства: "Датчики дверей и окон"
7. Назовите каналы:
   - Канал 1: "Входная дверь"
   - Канал 2: "Гараж дверь"
   - Канал 3: "Окно гостиной"
   - Канал 4: оставьте пустым
8. Нажмите **Сохранить**

**Результат:**
- `binary_sensor.door_window_sensors_front_door`
- `binary_sensor.door_window_sensors_garage_door`
- `binary_sensor.door_window_sensors_living_room_window`

### Пример конфигурации YAML

**Ориентированный на устройство:**

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

## Комплексный пример с несколькими устройствами

Вот полный файл конфигурации, показывающий несколько типов устройств, работающих вместе:

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

## Советы и лучшие практики

1. **Используйте интерфейс для простых установок** - Интерфейс предоставляет интуитивный способ добавления и управления устройствами без необходимости написания YAML.

2. **Используйте YAML для сложных или программных конфигураций** - YAML лучше подходит для больших установок или когда требуется управление версиями.

3. **Адреса** - Всегда используйте формат `subnet.device` для адресов (например, `1.5`, `2.10`). Значения `subnet` и `device` должны быть действительными адресами Buspro в вашей сети.

4. **Нумерация каналов** - Каналы нумеруются с 1. Оставьте название канала пустым в интерфейсе, чтобы отключить его, что предотвратит создание сущности для неиспользуемых каналов.

5. **Названия устройств** - Используйте описательные имена на основе расположения (например, "Освещение гостиной" вместо "Реле"). Это облегчает понимание автоматизаций и сцен.

6. **Object IDs** - В YAML `object_id` является опциональным, но рекомендуется. Это управляет слагом ID сущности. Если опущено, Home Assistant генерирует его из названия канала.

7. **Уникальные ID** - Для продвинутых случаев, когда требуется ручное управление записями реестра сущностей, используйте `unique_id` в конфигурации YAML. Это позволяет Home Assistant надежно отслеживать сущность даже при изменении названия устройства.

Для получения более подробной информации о форматах конфигурации YAML см. [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md).
