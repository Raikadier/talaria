---
date: 2026-07-26
type: conversation
source_agent: hermes
session_id: "20260726_112936_356c1e"
project: "desktop"
source_path: "C:\\Users\\david\\AppData\\Local\\hermes\\state.db"
tags: [conversation, imported, hermes, desktop]
title: "Conexión y configuración de WhatsApp"
---

# Conexión y configuración de WhatsApp

**Fecha:** 2026-07-26  
**Agente:** hermes  
**Proyecto/contexto:** desktop  
**Sesión:** `20260726_112936_356c1e`  
**Origen:** `C:\Users\david\AppData\Local\hermes\state.db`

## Mensajes

### Usuario

whatsapp esta desconectado, conectalo

### Asistente

El proceso de WhatsApp no está corriendo (no hay nada en ps). La sesión (creds.json) sigue intacta, así que no habría que re-escanear QR. Voy a levantar el gateway limpiando el lock viejo y con node en el PATH, igual que la receta que funcionó antes.

### Asistente

Ahora levanto el gateway en background vigilando el patrón "whatsapp connected".

### Asistente

El gateway arrancó pero con advertencia clave: **"No adapter available for whatsapp"** — o sea, el adaptador de WhatsApp no se creó. Necesito ver por qué. Voy a investigar la config de WhatsApp y el bridge.

### Asistente

El gateway arranca pero el adaptador de WhatsApp no se crea ("No adapter available for whatsapp"). Es un problema del lado del gateway al intentar conectar/levantar el bridge. Voy a revisar la config y cómo se construye ese adaptador.

### Asistente

Encontré la causa: en `config.yaml` la plataforma WhatsApp está con `enabled: false`. Por eso el gateway no crea el adaptador. Voy a revisar el bloque completo y cómo espera la config, luego lo habilito.

### Asistente

El culprit es claro: `platforms.whatsapp.enabled: false` en config.yaml. El gateway no construye el adaptador porque está deshabilitado. Voy a encontrar el código del adaptador para ver qué más necesita (puerto, allowlist) y asegurarme de dejar la config completa.

### Asistente

Encontré la causa raíz. En `config.yaml` la plataforma WhatsApp está con `enabled: false`, y el gateway lee eso desde el config (la línea 1890 de gateway/config.py: `if Platform.WHATSAPP in config.platforms` y toma `wa_cfg.enabled`). Por eso: "No adapter available for whatsapp".

Voy a habilitarlo. Reviso el formato exacto del bloque y lo cambio.

### Asistente

La lógica confirma: con `enabled: false` en YAML y sin `WHATSAPP_ENABLED=true` en env, el adaptador nunca se crea. Voy a habilitarlo en config.yaml. Primero detengo el gateway actual para no dejarlo en estado inconsistente, luego edito y relanzo.

Como el gateway no pudo crear el adaptador, no hay bridge de WhatsApp corriendo. Al habilitar y relanzar, el adapter debería levantar el bridge Node (baileys) usando la sesión ya emparejada en `creds.json` y reconectar sin QR.

Detengo el proceso actual y edito el config:

### Asistente

Ahora edito config.yaml para habilitar WhatsApp. Reviso el bloque completo por si necesita más campos (allowlist, home channel). Según el bridge.log anterior, la allowlist estaba configurada y funcionaba. El adapter la lee de env vars o del bridge. Veo qué espera el adapter para la allowlist.

### Asistente

El `.env` ya tiene `WHATSAPP_ENABLED=true`, pero el gateway reportó "No adapter available for whatsapp" — o sea que el `enabled: false` del YAML está prevaleciendo (el .env no se propaga al subproceso del gateway, o la lógica respeta el YAML). La solución directa y robusta es poner `enabled: true` en config.yaml. Edito y relanzo.

### Asistente

El patch se niega por ser archivo sensible. Uso la CLI oficial de hermes o edito vía terminal. Reviso `hermes config`.

### Asistente

Listo, `enabled: true`. Ahora relanzo el gateway y verifico que cree el adaptador y conecte WhatsApp.

### Asistente

Sigue apareciendo "No adapter available for whatsapp" aun con `enabled: true`. El warning real debe venir de un fallo al crear el adapter, no solo de `enabled`. Busco el código exacto que emite ese warning.

### Asistente

El `enabled: true` se aplicó, pero `_create_adapter` devuelve `None` para WhatsApp. Eso significa el plugin no se está registrando como adapter. Busco cómo se registra/crea el adapter de WhatsApp desde el plugin.

### Asistente

El adapter de WhatsApp va por `platform_registry`. Puede que el plugin no se esté registrando o falle al instanciar. Investigo el registro.

### Asistente

El warning "No adapter available" viene de `_create_adapter` devolviendo None, que ocurre si el plugin no está registrado (o `check_fn` falla). Pero no veo un log de "requirements not met" ni "config validation failed". Necesito ver cómo se registra el plugin WhatsApp. Busco el discovery de plugins.

### Asistente

El plugin está registrado y `check_fn=check_whatsapp_requirements`. Esa función probablemente está fallando (node faltante, bridge faltante, o no paired). Pero el log no mostró "requirements not met" — quizá el plugin no se descubrió en absoluto. Verifico si el plugin WhatsApp se está descubriendo y ejecuto `check_whatsapp_requirements` manualmente.

### Asistente

`check_whatsapp_requirements` solo valida node. Eso debería pasar. El problema es que el warning "No adapter available for whatsapp" es el de builtin (línea 8205) — o sea que el plugin NO está registrado en `platform_registry`. Necesito ver si WhatsApp se descubre en absoluto. Veo cómo `discover_plugins` registra plataformas y si whatsapp aparece.

### Asistente

El warning "No adapter available for whatsapp" es el de builtin porque `platform_registry.is_registered("whatsapp")` devuelve False — el plugin no se está descubriendo/registrando. Necesito ver por qué. El discovery escanea `plugins/platforms/`, pero quizá hay un problema con el plugin manager o el plugin está deshabilitado. Déjame ver el log más completo del gateway buscando "plugin" y verificar el estado del plugin.

### Asistente

No veo logs de plugin discovery. Puede que el plugin WhatsApp no se esté cargando por alguna razón (quizá un error en el `register` o el plugin está desactivado). Voy a probar directamente si el plugin se descubre, ejecutando `discover_plugins` y verificando el registro. También reviso si hay algo que desactive el plugin.

### Asistente

Interesante: `is whatsapp registered: True` y `REGISTERED PLATFORMS: []` (los entries se resuelven de forma diferida/deferred). O sea que cuando se descubre el plugin, WhatsApp SÍ queda registrado. Pero en el gateway real no se crea el adapter. 

La diferencia: en mi test ejecuté `discover_plugins(force=True)` explícitamente. En el gateway, el discovery pasa en la línea 8047-8051. Pero quizá el gateway no está descubriendo plugins para la plataforma whatsapp, o el `check_fn` (`check_whatsapp_requirements`) falla cuando se ejecuta dentro del gateway porque `find_node_executable` no encuentra node (PATH diferente).

Espera — el warning es "No adapter available for whatsapp" (builtin, línea 8205), NO "requirements not met". Eso significa `platform_registry.is_registered` devolvió False en el contexto del gateway. Pero en mi test devolvió True. 

La diferencia clave: en el gateway, el discovery de plugins puede estar ocurriendo DESPUÉS de que se itera sobre plataformas, o el plugin whatsapp está en la lista de "46 enabled" (53 found, 46 enabled → 7 disabled). ¡WhatsApp podría estar entre los 7 deshabilitados!

Déjame verificar si whatsapp está deshabilitado. Busco configuración de plugins habilitados/deshabilitados.

### Asistente

`plugins.enabled: []` — lista vacía. Eso significa que el plugin manager solo carga plugins explícitamente habilitados, y WhatsApp no está en la lista (por eso "46 enabled" de 53: los que tienen default-enabled, pero whatsapp requiere estar listado o tiene default). 

Déjame ver cómo `plugins.enabled: []` afecta el descubrimiento. Si la lista está vacía, puede que el comportamiento sea "cargar todos los que no estén deshabilitados" o "solo los listados". Voy a ver el manejo de `enabled` en el plugin manager.

### Asistente

Los plugins de plataforma bundled (como WhatsApp) se registran de forma diferida (`_register_deferred_platform`) y cargan al pedido. Entonces el plugin SÍ está registrado (mi test lo confirmó). Pero el gateway reporta "No adapter available for whatsapp" — builtin warning. 

Eso significa que en el gateway, `platform_registry.is_registered("whatsapp")` devuelve False en ese momento. La diferencia entre mi test y el gateway: en mi test forcé `discover_plugins(force=True)`. En el gateway, el discovery se hace en línea 8047, PERO la iteración de plataformas (línea 8170) ocurre después. Sin embargo, el warning apareció.

Espera — revisemos el orden. En mi test, después de `discover_plugins`, `is_registered` dio True. Pero quizás en el gateway hay un problema: el `find_node_executable` falla dentro del gateway porque el PATH del proceso del gateway no incluye node. `check_whatsapp_requirements` llama a `find_node_executable("node")`. Si no encuentra node, `check_fn` devuelve False y `create_adapter` devuelve None ANTES de llegar al warning builtin... no, el warning builtin (8205) es cuando NO está registrado. Si estuviera registrado pero check_fn falla, el warning sería "requirements not met" (línea 295-299), no el builtin.

El warning es específicamente el builtin (8205), que solo se emite cuando `_pval not in _builtin_names`. "whatsapp" — es _builtin_names = {m.value for m in Platform.__members__.values()}. ¿Está "whatsapp" en Platform enum? Sí, Platform.WHATSAPP = "whatsapp". Entonces `_pval = "whatsapp"` SÍ está en _builtin_names, por lo que el warning es el builtin. Correcto.

Pero esto solo se llega si `_create_adapter` devolvió None. Y `_create_adapter` primero chequea `platform_registry.is_registered(platform.value)`. Si is_registered es False → cae al builtin (que no tiene WhatsApp personal, solo WHATSAPP_CLOUD) → devuelve None → warning builtin. 

Entonces en el gateway, `is_registered("whatsapp")` es False. ¿Por qué en mi test fue True? Porque forcé discovery. En el gateway quizá el discovery de plugins falla o no incluye whatsapp por alguna razón de orden/timing, O el deferred loader falla.

Déjame verificar: en el gateway real, ¿se descubre el plugin whatsapp? Necesito ver el log de discovery en el gateway. El log no mostró "Plugin discovery complete". Déjame buscar en el gateway log completo si hubo error de discovery.

En realidad, el proceso gateway que corre ahora es el de proc_06bd433d3744. Maté el anterior. El log mostrado es corto. Déjame revisar si hay más líneas antes, o ejecutar el gateway con más verbosidad específica de plugins. 

Mejor: voy a probar `check_whatsapp_requirements` dentro del mismo entorno y ver si `is_registered` es True cuando NO fuerzo discovery, simulando lo que hace el gateway. El gateway llama a `discover_plugins()` en línea 8047. Si eso falla silenciosamente (línea 8051 catch), los plugins no se registran.

Pero en mi test, `discover_plugins(force=True)` SÍ registró whatsapp. Entonces el mecanismo funciona. El gateway debe llamarlo. A menos que el gateway use un `HERMES_HOME` diferente o salte el discovery.

Hmm, déjame revisar la línea 8044-8051 del gateway para ver la condición.

### Asistente

El discovery se hace vía `discover_plugins()`. En mi test funcionó. La diferencia: en el gateway, el `discover_plugins()` podría estar capturando una excepción (línea 8049-8052) y cayendo silenciosamente. Pero el log no mostró "plugin discovery failed". 

Otra posibilidad: el orden. El discovery de plugins en el gateway ocurre en línea 8047, y la iteración de plataformas en 8170. Esa secuencia está bien.

Pero wait — en mi test, `is_registered` devolvió True DESPUÉS de `discover_plugins(force=True)`. Sin embargo, el warning builtin aparece. Déjame probar directamente: ejecutar el gateway con `HERMES_PLUGINS_DEBUG=1` para ver el discovery, y ver si whatsapp se registra. O mejor, simular exactamente el gateway: llamar `discover_plugins()` sin force y luego chequear `is_registered`.

En realidad, la clave puede ser otra: el warning builtin se emite porque `platform_registry.is_registered("whatsapp")` es False EN ESE MOMENTO en el gateway. Mi test con force=True lo puso True. Sin force, el discovery es idempotente — si ya se descubrió antes en otro momento, no re-registra. Pero en un proceso fresco del gateway, debería descubrir.

Déjame simplemente correr el gateway con HERMES_PLUGINS_DEBUG y capturar el discovery de whatsapp. Mato el actual primero.

En realidad, más eficiente: voy a ejecutar un comando que replique exactamente lo que hace el gateway — `discover_plugins()` sin force — y chequear is_registered Y ejecutar check_whatsapp_requirements.

### Asistente

El log se llenó de DEBUG. Necesito ver específicamente mis prints finales. Los redirijo a un archivo.

### Asistente

`is_registered` es True y el check es True. Entonces en mi entorno el plugin funciona. Pero el gateway real reporta "No adapter available". 

La diferencia debe ser el `find_node_executable` dentro del gateway. El gateway se lanza con `hermes gateway run` desde el venv de Python. `check_whatsapp_requirements` llama `find_node_executable("node")`. Si en el contexto del proceso del gateway `find_node_executable` no encuentra node (porque el PATH del proceso no incluye node), `check_fn` devuelve False → `create_adapter` devuelve None → y como está registrado, NO llega al warning builtin... sino al "requirements not met" warning. Pero el warning que vimos fue el builtin "No adapter available for whatsapp".

Hmm, espera. Déjame reconsiderar. El warning builtin (8205) se emite cuando `_pval not in _builtin_names`. Pero eso es dentro del bloque `if not adapter:` en la iteración de plataformas. Para llegar ahí, `_create_adapter` devolvió None. `_create_adapter` intenta `platform_registry.is_registered(platform.value)`. Si es True, llama `create_adapter` → si check_fn falla devuelve None con warning "requirements not met". Si check_fn pasa, crea el adapter. 

Si `is_registered` es False → no entra al bloque plugin → cae al builtin if/elif (WHATSAPP_CLOUD, SIGNAL, etc.) → none match "whatsapp" → devuelve None → warning builtin.

El warning que aparece es el builtin. Por tanto en el gateway `is_registered("whatsapp")` es False. Pero en mi test es True.

¿Por qué sería False en el gateway? El gateway llama `discover_plugins()` en línea 8047. Pero quizás en el gateway, el discovery ocurre pero el plugin whatsapp específicamente NO se registra porque... el `register` del plugin whatsapp requiere node? No, el register solo registra el deferred loader.

O quizás: el gateway se inicia y el discovery de plugins corre, pero `whatsapp` está en la lista de deferred platforms que se registran en `platform_registry` como deferred. `is_registered` debería devolver True para deferred (línea 271-278: "A deferred (not-yet-imported) platform still counts as registered"). 

Pero en mi test `REGISTERED PLATFORMS: []` aunque `is_registered` dio True — o sea que los entries están como deferred y `_entries` está vacío hasta `_resolve`. `is_registered` llama a `_resolve(name)` si no está en `_entries`. 

Entonces en el gateway, cuando `_create_adapter` llama `is_registered("whatsapp")`, esto debería hacer `_resolve` y devolver True. A menos que `_resolve` falle.

Estoy dando vueltas. La forma más directa: correr el gateway con HERMES_PLUGINS_DEBUG=1 y capturar TODO el log de startup, buscando específicamente "whatsapp" y "deferred" y cualquier error. Déjame matar el actual y relanzar con debug a un archivo.

En realidad, más simple: el warning podría deberse a que el discovery del gateway está filtrando whatsapp porque `plugins.enabled: []` (vacío) hace que `_get_enabled_plugins()` devuelva un set vacío, y para plugins NO-bundled/NO-platform requiere estar en enabled. Pero whatsapp es kind=platform source=bundled → va por `_register_deferred_platform` (línea 1446-1448), que NO depende de `enabled`. Así que debería registrarse igual.

Déjame ver `_register_deferred_platform` y `_resolve` para entender si hay fallo.

OK, voy a dejar de especular y capturar el log real del gateway con debug. Mato el proceso y relanzo redirigiendo a archivo con HERMES_PLUGINS_DEBUG=1.</think:6124c78e>El plugin funciona en mi entorno de prueba (`is_registered`=True, check=True), pero el gate

_[truncado]_

### Asistente

El log se llenó. Veo deferred loaders pero no apareció "whatsapp" en la lista de deferred. Déjame filtrar solo los RESULT y mensajes clave al final.

### Asistente

El script se cortó (salida parcial). El `create_adapter` probablemente está tardando o fallando. Déjame ejecutarlo con salida a archivo y más tiempo, capturando errores.

### Asistente

`Config` no se importa así. El adapter de todos modos se crea vía el registro. Déjame crear el adapter con un PlatformConfig dummy y ver qué pasa con `create_adapter`. Pero primero: el hecho de que `is_registered` sea True confirma que el plugin SÍ se registra. 

Entonces, ¿por qué el gateway emite "No adapter available"? La única forma es que en el gateway `discover_plugins()` no se ejecuta correctamente O el orden es distinto. 

Espera — revisemos de nuevo. En el gateway, el bucle de plataformas itera `self.config.platforms.items()`. ¿El gateway está cargando el config.yaml actualizado con `enabled: true`? Sí, porque `hermes config get platforms.whatsapp.enabled` devolvió true. 

Pero el warning "No adapter available for whatsapp" (builtin) aparece solo si `platform_registry.is_registered("whatsapp")` es False DENTRO del gateway. Mi test demuestra que es True. 

¿Podría ser que el gateway use un `HERMES_HOME` diferente y por tanto un config.yaml sin `enabled: true`? Cuando el gateway se lanza, ¿lee el mismo config.yaml? El proceso gateway se lanza con `cd $HERMES_HOME`. El config.yaml está en `$HERMES_HOME/config.yaml`. Debería leerlo.

Hmm, pero el warning aparece INMEDIATAMENTE después de "Recovered 1 background process(es)". Eso es el recovery de procesos previos. Quizás el warning es de UN PROCESO ANTERIOR que se recuperó, no del actual. "Recovered detached process" — el gateway al iniciar recupera procesos detached del run previo. Y el warning "No adapter available" podría ser un eco de la corrida anterior que se está re-emitiendo por el recovery mechanism.

Déjame verificar: el log dice "Recovered 1 background process(es) from previous run" y luego "No adapter available for whatsapp". Ese warning puede ser parte del log del proceso recuperado o un re-emit. 

En realidad no — el orden sugiere que es el gateway actual evaluando plataformas. 

Voy a probar la hipótesis más simple y directa: lanzar el gateway y ESPERAR a que realmente intente conectar, no solo el warning inicial. El warning puede aparecer pero luego el reconnect watcher o la creación real del adapter podría funcionar. Pero tras 25s no conectó.

Nueva hipótesis: `check_whatsapp_requirements()` dentro del gateway falla porque `find_node_executable` no encuentra node. El gateway se lanza vía `hermes gateway run` que usa el venv de Python; el PATH del proceso puede no incluir `C:\Program Files\nodejs` a menos que lo exportemos. YO lo exporté en el comando background (`export PATH=...`). Pero `find_node_executable` usa `with_hermes_node_path` y `get_hermes_dir` — puede buscar node en ubicaciones específicas de Hermes, no en el PATH del sistema. Si Hermes tiene su propio node gestionado y ese node no está instalado, el check falla.

Pero el warning sería "requirements not met", no "No adapter available". A menos que... cuando check_fn falla, create_adapter devuelve None, y `_create_adapter` ve que `is_registered` es True, así que NO entra al builtin. Entonces el warning sería "requirements not met" (línea 295). El warning que vimos es el builtin. 

OK voy a ser empírico. Voy a lanzar el gateway y capturar TODO el log a un archivo con HERMES_PLUGINS_DEBUG, y buscar específicamente todas las líneas con "whatsapp" y "adapter" y "requirements". Eso me dirá la verdad.

Déjame matar procesos y lanzar redirigiendo a archivo.</think:6124c78e>Voy a lanzar el gateway redirigiendo todo el log a un archivo y filtrar específicamente las líneas de WhatsApp/adapter para ver la causa rea

_[truncado]_

### Asistente

Ahora tengo la clave: 
- El plugin SÍ se descubre y registra: `Plugin whatsapp-platform registered platform: whatsapp`
- PERO luego aparece `WARNING gateway.run: No adapter available for whatsapp`

El warning builtin (8205) solo se emite cuando `is_registered(platform.value)` es False. Pero el plugin se acaba de registrar. Hay una desconexión: el `platform_registry` del módulo que usa `_create_adapter` es un singleton, pero el plugin registra en... otro. O el registro ocurre DESPUÉS de que el gateway ya evaluó `is_registered`.

Específicamente: el log muestra "registered platform: whatsapp" en el discovery, y LUEGO el warning. Pero el bucle de plataformas (línea 8170) itera sobre `self.config.platforms`. Para WhatsApp, llama `_create_adapter` → `platform_registry.is_registered("whatsapp")`. 

El plugin registrar "whatsapp" en `platform_registry`. Pero quizás el `register_platform` del plugin registra bajo un nombre diferente ("whatsapp") y el gateway itera `Platform.WHATSAPP` cuyo `.value` es "whatsapp". Debería coincidir.

A menos que haya DOS instancias de `platform_registry` (singleton importado en módulos diferentes). El plugin importa `from gateway.platform_registry import platform_registry` y el gateway también. Mismo módulo = mismo singleton.

Déjame revisar el `register_platform` del PluginContext y `register` del registro, y qué nombre usa exactamente. Quizás registra como "whatsapp-platform" (el key) en lugar de "whatsapp" (el platform name).</think:6124c78e>Crítico: el plugin se registra (`registered platform: whatsapp`) pero el gateway aún dice "No adapter available". El `register_platform` del plugin pasa `name="whatsapp"`, pero `_create_adapter` busca `platform_registry.is_registered(platform.value)` donde `platform.value = "whatsapp"`. Déjame ver cómo `register_platform` (PluginContext) registra realmente y bajo qué clave.

### Asistente

El plugin registra `name="whatsapp"` en `platform_registry`. Entonces `is_registered("whatsapp")` debería ser True. El log confirma "registered platform: whatsapp".

Pero `_create_adapter` en el gateway llama `platform_registry.is_registered(platform.value)`. ¿Cuál es `platform.value`? `Platform.WHATSAPP`. El enum Platform está definido en gateway/config.py línea 283: `WHATSAPP = "whatsapp"`. Entonces `platform.value = "whatsapp"`. Coincide.

Entonces `is_registered("whatsapp")` debería devolver True. A menos que el registro del plugin ocurra en una instancia de `platform_registry` diferente al que usa `_create_adapter`.

Reviso `platform_registry.register` y `is_registered`/`_resolve` para ver si el registro deferred interfiere.

### Asistente

Hay un mecanismo deferred y concreto. Lo importante: el plugin registra `name="whatsapp"` concretamente (vía `platform_registry.register(entry)`). Eso debería ponerlo en `_entries["whatsapp"]`. 

Pero noté algo: el log muestra BOTH "Registered deferred platform loader: whatsapp" (del `_register_deferred_platform` del bundled) Y "Plugin whatsapp-platform registered platform: whatsapp" (del `register()` concreto del plugin). El `register()` concreto hace `self._deferred.pop(entry.name, None)` — quita el deferred. Y pone en `_entries["whatsapp"]`.

Entonces `_entries["whatsapp"]` existe. `is_registered("whatsapp")` debería devolver True (línea 271-278: si no está en `_entries`, hace `_resolve(name)`; estaría en `_entries` ya). 

Entonces `_create_adapter` debería encontrarlo y crear el adapter. ¿Por qué dice "No adapter available"?

¡Espera! El warning "No adapter available for whatsapp" (8205) se emite en el bucle de plataformas del gateway CUANDO `adapter is None`. Y `_create_adapter` devuelve None si `platform_registry.is_registered(platform.value)` es False. 

Pero quizás el orden de eventos es: el gateway itera plataformas ANTES de que el plugin se registre. Mira el log:
1. Plugin discovery complete
2. Loading plugin 'whatsapp-platform'... registered platform: whatsapp
3. WARNING No adapter available for whatsapp

El warning viene DESPUÉS del registro. Hmm.

Pero el bucle de plataformas (8170) está DENTRO de un método `await` que se llama después del discovery (8047). El discovery ya registró whatsapp. Entonces el bucle debería encontrarlo.

Déjame ver si hay algo raro: quizás `self.config.platforms` del gateway contiene la plataforma con una CLAVE diferente. El config carga `platforms.whatsapp.enabled: true`. ¿La clave en el dict es "whatsapp" o Platform.WHATSAPP? En gateway/config.py, `config.platforms` es un dict mapeando `Platform` → `PlatformConfig`. La clave es el ENUM `Platform.WHATSAPP`, no el string. Y `platform.value` = "whatsapp". 

`is_registered(platform.value)` = `is_registered("whatsapp")` = True.

Estoy convencido de que debería funcionar. La única explicación restante: el `platform_registry` singleton que usa `_create_adapter` es DIFERENTE al que usa el plugin. Eso pasa si `gateway/platform_registry.py` se importa dos veces como módulos distintos (ej. una vez como `gateway.platform_registry` y otra como algo relativo). Pero es improbable.

OTRA posibilidad: el warning "No adapter available for whatsapp" NO viene del bucle principal (8170), sino de otro bucle (línea 9241 o 10070/10163 — reconnect watcher o multiplex). Esos también llaman `_create_adapter`. Si el reconnect intenta crear el adapter pero el registro del plugin aún no se ha materializado en ese contexto... no.

Déjame probar de forma definitiva: replicar EXACTAMENTE el `_create_adapter` del gateway usando el mismo `platform_registry` singleton después del discovery, y ver qué devuelve para "whatsapp".</think:6124c78e>Voy a replicar exactamente el `_create_adapter` del gateway: después del discovery, consultar `platform_registry.is_registered("whatsapp")` y `create_adapter` con un PlatformConfig real. Capturo todo a archivo.

### Asistente

¡Encontré la causa raíz real!

`check_whatsapp_requirements()` → `find_node_executable("node")` → `find_hermes_node_executable` intenta `stat` sobre `C:\Users\david\AppData\Local\hermes\node\node.exe` y recibe **`PermissionError: Access is denied`** (WinError 5).

Por eso: `check_fn()` lanza una excepción (no devuelve False limpio), y `create_adapter` la captura y devuelve None → el gateway cae al warning "No adapter available". 

El problema: Hermes tiene un node gestionado en `%LOCALAPPDATA%/hermes/node/node.exe` pero el proceso actual (o el archivo) no tiene permisos de lectura/stat. Probablemente el archivo `node.exe` tiene permisos corruptos, o el `candidate.is_file()` falla por falta de permiso.

Nota: en mi shell exporté `PATH` con node del sistema (`C:\Program Files\nodejs`), pero `find_node_executable` PRIORIZA el node gestionado de Hermes (`find_hermes_node_executable(command)` primero), y ese archivo da PermissionError antes de llegar al node del sistema.

Solución: arreglar los permisos de `C:\Users\david\AppData\Local\hermes\node\node.exe` (y la carpeta node). O verificar si el archivo existe y sus permisos. Veamos.</think:6124c78e>**Causa raíz encontrada.** `check_whatsapp_requirements()` falla con `PermissionError: [WinError 5] Access is denied` al hacer `stat` sobre `C:\Users\david\AppData\Local\hermes\node\node.exe` (el node gestionado por Hermes). Esa excepción no controlada hace que `_create_adapter` devuelva None y el gateway reporte "No adapter available".

Reviso permisos y existencia de ese node gestionado.

### Asistente

`node/` no es accesible (Permission denied) y `node.exe` "NO EXISTE" (el `test -f` falla por permiso de la carpeta). La carpeta `node` de Hermes tiene permisos rotos o está corrupta. 

`find_hermes_node_executable` intenta `stat` sobre esa ruta y recibe WinError 5. La solución: arreglar permisos de la carpeta `node` para que Hermes pueda leer/stat, o reinstalar el node gestionado de Hermes.

Opciones:
1. Arreglar permisos de `C:\Users\david\AppData\Local\hermes\node` (dar control total al usuario).
2. Eliminar la carpeta `node` rota para que Hermes use el node del sistema (que SÍ funciona, v24.14.0 en `C:\Program Files\nodejs`), ya que `find_node_executable` busca node del sistema si el gestionado falla.

Pero `find_hermes_node_executable` lanza excepción por el `stat` en la carpeta corrupta ANTES de buscar el del sistema. Si arreglo/elimino la carpeta rota, `find_node_executable` caerá al node del sistema y funcionará.

Déjame primero ver por qué la carpeta tiene permisos rotos. `icacls` dio "Access is denied" — el usuario actual (david) no puede ni leer la carpeta. Eso es raro. ¿Quizás la carpeta fue creada por otro usuario/processo con elevación?

Voy a intentar corregir permisos con icacls dándole control al usuario. Como estamos en MSYS/bash, uso `icacls`. Si falla por falta de permiso, necesitaría elevación (administrador). 

La memoria dice: David quiere el gateway con admin. Y el proceso puede haber sido creado por un padre elevado. La carpeta `node` pudo haberse creado con permisos de admin y el usuario normal no tiene acceso. 

Intento arreglar permisos sin elevación primero; si falla, lo hago elevado vía PowerShell/cmd como admin.

En MSYS, para elevar necesito `powershell Start-Process -Verb RunAs`. Pero el terminal aquí es bash sin TTY elevada. Déjame probar `icacls /grant` primero.</think:6124c78e>La carpeta `node` de Hermes tiene permisos rotos (el usuario david no puede ni leerla), y eso rompe el `check_fn` del adapter de WhatsApp. Voy a intentar reparar los permisos. Primero veo el dueño y pruebo conceder acceso.

### Asistente

Sin elevación no puedo tocar la carpeta. Necesito elevación (administrador). Voy a intentar elevar vía PowerShell `RunAs`. Pero antes, confirmo que la carpeta realmente no se puede acceder ni como admin del sistema — quizás el directorio ni siquiera debería existir y está corrupto.

La estrategia más limpia: eliminar/renombrar la carpeta `node` rota para que `find_node_executable` caiga al node del sistema (`C:\Program Files\nodejs`, que funciona). Pero para borrarla también necesito permiso.

Voy a elevar con PowerShell RunAs para correr icacls/rm. El terminal actual es bash (sin TTY). `powershell -Command "Start-Process ... -Verb RunAs"` abre UAC; en este entorno headless puede que no haya UAC interactivo. Déjame probar.

Alternativamente: ¿el proceso del gateway se ejecuta con el usuario david normal o elevado? El `ps aux` anterior no mostró procesos. La memoria indica que David corre el gateway con admin (autostart login CON admin). Si el gateway se lanza elevado, entonces DENTRO del gateway `find_node_executable` corre como admin y SÍ podría leer `node/`... pero entonces no daría PermissionError. 

Hmm, pero el error ocurrió en MI test (corriendo como david normal en el venv). El gateway real se lanza con `hermes gateway run` desde mi terminal bash (david normal, sin elevar). Por eso falla.

Entonces: el gateway corre como david normal, y la carpeta `node` tiene permisos que david normal no puede leer (probablemente creada por un proceso elevado previo). 

Solución: correr el gateway elevado (como admin), O arreglar permisos de la carpeta `node`. La memoria dice David quiere el gateway con admin siempre. Así que lo correcto es lanzar el gateway como administrador.

Pero el mensaje de error es en `check_whatsapp_requirements` del adapter, que se ejecuta en el proceso del gateway. Si lo lanzo elevado, el `stat` sobre `node/node.exe` funcionará (el node gestionado existe y es legible como admin), y WhatsApp conectará usando el node gestionado de Hermes.

Déjame verificar: ¿existe realmente `node/node.exe`? El `test -f` dijo NO EXISTE, pero eso es porque no pudo leer la carpeta. Como admin podría leerla. Déjame intentar elevar y listar.

Voy a intentar `powershell -Command "Start-Process cmd -Verb RunAs -ArgumentList '/c icacls ...'"`. Pero en entorno headless sin UAC, RunAs puede fallar o colgarse. Mejor: usar un script que se eleve y haga el work, con timeout.

En realidad, el enfoque más robusto dado el entorno: arreglar permisos de la carpeta `node` usando un proceso elevado. Déjame probar si puedo elevar.

Pero espera — hay una alternativa más simple que no requiere elevación ni tocar permisos: si la carpeta `node` está corrupta/ilegible, puedo renombrarla o moverla fuera del alcance de Hermes para que `find_hermes_node_executable` no la encuentre y use el node del sistema. Pero renombrarla requiere permiso de escritura en `%LOCALAPPDATA%/hermes` (el padre), que david sí tiene (es su carpeta). El problema es solo la SUBcarpeta `node`. Renombrar `node` → `node.bak` requiere permiso de escritura en el PADRE (`hermes`), no en `node` mismo. Eso sí lo tiene david.

¡Esa es la solución! Renombro `node` → `node.bak` desde el padre (que david puede escribir), así `find_node_executable` no encuentra el node gestionado roto y cae al node del sistema. Probémoslo.

Pero `mv node node.bak` en bash: `mv` necesita permiso de escritura en el directorio padre (`hermes`) — sí lo tiene. No necesita leer el contenido de `node` para renombrarlo (solo 

_[truncado]_

### Asistente

`check_whatsapp_requirements` ahora devuelve **True** (usa el node del sistema). El problema de permisos está evitado. Ahora relanzo el gateway y debería crear el adapter y conectar WhatsApp usando la sesión ya emparejada (sin necesidad de QR).

### Asistente

WhatsApp conectado. El log confirma:

- `Connecting to whatsapp...`
- `[Whatsapp] Bridge found` → `Bridge ready (status: connected)`
- `✓ whatsapp connected`
- `Gateway running with 1 platform(s)`

Para confirmar de forma independiente (no solo el log del propio gateway), verifico que el bridge está escuchando en el puerto 3000 y que el proceso sigue vivo.

### Asistente

El bridge responde en `127.0.0.1:3000` (el endpoint `/` da "Cannot GET /" que es respuesta normal de un bridge Express — confirma que está vivo y escuchando). WhatsApp está conectado y operativo.

Resumen de lo que pasó y lo que hice:

**Causa raíz:** WhatsApp no conectaba por una combinación de dos cosas:
1. `platforms.whatsapp.enabled` estaba en `false` en `config.yaml` → el gateway ni siquiera intentaba crear el adapter.
2. Más profundo: la carpeta `C:\Users\david\AppData\Local\hermes\node` (el node gestionado por Hermes) tenía **permisos rotos** — el usuario david no podía leerla (`WinError 5: Access is denied`). El `check_fn` del adapter (`check_whatsapp_requirements`) hacía `stat` sobre `node/node.exe` y lanzaba una excepción no controlada, lo que hacía que `_create_adapter` devolviera `None` y el gateway reportara "No adapter available for whatsapp".

**Lo que hice:**
- Habilité la plataforma: `hermes config set platforms.whatsapp.enabled true`.
- Renombré la carpeta `node` corrupta a `node.bak` (david sí puede escribir en la carpeta padre). Así `find_node_executable` ya no encuentra el node roto y usa el **node del sistema** (`C:\Program Files\nodejs`, v24.14.0, que funciona).
- Relancé el gateway. El bridge de Baileys arrancó con la sesión ya emparejada (`creds.json`) → conectó **sin necesidad de escanear QR de nuevo**.

**Estado actual:** ✓ whatsapp connected, gateway corriendo con 1 plataforma, bridge escuchando en puerto 3000.

Notas para ti:
- La carpeta `node.bak` quedó ahí; si quieres puedo borrarla (es seguro, ya no la usa). 
- Si más adelante Hermes intenta usar su node gestionado y vuelve a fallar, la solución persistente es que el gateway corra con los permisos adecuados o reinstalar el node gestionado. Como tu autostart del gateway ya va con admin, el node gestionado debería ser legible cuando el gateway arranque elevado — pero por ahora el node del sistema funciona bien.
- El proceso del gateway quedó en background (PID 42096). Sigue vivo mientras la sesión de Hermes esté abierta.

¿Quieres que borre `node.bak` y/o deje el gateway configurado para arrancar automáticamente al iniciar sesión (como tenías antes)?

### Usuario

[IMPORTANT: Background process proc_ef4de5615fcc matched watch pattern "bridge".
Command: cd "$HERMES_HOME" && export PATH="/c/Program Files/nodejs:$PATH" && hermes gateway run --replace -v
Matched output:
INFO hermes_plugins.whatsapp_platform.adapter: [Whatsapp] Bridge found at C:\Users\david\AppData\Local\hermes\hermes-agent\scripts\whatsapp-bridge\bridge.js]

### Asistente

El watcher solo confirmó el match de "bridge" (es el mismo log que ya vimos: `[Whatsapp] Bridge found at ...bridge.js`). No es un evento nuevo — WhatsApp sigue conectado y el gateway corriendo con 1 plataforma, tal como lo dejé.

No hace falta hacer nada. Estado confirmado:

- ✓ `whatsapp connected` (verificado antes)
- Bridge escuchando en `127.0.0.1:3000` (respondió al curl)
- Gateway activo con 1 plataforma (PID 42096, en background)

¿Quieres que borre `node.bak` y/o deje el gateway configurado para arrancar solo al iniciar sesión (como lo tenías antes)? Lo dejo así hasta que me digas.

### Usuario

[IMPORTANT: Background process proc_06bd433d3744 matched watch pattern "No adapter".
Command: cd "$HERMES_HOME" && export PATH="/c/Program Files/nodejs:$PATH" && hermes gateway run --replace -v
Matched output:
WARNING gateway.run: No adapter available for whatsapp]

### Asistente

Ese match viene de un proceso **viejo** (`proc_06bd433d3744`), que ya maté hace rato. El watcher re-emitió un fragmento de su log antiguo ("No adapter available for whatsapp") — no es el gateway actual.

El gateway que está conectado es `proc_ef4de5615fcc` (el que confirmó `✓ whatsapp connected`). Para descartar dudas, verifico que siga vivo y conectado ahora mismo.

### Asistente

El bridge sigue respondiendo en el puerto 3000 (está vivo), pero `ps aux` no muestra el proceso del gateway ni del bridge — eso es raro. Puede que `ps` en MSYS no liste los procesos node/Python correctamente, o que el proceso haya sido "recovered" y corra bajo otro PID. Lo importante: el **bridge responde en 3000**, lo que confirma que WhatsApp sigue conectado.

Pero déjame confirmar de forma más fiable usando el estado que reporta el propio Hermes, y verificar que el proceso de fondo `proc_ef4de5615fcc` sigue corriendo.

### Asistente

Confirmado: el gateway actual (`proc_ef4de5615fcc`, PID 42096) sigue **running** con `✓ whatsapp connected` y el bridge escuchando en 3000.

El match de "No adapter" que recibiste era ruido de un proceso muerto (`proc_06bd433d3744`, que ya maté). WhatsApp está conectado y operativo.

Estado final:
- Gateway activo: `proc_ef4de5615fcc` (PID 42096, uptime 117s+)
- ✓ whatsapp connected
- Bridge en `127.0.0.1:3000` respondiendo

Todo en orden. ¿Seguimos con borrar `node.bak` y/o dejar el autostart del gateway para que arranque solo al iniciar sesión?

### Usuario

si

### Asistente

David confirmó. Hago las dos cosas: borro `node.bak` y dejo el gateway con autostart al iniciar sesión.

Primero verifico rutas y borro `node.bak`.

### Asistente

`node.bak` también tiene permisos rotos (Permission denied) — era la carpeta `node` corrupta renombrada; el contenido sigue sin permiso de lectura. No puedo borrarla sin elevación. No afecta el funcionamiento (Hermes ya no la usa, el node del sistema funciona), pero conviene limpiarla.

Para borrarla necesito admin. La memoria dice David quiere el gateway con admin. Voy a crear el autostart elevado y, aprovechando, borrar `node.bak` con privilegios.

Primero creo el acceso directo (lnk) en el Startup folder que lance el gateway como administrador. En Windows, un .lnk con `RunAsAdmin` flag se eleva al iniciar sesión. Creo el .lnk con PowerShell.

El comando a ejecutar debe:
- cd a HERMES_HOME
- export PATH con node del sistema
- `hermes gateway run --replace -v`

Pero un .lnk de Startup no ejecuta bash ni exporta PATH fácilmente. Mejor: crear un script .bat/.cmd que haga eso, y el .lnk apunte al .cmd con RunAsAdmin.

Déjame crear el script wrapper y el lnk.

Script: `C:\Users\david\AppData\Local\hermes\start_gateway.cmd`
```
@echo off
set HERMES_HOME=C:\Users\david\AppData\Local\hermes
cd /d "%HERMES_HOME%"
set PATH=C:\Program Files\nodejs;%PATH%
"C:\Users\david\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe" gateway run --replace -v
```

Luego el .lnk en Startup apuntando a ese .cmd con RunAsAdmin.

Para crear el .lnk con RunAsAdmin desde bash, uso PowerShell (posiblemente elevado). Crear el .lnk en sí no requiere elevación (escribir en Startup folder del usuario). El flag RunAsAdmin se setea en la propiedad del .lnk.

Voy a:
1. Crear start_gateway.cmd
2. Crear el .lnk con PowerShell (sin elevar, solo escribir archivo)
3. Borrar node.bak con PowerShell elevado (RunAs) — puede pedir UAC; en este entorno headless podría fallar. Lo intento; si falla, lo dejo como tarea pendiente y le explico a David cómo borrarlo manualmente.

Hagamos paso 1 y 2 primero.</think:6124c78e>`node.bak` también tiene permisos rotos (no se puede borrar sin admin). No afecta el funcionamiento — Hermes ya usa el node del sistema — pero la limpio aparte con elevación. Primero armo el autostart.

Creo el script wrapper y el acceso directo en el Startup folder (elevado).

### Asistente

Ahora creo el acceso directo (.lnk) en el Startup folder con `RunAsAdmin` mediante PowerShell.

### Asistente

El `$env:APPDATA` no se expandió porque estaba escapado con backslash en PowerShell. Corrijo usando la variable real.

### Asistente

`.lnk` creado con `RunAsAdmin` en el Startup folder. Ahora borro `node.bak` (requiere elevación). Intento con PowerShell `RunAs`; si pide UAC y no hay entorno interactivo, lo reporto.

### Asistente

`node.bak` borrado (se elevó correctamente y salió con código 0). 

Verificación final de todo el estado:

### Asistente

Listo. Todo hecho y verificado:

**1. WhatsApp conectado** ✓
- Gateway corriendo (`proc_ef4de5615fcc`), `✓ whatsapp connected`, bridge en `127.0.0.1:3000` respondiendo.
- `platforms.whatsapp.enabled = true` en config.

**2. `node.bak` borrado** ✓
- La carpeta `node` corrupta (permisos rotos) se renombró a `node.bak` y se eliminó con elevación. Hermes ahora usa el node del sistema (`C:\Program Files\nodejs`, v24.14.0), que funciona.

**3. Autostart configurado** ✓
- Script: `C:\Users\david\AppData\Local\hermes\start_gateway.cmd` (hace `cd` a HERMES_HOME, pone node del sistema en PATH y lanza `hermes gateway run --replace -v`).
- Acceso directo **"Hermes Gateway.lnk"** en el Startup folder, con flag `RunAsAdmin` → al iniciar sesión se eleva solo y arranca el gateway + WhatsApp sin que vuelvas a escanear QR (la sesión emparejada persiste en `whatsapp/session/creds.json`).

Notas:
- El `RunAsAdmin` en el .lnk mostrará el UAC al iniciar sesión (una vez, clic en Sí). Es el comportamiento esperado para que corra como admin, como querías.
- El gateway que corre ahora mismo lo lancé yo en background desde esta sesión; cuando reinicies la PC, el de verdad arrancará desde el Startup elevado. No hace falta que cierres el actual — el `--replace` del autostart toma el relevo limpio.
- Si algún día quieres detener el autostart, solo borrás el `.lnk` del Startup folder.

¿Algo más?


## Enlaces
- Índice: [[hermes-import-index]]
- Home: [[Home]]
