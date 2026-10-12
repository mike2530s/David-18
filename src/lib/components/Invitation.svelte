<script>
  import { scrollReveal } from '$lib/actions/scrollReveal.js';
  import RSVP from '$lib/components/RSVP.svelte';
  import FloatingMonkey from '$lib/components/FloatingMonkey.svelte';
  import PhotoUpload from '$lib/components/PhotoUpload.svelte';
  import Gallery from '$lib/components/Gallery.svelte';

  function handleRsvpSuccess() {}
</script>

<main class="relative min-h-screen bg-gradient-to-b from-[#0a1929] via-party-navy to-[#0a1929] stars-bg font-body text-white overflow-x-hidden">

  <!-- Foto de David entre el fondo y las cards -->
  <div class="fixed inset-0 pointer-events-none z-0 overflow-hidden flex items-center justify-center">
    <img
      src="/david.png"
      alt=""
      aria-hidden="true"
      class="w-full h-full object-cover object-top opacity-60 filter contrast-105 brightness-95"
    />
    <div class="absolute inset-0 bg-gradient-to-b from-[#0a1929]/75 via-party-navy/60 to-[#0a1929]/85"></div>
  </div>

  <!-- Monito flotante que anda siempre por la pantalla -->
  <FloatingMonkey />

  <div class="relative z-10">

    <!-- Foto card de David -->
    <div class="flex flex-col items-center pt-10 pb-2 px-6">
      <div class="
        w-48 h-60 sm:w-56 sm:h-72
        rounded-3xl overflow-hidden
        border-2 border-party-silver/40
        shadow-[0_0_40px_rgba(147,197,253,0.3)]
        animate-float
      ">
        <img
          src="/david.png"
          alt="David"
          class="w-full h-full object-cover object-top"
        />
      </div>
    </div>

    <!-- Top ornament -->
  <div class="flex flex-col items-center pt-4 pb-6 px-6">
    <div class="flex items-center gap-4 mb-2">
      <span class="h-px flex-1 max-w-[60px] bg-party-silver/40"></span>
      <span class="text-party-silver text-3xl">✦</span>
      <span class="h-px flex-1 max-w-[60px] bg-party-silver/40"></span>
    </div>
    <p class="text-party-silver tracking-[0.35em] uppercase text-xs">Una noche especial</p>
  </div>

  <!-- Main invitation card -->
  <article
    use:scrollReveal
    class="reveal-on-scroll mx-auto max-w-sm sm:max-w-md px-6"
  >
    <div class="
      rounded-3xl border border-party-silver/20
      bg-white/5 backdrop-blur-sm
      p-8 shadow-2xl
    ">
      <!-- Name header -->
      <h2 class="font-display text-party-light text-4xl sm:text-5xl font-bold text-center mb-6 drop-shadow">
        David
      </h2>

      <!-- Invitation text -->
      <p class="font-display text-white/90 text-base sm:text-lg leading-relaxed text-center italic">
        "Hay momentos en la vida que merecen celebrarse en grande, y este es uno de ellos.
        Te considero una persona muy especial en mi vida, por lo que será un verdadero honor
        contar con tu presencia en mis 18 años. Nos espera una noche inolvidable: buena comida,
        el mejor ambiente con grupo norteño, banda y sonido hasta que el cuerpo aguante.
        Espero contar con tu asistencia. ¡No faltes!"
      </p>
    </div>
  </article>

  <!-- Divider -->
  <div
    use:scrollReveal
    class="reveal-on-scroll flex items-center gap-4 max-w-xs mx-auto px-6 my-8"
  >
    <span class="h-px flex-1 bg-party-light/30"></span>
    <span class="text-party-light text-xl">💫</span>
    <span class="h-px flex-1 bg-party-light/30"></span>
  </div>

  <!-- Event details -->
  <section
    use:scrollReveal
    class="reveal-on-scroll mx-auto max-w-sm sm:max-w-md px-6"
  >
    <div class="
      rounded-3xl border border-party-light/30
      bg-party-navy/60 backdrop-blur-sm
      p-6 shadow-lg
    ">
      <h3 class="font-display text-party-silver text-xl text-center mb-5 tracking-wide uppercase text-sm">
        Detalles del evento
      </h3>

      <div class="space-y-4">
        <div class="flex items-center gap-4">
          <span class="text-2xl">📅</span>
          <div>
            <p class="text-party-light font-bold text-base">Sábado 17 de octubre de 2026</p>
            <p class="text-white/60 text-sm">¡Aparta la fecha!</p>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-2xl">🕔</span>
          <div>
            <p class="text-party-light font-bold text-base">5:00 PM</p>
            <p class="text-white/60 text-sm">¡No llegues tarde!</p>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-2xl">🎶</span>
          <div>
            <p class="text-party-light font-bold text-base">Grupo Norteño & Banda</p>
            <p class="text-white/60 text-sm">Sonido hasta que el cuerpo aguante</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Location button -->
  <div
    use:scrollReveal
    class="reveal-on-scroll flex justify-center mt-8 px-6"
  >
    <a
      href="https://www.google.com/maps?q=20.867156982421875,-100.70508575439453&z=17&hl=en"
      target="_blank"
      rel="noopener noreferrer"
      class="
        inline-flex items-center gap-3
        px-8 py-4 rounded-2xl
        bg-gradient-to-r from-party-navy via-blue-800 to-party-navy
        border border-party-light/50
        text-party-light font-bold text-base
        shadow-[0_0_20px_rgba(147,197,253,0.3)]
        hover:shadow-[0_0_35px_rgba(147,197,253,0.6)]
        hover:scale-105 hover:border-party-light
        transition-all duration-200
      "
    >
      <span class="text-xl">📍</span>
      Cómo llegar
    </a>
  </div>

  <!-- RSVP / Confirmar asistencia (confidencial) -->
  <RSVP onRegistered={handleRsvpSuccess} />

  <!-- Photo upload form & Legal warning -->
  <PhotoUpload />

  <!-- Live masonry gallery -->
  <Gallery />

  <!-- Bottom ornament -->
  <div
    use:scrollReveal
    class="reveal-on-scroll flex flex-col items-center pt-12 pb-16 px-6 gap-2"
  >
    <div class="flex items-center gap-4">
      <span class="h-px flex-1 max-w-[60px] bg-party-silver/40"></span>
      <span class="text-party-silver text-2xl">✦</span>
      <span class="h-px flex-1 max-w-[60px] bg-party-silver/40"></span>
    </div>
    <p class="text-party-silver/60 text-xs tracking-widest uppercase mt-2">
      Con todo el amor del mundo 🤍
    </p>
  </div>

  </div>
</main>
