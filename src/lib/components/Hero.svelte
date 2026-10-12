<script>
  let { onUnlock } = $props();
</script>

<section
  class="fixed inset-0 flex flex-col items-center justify-center bg-party-navy"
  style="background-image: url('/david.png'); background-size: cover; background-position: center top;"
>
  <!-- Dark gradient overlay -->
  <div class="absolute inset-0 bg-gradient-to-b from-black/20 via-party-navy/40 to-party-navy/90"></div>

  <!-- Floating sparkles -->
  <div class="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
    {#each [
      { top: '10%', left: '8%',  delay: '0s',    size: 'text-xl' },
      { top: '20%', left: '85%', delay: '0.8s',  size: 'text-2xl' },
      { top: '35%', left: '92%', delay: '1.6s',  size: 'text-lg' },
      { top: '60%', left: '5%',  delay: '0.4s',  size: 'text-2xl' },
      { top: '75%', left: '88%', delay: '1.2s',  size: 'text-xl' },
      { top: '85%', left: '15%', delay: '2s',    size: 'text-lg' },
    ] as s}
      <span
        class="absolute animate-sparkle {s.size} select-none"
        style="top:{s.top}; left:{s.left}; animation-delay:{s.delay};"
      >✨</span>
    {/each}
  </div>

  <!-- Content -->
  <div class="relative z-10 flex flex-col items-center gap-6 px-6 text-center">
    <div class="animate-float">
      <p class="font-display text-party-silver text-lg tracking-[0.3em] uppercase mb-1">
        Te invita a celebrar
      </p>
      <h1 class="font-display text-white text-5xl sm:text-7xl font-bold drop-shadow-lg">
        David
      </h1>
      <div class="flex items-center justify-center gap-3 mt-2">
        <span class="h-px w-12 bg-party-silver/60"></span>
        <span class="font-display text-party-light text-2xl sm:text-3xl font-bold tracking-widest">
          18 Años
        </span>
        <span class="h-px w-12 bg-party-silver/60"></span>
      </div>
    </div>

    <button
      onclick={onUnlock}
      class="
        mt-4 px-8 py-5 rounded-2xl
        bg-gradient-to-r from-party-light via-blue-400 to-party-light
        text-party-navy font-body font-bold text-lg sm:text-xl
        shadow-[0_0_30px_rgba(147,197,253,0.6)]
        hover:shadow-[0_0_50px_rgba(147,197,253,0.9)]
        hover:scale-105 transition-all duration-200
        animate-pulse-slow
        cursor-pointer select-none
      "
    >
      🎉 ¡Desbloquear la fiesta!
    </button>
  </div>
</section>
