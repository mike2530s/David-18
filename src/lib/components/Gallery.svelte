<script>
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  import { collection, addDoc, onSnapshot, orderBy, query, serverTimestamp, doc, deleteDoc } from 'firebase/firestore';
  import { db } from '$lib/firebase.js';
  import { uploadToCloudinary } from '$lib/cloudinary.js';
  import { scrollReveal } from '$lib/actions/scrollReveal.js';

  // Sábado 17 de octubre de 2026 a las 4:00 PM (hora centro México, CDT = UTC-5)
  const PARTY_DATE = new Date('2026-10-17T16:00:00-05:00');

  let now = $state(new Date());
  // ?unlock=true o ?preview=true desbloquea la galería para pruebas
  const testMode = typeof window !== 'undefined' && (
    new URLSearchParams(window.location.search).get('unlock') === 'true' ||
    new URLSearchParams(window.location.search).get('preview') === 'true'
  );
  let isOpen = $derived(testMode || now >= PARTY_DATE);

  let timeLeft = $derived(() => {
    const diff = PARTY_DATE - now;
    if (diff <= 0) return null;
    return {
      dias:     Math.floor(diff / 86400000),
      horas:    Math.floor((diff % 86400000) / 3600000),
      minutos:  Math.floor((diff % 3600000)  / 60000),
      segundos: Math.floor((diff % 60000)    / 1000)
    };
  });

  let nombre   = $state('');
  let telefono = $state('');
  let archivo  = $state(null);
  let preview  = $state('');
  let enviando = $state(false);
  let error    = $state('');
  let exito    = $state(false);
  let fotos    = $state([]);

  onMount(() => {
    // Tick cada segundo para el countdown
    const tick = setInterval(() => { now = new Date(); }, 1000);

    // Listener en tiempo real de Firestore
    const q = query(collection(db, 'invitados_fotos'), orderBy('timestamp', 'desc'));
    const unsub = onSnapshot(q, (snap) => {
      fotos = snap.docs.map((d) => ({ id: d.id, ...d.data() }));
    });

    return () => { clearInterval(tick); unsub(); };
  });

  function handleFile(e) {
    const f = e.target.files?.[0];
    if (!f) return;
    archivo = f;
    preview = URL.createObjectURL(f);
    e.target.value = '';
  }

  async function handleSubmit(e) {
    e.preventDefault();
    error = '';
    if (!nombre.trim())              { error = 'Escribe tu nombre.'; return; }
    if (!/^\d{10}$/.test(telefono))  { error = 'El teléfono debe tener exactamente 10 dígitos.'; return; }
    if (!archivo)                    { error = 'Selecciona una foto.'; return; }

    enviando = true;
    try {
      const url_foto = await uploadToCloudinary(archivo);
      await addDoc(collection(db, 'invitados_fotos'), {
        url_foto,
        nombre: nombre.trim(),
        telefono,
        timestamp: serverTimestamp()
      });
      nombre = ''; telefono = ''; archivo = null; preview = '';
      exito = true;
      setTimeout(() => (exito = false), 4000);
    } catch {
      error = 'No se pudo subir la foto. Intenta de nuevo.';
    } finally {
      enviando = false;
    }
  }

  async function eliminarFoto(id) {
    if (!confirm('¿Deseas eliminar esta foto de la galería?')) return;
    try {
      await deleteDoc(doc(db, 'invitados_fotos', id));
    } catch (err) {
      console.error(err);
      alert('No se pudo eliminar la foto.');
    }
  }
</script>

<!-- ── Sección galería ──────────────────────────────────── -->
<section use:scrollReveal class="reveal-on-scroll mx-auto max-w-sm sm:max-w-md px-6 mt-12">
  <div class="rounded-3xl border border-party-light/30 bg-white/5 backdrop-blur-sm p-8 shadow-2xl">

    <h2 class="font-display text-party-light text-2xl font-bold text-center mb-2">
      📸 Galería de recuerdos
    </h2>
    <p class="text-white/70 text-sm text-center leading-relaxed mb-6">
      Los mejores recuerdos se construyen juntos. Ayúdanos a capturar cada momento de esta noche
      inolvidable: sube aquí tus fotos para que formen parte de nuestra galería compartida.
    </p>

    {#if !isOpen}
      <!-- ── Countdown ── -->
      <div class="text-center space-y-4">
        <p class="text-party-silver text-xs uppercase tracking-widest">La galería se abre en</p>

        {#if timeLeft()}
          <div class="grid grid-cols-4 gap-2">
            {#each [
              { v: timeLeft().dias,     l: 'Días' },
              { v: timeLeft().horas,    l: 'Horas' },
              { v: timeLeft().minutos,  l: 'Min' },
              { v: timeLeft().segundos, l: 'Seg' }
            ] as unit}
              <div class="flex flex-col items-center bg-party-navy/60 rounded-2xl py-3 border border-party-light/20">
                <span class="font-display text-party-light text-3xl font-bold leading-none">
                  {String(unit.v).padStart(2, '0')}
                </span>
                <span class="text-white/40 text-xs mt-1">{unit.l}</span>
              </div>
            {/each}
          </div>
        {/if}

        <p class="text-white/40 text-xs">
          🔒 Se abre el sábado 17 de octubre a las 4:00 PM
        </p>
      </div>

    {:else}
      <!-- ── Formulario de subida ── -->
      <form onsubmit={handleSubmit} class="space-y-4">
        <div>
          <label class="text-party-silver text-xs uppercase tracking-wider block mb-1" for="nombre">Tu nombre</label>
          <input
            id="nombre" type="text" bind:value={nombre} placeholder="¿Cómo te llamas?"
            class="w-full rounded-xl bg-white/10 border border-party-silver/30 text-white placeholder-white/30 px-4 py-3 text-sm focus:outline-none focus:border-party-light transition-colors"
          />
        </div>

        <div>
          <label class="text-party-silver text-xs uppercase tracking-wider block mb-1" for="tel">Teléfono (10 dígitos)</label>
          <input
            id="tel" type="tel" inputmode="numeric" maxlength="10" bind:value={telefono} placeholder="5512345678"
            class="w-full rounded-xl bg-white/10 border border-party-silver/30 text-white placeholder-white/30 px-4 py-3 text-sm focus:outline-none focus:border-party-light transition-colors"
          />
        </div>

        <div>
          <span class="text-party-silver text-xs uppercase tracking-wider block mb-2">Tu foto</span>
          {#if preview}
            <div class="relative w-full h-44 rounded-2xl overflow-hidden border border-party-light/40 bg-black/40">
              <img src={preview} alt="preview" class="w-full h-full object-cover" />
              <button
                type="button"
                onclick={() => { archivo = null; preview = ''; }}
                class="absolute top-2 right-2 bg-black/80 hover:bg-black text-white text-xs px-3 py-1.5 rounded-full border border-white/20 transition-colors flex items-center gap-1 shadow-lg"
              >
                ✕ Cambiar
              </button>
            </div>
          {:else}
            <div class="grid grid-cols-2 gap-3">
              <!-- Botón Cámara -->
              <label
                for="foto-camara"
                class="flex flex-col items-center justify-center p-4 rounded-2xl cursor-pointer border-2 border-dashed border-party-light/40 hover:border-party-light bg-white/5 active:scale-95 transition-all text-center"
              >
                <span class="text-3xl mb-1">📸</span>
                <span class="text-party-light text-xs font-semibold">Tomar foto</span>
                <span class="text-white/40 text-[10px] mt-0.5">Abrir cámara</span>
              </label>
              <input
                id="foto-camara"
                type="file"
                accept="image/*"
                capture="environment"
                onchange={handleFile}
                class="hidden"
              />

              <!-- Botón Galería -->
              <label
                for="foto-galeria"
                class="flex flex-col items-center justify-center p-4 rounded-2xl cursor-pointer border-2 border-dashed border-party-silver/40 hover:border-party-light bg-white/5 active:scale-95 transition-all text-center"
              >
                <span class="text-3xl mb-1">🖼️</span>
                <span class="text-party-silver text-xs font-semibold">De galería</span>
                <span class="text-white/40 text-[10px] mt-0.5">Elegir archivo</span>
              </label>
              <input
                id="foto-galeria"
                type="file"
                accept="image/*"
                onchange={handleFile}
                class="hidden"
              />
            </div>
          {/if}
        </div>

        {#if error}
          <p class="text-red-400 text-sm text-center" transition:fade>{error}</p>
        {/if}
        {#if exito}
          <p class="text-green-400 text-sm text-center font-bold" transition:fade>🎉 ¡Foto subida! Gracias por compartir el momento.</p>
        {/if}

        <button
          type="submit" disabled={enviando}
          class="w-full py-4 rounded-2xl font-bold text-base bg-gradient-to-r from-party-light via-blue-400 to-party-light text-party-navy disabled:opacity-50 hover:scale-[1.02] transition-transform shadow-[0_0_20px_rgba(147,197,253,0.3)]"
        >
          {enviando ? '⏳ Subiendo...' : '📤 Subir mi foto'}
        </button>

        <p class="text-white/40 text-xs text-center leading-relaxed pt-1">
          ⚠️ Aviso: Este es un evento familiar. No se permite subir fotografías no aptas para todo
          público. Si lo haces, atente a las consecuencias de las autoridades correspondientes.
        </p>
      </form>
    {/if}
  </div>
</section>

<!-- ── Galería en vivo ─────────────────────────────────── -->
{#if fotos.length > 0}
  <section use:scrollReveal class="reveal-on-scroll mx-auto max-w-sm sm:max-w-md px-6 mt-8 pb-4">
    <h3 class="font-display text-party-silver text-lg text-center mb-4 tracking-wide">✨ Fotos de la noche</h3>
    <div class="columns-2 gap-2">
      {#each fotos as foto (foto.id)}
        <div in:fade={{ duration: 400 }} class="break-inside-avoid mb-3 relative group">
          <img src={foto.url_foto} alt={foto.nombre} loading="lazy" class="w-full rounded-2xl object-cover shadow-lg" />
          <button
            onclick={() => eliminarFoto(foto.id)}
            class="absolute top-2 right-2 w-7 h-7 rounded-full bg-black/60 hover:bg-red-600 text-white flex items-center justify-center text-xs shadow-md backdrop-blur-sm transition-colors cursor-pointer"
            title="Eliminar foto"
            aria-label="Eliminar foto"
          >
            🗑️
          </button>
          <p class="text-white/70 text-xs text-center mt-1 pb-1">{foto.nombre}</p>
        </div>
      {/each}
    </div>
  </section>
{/if}
