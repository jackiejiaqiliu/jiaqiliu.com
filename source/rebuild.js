// Shared image viewer. Each gallery retains its own image order and descriptions.
(() => {
  'use strict';
  let active = [];
  let index = 0;
  let opener;
  const dialog = document.createElement('dialog');
  dialog.className = 'local-lightbox';
  dialog.setAttribute('aria-label', 'Image viewer');
  dialog.innerHTML = '<img alt=""><button class="close" aria-label="Close">×</button>' +
    '<button class="prev" aria-label="Previous image">‹</button>' +
    '<button class="next" aria-label="Next image">›</button>';
  document.body.append(dialog);
  const image = dialog.querySelector('img');

  function show(nextIndex) {
    index = (nextIndex + active.length) % active.length;
    image.src = active[index].dataset.full;
    image.alt = active[index].querySelector('img').alt;
  }

  function close() {
    dialog.close();
    document.body.style.overflow = '';
    opener?.focus();
  }

  document.querySelectorAll('[data-full]').forEach(item => {
    item.addEventListener('click', () => {
      opener = item;
      active = [...item.closest('.local-gallery').querySelectorAll('[data-full]')];
      show(active.indexOf(item));
      dialog.showModal();
      document.body.style.overflow = 'hidden';
    });
  });
  dialog.querySelector('.close').onclick = close;
  dialog.querySelector('.prev').onclick = () => show(index - 1);
  dialog.querySelector('.next').onclick = () => show(index + 1);
  dialog.addEventListener('cancel', event => {
    event.preventDefault();
    close();
  });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') show(index - 1);
    if (event.key === 'ArrowRight') show(index + 1);
  });
})();

// Use the captured responsive navigation DOM and its existing open-state class.
(() => {
  const trigger = document.querySelector('svg[aria-label="Open Site Navigation"]')?.closest('button');
  const menu = document.querySelector('[data-block-level-container="MenuContainer"]')?.parentElement;
  if (!trigger || !menu) return;
  const dialog = menu.querySelector('[role="dialog"]');
  const closeButton = menu.querySelector('button');
  trigger.setAttribute('aria-label', 'Open Site Navigation');
  trigger.setAttribute('aria-controls', menu.id);
  trigger.setAttribute('aria-expanded', 'false');
  menu.setAttribute('aria-hidden', 'true');
  menu.inert = true;
  closeButton?.setAttribute('aria-label', 'Close Site Navigation');
  let previousOverflow = '';

  function close() {
    menu.classList.remove('Wy7QN0');
    menu.inert = true;
    menu.setAttribute('aria-hidden', 'true');
    trigger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = previousOverflow;
    trigger.focus();
  }

  trigger.onclick = () => {
    previousOverflow = document.body.style.overflow;
    menu.inert = false;
    menu.classList.add('Wy7QN0');
    menu.setAttribute('aria-hidden', 'false');
    trigger.setAttribute('aria-expanded', 'true');
    dialog?.setAttribute('aria-modal', 'true');
    document.body.style.overflow = 'hidden';
    closeButton?.focus();
  };
  if (closeButton) closeButton.onclick = close;
  menu.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      event.preventDefault();
      close();
    }
    if (event.key === 'Tab') {
      const focusables = [...menu.querySelectorAll('a[href],button')];
      const first = focusables[0];
      const last = focusables.at(-1);
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });
})();
