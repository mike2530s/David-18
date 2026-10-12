/**
 * Svelte action: adds 'is-revealed' when the element enters the viewport.
 * Pair with CSS class 'reveal-on-scroll' for the visual transition.
 */
export function scrollReveal(node) {
  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        node.classList.add('is-revealed');
        observer.unobserve(node);
      }
    },
    { threshold: 0.12 }
  );
  observer.observe(node);
  return { destroy: () => observer.disconnect() };
}
