'use strict';

const menu = document.querySelector('.mobile-menu');
const menuTrigger = document.querySelector('.menu-open');
const lightbox = document.querySelector('.lightbox');
const viewerImage = lightbox.querySelector('img');
const gallery = [...document.querySelectorAll('.project-image')];
let imageIndex = 0;

// Native modal dialogs contain keyboard focus and make the page behind them inert.
function openModal(dialog, opener) {
  const previousOverflow = document.body.style.overflow;
  dialog.showModal();
  document.body.style.overflow = 'hidden';
  dialog.addEventListener('close', () => {
    document.body.style.overflow = previousOverflow;
    opener.focus();
  }, {once: true});
}

menuTrigger.addEventListener('click', () => {
  openModal(menu, menuTrigger);
  menuTrigger.setAttribute('aria-expanded', 'true');
});
menu.querySelector('.menu-close').addEventListener('click', () => menu.close());
menu.addEventListener('close', () => menuTrigger.setAttribute('aria-expanded', 'false'));
window.matchMedia('(min-width: 1001px)').addEventListener('change', event => {
  if (event.matches && menu.open) menu.close();
});

function showImage(index) {
  imageIndex = (index + gallery.length) % gallery.length;
  const image = gallery[imageIndex].querySelector('img');
  viewerImage.src = image.src;
  viewerImage.alt = image.alt;
}
gallery.forEach((button, index) => {
  button.addEventListener('click', () => {
    showImage(index);
    openModal(lightbox, button);
  });
});
lightbox.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
lightbox.querySelector('.lightbox-previous').addEventListener('click', () => showImage(imageIndex - 1));
lightbox.querySelector('.lightbox-next').addEventListener('click', () => showImage(imageIndex + 1));
lightbox.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    showImage(imageIndex + (event.key === 'ArrowLeft' ? -1 : 1));
  }
});
// Escape uses each dialog's native cancel/close behavior, including focus return.
