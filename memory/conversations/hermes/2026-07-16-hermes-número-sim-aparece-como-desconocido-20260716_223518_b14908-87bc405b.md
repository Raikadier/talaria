---
date: 2026-07-16
type: conversation
source_agent: hermes
session_id: "20260716_223518_b14908"
project: "desktop"
source_path: "C:\\Users\\david\\AppData\\Local\\hermes\\state.db"
tags: [conversation, imported, hermes, desktop]
title: "Número SIM aparece como desconocido"
---

# Número SIM aparece como desconocido

**Fecha:** 2026-07-16  
**Agente:** hermes  
**Proyecto/contexto:** desktop  
**Sesión:** `20260716_223518_b14908`  
**Origen:** `C:\Users\david\AppData\Local\hermes\state.db`

## Mensajes

### Usuario

tengo una sim tigo pero al entrar a ajustes, acerca del telefono, estado, red no aparece el numero de telefono de la sim sino que todo aparece como desconocido. que pasa?

### Asistente

Es normal y **no significa que tu SIM esté dañada**. Te explico qué pasa:

## Por qué aparece "Desconocido"

El número de teléfono que ves en *Ajustes → Acerca del teléfono → Estado → Red* (el campo "Mi número") lo lee el celular **directamente de la SIM**, de un registro interno que se llama **MSISDN**.

El problema es que **muchas operadoras (incluida Tigo) no escriben el número en la SIM** cuando la activan. El número está asignado a nivel de red (en los servidores de Tigo, la base HLR/HSS), no guardado en la tarjeta. Como la SIM está "vacía" en ese campo, Android muestra "Desconocido".

O sea: tu línea funciona perfecto para llamar, recibir y datos — solo que el sistema operativo no tiene de dónde leer el número para mostrarlo.

## Cómo confirmar tu número real

Cualquiera de estas opciones te lo da seguro:

1. **App Mi Tigo** (la oficial de Tigo Colombia) → ahí sale tu número y plan.
2. **Marcar a otro celular** desde el tuyo y mirar quién llama.
3. **USSD**: en Tigo Colombia prueba `*655#` o `*555#` (te envía un SMS con el número) — varía según el país, así que la app es lo más confiable.
4. **Llamar al *tigo desde otro teléfono** o al soporte 018000.

## ¿Se puede arreglar para que aparezca?

Sí, en algunos casos:

- En *Ajustes → Conexiones/Red móvil → Tarjetas SIM*, muchos Android permiten **editar el "nombre" o "número" de la SIM** manualmente. Si pones tu número ahí, algunos menús lo muestran (pero es solo una etiqueta local, no escribe nada en la SIM).
- El verdadero arreglo (que el número se lea solo) depende de que Tigo lo escriba en la SIM, lo cual ellos no suelen hacer y no es algo que configures tú.

**En resumen:** no te preocupes. Es un "vacío de datos en la SIM", no un fallo. Tu número sigue activo en la red de Tigo; solo úsalo desde la app Mi Tigo o marcando a otro teléfono para verlo.

¿Quieres que busque el código USSD exacto de Tigo para tu país, o cómo editar la etiqueta de la SIM en tu modelo de celular en particular?

### Usuario

parece que el telefono no reconoce la targeta sim

### Asistente

Ojo, eso ya es **distinto** al caso anterior. Si el teléfono *no reconoce* la SIM (no solo le falta el número), verás cosas como *"Sin tarjeta SIM"*, *"SIM no válida"*, *"Insertar SIM"*, barras de señal vacías o *"solo llamadas de emergencia"*. Ahí el problema es físico o de activación, no de lectura del MSISDN.

Vamos por descartes, de lo más simple a lo más serio:

## 1. Reinicia el teléfono
Suena obvio pero resuelve un montón de casos. Apaga, espera 30 seg y enciende.

## 2. Verifica el estado en *Ajustes → Conexiones → Tarjetas SIM*
- Si dice **"Sin tarjeta SIM" / "No detectada"** → el problema es físico (bandeja, contactos sucios, corte, SIM dañada, o el lector del celular).
- Si dice **"Sin servicio" / "Buscando"** pero reconoce la tarjeta → la línea misma puede estar suspendida, bloqueada o fuera de cobertura.

## 3. Revisa la bandeja físicamente
- Apaga el teléfono, saca la SIM y mírala a contraluz: ¿está rayada, quemada, o con los contactos dorados sucios/opacos?
- Límpiala con un trapo seco suave (nada de líquidos ni alcohol fuerte).
- Revisa que la bandeja esté bien asentada y la SIM quede firme (si usaste adaptador de tamaño, a veces queda floja).

## 4. Prueba la SIM en otro celular
Esto es **la prueba definitiva**:
- SIM en otro teléfono → reconoce y da señal = el problema es tu celular (lector o bandeja).
- SIM en otro teléfono → tampoco la reconoce = la SIM está dañada o la línea está bloqueada.

## 5. Prueba otra SIM en TU celular
- Otra SIM

### Usuario

[System: The previous response was cut off by a network error mid-stream. Continue exactly where you left off. Do not restart or repeat prior text. Finish the answer directly.]

### Asistente

- Otra SIM en tu celular → funciona = tu SIM es la fallida (debes pedir reposición en Tigo).
- Otra SIM en tu celular → tampoco se reconoce = el lector de SIM de tu teléfono está dañado (es hardware, lo arregla un técnico).

## 6. Revisa el bloqueo de la línea
Si la SIM parece físicamente bien pero da *"SIM no válida"* o *"bloqueada"*:
- Puede estar **PIN bloqueado** (te pide PUK). Si no tienes el PUK, Tigo lo da por soporte.
- La línea pudo ser **suspendida por falta de pago** o por seguridad. Llama al soporte de Tigo desde otro teléfono.

## 7. Restablece red (si la reconoce pero sin servicio)
*Ajustes → Conexiones → Restablecer → Restablecer configuración de red* (no borra fotos ni apps). Luego vuelve a elegir la SIM para datos.

---

**Resumen de la prueba cruzada:**

| Prueba | Resultado | Diagnóstico |
|---|---|---|
| Tu SIM en otro teléfono | reconocida | Tu celular falla |
| Tu SIM en otro teléfono | no reconocida | SIM/linea falla |
| Otra SIM en tu celular | reconocida | Tu SIM falla |
| Otra SIM en tu celular | no reconocida | Lector de tu celular dañado |

Lo más probable, si la SIM se ve entera y se asentó bien, es que o **está sucia/floja** o que la **línea está bloqueada/suspendida** en Tigo.

¿En qué mensaje exacto aparece ahora el teléfono (pantalla de estado / barra de señal)? Con eso te digo si es físico o de línea en 1 línea.

### Usuario

como puedo pedirle a tigo que la habilite si nose cual es el numero de la sim?

### Asistente

Buena noticia: **no necesitas saber el número para que Tigo te ayude**. La línea está atada a tu **cédula** y a un **serial de la SIM (ICCID)**, y con cualquiera de los dos te ubican todo.

## Lo que necesitas tener a la mano

1. **Tu cédula** (obligatoria) — con ella buscan todas las líneas a tu nombre.
2. **El serial de la SIM (ICCID)**: es el número largo que viene impreso en la tarjeta plástica (la base donde iba montada la SIM) o a veces en un costado de la misma SIM. Empieza por 89… y tiene ~19 dígitos. Si tienes la "camita" de plástico original, ahí está.

## Cómo pedir la habilitación (en orden de facilidad)

**A. Ir a un Centro de Experiencia Tigo (lo más seguro)**
Llevas la cédula y la SIM física. Te verifican por huella/datos y reactivan o reemplazan la SIM en el momento. Sin saber el número.

**B. Llamar al soporte desde OTRO teléfono**
- Desde fijo: **018000 910 500** (línea gratuita Tigo Colombia).
- Si tienes otro cel Tigo: **611** o **\*888**.
- Dices: *"No reconozco mi SIM y no sé el número, quiero verificar el estado de la línea asociada a mi cédula"*. Te piden cédula + datos de verificación (fecha de nacimiento, último recarga, etc.).

**C. App/Web Mi Tigo (si tienes otro acceso)**
Desde la web mitigo.com.co puedes iniciar sesión con tu cédula (no con el número) y ver tus líneas y su estado.

## Para que te dejen habilitarla, prepárate a confirmar que eres tú

Por seguridad (ley de portabilidad/biometría en Colombia) te van a pedir demostrar que la línea es tuya:
- Cédula al día.
- A veces: última recarga que hiciste, fecha de activación, o un código que envían a un correo que diste al registrar.
- Si la línea está **suspendida por falta de pago** (prepago vencido hace meses), pagas y reactiva; si está **dada de baja** por inactividad prolongada, normalmente te dan una SIM nueva con línea nueva.

## Un tip rápido para saber el número AHORA
Aunque el celular no reconozca la SIM, si en algún momento la reconoció, prueba meterla de nuevo y marcar **\*555#** o **\*655#** — Tigo envía SMS con el número. Si no la lee, no funcionará, pero vale el intento antes de ir a la tienda.

¿Tienes a mano la cédula y la tarjeta plástica de la SIM (para el ICCID)? Con eso yo te diría exactamente qué decirles por teléfono.

### Usuario

es decir que si una sim esta suspendida, el telefono no la reconoce?

### Asistente

No necesariamente. **Son dos cosas distintas y es clave no confundirlas**, porque el síntoma en pantalla es diferente:

## 1. El teléfono "no reconoce la SIM" = falla FÍSICA o de LECTURA
El celular no puede leer la tarjeta en absoluto. Ves: *"Sin tarjeta SIM"*, *"Insertar SIM"*, *"SIM no detectada"*, o barras de señal vacías con "solo emergencias". Aquí el teléfono y la SIM no "hablan" ni siquiera para preguntarle a la red. **Esto NO lo causa una suspensión de la línea.**

## 2. La línea está SUSPENDIDA (en la red de Tigo) = falla de RED
El teléfono **SÍ reconoce la SIM** (la lee perfecto, muestra señal, operador "Tigo"), pero la red **rechaza el servicio**: sin datos, sin poder llamar, a veces dice *"Sin servicio"*, *"Registro denegado"* o *"Solo llamadas de emergencia". La SIM funciona, pero la cuenta está bloqueada/suspendida.

**O sea:** si tu teléfono dice *"Sin tarjeta SIM"* / *"No reconocida"*, la suspensión de la línea NO es la causa — es físico (bandeja, contactos sucios, SIM dañada, o lector del celular). La suspensión solo pasa **después** de que la SIM ya fue reconocida.

## Cómo saber cuál es tu caso (míralo en pantalla)

| Lo que dice el teléfono | Significa |
|---|---|
| **"Sin tarjeta SIM" / "No detectada"** | Falla física/lectura (no es suspensión) |
| **"Tigo" + señal, pero "Sin servicio" / "Solo emergencias"** | SIM bien leída, línea suspendida/bloqueada en red |
| **"SIM no válida" / pide PUK** | SIM bloqueada por PIN/PUK (no es suspensión de pago) |

## Entonces, ¿cuál es tu situación?
Volviendo a tu caso original: tú dijiste que el número aparecía como **"Desconocido"** (y luego que el teléfono "no la reconoce"). Si realmente es *"Sin tarjeta SIM"*, **no es por suspensión** — es físico y la prueba cruzada (otra SIM en tu celular / tu SIM en otro celular) es lo que te lo confirma.

Si en cambio ves el nombre **"Tigo"** con señal pero sin poder usarla, ahí sí puede ser suspensión y Tigo la reactiva con tu cédula.

¿Qué mensaje exacto sale en la barra de estado o en *Ajustes → Tarjetas SIM*? Con eso te digo 100% a qué te enfrentas.

### Usuario

puedo sacar la sim sin apagar el telefono?

### Asistente

Sí **puedes**, pero **no es lo recomendado**. Te explico el riesgo real y cómo hacer

### Usuario

[System: The previous response was cut off by a network error mid-stream. Continue exactly where you left off. Do not restart or repeat prior text. Finish the answer directly.]

### Asistente

lo con menos riesgo posible.

## ¿Qué pasa si la sacas en caliente (sin apagar)?

- El celular detecta la extracción de golpe y **se reinicia la radio** (se pierde señal un momento y vuelve a registrar). En la mayoría de los teléfonos modernos **no daña nada**.
- El riesgo real es **mecánico/físico**, no eléctrico: si la bandeja está en una ranura tipo **tray con pin** que se saca con el clip, al forzarla con el teléfono encendido no pasa nada eléctrico, pero si la tarjeta se mueve mientras el lector está activo pueden aparecer avisos de *"SIM removida"*. Nada se quema.
- Lo que **SÍ** puede pasar: si la SIM ya estaba floja/mala, sacarla y meterla en caliente puede dejarte en *"Sin tarjeta SIM"* hasta que reinicies. Pero no es un daño permanente.

## Recomendación

**Apaga el teléfono** (2 segundos) antes de sacarla. Es lo correcto porque:
- Evitas que se corte a medias una lectura/escritura de la SIM (raro pero posible).
- El sistema desmonta limpio y al volver a encender relee todo desde cero, que es justo lo que quieres para diagnosticar si la reconoce.

Si necesitas hacerlo ya mismo sin apagar (ej. para probar la SIM en otro teléfono urgente):
1. Usa el clip/expulsor y saca la bandeja con cuidado, sin torcer.
2. Ponla en el otro teléfono (mejor apagado él también al insertar).
3. Al volver, inserta y **reinicia** tu celular para que relea bien.

## En resumen
Sacarla sin apagar **no quema la SIM ni el celular**; el riesgo es mínimo y sobre todo molestia de que se reinicie la señal. Para diagnosticar tu problema (¿reconoce o no la SIM?), lo ideal es **apagar, sacar, limpiar contactos, meter en otro teléfono y encender** — así la prueba es limpia.

¿Quieres que te diga cómo abrir la bandeja de tu modelo exacto de celular (marca y modelo) para no dañar el clip ni la bandeja?

### Usuario

que es el sms center number?

### Usuario

continua

### Usuario

continua

### Asistente

## ¿Qué es el SMS Center Number (SMSC)?

Es el **número del servidor de Tigo que recibe, enruta y entrega tus mensajes de texto (SMS)**. No es un número de teléfono "normal" al que llamas; es la **dirección del centro de mensajería** de la operadora.

Cuando envías un SMS, tu celular no lo manda directo al destinatario: lo manda al **SMSC de Tigo**, y ese servidor se encarga de guardarlo y entregarlo al teléfono de la otra persona (aunque ella esté apagada, el SMSC lo retiene y lo suelta cuando encienda).

## ¿Dónde se configura y cómo se ve?

- Normalmente **viene preconfigurado e invisible** en la SIM. No tienes que tocarlo.
- Formato típico en Colombia/Tigo: algo como **+573****0001** o **+573****0405** (empieza por +57 y luego el número del centro).
- Para verlo/editarlo: *Ajustes → Apps → Mensajes (o "Mensajería") → Ajustes de la app → Más ajustes/SMS → Centro de mensajes (SMSC)*. (La ruta varía por marca; en Samsung suele ser ahi.)

## ¿Por qué importa para tu problema?

Si tu número sale "Desconocido" o la SIM no se reconoce, **el SMSC no es la causa** — pero sí lo es si:
- **Recibes SMS pero no puedes ENVIARLOS** (se quedan en "enviando" o dan error). Ahí el SMSC está borrado o mal escrito.
- Tras cambiar de SIM o formatear, a veces el campo SMSC queda vacío y solo falla el envío de texto.

## Relación con tu caso (SIM no reconocida / suspendida)

- Si el teléfono **no reconoce la SIM** (físico), no llegas ni a usar el SMSC.
- Si la línea está **suspendida en red**, el SMSC existe pero la red te rechaza el servicio; corregir el SMSC no arregla la suspensión.
- Si la SIM se reconoce y tienes señal "Tigo" pero **no envías SMS**, ahí sí revisas y pones el SMSC correcto de Tigo.

## El SMSC correcto de Tigo Colombia

El valor oficial lo da Tigo, pero suele ser:
- **+573****0001** (uno común)
- o **+573****0405**

Si lo vas a editar, **anota primero el que ya estaba** por si hay que revertir. Y ojo: si lo dejas en blanco o mal, dejas de enviar SMS aunque recibas.

---

¿Quieres que te confirme el SMSC exacto de Tigo para tu ciudad/país, o te explico cómo ver el que trae tu SIM ahora mismo? (Si tu SIM no se reconoce, no podrás verlo hasta que la lea el teléfono.)

### Usuario

parece que *665# y *555# para tiog no sirve, que mas puedo hacer para saber el numero de la sim?

### Asistente

Claro, y tiene sentido que no sirvan: **los códigos USSD como \*665# y \*555# requieren que la SIM esté reconocida y registrada en la red**. Si el teléfono no la lee, esos códigos nunca responden. Entonces hay que ir por otro lado — **usando datos que no dependen de que el celular la reconozca**:

## 1. El ICCID (serial de la SIM) + tu cédula → Tigo te da el número
Es la vía más segura cuando la SIM no se lee. El **ICCID** es el número largo impreso en la **tarjeta plástica** (la "camita" donde iba la SIM) o a veces en un costado de la SIM misma. Empieza por **89…** y tiene ~19 dígitos.

- Llamas a Tigo (desde otro teléfono): **018000 910 500** (fijo) o **611** desde otro cel Tigo.
- Dices: *"Tengo la SIM con ICCID 89… pero el celular no la reconoce y no sé el número. Quiero que me confirmen la línea asociada a mi cédula"*. Con cédula + ICCID te ubican todo.

## 2. Llévala a un Centro de Experiencia Tigo
Llevas **cédula + la SIM física**. Ellos la prueban en un equipo de la tienda, ven si la línea está activa y te dicen el número en el momento. Sin que tú sepas el número.

## 3. Web/app Mi Tigo iniciando con la CÉDULA (no con el número)
En mitigo.com.co puedes entrar con tu cédula y ver las líneas a tu nombre, planes y números. Útil si tienes otro cel Tigo o datos para el login.

## 4. Busca el número en tus propios rastros
Antes de ir a la tienda, revisa si el número quedó guardado en:
- **WhatsApp/Telegram** registrados con esa SIM (el número aparece en el perfil).
- Un **recibo de recarga**, comprobante de pago, o correo de Tigo.
- **Mensajes viejos** que te enviaron a ese número, o contactos que tengan guardado ese número.
- **Caja/empaque** de cuando compraste la SIM (a veces viene el número impreso).

## 5. Prueba la SIM en OTRO teléfono que SÍ la reconozca
Si en otro cel sí la lee, ya puedes usar los USSD o la app Mi Tigo ahí mismo para ver el número. Si en ningún teléfono la reconoce, la SIM está dañada y Tigo te da una reposición (allí mismo te asignan línea nueva o recuperan la tuya).

## 6. Restablecer configuración de red (solo si la reconoce pero sin servicio)
*Ajustes → Conexiones → Restablecer → Restablecer config. de red*. No borra fotos. Esto no saca el número, pero a veces tras un cambio la SIM se registra bien y ya puedes usar USSD/app.

---

**Resumen práctico:** como la SIM no se reconoce, **ni USSD ni app desde ese celular te sirven**. Tu mejor jugada es: busca el **ICCID en la tarjeta plástica**, llévalo con tu **cédula** a Tigo (tienda o llamada 018000 910 500) y te dan el número y el estado de la línea de inmediato.

¿Tienes a mano la tarjeta plástica de la SIM para leer el ICCID? Si quieres, te armo exactamente qué decirles por teléfono para que no te den vueltas.

### Usuario

no no  no, probe los codigos con una sim que sirve y no funciono, la sim de la que hablamos es una sim que tenia guardada hace tiempo

### Asistente

¡Ah, eso cambia todo el diagnóstico! Gracias por aclarar. Entonces:

1. **Los códigos no funcionan porque simplemente no son los de Tigo** — no porque la SIM esté mal. Lo confirmaste: con una SIM buena tampoco sirven. Descartado.
2. **La SIM en cuestión es una que tenías guardada hace tiempo.** Ahí está la clave real del problema.

## Lo más probable: la línea ya no existe

En Colombia, Tigo (y todas las operadoras) **dan de baja las líneas prepago por inactividad prolongada** (meses sin recarga ni uso) y luego **reciclan el número** para dárselo a otro cliente. Una SIM guardada "hace tiempo":

- La red la puede rechazar con **"SIM no válida"**, **"no registrada en la red"**, o directamente el teléfono puede no reconocerla (la SIM también se degrada guardada, oxidación de contactos, etc.).
- El número que tenía **ya fue asignado a otra persona** (reciclaje). Por eso el sistema no muestra nada: no hay línea viva detrás de esa SIM.

Eso explica tu reporte original: el número salía **"Desconocido"** porque la SIM nunca tuvo el MSISDN escrito, **y encima la línea está muerta**. No es un fallo raro, es SIM vieja sin servicio.

## Qué puedes hacer (según lo que quieras)

**A. Querías recuperar ESE número en particular**
Muy difícil. Si pasaron meses y el número fue reciclado, Tigo **no lo devuelve** — ya está con otro cliente. Solo en ventanas cortas de "suspensión pero no baja todavía" se podría reactivar pagando. Verifícalo con tu cédula, pero el panorama es que ese número se perdió.

**B. Solo necesitabas una línea activa (el número da igual)**
Tigo te da una **SIM nueva** (gratis o muy barata en centro de experiencia). La vieja ya no sirve. Vas con la cédula y listo.

**C. Quieres confirmar el estado exacto de esa SIM vieja**
Llevas la **cédula + la tarjeta plástica (ICCID)** y preguntas: *"¿Esta SIM/ICCID sigue activa o ya fue dada de baja?"*. Te confirman en segundos si la línea existe o fue reciclada.

## Diagnóstico práctico ahora

| Prueba | Si pasa | Conclusión |
|---|---|---|
| Meter la SIM vieja → teléfono dice "SIM no válida"/"no registrada" | se lee pero red la rechaza | línea dada de baja (reciclada) |
| Meter la SIM vieja → "Sin tarjeta SIM" | no la lee | SIM dañada por tiempo + línea muerta |
| Meter la SIM vieja en OTRO cel → igual | confirma que es la SIM/línea, no tu celular | deséchala, pide una nueva |

## En resumen
No vale la pena pelear con esa SIM: es vieja, la línea casi seguro fue reciclada y el número ya no es tuyo. **La solución real es una SIM nueva en Tigo con tu cédula.** Solo sírvele si querías ese número específico y hace poco que la guardaste — en ese caso, llámalos al **018000 910 500** con tu cédula para ver si la línea sigue en período de gracia.

¿Hace cuánto la tenías guardada? Con eso te digo si vale la pena intentar recuperarla o directo vas por una nueva.

### Usuario

me di cuenta que la sim card tiene 2 numeros grabados. uno es 313654815 y 8957732111. que significan estos numeros?

### Asistente

¡Bingo! Esos dos números son justo lo que necesitabas para identificar la SIM. Te los traduzco:

## 1. `313654815` = el NÚMERO DE TELÉFONO (MSISDN)
Es el número que se le asignó a esa SIM cuando se activó, **impreso físicamente en la tarjeta**. Esto responde tu duda original del "Desconocido": el número **sí existe, pero está grabado en el plástico, no en la memoria que lee el celular** (por eso el teléfono no lo mostraba).

Pero hay **dos cosas raras** en ese número que debes notar:

- **Es de 9 dígitos.** En Colombia los celulares son de **10 dígitos** (3 de prefijo + 7). Falta un dígito al final. El completo sería tipo `313 654 815X`.
- **El prefijo 313 es de CLARO, no de Tigo.** En Colombia: Tigo usa `300-305` (y `350`), Claro usa `310-319`, Movistar `320-323`. **313 es Claro.**

Eso sugiere fuerte que **esa SIM nunca fue de Tigo** (o la etiqueta está mezclada), a menos que haya habido portabilidad numérica (conservar el número al cambiar de operador). Por eso los códigos de Tigo no servían.

## 2. `8957732111` = inicio del ICCID (serial único de la SIM)
- El **ICCID** es el número de serie de fábrica de la tarjeta, único en el mundo. Siempre empieza por **89** (código de industria de telecom) y **57** es Colombia (`89-57-...`).
- El ICCID completo tiene **~19-20 dígitos**; la tarjeta solo muestra los primeros 10 (`8957732111`). Con ese serial la operadora identifica la SIM sin importar el número de teléfono.

## Qué significa esto para tu caso

| Dato | Para qué sirve |
|---|---|
| `313654815` | Es el número que tuvo la SIM (llámalo para ver si aún existe) |
| `8957732111` | Serial para que la operadora busque la SIM en su sistema |

Como la SIM es vieja y guardada, casi seguro la línea fue **reciclada** y ese número ya es de otra persona. Pero ahora ya tienes cómo preguntar.

## Tu siguiente paso (y un aviso importante)
Dado que el prefijo es **313 (Claro)**, llama a **Claro**, no a Tigo:
- Desde otro cel Claro: **611** o **\*611**.
- Fijo: **018000 954 555** (Claro Colombia).
- Dices: *"Tengo una SIM con número 313654815 e ICCID que empieza en 8957732111, ¿sigue activa o ya fue dada de baja?"*

Si te confirman que está muerta/reciclada, pides reposición o una SIM nueva. Y si resulta que **sí era Tigo por portabilidad**, con ese ICCID Tigo también te la ubica.

¿Estás seguro de que era Tigo? Si el prefijo 313 es Claro, probablemente la confundiste con otra, y por eso nada de Tigo cuadraba. ¿Revisamos si tienes otra SIM por ahí etiquetada como Tigo de verdad?


## Enlaces
- Índice: [[hermes-import-index]]
- Home: [[Home]]
