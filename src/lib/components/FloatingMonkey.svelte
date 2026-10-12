<script>
  import { onMount } from 'svelte';

  let x = $state(50);
  let y = $state(80);
  let dir = $state(1);

  onMount(() => {
    let frame;
    let step = 0;
    function tick() {
      step++;
      x = 50 + 40 * Math.sin(step / 120);
      y = 80 + 8 * Math.sin(step / 60);
      dir = Math.cos(step / 120) > 0 ? 1 : -1;
      frame = requestAnimationFrame(tick);
    }
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  });
</script>

<div
  aria-hidden="true"
  class="fixed pointer-events-none z-20 select-none"
  style="left:{x}%; top:{y}%; transform: translateX(-50%) scaleX({dir});"
>
  <img src="/elmono.png" alt="" class="w-20 h-20 object-contain" />
</div>
