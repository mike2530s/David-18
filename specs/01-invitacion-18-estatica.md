# SPEC 01 — Invitación de 18 años: Hero, transición y contenido animado

> **Estado:** Aprobado
> **Depende de:** —
> **Fecha:** 2026-10-11
> **Objetivo:** Crear la app SvelteKit base con la pantalla Hero, la transición confeti+audio y el contenido de la invitación con animaciones al scroll.

---

## Alcance

**Dentro:**

- Setup del proyecto: SvelteKit (Svelte 5 + Runes), Tailwind CSS, `@sveltejs/adapter-vercel`, `canvas-confetti`.
- `Hero.svelte`: pantalla completa con `static/david.png` (fallback: gradiente CSS azul marino → azul claro), botón "¡Desbloquear la fiesta!" con `animate-pulse` de Tailwind.
- Transición al presionar el botón: fade-out Hero, fade-in Invitation, confeti en toda la pantalla, reproducción de `static/Music_ly_mp3.mp3`.
- `Invitation.svelte`: texto exacto de la invitación, detalles del evento (sábado 17 oct 2026, 5:00 PM), botón "Cómo llegar" (`target="_blank"`) → Google Maps.
- Animaciones al scroll: Svelte action con IntersectionObserver + clases CSS Tailwind.
- Paleta: azul claro (`#93C5FD`), azul marino (`#1E3A5F`), blanco (`#FFFFFF`), plata (`#C0C0C0`).
- `.env.example` con las llaves de Firebase y Cloudinary documentadas (aunque no se usan en este spec).
- Deploy target: Vercel.

**Fuera de alcance (para SPEC 02):**

- Formulario de galería (nombre, teléfono, archivo).
- Integración con Cloudinary.
- Integración con Firebase Firestore.
- Galería masonry en tiempo real.
- Panel de administración o moderación de fotos.

---

## Modelo de datos

Este spec no introduce estructuras persistentes. El único estado es local en `+page.svelte`:

```js
// Svelte 5 Runes
let partyUnlocked = $state(false); // false = Hero visible, true = Invitation visible
```

---

## Plan de implementación

1. Crear el proyecto: `npm create svelte@latest davi-18` (Svelte 5, sin TypeScript obligatorio). Instalar dependencias:
   ```bash
   npm i -D tailwindcss postcss autoprefixer @sveltejs/adapter-vercel
   npm i canvas-confetti
   ```
2. Configurar `svelte.config.js` con `adapter-vercel`. Configurar `tailwind.config.js` con la paleta del evento (tokens: `party-light`, `party-navy`, `party-silver`).
3. Crear `src/lib/actions/scrollReveal.js`: Svelte action (~15 líneas) que usa `IntersectionObserver` para agregar la clase `is-revealed` cuando el elemento entra al viewport; limpiar el observer en `destroy`.
4. Crear `src/lib/components/Hero.svelte`: fondo `url('/david.png')` con fallback `background-color` del gradiente. Botón con `animate-pulse`. Al click llama a `onUnlock()` (prop o evento).
5. Crear `src/lib/components/Invitation.svelte`: secciones con el texto exacto de la invitación, detalles del evento y botón "Cómo llegar". Cada bloque usa la action `scrollReveal` con clase `is-revealed` para fade-in + slide-up.
6. Crear `src/routes/+page.svelte`: orquesta Hero e Invitation. Al `onUnlock`:
   - `partyUnlocked = true` (dispara la transición CSS fade-out/fade-in).
   - `(await import('canvas-confetti')).default({ ... })` (importación dinámica para evitar error SSR).
   - `new Audio('/Music_ly_mp3.mp3').play()` (dentro del handler de clic del usuario — autoplay permitido).
7. Copiar los archivos reales a `static/`:
   - `static/david.png`: la foto del festejado (ya existe en la raíz del repo).
   - `static/Music_ly_mp3.mp3`: la canción (ya existe en la raíz del repo).
8. Crear `.env.example` con todos los campos necesarios para SPEC 02:
   ```
   PUBLIC_FIREBASE_API_KEY=
   PUBLIC_FIREBASE_AUTH_DOMAIN=
   PUBLIC_FIREBASE_PROJECT_ID=
   PUBLIC_FIREBASE_STORAGE_BUCKET=
   PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
   PUBLIC_FIREBASE_APP_ID=
   PUBLIC_CLOUDINARY_CLOUD_NAME=
   PUBLIC_CLOUDINARY_UPLOAD_PRESET=
   ```
9. Verificar en mobile (`npm run dev` + dispositivo real o túnel). Ejecutar `npm run build` sin errores. Deploy a Vercel.

---

## Criterios de aceptación

- [ ] La app carga en `/` sin errores en la consola del navegador.
- [ ] El Hero ocupa 100% de la pantalla (`h-screen w-screen`) en mobile (375px) y desktop.
- [ ] El botón "¡Desbloquear la fiesta!" muestra animación de pulso continua (`animate-pulse`).
- [ ] Al hacer clic: el Hero desaparece con fade-out y la Invitation aparece con fade-in (duración total ≤ 600ms).
- [ ] El confeti cubre toda la pantalla durante ≥ 3 segundos al hacer clic.
- [ ] El audio `static/Music_ly_mp3.mp3` comienza a reproducirse al clic sin error en consola.
- [ ] El texto exacto de la invitación está visible y sin recortes en pantalla de 375px de ancho.
- [ ] Las secciones de la invitación entran con animación al hacer scroll (no aparecen todas de golpe).
- [ ] El botón "Cómo llegar" abre la URL del mapa de Google en una nueva pestaña.
- [ ] La paleta azul claro / azul marino / blanco / plata es coherente en todos los componentes.
- [ ] `npm run build` termina sin errores ni advertencias de SSR.
- [ ] El proyecto deployado en Vercel carga en < 3s en una conexión 4G simulada.

---

## Decisiones

- **Sí: Svelte 5 + Runes.** Proyecto nuevo, sin deuda de migración. `$state` es más limpio para `partyUnlocked` que un store writable.
- **No: Svelte 4 + stores.** Sin razón para usarlo en un proyecto que parte de cero.
- **Sí: `adapter-vercel`.** Zero config, CDN automático, free tier. Firebase Hosting requeriría prerenderizado total o workaround SSR.
- **Sí: IntersectionObserver como Svelte action.** Sin dependencias extra, ~15 líneas, idiomático en Svelte 5.
- **No: librería AOS.** +14KB por algo que se resuelve con código nativo.
- **Sí: importación dinámica de `canvas-confetti`.** Evita error de SSR (`window is not defined`) sin configurar `ssr: false` en toda la página.
- **Sí: `static/david.png` y `static/Music_ly_mp3.mp3`.** Archivos reales ya disponibles en la raíz del repo; se copian a `static/` al crear el proyecto SvelteKit.
- **Sí: `target="_blank"` en "Cómo llegar".** El usuario no pierde la invitación abierta al ver el mapa.
- **Sí: `.env.example` con llaves de SPEC 02 desde ahora.** El proyecto queda listo para que SPEC 02 solo necesite rellenar valores, no rediseñar la configuración.

---

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Autoplay de audio bloqueado por política del navegador | El audio se dispara dentro del handler del click del usuario — gesto explícito, los navegadores modernos lo permiten sin workaround. |
| `image_e50adf.jpg` no existe o falla al cargar | El CSS define un gradiente azul marino como `background-color` detrás del `background-image`. Si la imagen falla, el gradiente es el fallback visible. |
| `canvas-confetti` accede a `window` en SSR | Importación dinámica `await import('canvas-confetti')` dentro del handler resuelve el problema sin afectar el resto de la página. |

---

## Qué NO está en este spec

- Formulario de subida de fotos.
- Integración con Cloudinary ni con Firebase.
- Galería masonry ni actualizaciones en tiempo real.
- Panel de administración.

Todo lo anterior va en **SPEC 02**.
