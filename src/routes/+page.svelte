<script>
  import { fade, fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import Hero from '$lib/components/Hero.svelte';
  import Invitation from '$lib/components/Invitation.svelte';

  let partyUnlocked = $state(false);
  let showInvitation = $state(false);

  async function handleUnlock() {
    partyUnlocked = true;

    // Wait for Hero fade-out to finish (500ms)
    await new Promise((r) => setTimeout(r, 500));
    showInvitation = true;

    // Confetti from both sides for 3 seconds
    const confetti = (await import('canvas-confetti')).default;
    const colors = ['#93C5FD', '#C0C0C0', '#FFFFFF', '#60A5FA', '#BFDBFE'];
    const end = Date.now() + 3000;
    (function frame() {
      confetti({ particleCount: 4, angle: 60,  spread: 55, origin: { x: 0 }, colors });
      confetti({ particleCount: 4, angle: 120, spread: 55, origin: { x: 1 }, colors });
      if (Date.now() < end) requestAnimationFrame(frame);
    })();

    // Audio — safe to call here because we're inside a user gesture handler
    new Audio('/Music_ly_mp3.mp3').play().catch(() => {});
  }
</script>

<svelte:head>
  <title>David • 18 Años</title>
  <meta name="description" content="Invitación a los 18 años de David — Sábado 17 de octubre de 2026, 5:00 PM" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://david-18.vercel.app/" />
  <meta property="og:title" content="David • 18 Años 🎉" />
  <meta property="og:description" content="¡Estás invitado a celebrar mis 18 años! Sábado 17 de octubre de 2026, 5:00 PM." />
  <meta property="og:image" content="https://david-18.vercel.app/og-image.jpg" />
  <meta property="og:image:secure_url" content="https://david-18.vercel.app/og-image.jpg" />
</svelte:head>

{#if !partyUnlocked}
  <div out:fly={{ y: -80, duration: 600, easing: quintOut }} style="position:fixed;inset:0;z-index:50;">
    <Hero onUnlock={handleUnlock} />
  </div>
{/if}

{#if showInvitation}
  <div in:fly={{ y: 60, duration: 700, easing: quintOut }}>
    <Invitation />
  </div>
{/if}
