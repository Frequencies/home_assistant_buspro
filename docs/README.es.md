# HDL Buspro para Home Assistant

[English](../README.md) | **Español**

La integración administra la pasarela y los dispositivos físicos HDL Buspro
desde la interfaz de Home Assistant. La lista completa de modelos, entidades y
servicios está en la [documentación en inglés](../README.md).

## Instalación

### HACS (recomendado)

1. Abra **HACS > Integraciones**.
2. Abra el menú de tres puntos y seleccione **Repositorios personalizados**.
3. Añada `https://github.com/Frequencies/home_assistant_buspro` con la categoría
   **Integración**.
4. Busque **HDL Buspro**, ábralo y seleccione **Descargar**.
5. Reinicie Home Assistant cuando HACS lo solicite.

Las versiones futuras se podrán instalar desde **HACS > Integraciones**.
Reinicie Home Assistant después de cada actualización de la integración.

### Instalación manual

1. Descargue el repositorio de la integración.
2. Copie su directorio `custom_components/buspro` en
   `/config/custom_components/buspro` de Home Assistant.
3. Reinicie Home Assistant.

## Primera configuración

1. Abra **Ajustes > Dispositivos y servicios > Añadir integración** y
   seleccione **HDL Buspro**.
2. Introduzca la dirección de la pasarela y los puertos UDP. El puerto habitual
   es `6000`.
3. Introduzca una dirección Buspro libre para Home Assistant con el formato
   `subred.dispositivo`. El valor predeterminado `200.200` no debe pertenecer a
   otro dispositivo Buspro.
4. Abra **Configurar > Añadir dispositivo**, seleccione el tipo y el modelo
   exacto e introduzca su dirección Buspro física y un nombre.
5. Asigne nombres a los canales o funciones necesarios. Un nombre vacío deja
   el canal deshabilitado e impide que se cree su entidad.

Los modelos conocidos usan la cantidad fija de canales o la lista de funciones
del catálogo. En los perfiles genéricos, el usuario indica una cantidad dentro
del límite admitido. Al guardar, se recarga la entrada de configuración y las
entidades se agrupan bajo un único dispositivo físico.

Para realizar cambios, abra **Configurar > Editar dispositivo**. En los
dispositivos administrados desde la interfaz puede cambiar el modelo, el nombre
y los canales, o eliminar el dispositivo. La configuración de protocolo de los
dispositivos YAML antiguos todavía debe modificarse en YAML; reinicie Home
Assistant después.

## Cambios incompatibles en 2.2.0

- Las direcciones, los nombres, la cantidad de dispositivos y las asignaciones
  de canales ya no están integrados en el componente. Se guardan en las
  opciones de la entrada de configuración.
- El modelo exacto determina la cantidad física de canales y las entidades que
  se crean.
- Un canal sin nombre queda deshabilitado y no se crea.
- La dirección Buspro de Home Assistant se migra a `200.200` de forma
  predeterminada. Debe estar libre en la red.
- Los eventos de panel ahora se decodifican como `channel_on`, `channel_off`,
  `channel_level`, `scene` y eventos de interruptor universal.
- El constructor `Buspro` integrado ahora requiere `client_address`.

## Actualización

1. Reinicie Home Assistant después de reemplazar el componente.
2. Abra **Ajustes > Dispositivos y servicios > HDL Buspro > Configurar**.
3. Compruebe la pasarela, los puertos UDP y una dirección Buspro libre para
   Home Assistant.
4. Seleccione el modelo exacto de cada dispositivo y revise los nombres de los
   canales.
5. Revise las automatizaciones que usan eventos de panel.
6. Elimine o comente las entidades YAML antiguas solo después de comprobar sus
   reemplazos administrados desde la interfaz.

No configure el mismo canal físico en YAML y en la interfaz al mismo tiempo:
se crearán entidades y suscripciones de protocolo duplicadas.

## Verificación de catálogo y pruebas

Para comprobar el catálogo de modelos frente a la lista oficial mantenida de HDL:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

En dispositivos YAML heredados, la integración ahora normaliza perfiles
faltantes usando metadatos del modelo. Los modelos desconocidos o perfiles
inválidos se registran como advertencia y hacen fallback a `sensor_status`.

Pruebas focalizadas de la integración:

```bash
python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -p 'test_*.py'
python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -p 'test_*.py'
```
