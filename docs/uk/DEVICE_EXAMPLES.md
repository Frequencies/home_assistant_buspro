# Приклади конфігурації пристроїв HDL Buspro
[🇧🇾 Беларуская](../be/DEVICE_EXAMPLES.md) | [🇩🇪 Deutsch](../de/DEVICE_EXAMPLES.md) | [🇬🇧 English](../en/DEVICE_EXAMPLES.md) | [🇪🇸 Español](../es/DEVICE_EXAMPLES.md) | [🇫🇷 Français](../fr/DEVICE_EXAMPLES.md) | [🇮🇹 Italiano](../it/DEVICE_EXAMPLES.md) | [🇳🇱 Nederlands](../nl/DEVICE_EXAMPLES.md) | [🇳🇴 Norsk](../no/DEVICE_EXAMPLES.md) | [🇷🇺 Русский](../ru/DEVICE_EXAMPLES.md) | 🇺🇦 Українська

Цей посібник містить практичні приклади конфігурації інтерфейсу та YAML для всіх підтримуваних типів пристроїв у інтеграції HDL Buspro.

**Зміст:**
- [Підтвердження Команди (НОВЕ!)](#підтвердження-команди-нове)
- [Реле пристрої](#реле-пристрої)
- [Диммерні пристрої](#диммерні-пристрої)
- [Пристрої керування жалюзі](#пристрої-керування-жалюзі)
- [Вентилятори](#вентилятори)
- [Кліматичні пристрої](#кліматичні-пристрої)
- [Датчики](#датчики)
- [Бінарні датчики](#бінарні-датчики)

---

## Підтвердження Команди (НОВЕ!)

### Що таке Підтвердження Команди?

Підтвердження команди гарантує, що зміни стану пристрою відображаються в Home Assistant лише після того, як фізичний пристрій підтвердить отримання та виконання команди. Це запобігає рассинхронізації інтерфейсу, коли команди втрачаються через перешкоди в мережі.

**Без Підтвердження:**
- Користувач натискає "Увімкнути"
- Інтерфейс оновлюється одразу (~5ms)
- Пристрій отримує команду через ~100ms
- Якщо пристрій не отримає → Інтерфейс показує невірний стан

**З Підтвердженням:**
- Користувач натискає "Увімкнути"
- Система чекає на підтвердження пристрою (~100-500ms)
- Пристрій підтверджує отримання та виконання
- Інтерфейс оновлюється тільки після підтвердження
- Якщо пристрій не відповідає → Явна помилка часу очікування

### Чому вам це потрібно

Включіть підтвердження для:
- **Критичних пристроїв** - Реле аварійної зупинки, головні вимикачі
- **Ненадійних мереж** - Високі перешкоди, багато колізій
- **Залежностей автоматизації** - Автоматизація, яка потребує гарантованого стану
- **Пристроїв, критичних для безпеки** - Системи HVAC, теплові підлоги

### Приклади Конфігурації

#### Для Критичного Реле

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.10.1":
        name: "Реле аварійної зупинки"
        enable_confirmation: true
        confirmation_timeout: 5.0
        confirmation_retries: 3
```

#### Для Кількох Критичних Пристроїв

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      # Критичний - підтвердити отримання
      "1.10.1":
        name: "Основне стельове світло"
        enable_confirmation: true
      
      # Деякритичний - тримати швидким (за замовчуванням)
      "1.10.2":
        name: "Фонове освітлення"
        # enable_confirmation за замовчуванням false

cover:
  - platform: buspro
    devices:
      "2.10.1":
        name: "Спальні штори"
        enable_confirmation: true
        confirmation_timeout: 10.0  # Більше для механічних пристроїв
        confirmation_retries: 2

climate:
  - platform: buspro
    devices:
      - address: "3.1"
        name: "Кондиціонер вітальні"
        enable_confirmation: true
        confirmation_timeout: 5.0
        confirmation_retries: 3
```

### Параметри Конфігурації

| Параметр | Тип | За замовчуванням | Діапазон | Мета |
|-----------|------|---------|-------|---------| 
| `enable_confirmation` | boolean | `false` | `true`/`false` | Включити/вимкнути підтвердження |
| `confirmation_timeout` | float | `5.0` | 0.1-60 секунд | Макс. час очікування відповіді пристрою |
| `confirmation_retries` | integer | `3` | 0-10 | Спроби повтору при часі очікування |

### Рекомендації за Типами Пристроїв

| Тип Пристрою | Час Очікування | Повтори | Примітки |
|------------|---------|---------|-------|
| Реле/Вимикач | 5.0s | 3 | Швидкий електронний пристрій |
| Світло/Диммер | 5.0s | 3 | Швидкий електронний пристрій |
| Вентилятор | 5.0s | 3 | Швидкий електронний пристрій |
| Жалюзі/Штора | 10.0s | 2 | Механічний пристрій, повільніший |
| Клімат AC | 5.0s | 3 | Електронний пристрій |
| Теплий підлога | 5.0s | 3 | Електронний пристрій |

### Вплив на Користувацький Інтерфейс

Коли підтвердження включено:
- **Затримка:** Затримка 100-500ms (проти 5-10ms без)
- **Зворотний зв'язок:** Чітке зазначення успіху/невдачі
- **Надійність:** Гарантована синхронізація стану

Коли підтвердження вимкнено (за замовчуванням):
- **Затримка:** ~5-10ms (без змін)
- **Поведінка:** Fire-and-forget (поточна поведінка)
- **Ризик:** Можливі тихі відмови команд

---

## Реле пристрої

Реле пристрої - це прості вмикачі вкл./викл., що використовуються для освітлення, вентиляторів та інших двійкових навантажень.

**Підтримувані моделі:**
- `HDL-MR0410.431` - 4 канали реле
- `HDL-MR0810.432` - 8 каналів реле
- `HDL-MR1210.433` - 12 каналів реле
- `HDL-MR1610.433` - 16 каналів реле
- Варіанти потужних реле HDL (MR0416, MR0816, MR1216, MR1616, MR0420C тощо)

### Приклад конфігурації через інтерфейс

**Кроки:**
1. Перейдіть до **Параметри > Пристрої та послуги > HDL Buspro > Налаштувати**
2. Натисніть **Додати пристрій**
3. Виберіть тип пристрою: **Реле**
4. Виберіть точну модель: **HDL-MR0410.431** (4 канали)
5. Введіть адресу Buspro: `1.10`
6. Введіть назву пристрою: "Освітлення гостинної"
7. Назвіть канали:
   - Канал 1: "Стельовий світильник"
   - Канал 2: "Настільна лампа"
   - Канал 3: "Настінний світильник"
   - Канал 4: "" (залиште порожнім для вимкнення)
8. Натисніть **Зберегти**

**Результат:**
- `light.living_room_lights_ceiling_light`
- `light.living_room_lights_table_lamp`
- `light.living_room_lights_wall_sconce`

### Приклад конфігурації YAML

**Орієнтований на сутності (окремі файли):**

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

**Орієнтований на пристрій (повне визначення пристрою):**

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

## Диммерні пристрої

Диммерні пристрої управляють рівнем яскравості (0-255) для затемнюваних світильників.

**Підтримувані моделі:**
- `HDL-MD0206.432` - 2 канали диммера
- `HDL-MD0403.432` - 4 канали диммера
- `HDL-MD0602.432` - 6 каналів диммера
- Диммери HDL з заднім фронтом (MDT0203, MDT04015, MDT06015 тощо)
- `HDL-MDLED0605.432` - 6 каналів диммера з діагностикою

### Приклад конфігурації через інтерфейс

**Кроки:**
1. Перейдіть до **Параметри > Пристрої та послуги > HDL Buspro > Налаштувати**
2. Натисніть **Додати пристрій**
3. Виберіть тип пристрою: **Диммер**
4. Виберіть точну модель: **HDL-MD0602.432** (6 каналів)
5. Введіть адресу Buspro: `1.5`
6. Введіть назву пристрою: "Спальня диммери"
7. Назвіть канали:
   - Канал 1: "Основне освітлення"
   - Канал 2: "Прикроватна ліва"
   - Канал 3: "Прикроватна права"
   - Канали 4-6: залиште порожніми
8. Натисніть **Зберегти**

**Результат:**
- `light.bedroom_dimmers_main_light` (затемнюваний 0-255)
- `light.bedroom_dimmers_bedside_left` (затемнюваний 0-255)
- `light.bedroom_dimmers_bedside_right` (затемнюваний 0-255)

### Приклад конфігурації YAML

**Орієнтований на сутності:**

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

**Орієнтований на пристрій:**

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

## Пристрої керування жалюзі

Пристрої керування жалюзі управляють моторизованими жалюзі, ставнями та завісками.

**Підтримувані моделі:**
- `HDL-MW02.431` - 2 канали завіс/жалюзі
- `HDL-MWM45.431` - Сутності завіс/жалюзі (налаштовувані канали)

### Приклад конфігурації через інтерфейс

**Кроки:**
1. Перейдіть до **Параметри > Пристрої та послуги > HDL Buspro > Налаштувати**
2. Натисніть **Додати пристрій**
3. Виберіть тип пристрою: **Жалюзі**
4. Виберіть точну модель: **HDL-MW02.431** (2 канали)
5. Введіть адресу Buspro: `2.10`
6. Введіть назву пристрою: "Жалюзі гостинної"
7. Назвіть канали:
   - Канал 1: "Вікна"
   - Канал 2: "Двері патіо"
8. Натисніть **Зберегти**

**Результат:**
- `cover.living_room_blinds_windows`
- `cover.living_room_blinds_patio_door`

### Приклад конфігурації YAML

**Орієнтований на пристрій:**

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

## Вентилятори

Вентилятори управляють вентиляторами зі змінною швидкістю.

**Підтримувані моделі:**
- Універсальний профіль вентилятора (вентилятори зі змінною швидкістю)

### Приклад конфігурації через інтерфейс

**Кроки:**
1. Перейдіть до **Параметри > Пристрої та послуги > HDL Buspro > Налаштувати**
2. Натисніть **Додати пристрій**
3. Виберіть тип пристрою: **Вентилятор**
4. Виберіть точну модель: **Універсальний** (вкажіть кількість каналів)
5. Введіть адресу Buspro: `3.5`
6. Введіть назву пристрою: "Витяжний вентилятор у ванній"
7. Назвіть канал: "Основний вентилятор"
8. Натисніть **Зберегти**

**Результат:**
- `fan.bathroom_exhaust_fan_main_fan` (керування швидкістю 0-255)

### Приклад конфігурації YAML

**Орієнтований на пристрій:**

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

## Кліматичні пристрої

Кліматичні пристрої управляють температурою та системами HVAC.

**Підтримувані моделі:**
- `HDL-MFH04.432` - 4 канали теплої підлоги
- `HDL-MFH06.432` - 6 каналів теплої підлоги
- `HDL-M/HVAC8.1` - Керування кліматом AC
- `HDL-MPED4.431` - Керування кліматом AC
- Універсальний профіль AC
- Універсальний профіль теплої підлоги

### Приклад конфігурації через інтерфейс - AC

**Кроки:**
1. Перейдіть до **Параметри > Пристрої та послуги > HDL Buspro > Налаштувати**
2. Натисніть **Додати пристрій**
3. Виберіть тип пристрою: **Клімат**
4. Виберіть точну модель: **HDL-M/HVAC8.1** (AC)
5. Введіть адресу Buspro: `3.1`
6. Введіть назву пристрою: "AC гостинної"
7. Натисніть **Зберегти**

**Результат:**
- `climate.living_room_ac` (цільова температура, режим, керування живленням)

### Приклад конфігурації YAML

**Орієнтований на пристрій:**

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

Датчики надають дані про температуру, вологість, освітленість та рух.

**Підтримувані моделі:**
- `HDL-MSP02.4C` - Температура, освітленість, рух
- `HDL-MSP07M.4C` - Температура, освітленість, вологість, рух, 2 контакти
- `HDL-MS08M.4C` - Температура, освітленість, рух
- `HDL-MS12M.4C` - Температура, освітленість, вологість, рух, 2 контакти
- `HDL-MCLog.431` - Логічний контролер (лише читання)
- Датчики температури панелі (MPTL, MP2B, MP4B, MPL8 тощо)

### Приклад конфігурації через інтерфейс

**Кроки:**
1. Перейдіть до **Параметри > Пристрої та послуги > HDL Buspro > Налаштувати**
2. Натисніть **Додати пристрій**
3. Виберіть тип пристрою: **Мультидатчик**
4. Виберіть точну модель: **HDL-MSP07M.4C**
5. Введіть адресу Buspro: `2.5`
6. Введіть назву пристрою: "Датчик гостинної"
7. Натисніть **Зберегти**

**Результат:**
- `sensor.living_room_sensor_temperature`
- `sensor.living_room_sensor_illuminance`
- `sensor.living_room_sensor_humidity`
- `binary_sensor.living_room_sensor_motion`
- 2 додаткові сухі контакти

### Приклад конфігурації YAML

**Орієнтований на сутності:**

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

**Орієнтований на пристрій:**

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

## Бінарні датчики

Бінарні датчики надають статус вкл./викл. від сухих контактів та датчиків дверей/вікон.

**Підтримувані моделі:**
- `HDL-MS04.432` - 4 канали сухих контактів
- `HDL-MS24.232` - 24 канали сухих контактів
- Мультидатчики з інтегрованими контактами (MSP07M, MS12M тощо)

### Приклад конфігурації через інтерфейс

**Кроки:**
1. Перейдіть до **Параметри > Пристрої та послуги > HDL Buspro > Налаштувати**
2. Натисніть **Додати пристрій**
3. Виберіть тип пристрою: **Сухий контакт**
4. Виберіть точну модель: **HDL-MS04.432** (4 канали)
5. Введіть адресу Buspro: `1.20`
6. Введіть назву пристрою: "Датчики дверей і вікон"
7. Назвіть канали:
   - Канал 1: "Вхідні двері"
   - Канал 2: "Двері гаража"
   - Канал 3: "Вікно гостинної"
   - Канал 4: залиште порожнім
8. Натисніть **Зберегти**

**Результат:**
- `binary_sensor.door_window_sensors_front_door`
- `binary_sensor.door_window_sensors_garage_door`
- `binary_sensor.door_window_sensors_living_room_window`

### Приклад конфігурації YAML

**Орієнтований на пристрій:**

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

## Комплексний приклад з кількома пристроями

Ось повний файл конфігурації, що показує кілька типів пристроїв, що працюють разом:

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

## Поради та кращі практики

1. **Використовуйте інтерфейс для простих установок** - Інтерфейс надає інтуїтивний спосіб додавання та управління пристроями без необхідності написання YAML.

2. **Використовуйте YAML для складних або програмних конфігурацій** - YAML краще підходить для великих установок або коли потрібен контроль версій.

3. **Адреси** - Завжди використовуйте формат `subnet.device` для адрес (наприклад, `1.5`, `2.10`). Значення `subnet` та `device` мають бути дійсними адресами Buspro у вашій мережі.

4. **Нумерація каналів** - Канали нумеруються починаючи з 1. Залиште назву каналу порожною в інтерфейсі, щоб вимкнути його, що запобігає створенню сутності для невикористовуваних каналів.

5. **Назви пристроїв** - Використовуйте описові імена на основі місцезнаходження (наприклад, "Освітлення гостинної" замість "Реле"). Це полегшує розуміння автоматизацій і сцен.

6. **Object IDs** - У YAML `object_id` є необов'язковим, але рекомендується. Це управляє слагом ID сутності. Якщо опущено, Home Assistant генерує його з назви каналу.

7. **Унікальні ID** - Для розширених випадків, коли потрібне ручне управління записами реєстру сутностей, використовуйте `unique_id` у конфігурації YAML. Це дозволяє Home Assistant надійно відстежувати сутність навіть при зміні назви пристрою.

Для отримання більш детальної інформації про формати конфігурації YAML див. [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md).
