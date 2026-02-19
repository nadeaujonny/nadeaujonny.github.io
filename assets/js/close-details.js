(() => {
  const detailsList = Array.from(document.querySelectorAll('details'));
  if (!detailsList.length) {
    return;
  }

  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'floating-close-btn';
  button.textContent = 'Close section';
  button.hidden = true;
  button.setAttribute('aria-hidden', 'true');
  button.setAttribute('aria-label', 'Close the current open section');

  let lastActiveOpen = null;

  const updateButtonVisibility = () => {
    const openDetails = detailsList.filter((detail) => detail.open);
    if (openDetails.length === 0) {
      lastActiveOpen = null;
      button.hidden = true;
      button.setAttribute('aria-hidden', 'true');
      return;
    }

    if (!lastActiveOpen || !lastActiveOpen.open) {
      lastActiveOpen = openDetails[openDetails.length - 1];
    }

    button.hidden = false;
    button.setAttribute('aria-hidden', 'false');
  };

  detailsList.forEach((detail) => {
    detail.addEventListener('toggle', () => {
      if (detail.open) {
        lastActiveOpen = detail;
      }
      updateButtonVisibility();
    });
  });

  document.addEventListener('focusin', (event) => {
    const focusedDetail = event.target.closest('details');
    if (focusedDetail && focusedDetail.open) {
      lastActiveOpen = focusedDetail;
      updateButtonVisibility();
    }
  });

  document.addEventListener('click', (event) => {
    const clickedDetail = event.target.closest('details');
    if (clickedDetail && clickedDetail.open) {
      lastActiveOpen = clickedDetail;
      updateButtonVisibility();
    }
  });

  button.addEventListener('click', () => {
    if (lastActiveOpen && lastActiveOpen.open) {
      const target = lastActiveOpen;
      // Hide button immediately for snappy feedback
      lastActiveOpen = null;
      button.hidden = true;
      button.setAttribute('aria-hidden', 'true');

      if (target._animatedClose) {
        target._animatedClose();
      } else {
        target.open = false;
      }
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });

  document.body.appendChild(button);
  updateButtonVisibility();
})();
