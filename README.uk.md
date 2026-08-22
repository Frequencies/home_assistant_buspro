# HDL Buspro

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## Мови

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


# Інтеграція HDL Buspro дозволяє вам керувати системою HDL Buspro за допомогою Home Assistant.

## Встановлення

### Встановлення в один клік (HACS)

[![Відкрийте свій екземпляр Home Assistant і відкрийте репозиторій у Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Frequencies&repository=home_assistant_buspro&category=integration)

### Встановлення вручну

У HACS -> Integrations додайте кастомний репозиторій "https://github.com/Frequencies/home_assistant_buspro" з категорією "Integration". Виберіть інтеграцію з назвою "HDL Buspro" і завантажте її.

Перезапустіть Домашній помічник.

Перейдіть до Налаштування > Інтеграції та Додайте інтеграцію «HDL Buspro». Введіть IP-адресу та номер порту шлюзу.

## Конфігурація

#### Легка платформа
   
Щоб використовувати світло Buspro у своїй установці, додайте наступне до файлу configuration.yaml:

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
+ **running_time** _(int) (необов’язково)_: час роботи за умовчанням у секундах для всіх пристроїв. Час роботи становить 0 секунд, якщо не встановлено.
+ **ack_retry_enabled** _(boolean) (необов'язково)_: Увімкнути одноразовий повтор команди, якщо ACK не отримано протягом 0,8 с. Типово: `True`.
+ **пристрої** _(обов’язково)_: список пристроїв для налаштування
  + **X.X.X** _(обов’язково)_: адреса пристрою у форматі «<ідентифікатор підмережі>.<ідентифікатор пристрою>.<номер каналу>».
    + **name** _(рядок) (обов’язково)_: ім’я пристрою
    + **running_time** _(int) (необов’язково)_: час роботи пристрою в секундах. Якщо пропущено, використовується час роботи за замовчуванням для всіх пристроїв.
    + **ack_retry_enabled** _(boolean) (необов'язково)_: Перевизначення повтору ACK для конкретного пристрою.
    + **з можливістю затемнення** _(логічний) (необов’язковий)_: чи пристрій можна затемнювати? Типовим значенням є True.
    + **object_id** _(рядок) (необов’язковий)_: Device object_id. За замовчуванням автоматично генерується з назви пристрою.
    + **unique_id** _(рядок) (необов’язковий)_: Стабільний унікальний ідентифікатор сутності для реєстру сутностей Home Assistant.

#### Змінити платформу

Щоб використовувати перемикач Buspro у своїй установці, додайте наступне до файлу configuration.yaml:

```yaml
switch:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Switch
      1.89.2:
        name: Front Door Switch
```
+ **пристрої** _(обов’язково)_: список пристроїв для налаштування
  + **X.X.X** _(обов’язково)_: адреса пристрою у форматі «<ідентифікатор підмережі>.<ідентифікатор пристрою>.<номер каналу>».
    + **name** _(рядок) (обов’язково)_: ім’я пристрою
    + **object_id** _(рядок) (необов’язковий)_: Device object_id. За замовчуванням автоматично генерується з назви пристрою.
    + **unique_id** _(рядок) (необов’язковий)_: Стабільний унікальний ідентифікатор сутності для реєстру сутностей Home Assistant.

#### Сенсорна платформа

Щоб використовувати датчик Buspro у своїй установці, додайте наступне до файлу configuration.yaml:

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
+ **пристрої** _(обов’язково)_: список пристроїв для налаштування
  + **адреса** _(рядок) (обов’язково)_: адреса сенсорного пристрою у форматі «<ідентифікатор підмережі>.<ідентифікатор пристрою>».
  + **name** _(рядок) (обов’язково)_: ім’я пристрою
  + **тип** _(рядок) (обов’язково)_: Тип датчика для моніторингу.
    + Доступні датчики:
     + температура
     + освітленість
     + вологість
  + **одиниця_виміру** _(рядок) (необов’язково)_: текст, який буде відображатися як одиниця вимірювання
  + **object_id** _(рядок) (необов’язковий)_: Device object_id. За замовчуванням автоматично генерується з назви пристрою.
  + **unique_id** _(рядок) (необов’язковий)_: Стабільний унікальний ідентифікатор сутності для реєстру сутностей Home Assistant.
  + **device_class** _(рядок) (необов’язковий)_: клас пристрою HASS, наприклад, «температура»
  + **scan_interval** _(int) (Необов'язково)_: Інтервал опитування в секундах. Якщо не вказано або `0`, оновлення виконуються лише за повідомленнями Buspro.
(https://www.home-assistant.io/components/sensor/)
  + **пристрій** _(рядок) (необов’язково)_: тип сенсорного пристрою:
    + dlp

#### Двійкова сенсорна платформа

Щоб використовувати бінарний датчик Buspro у своїй інсталяції, додайте наступне до файлу configuration.yaml:

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
+ **пристрої** _(обов’язково)_: список пристроїв для налаштування
  + **адреса** _(рядок) (обов’язково)_: адреса пристрою датчика у форматі «<ідентифікатор підмережі>.<ідентифікатор пристрою>». Якщо
'type' = 'universal_switch' номер універсального комутатора має бути додано до адреси.
  + **name** _(рядок) (обов’язково)_: ім’я пристрою
  + **object_id** _(рядок) (необов’язковий)_: Device object_id. За замовчуванням автоматично генерується з назви пристрою.
  + **unique_id** _(рядок) (необов’язковий)_: Стабільний унікальний ідентифікатор сутності для реєстру сутностей Home Assistant.
  + **тип** _(рядок) (обов’язково)_: Тип датчика для моніторингу.
    + Доступні датчики:
      + руху
      + сухий_контакт_1
      + сухий_контакт_2
      + універсальний_перемикач
      + одноканальний
      + dry_contact
    + Примітки щодо формату адреси:
      + `motion`, `dry_contact_1`, `dry_contact_2`: `<subnet ID>.<device ID>`
      + `universal_switch`, `single_channel`, `dry_contact`: `<subnet ID>.<device ID>.<number>`
  + **device_class** _(рядок) (необов’язковий)_: клас пристрою HASS, наприклад, «рух»
  + **scan_interval** _(int) (Необов'язково)_: Інтервал опитування в секундах. Якщо не вказано або `0`, оновлення виконуються лише за повідомленнями Buspro.
(https://www.home-assistant.io/components/binary_sensor/)

#### Кліматична платформа

Щоб використовувати панель клімат-контролю Buspro у своїй установці, додайте наступне до свого файлу configuration.yaml:

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
+ **пристрої** _(обов’язково)_: список пристроїв для налаштування
  + **адреса** _(рядок) (обов’язково)_: адреса сенсорного пристрою у форматі «<ідентифікатор підмережі>.<ідентифікатор пристрою>».
  + **name** _(рядок) (обов’язково)_: ім’я пристрою
  + **тип** _(рядок) (необов’язковий)_: `ac` або `floor_heating`. Типовим є `підігрів підлоги`.
  + **floor_heating_device_type** _(рядок) (необов’язково)_: `dlp` або `module`.
Якщо опущено, `module` вибирається автоматично, коли вказано `channel`, інакше `dlp`.
  + **relay_address** _(string) (Необов'язково)_: Адреса каналу реле у форматі `<subnet ID>.<device ID>.<channel>`. Використовується як зовнішній зворотний зв'язок стану реле для HVAC-дії.
  + **object_id** _(рядок) (необов’язковий)_: Device object_id. За замовчуванням автоматично генерується з назви пристрою.
  + **unique_id** _(рядок) (необов’язковий)_: Стабільний унікальний ідентифікатор сутності для реєстру сутностей Home Assistant.
  + **preset_modes** _(список) (необов’язково)_: список підтримуваних попередньо встановлених режимів. Вибір попередньо встановленого режиму вимкнено, якщо не встановлено. Можливі значення наведено в таблиці нижче. Відповідні режими повинні бути ввімкнені в HDL (Floor Heating > Working Settings > Mode).
  + **channel** _(int) (Необов’язково)_: Канал модуля опалення підлоги (`1..6`) для `floor_heating_device_type: module`.
  + **min_temp** _(float) (Необов’язково)_: Мінімальна цільова температура, що відображається в інтерфейсі Home Assistant.
  + **max_temp** _(float) (Необов’язково)_: Максимальна цільова температура, що відображається в інтерфейсі Home Assistant.
  + **precision** _(float) (Необов’язково)_: Крок зміни цільової температури в інтерфейсі Home Assistant. Дозволені значення: `1`, `0.5`, `0.1`.
    
| HA preset mode | HDL mode |
|:--------------:|:--------:|
|      none      |  Normal  |
|      away      |   Away   |
|      home      |   Day    |
|     sleep      |  Night   |


#### Платформа штор (Cover)

Щоб використовувати штори Buspro у вашій інсталяції, додайте наступне до файлу `configuration.yaml`:

```yaml
cover:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Curtain
        invert: false
        object_id: living_room_curtain
```
+ **devices** _(обов'язково)_: відповідність каналів штор Buspro
  + **ключ** _(string)_: `<ID підмережі>.<ID пристрою>.<канал>`
  + **name** _(string) (обов'язково)_: відображувана назва
  + **invert** _(bool) (необов'язково)_: інвертувати напрямок відкриття/закриття. Типово `false`.
  + **object_id** _(string) (необов'язково)_: `object_id` сутності. Типово генерується з назви.
  + **unique_id** _(рядок) (необов’язковий)_: Стабільний унікальний ідентифікатор сутності для реєстру сутностей Home Assistant.

Підтримувані функції:
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

---
## Нотатки Щодо Міграції

Якщо ви оновлюєтесь зі старішої версії цієї інтеграції, перевірте таке:

- **Зламні зміни climate v1.7.1 -> v2.0.0**
  - Модель climate була розділена:
    - `type: ac` тепер створює поведінку climate для AC.
    - `type: floor_heating` тепер створює поведінку теплої підлоги.
    - Якщо `type` не вказано, значення за замовчуванням — `floor_heating`.
  - Нова типізація теплої підлоги:
    - Додано `floor_heating_device_type: dlp | module`.
    - Якщо задано `channel`, а `floor_heating_device_type` не вказано, тип автоматично стає `module`.
    - Для `floor_heating_device_type: module` обов'язковий `channel` (`1..6`), інакше сутність не буде створена.
  - Змінено поведінку режимів HVAC:
    - AC-сутності мають `COOL/OFF`.
    - Сутності теплої підлоги мають `HEAT/OFF` (`COOL` додатково доступний для `module`).
  - Необхідні дії:
    - Явно вкажіть `type` для кожної climate-сутності.
    - Додайте `floor_heating_device_type` і `channel` для модулів теплої підлоги.
    - Перевірте автоматизації/скрипти, які покладаються на стару семантику режимів climate.

---

#### Платформа Вентилятора

Щоб використовувати вентилятор Buspro, додайте в `configuration.yaml`:

```yaml
fan:
  - platform: buspro
    running_time: 3
    ack_retry_enabled: true
    devices:
      1.89.3:
        name: Вентилятор Спальні
        dimmable: true
      1.89.4:
        name: Вентилятор Ванної
        dimmable: false
```
+ **running_time** _(int) (Необов'язково)_: Стандартний час виконання в секундах.
+ **ack_retry_enabled** _(boolean) (Необов'язково)_: Одноразовий повтор без ACK через 0,8с.
+ **devices** _(Обов'язково)_: Список пристроїв у форматі `<subnet>.<device>.<channel>`.


---
## Послуги

#### Надсилання довільного повідомлення:
```
Domain: buspro
Service: send_message
Service Data: {"address": [1,74], "operate_code": [4,78], "payload": [1,100,0,3]}
```
#### Активація сцени:
```
Domain: buspro
Service: activate_scene
Service Data: {"address": [1,74], "scene_address": [3,5]}
```
#### Установка універсального перемикача:
```
Domain: buspro
Service: set_universal_switch
Service Data: {"address": [1,74], "switch_number": 100, "status": 1}
```
