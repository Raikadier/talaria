---
date: 2026-06-15
type: conversation
source_agent: cursor
session_id: "cfb90943-cbfb-477a-be09-6be7a3b4e012"
project: "d-Github-repos-togesc"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-togesc\\agent-transcripts\\cfb90943-cbfb-477a-be09-6be7a3b4e012\\cfb90943-cbfb-477a-be09-6be7a3b4e012.jsonl"
tags: [conversation, imported, cursor]
title: "desdela fase 0 hasta la 4, que hace falta hacer para poder pasar a la fase 5?"
---

# desdela fase 0 hasta la 4, que hace falta hacer para poder pasar a la fase 5?

**Fecha:** 2026-06-15  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-togesc  
**Sesión:** `cfb90943-cbfb-477a-be09-6be7a3b4e012`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-togesc\agent-transcripts\cfb90943-cbfb-477a-be09-6be7a3b4e012\cfb90943-cbfb-477a-be09-6be7a3b4e012.jsonl`

## Mensajes

### Usuario

desdela fase 0 hasta la 4, que hace falta hacer para poder pasar a la fase 5?

### Asistente

Revisando el plan de fases del proyecto para identificar qué falta entre la fase 0 y la 4 antes de pasar a la 5.


[tool:Read]
[tool:Read]

### Asistente

Comprobando el estado real del código frente a lo que marca el plan como pendiente.


[tool:Grep]
[tool:SemanticSearch]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Glob]

### Asistente

Según `Plan/plan_fases.txt` y el estado actual del repo, esto es lo que queda entre las fases 0–4 antes de poder abrir la **Fase 5 (monetización)** con criterio.

## Resumen ejecutivo

Las fases **0, 1, 2 y 3 (web)** están marcadas como **completadas**. La **Fase 4** está completada en alcance **Must**, pero **no cumple el DoD al 100%**. Ese es el bloqueo formal para pasar a Fase 5.

La Fase 5 depende explícitamente de:

> *Fase 4 DoD (cuentas necesarias para sync Pro)*

---

## Bloqueo principal (Fase 4 — DoD pendiente)

| Criterio | Estado |
|----------|--------|
| Mismo usuario en **web + móvil** ve el **mismo progreso SRS** tras sync | **Pendiente** — prueba manual post-deploy |

Lo demás del DoD de Fase 4 ya está hecho según el plan:

- RLS en Supabase
- App offline-first (sync no bloquea el juego)
- Secrets `SUPABASE_*` en GitHub + `dart-define` en deploy web
- Migración `user_progress` en remoto
- Auth, repositorio híbrido, flujo `/account`, `mergeOnSignIn`

**Acción concreta:** crear cuenta en producción (p. ej. https://togesc.vercel.app), jugar varias rondas, abrir en otro dispositivo/navegador con la misma cuenta y confirmar que el SRS coincide. Sin eso, la Fase 4 no se puede cerrar formalmente.

---

## Fase 4 — entregables Should (no bloquean el DoD, pero incompletos)

| Entregable | Estado |
|------------|--------|
| Sync incremental offline-first (cola local → push al reconectar) | Parcial: `HybridProgressRepository` guarda local y empuja al remoto si hay sesión, pero **no hay cola de reintentos** explícita |
| Recuperación de contraseña | **No implementada** (solo signup/signin en `account_screen.dart`) |
| Verificación de email | **Solo mensaje informativo** al registrarse |

Recomendable antes o durante Fase 5 si las cuentas son reales, pero no figuran como criterio Must del DoD.

---

## Fases anteriores — pendientes que **sí importan** para Fase 5

La Fase 5 exige **RevenueCat (iOS + Android)** y **Stripe (web)**. Eso hace relevante lo que quedó diferido en Fase 3:

| Fase | Pendiente | Por qué importa para Fase 5 |
|------|-----------|------------------------------|
| **3** | Build release Android (AAB) + firma | RevenueCat en móvil |
| **3** | Build release iOS + TestFlight | RevenueCat en móvil |
| **3** | Listings en stores (descripción, capturas, icono) | Publicar compras reales |
| **1** | Probar `flutter run` en Android/iOS | Validar audio y UX móvil antes de pagos |

La web ya está en v1.0.0 (`v1.0.0`, https://togesc.vercel.app), así que **Stripe en web** puede avanzarse antes que las stores móviles, pero el DoD de Fase 5 pide compra sandbox en **iOS + Android + web**.

---

## Fases 0–2 — diferidos (no bloquean Fase 5)

Estos ítems quedaron para más adelante y **no son prerequisito** del plan para monetización:

- **Fase 1:** prueba manual en Android/iOS (útil, no formalmente bloqueante)
- **Fase 2:** Lighthouse accesibilidad ≥ 90, Sentry, analytics, design system, Semantics del piano, PWA offline
- **Fase 3:** builds desktop Windows/macOS (Could)

---

## Checklist mínimo para pasar a Fase 5

### Obligatorio (cerrar Fase 4)

1. **Validar sync multi-dispositivo en producción** (web ↔ otro cliente con la misma cuenta)
2. Confirmar que `flutter test` sigue en verde tras cualquier fix de sync

### Muy recomendable antes de cobrar

3. **Recuperación de contraseña** y flujo de verificación de email (cuentas reales)
4. **Cola de sync offline** si quieres que Pro incluya sync fiable tras desconexión
5. **Builds móvi

_[truncado]_

### Usuario

PS D:\Github repos\togesc\TOGESC\togesc> flutter devices
Found 3 connected devices:
  Windows (desktop) • windows • windows-x64    • Microsoft Windows [Version 10.0.26200.8655]
  Chrome (web)      • chrome  • web-javascript • Google Chrome 149.0.7827.104
  Edge (web)        • edge    • web-javascript • Microsoft Edge 149.0.4022.62

Run "flutter emulators" to list and start any available device emulators.

If you expected another device to be detected, please run "flutter doctor" to diagnose potential issues. You may also try increasing the time to
wait for connected devices with the "--device-timeout" flag. Visit https://flutter.dev/setup/ for troubleshooting tips.
PS D:\Github repos\togesc\TOGESC\togesc> flutter run
Resolving dependencies... (3.3s)
Downloading packages...
  app_links 7.0.0 (7.1.2 available)
  app_links_platform_interface 2.0.2 (2.0.3 available)
  code_assets 1.0.0 (1.2.1 available)
  flutter_riverpod 2.6.1 (3.3.2 available)
  flutter_soloud 2.1.7 (4.0.9 available)
  go_router 14.8.1 (17.3.0 available)
  hooks 1.0.2 (2.0.2 available)
  matcher 0.12.19 (0.12.20 available)
  meta 1.17.0 (1.18.3 available)
  mocktail 1.0.4 (1.0.5 available)
  native_toolchain_c 0.17.6 (0.19.1 available)
  objective_c 9.3.0 (9.4.1 available)
  path_provider 2.1.5 (2.1.6 available)
  path_provider_android 2.2.23 (2.3.1 available)
  path_provider_platform_interface 2.1.2 (2.1.3 available)
  riverpod 2.6.1 (3.3.2 available)
  shared_preferences_android 2.4.23 (2.4.26 available)
  test_api 0.7.10 (0.7.12 available)
  url_launcher_android 6.3.30 (6.3.32 available)
  vector_math 2.2.0 (2.4.0 available)
  vm_service 15.0.2 (15.2.0 available)
Got dependencies!
21 packages have newer versions incompatible with dependency constraints.
Try `flutter pub outdated` for more information.
Launching lib\main.dart on moto e 7 plus in debug mode...

FAILURE: Build failed with an exception.

* What went wrong:
A problem occurred configuring project ':flutter_soloud'.
> [CXX1101] NDK at C:\Users\david\AppData\Local\Android\sdk\ndk\23.1.7779620 did not have a source.properties file

* Try:
> Run with --stacktrace option to get the stack trace.
> Run with --info or --debug option to get more log output.
> Run with --scan to get full insights.
> Get more help at https://help.gradle.org.

BUILD FAILED in 18s
Running Gradle task 'assembleDebug'...                             19.8s

┌─ Flutter Fix ──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     [!] This is likely due to a malformed download of the NDK.                                                     │
│     This can be fixed by deleting the local NDK copy at: C:\Users\david\AppData\Local\Android\sdk\ndk\23.1.7779620 │
│     and allowing the Android Gradle Plugin to automatically re-download it.                                        │
│                                                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
Error: Gradle task assembleDebug failed with exit code 1

### Asistente

El fallo apunta a una instalación corrupta del NDK de Android. Comprobando el estado del SDK y reparándolo.


[tool:Shell]
[tool:Grep]
[tool:Shell]

### Asistente

[tool:Shell]
[tool:Grep]

### Asistente

[tool:Shell]
[tool:Shell]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Glob]

### Asistente

[tool:Glob]
[tool:Read]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Glob]

### Asistente

[tool:Read]

### Asistente

El plugin `flutter_soloud` exige el NDK 23.1.7779620, pero la instalación está corrupta. Eliminando la carpeta dañada y reinstalando el NDK.


[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

[tool:Shell]

### Asistente

NDK reinstalado correctamente. Compilando para Android para verificar.


[tool:Shell]

### Asistente

[tool:Await]

### Asistente

[tool:Read]

### Asistente

[tool:Await]

### Asistente

[tool:Read]

### Asistente

El problema era una **instalación corrupta del NDK 23.1.7779620**. El plugin `flutter_soloud` lo exige explícitamente en su `build.gradle`, y la carpeta solo contenía `.installer` sin `source.properties` (descarga a medias).

## Qué hice

1. Eliminé la carpeta corrupta:
   `C:\Users\david\AppData\Local\Android\sdk\ndk\23.1.7779620`
2. Reinstalé el NDK con `sdkmanager`:
   ```powershell
   sdkmanager --sdk_root="C:\Users\david\AppData\Local\Android\sdk" "ndk;23.1.7779620"
   ```
3. Verifiqué que `source.properties` existe y compilé el APK debug — **build exitoso** (~18 min la primera vez, por compilar código nativo de SoLoud + instalar CMake/Platform 33).

## Qué debes hacer tú

Con el móvil conectado por USB y depuración USB activada:

```powershell
cd "D:\Github repos\togesc\TOGESC\togesc"
flutter run -d ZT3224HXB9
```

O simplemente `flutter run` si solo está el Moto conectado.

La **primera compilación** puede tardar mucho (10–20 min); las siguientes serán mucho más rápidas.

## Si vuelve a fallar

Repite el borrado + reinstalación del NDK:

```powershell
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\Android\sdk\ndk\23.1.7779620"
echo y | & "$env:LOCALAPPDATA\Android\sdk\cmdline-tools\latest\bin\sdkmanager.bat" `
  --sdk_root="$env:LOCALAPPDATA\Android\sdk" "ndk;23.1.7779620"
```

También puedes hacerlo desde **Android Studio → SDK Manager → SDK Tools → NDK (Side by side)** y marcar la versión **23.1.7779620**.

---

**Nota:** Flutter 3.41 usa NDK **28.2** para la app, pero `flutter_soloud 2.1.7` fuerza **23.1** para compilar su código C++. Por eso hacen falta las dos versiones instaladas (ya tienes ambas).

Cuando arranque en el Moto, podrás hacer la prueba de **sync multi-dispositivo** (web ↔ móvil) que falta para cerrar la Fase 4.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.

### Asistente

El NDK **23.1.7779620** estaba corrupto (faltaba `source.properties`). Se eliminó la carpeta dañada, se reinstaló con `sdkmanager` y la compilación Android ya funciona: **`app-debug.apk` generado correctamente**.

Puedes lanzar la app en tu Moto con:

```powershell
cd "D:\Github repos\togesc\TOGESC\togesc"
flutter run
```

La primera compilación tardó ~18 minutos por el código nativo de `flutter_soloud`; las siguientes deberían ser mucho más rápidas.

### Usuario

okey, que falta entonces?

### Asistente

El Android ya compila, así que el panorama queda más claro. Esto es lo que **falta de verdad** para cerrar Fase 4 y poder pasar a Fase 5:

## Bloqueo principal (Fase 4)

**Validar sync multi-dispositivo en producción** — el único criterio Must sin cerrar:

1. En el **Moto**: crear/vincular cuenta, jugar 5–10 rondas
2. En **Chrome** (https://togesc.vercel.app): iniciar sesión con la misma cuenta
3. Confirmar que el **progreso SRS coincide** (y viceversa: jugar en web y verificar en móvil)

Sin esa prueba manual, la Fase 4 no cumple DoD formalmente.

---

## Recomendable antes de monetizar (Fase 4 Should)

| Pendiente | Estado |
|-----------|--------|
| Recuperación de contraseña | No implementada |
| Verificación de email (flujo completo) | Solo mensaje al registrarse |
| Cola de sync offline con reintentos | Parcial (sync directo, sin cola) |

---

## Para Fase 5 (aún no empezada)

Todo esto hay que **implementarlo desde cero**:

- Definir **Free vs Pro** (qué modos/features van detrás del paywall)
- **RevenueCat** (iOS + Android)
- **Stripe** (web)
- Paywall UI en Flutter
- Entitlements en Supabase
- Trial, restaurar compras, pantalla de suscripción

---

## Móvil / stores (Fase 3, necesario para Fase 5 completa)

| Pendiente | Notas |
|-----------|-------|
| Probar app en el Moto (audio, SRS, flujo completo) | Ya puedes con `flutter run` |
| Build release Android (AAB) + firma | Para Play Store y RevenueCat |
| Build iOS + TestFlight | Requiere Mac |
| Listings en stores (capturas, icono, descripción) | Para publicar |

---

## Diferido (no bloquea Fase 5)

- Lighthouse accesibilidad ≥ 90
- Sentry, analytics, design system
- PWA offline
- Builds desktop Windows/macOS

---

## Orden práctico ahora

1. **`flutter run`** en el Moto → comprobar que audio + SRS funcionan bien
2. **Prueba de sync** web ↔ móvil con la misma cuenta
3. Si sync OK → **cerrar Fase 4** y arrancar Fase 5 (definir planes + Stripe web primero; móvil cuando tengas AAB firmado)

¿Quieres que te prepare un protocolo paso a paso para la prueba de sync, o que revisemos el código de `HybridProgressRepository` por si algo puede fallar en esa prueba?

### Usuario

okey, implementa todo para estar listos para la fase 5

### Asistente

Implementando lo pendiente de Fase 4 y la base de Fase 5. Explorando el código y la arquitectura actuales.


[tool:Task]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Glob]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

Implementando Fase 4 (Should) y la base completa de Fase 5: sync offline, auth mejorado, suscripciones, paywall y gating.


[tool:TodoWrite]
[tool:Write]
[tool:Write]
[tool:Write]
[tool:Write]

### Asistente

[tool:Write]
[tool:Write]
[tool:Write]
[tool:Write]
[tool:Write]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:Write]
[tool:StrReplace]

### Asistente

[tool:Write]

### Asistente

[tool:Write]
[tool:Write]

### Asistente

[tool:Write]
[tool:Write]

### Asistente

[tool:StrReplace]
[tool:Write]

### Asistente

[tool:Write]
[tool:Write]
[tool:Write]

### Asistente

[tool:Write]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:Write]
[tool:Write]

### Asistente

[tool:Write]
[tool:Write]
[tool:Read]

### Asistente

[tool:Read]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]

### Asistente

[tool:Read]
[tool:StrReplace]
[tool:StrReplace]
[tool:Write]

### Asistente

[tool:StrReplace]
[tool:Write]
[tool:StrReplace]
[tool:Read]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:Read]

### Asistente

[tool:StrReplace]
[tool:Shell]

### Asistente

[tool:Await]

### Asistente

[tool:Read]

### Asistente

[tool:Grep]
[tool:StrReplace]

### Asistente

[tool:StrReplace]
[tool:Shell]

### Asistente

[tool:Read]
[tool:StrReplace]

### Asistente

[tool:StrReplace]
[tool:Read]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:Shell]

### Asistente

[tool:Shell]
[tool:TodoWrite]

### Asistente

Implementación lista. **221 tests pasando**. Resumen de lo hecho y lo que falta configurar fuera del código:

## Fase 4 — completada en código

| Feature | Implementación |
|---------|----------------|
| **Cola sync offline** | `SyncPendingStore` + `flushPendingSync()` en `HybridProgressRepository`; flush al reconectar, login y resume app |
| **Recuperación contraseña** | Flujo en `/account` + pantalla de nueva contraseña tras enlace Supabase |
| **Verificación email** | Banner + reenvío si `emailConfirmedAt` es null |
| **Sync Pro** | Cloud sync solo con plan Pro cuando monetización está activa |

## Fase 5 — base implementada

| Feature | Implementación |
|---------|----------------|
| **Free vs Pro** | `SubscriptionConstants` — Free: una nota, intervalo, sostenidos; Pro: acorde, aleatorio, velocidad, stats avanzadas, sync |
| **Paywall** | `/paywall` con trial 14 días, compra y restaurar |
| **Gestión suscripción** | `/subscription` |
| **Gating** | Home (candados PRO), `ProRouteGuard` en rutas, stats avanzadas bloqueadas |
| **RevenueCat** | `purchases_flutter` en móvil |
| **Stripe web** | Checkout/Portal vía `url_launcher` |
| **Supabase entitlements** | Migración `user_subscriptions` con RLS |

## Comportamiento por defecto

Con `MONETIZATION_ENABLED=false` (default) **todo sigue gratis** — CI y desarrollo sin cambios. Para activar freemium en producción:

```json
// dart_defines.json
{
  "MONETIZATION_ENABLED": "true",
  "REVENUECAT_GOOGLE_KEY": "goog_...",
  "REVENUECAT_APPLE_KEY": "appl_...",
  "STRIPE_CHECKOUT_URL": "https://buy.stripe.com/...",
  "STRIPE_PORTAL_URL": "https://billing.stripe.com/..."
}
```

## Pasos manuales que te quedan

1. **Aplicar migración Supabase:**
   ```powershell
   .\scripts\supabase-push.ps1
   ```
   (incluye `user_subscriptions`)

2. **RevenueCat:** crear proyecto, entitlement `pro`, productos iOS/Android, pegar API keys

3. **Stripe:** crear Checkout + Customer Portal; webhook que actualice `user_subscriptions` (Edge Function recomendada)

4. **GitHub Secrets** (deploy web): `MONETIZATION_ENABLED`, `STRIPE_CHECKOUT_URL`, `STRIPE_PORTAL_URL`

5. **Validar sync multi-dispositivo** (DoD Fase 4): misma cuenta web ↔ Moto

6. **Probar en Moto:** `flutter run` con monetización desactivada primero, luego activar y probar paywall

¿Quieres que prepare la Edge Function de Stripe para actualizar `user_subscriptions` automáticamente?

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.

### Asistente

La primera ejecución falló por errores de compilación en `MobilePurchasesService` y `subscription_provider` (API de RevenueCat e imports). Eso ya está corregido.

**Estado actual:** `flutter test` — **221 tests pasando**. La implementación de Fase 4 + base Fase 5 está lista en código.

**Siguiente paso tuyo:** aplicar la migración Supabase (`user_subscriptions`) y configurar las claves de RevenueCat/Stripe cuando quieras activar monetización en producción.

### Usuario

completa la fase 5

### Asistente

Completando la Fase 5: revisando qué hay implementado y qué falta para cerrar monetización de punta a punta.


[tool:Grep]
[tool:Glob]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

Completando la Fase 5: webhooks (Stripe + RevenueCat), retorno post-pago en web, export Pro y tests.


[tool:TodoWrite]
[tool:Write]
[tool:Write]
[tool:Write]

### Asistente

[tool:Write]
[tool:Write]

### Asistente

[tool:Grep]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]

### Asistente

[tool:Write]
[tool:Write]
[tool:Write]
[tool:Write]

### Asistente

[tool:StrReplace]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]

### Asistente

[tool:Write]
[tool:Read]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:Write]

### Asistente

[tool:Write]
[tool:Write]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]

### Asistente

[tool:Shell]

### Asistente

[tool:Await]

### Asistente

[tool:Read]

### Asistente

[tool:Await]

### Asistente

[tool:Read]
[tool:StrReplace]

### Asistente

[tool:StrReplace]
[tool:TodoWrite]

### Asistente

**Fase 5 completada en código** — 223 tests pasando.

## Qué se añadió

### Webhooks Supabase (entitlements en servidor)
- **`stripe-webhook`** — `checkout.session.completed`, `subscription.updated/deleted` → actualiza `user_subscriptions`
- **`revenuecat-webhook`** — compras, renovaciones, cancelaciones → mismo cache
- Script: `scripts/deploy-functions.ps1`

### Migración DB
- `20260616000000_user_subscriptions_stripe.sql` — campos `stripe_customer_id` y `stripe_subscription_id`

### Flujo web Stripe
- **`SubscriptionCheckoutListener`** — detecta `?checkout=success|cancel`, refresca plan y limpia URL
- Paywall exige **login** antes de pagar
- Email prefilled en Checkout

### Export Pro
- **Export CSV** en estadísticas (descarga web / portapapeles móvil)

### Mejoras sync
- RevenueCat siempre sincroniza estado a Supabase (también bajadas/expiraciones)
- Refresh de suscripción al resume app y al iniciar sesión

---

## Activar monetización en producción

**1. Migraciones + functions:**
```powershell
.\scripts\supabase-push.ps1
.\scripts\deploy-functions.ps1
```

**2. Secrets en Supabase** (Edge Functions):
- `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
- `REVENUECAT_WEBHOOK_SECRET`

**3. Webhooks externos:**
| Servicio | URL |
|----------|-----|
| Stripe | `https://puetlvcsrntwweuxinee.supabase.co/functions/v1/stripe-webhook` |
| RevenueCat | `https://puetlvcsrntwweuxinee.supabase.co/functions/v1/revenuecat-webhook` |

**4. Stripe Checkout** — Success URL: `https://togesc.vercel.app/?checkout=success`

**5. `dart_defines.json` / GitHub Secrets:**
```json
{
  "MONETIZATION_ENABLED": "true",
  "REVENUECAT_GOOGLE_KEY": "goog_...",
  "REVENUECAT_APPLE_KEY": "appl_...",
  "STRIPE_CHECKOUT_URL": "https://buy.stripe.com/...",
  "STRIPE_PORTAL_URL": "https://billing.stripe.com/..."
}
```

**6. RevenueCat** — entitlement `pro`, `app_user_id` = UUID Supabase del usuario

---

## DoD pendiente (manual)

- Compra **sandbox** iOS/Android + Stripe test mode
- Validar sync **web ↔ móvil** (Fase 4)

Con `MONETIZATION_ENABLED=false` (default) la app sigue **100% gratis** para desarrollo y CI.

### Usuario

Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.

### Asistente

Análisis y tests completados correctamente.

- **`flutter analyze`**: 3 avisos menores (import duplicado y similares), ya corregidos.
- **`flutter test`**: **223 tests pasando**.

La Fase 5 queda implementada en código; solo falta la configuración externa (claves, webhooks, compras sandbox) para activar monetización en producción.

### Usuario

estado de las fases de la 0 a la 5 y que falta para pasar a la fase 6

### Asistente

[tool:Read]

### Asistente

## Panorama general (Fases 0–5)

| Fase | Estado | Resumen |
|------|--------|---------|
| **0** | ✅ Completada | Repo unificado Flutter, sin Python, docs y tests OK |
| **1** | ✅ Completada* | MVP funcional; falta validación manual formal en iOS |
| **2** | ✅ Completada (web) | CI + deploy web; UX avanzada diferida |
| **3** | ✅ Completada (web) | https://togesc.vercel.app v1.0.0; móvil/stores diferidos |
| **4** | ⚠️ Casi cerrada | Código Must + Should hecho; **1 DoD manual pendiente** |
| **5** | ⚠️ Casi cerrada | Código completo; **activación externa + 1 DoD manual pendiente** |

\* Android ya compila (`flutter run` en Moto); falta cerrar la prueba manual como criterio formal de Fase 1.

---

## Fase 0 — Consolidación ✅

**Hecho:** Flutter único producto, Python eliminado, README, `.cursorrules`, `flutter test` verde.

**Pendiente menor:** ADR en `Plan/adr/` (Could, opcional).

---

## Fase 1 — MVP Flutter ✅

**Hecho:** 6 modos, SRS, audio, piano, stats, onboarding, Go Router, tema claro/oscuro, 223 tests.

**Pendiente:**
- Prueba manual formal en **iOS** (Android/Moto ya viable tras fix NDK)

---

## Fase 2 — Calidad y pre-lanzamiento ✅ (web)

**Hecho:** CI GitHub Actions, deploy Vercel, About, Privacidad, smoke test Chrome.

**Diferido (Should/Could):** Sentry, analytics, design system, Semantics piano, Lighthouse ≥ 90, PWA, i18n.

---

## Fase 3 — Distribución pública ✅ (web)

**Hecho:** Web pública, privacidad, tag `v1.0.0`.

**Diferido:**
- AAB Android firmado + Play Store
- iOS + TestFlight
- Listings stores (capturas, icono)
- Desktop Windows/macOS (Could)

---

## Fase 4 — Cuentas y sync ⚠️

**Hecho (Must):**
- Supabase Auth + `user_progress` + RLS
- Sync híbrido offline-first + cola pendiente
- `/account`, `mergeOnSignIn`, deploy con secrets

**Hecho (Should, ya en código):**
- Recuperación contraseña + verificación email
- Cola sync → push al reconectar

**DoD pendiente (bloqueante formal):**
- [ ] **Mismo usuario web + móvil ve el mismo SRS** tras sync (prueba manual en prod)

---

## Fase 5 — Monetización ⚠️

**Hecho (código):**
- Free vs Pro + gating (modos, stats, sync, export CSV)
- Paywall, trial 14 días, restaurar compras, `/subscription`
- RevenueCat (móvil) + Stripe (web)
- Webhooks Supabase (`stripe-webhook`, `revenuecat-webhook`)
- Tabla `user_subscriptions` + retorno `?checkout=success`

**DoD pendiente:**
- [ ] **Compra sandbox** iOS + Android + Stripe test mode (manual)
- [ ] Activar en producción:
  - `MONETIZATION_ENABLED=true` + claves
  - `scripts/supabase-push.ps1` + `scripts/deploy-functions.ps1`
  - Webhooks Stripe/RevenueCat configurados
  - Success URL Stripe: `https://togesc.vercel.app/?checkout=success`

**Nota:** Con `MONETIZATION_ENABLED=false` (default) todo sigue gratis — CI/dev sin cambios.

---

## ¿Qué falta para pasar a Fase 6?

Según el plan, Fase 6 depende de **Fase 5 con negocio activo** (o Fase 3 si permanece gratuito). Para entrar con criterio:

### Cierre mínimo recomendado (DoD)

1. **Sync multi-dispositivo validado** (Fase 4)
2. **Monetización activada y probada en sandbox** (Fase 5)
3. **`flutter test` verde** (ya cumplido — 223 tests)

### Luego arranca Fase 6 (escala y operación)

| Prioridad | Entregable | Estado |
|-----------|------------|--------|
| **Should** | Dashboard métricas (retención D1/D7, conversión Free→Pro, modos) | No iniciado |
| **Should** | Sentry + alertas uptime web | Diferido desde Fase 2 |
| **Should** | Backups Supabase automatizados | No iniciado |
| **S

_[truncado]_

### Usuario

okey implementa segun el orden practico sugerido

### Asistente

Implementando el orden práctico: mejorando sync, preparando sandbox de pagos, activando monetización en deploy y arrancando Fase 6.


[tool:Read]
[tool:Glob]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:TodoWrite]
[tool:Write]
[tool:Write]
[tool:Write]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:Write]
[tool:Write]
[tool:Write]
[tool:Write]
[tool:Write]

### Asistente

[tool:Grep]
[tool:Read]

### Asistente

[tool:StrReplace]
[tool:Write]
[tool:Write]

### Asistente

[tool:Write]
[tool:StrReplace]
[tool:Read]

### Asistente

[tool:Read]
[tool:StrReplace]

### Asistente

[tool:Read]

### Asistente

[tool:Grep]
[tool:StrReplace]
[tool:StrReplace]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:Write]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]

### Asistente

[tool:Read]
[tool:Read]

### Asistente

[tool:Write]
[tool:StrReplace]
[tool:Grep]

### Asistente

[tool:Read]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:Read]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:Write]
[tool:Write]
[tool:Write]
[tool:Write]
[tool:Write]
[tool:Write]
[tool:Write]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:StrReplace]
[tool:Shell]

### Asistente

[tool:Grep]

### Asistente

[tool:Read]

### Asistente

[tool:StrReplace]
[tool:StrReplace]
[tool:Shell]

### Usuario

If the available MCP tools do not fully support what the user asked you to do, complete the work you can with the current tool set. In your work summary, include what you were unable to do with MCP and why. Do not use browser automation to work around missing or unavailable MCP tools unless the user explicitly asks you to use the browser.

### Usuario

okey implementa segun el orden practico sugerido

### Asistente

[tool:Shell]
[tool:TodoWrite]

### Asistente

Verificando el estado final del código para dar un resumen preciso de lo implementado.


[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Glob]

### Asistente

Implementación completada según el orden práctico sugerido. **225 tests pasando**.

## Resumen por paso

### 1. Sync web ↔ móvil (Fase 4)
- **`SyncCoordinator`**: orquesta pull/push con reintentos y estado observable
- **`SyncDiagnosticsCard`** en `/account`: último sync, pendientes, errores
- **Auto-sync** en login, resume de app, activación Pro y tras `saveProgress`
- **Cola offline** (`SyncPendingStore`) + flush al reconectar
- **Test** `sync_multi_device_test.dart` (2 escenarios multi-dispositivo)

### 2–3. Monetización + sandbox (Fase 5)
- **Free vs Pro** con gating en router, home y estadísticas
- **RevenueCat** (móvil) + **Stripe Checkout** (web) + webhooks Supabase
- **Paywall**, trial 14 días, restaurar compras, export CSV Pro
- **Deploy web** activa `MONETIZATION_ENABLED=true` si hay `STRIPE_CHECKOUT_URL`
- **Default dev/CI**: monetización desactivada (todo gratis)

### 4. Fase 6 — Observabilidad
- **Analytics**: tabla `analytics_events`, servicio + eventos en juego/paywall/sync
- **Sentry** opcional vía `SENTRY_DSN` en `main.dart`
- **Dependabot** para Flutter y GitHub Actions
- **Backup semanal** Supabase (`.github/workflows/supabase-backup.yml`)
- **Scripts**: `validate-production.ps1`, `metrics-report.ps1`

---

## Lo que queda manual (infra + DoD)

```powershell
# 1. Validar configuración local
.\scripts\validate-production.ps1

# 2. Aplicar migraciones (user_progress, subscriptions, analytics)
.\scripts\supabase-push.ps1

# 3. Desplegar webhooks Stripe + RevenueCat
.\scripts\deploy-functions.ps1
```

**Secrets en GitHub** (si aún no están): `SUPABASE_*`, `STRIPE_*`, `MONETIZATION_ENABLED`, `SENTRY_DSN`, `SUPABASE_ACCESS_TOKEN`, `SUPABASE_DB_PASSWORD`

**Pruebas manuales pendientes:**
| DoD | Cómo probarlo |
|-----|----------------|
| Sync multi-dispositivo | Misma cuenta en web + Moto → panel en `/account` |
| Sandbox pagos | Stripe test mode + RevenueCat sandbox en móvil |
| Monetización prod | `MONETIZATION_ENABLED=true` + claves reales |

**Nota sync sin pagar:** con monetización desactivada o trial de 14 días en el paywall puedes probar sync sin suscripción Pro.

---

## Estado de fases

| Fase | Código | DoD manual |
|------|--------|------------|
| 0–3 | ✅ | — |
| 4 | ✅ | Sync web + móvil |
| 5 | ✅ | Compras sandbox |
| 6 | 🔄 Base lista | Uptime externo (Could) |

¿Quieres que ejecute `validate-production.ps1` o el deploy a Supabase desde aquí?

### Usuario

explicame en que consiste la fase 6

### Asistente

Revisando el plan y lo ya implementado para explicarte la Fase 6 con precisión.


[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

La **Fase 6** no es “terminar el producto” como las anteriores. Es la fase de **operar, medir y hacer crecer TOGESC de forma sostenible** una vez que ya hay app publicada, cuentas, sync y (opcionalmente) monetización.

## Idea central

Las fases 0–5 construyen el producto. La Fase 6 responde a:

> *¿Cómo sabemos que la app funciona bien en producción, no perdemos datos, no nos rompemos con dependencias obsoletas, y qué mejoramos después del lanzamiento?*

Es **continua** (no tiene fecha de cierre fija) y depende de si hay negocio (Fase 5) o la app sigue gratuita (Fase 3).

---

## Tres pilares

### 1. Observabilidad — ver qué pasa en producción

**Métricas de producto**
- Eventos en Supabase (`analytics_events`): aperturas, modos iniciados, rondas completadas, paywall visto, sync, etc.
- Vista SQL agregada `metrics_daily` + script `scripts/metrics-report.ps1` para consultar los últimos 7 días.
- Sirve para retención, uso por modo, conversión free→Pro, etc.

**Errores y crashes**
- **Sentry** (opcional): si configuras `SENTRY_DSN`, la app reporta crashes y excepciones.
- Objetivo de referencia: crash rate móvil ≤ 0.1% de sesiones.

**Disponibilidad web**
- Uptime monitoring externo (p. ej. UptimeRobot, Better Stack) — **aún pendiente de configurar manualmente**.

### 2. Operación — no perder datos ni romper el repo

**Backups automáticos**
- Workflow semanal (domingos 04:00 UTC) que hace dump de la base Supabase y guarda el artefacto 30 días en GitHub Actions.

**Dependabot**
- PRs automáticos para actualizar dependencias Flutter y GitHub Actions, reduciendo vulnerabilidades y roturas por deps viejas.

**Deuda técnica**
- Revisión trimestral; mantener deuda ≤ 5% del backlog (criterio de gestión, no código).

### 3. Evolución — features “Could” post-lanzamiento

Cosas deseables pero no bloqueantes:

| Feature | Descripción |
|---------|-------------|
| Canto/tarareo | Responder con micrófono en lugar de piano/teclado |
| Solfeo Do/Re/Mi | Además de C/D/E |
| Push notifications | “Tienes notas vencidas para repasar” |
| Export CSV | Ya hecho en Fase 5 |

---

## Métricas de negocio (objetivos, no código)

La fase también define **KPIs** a perseguir:

- **Retención D7** — ¿vuelven a la semana?
- **CSAT ≥ 4.2/5** — encuesta in-app ocasional (aún no implementada)
- **Crash rate** — vía Sentry

Son metas de producto; la infraestructura (analytics + Sentry) es el soporte para medirlos.

---

## Estado actual en el repo

| Entregable | Estado |
|------------|--------|
| Analytics + `metrics_daily` + script | ✅ Código listo |
| Sentry opcional | ✅ Código listo (falta `SENTRY_DSN` en prod) |
| Backups Supabase | ✅ Workflow listo (faltan secrets) |
| Dependabot | ✅ Configurado |
| Uptime externo | ⏳ Manual |
| Canto, solfeo, push | ⏳ Could — no empezado |
| Encuesta CSAT in-app | ⏳ No implementada |

En resumen: **Fase 6 = mantener TOGESC vivo, medible y seguro en producción**, mientras se priorizan mejoras pedagógicas según lo que digan las métricas.

Si quieres, puedo detallar solo la parte de analytics (qué eventos se registran y cómo leer `metrics_daily`) o lo que falta para cerrar la Fase 6 operativamente.


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]
