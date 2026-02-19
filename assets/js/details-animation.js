(() => {
  const DURATION = 300;
  const EASING = 'ease';

  document.querySelectorAll('details').forEach((details) => {
    const summary = details.querySelector('summary');
    if (!summary) return;

    let animation = null;
    let isClosing = false;
    let isExpanding = false;

    // Expose animated close for external callers (e.g., floating close button)
    details._animatedClose = () => {
      if (details.open) shrink();
    };

    summary.addEventListener('click', (e) => {
      e.preventDefault();
      if (isClosing || !details.open) {
        expand();
      } else if (isExpanding || details.open) {
        shrink();
      }
    });

    function expand() {
      if (animation) animation.cancel();
      isClosing = false;
      isExpanding = true;
      details.classList.remove('is-closing');

      const startHeight = details.offsetHeight;
      details.style.height = `${startHeight}px`;
      details.open = true;

      requestAnimationFrame(() => {
        const endHeight = details.scrollHeight;

        animation = details.animate(
          { height: [`${startHeight}px`, `${endHeight}px`] },
          { duration: DURATION, easing: EASING }
        );
        animation.onfinish = () => finish(true);
        animation.oncancel = () => { isExpanding = false; };
      });
    }

    function shrink() {
      if (animation) animation.cancel();
      isExpanding = false;
      isClosing = true;
      details.classList.add('is-closing');

      const startHeight = details.offsetHeight;
      const endHeight = summary.offsetHeight;

      animation = details.animate(
        { height: [`${startHeight}px`, `${endHeight}px`] },
        { duration: DURATION, easing: EASING }
      );
      animation.onfinish = () => finish(false);
      animation.oncancel = () => { isClosing = false; };
    }

    function finish(open) {
      details.open = open;
      animation = null;
      isClosing = false;
      isExpanding = false;
      details.style.height = '';
      details.classList.remove('is-closing');
    }
  });
})();
