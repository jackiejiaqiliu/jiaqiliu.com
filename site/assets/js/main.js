'use strict';

const menu = document.querySelector('.mobile-menu');
const menuTrigger = document.querySelector('.menu-open');
const lightbox = document.querySelector('.lightbox');
const viewerImage = lightbox?.querySelector('img');
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
window.matchMedia('(min-width: 601px)').addEventListener('change', event => {
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
lightbox?.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
lightbox?.querySelector('.lightbox-previous').addEventListener('click', () => showImage(imageIndex - 1));
lightbox?.querySelector('.lightbox-next').addEventListener('click', () => showImage(imageIndex + 1));
lightbox?.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    showImage(imageIndex + (event.key === 'ArrowLeft' ? -1 : 1));
  }
});
// Escape uses each dialog's native cancel/close behavior, including focus return.

// Only the description sticks; both columns use the document scrollport.
const projectDetail = document.querySelector('.project-page .project');
if (projectDetail) {
  const columns = [...projectDetail.querySelectorAll('.project-copy, .project-gallery')];
  const header = document.querySelector('.site-header');
  const pagination = document.querySelector('.project-page > .project-pagination');
  const desktop = window.matchMedia('(min-width: 1001px)');
  let pendingLayout = false;

  function updateStickyColumn() {
    pendingLayout = false;
    const copy = projectDetail.querySelector('.project-copy');
    const media = projectDetail.querySelector('.project-gallery');
    const navigationBottom = header.getBoundingClientRect().height +
      (pagination ? pagination.getBoundingClientRect().height : 0) +
      (desktop.matches ? parseFloat(getComputedStyle(projectDetail).marginTop) || 0 : 0);
    // One top anchor from the start. The grid container's bottom is the only
    // release boundary; tall descriptions reveal their remaining text as they
    // leave with the section, without an initial slide into a second anchor.
    projectDetail.style.setProperty('--project-sticky-top', `${navigationBottom}px`);
    copy.classList.toggle('sticky-project-column', desktop.matches);
    media.classList.remove('sticky-project-column');
  }

  function scheduleStickyColumn() {
    if (pendingLayout) return;
    pendingLayout = true;
    requestAnimationFrame(updateStickyColumn);
  }

  const columnResize = new ResizeObserver(scheduleStickyColumn);
  columns.forEach(column => columnResize.observe(column));
  columnResize.observe(header);
  if (pagination) columnResize.observe(pagination);
  window.addEventListener('resize', scheduleStickyColumn, {passive: true});
  projectDetail.addEventListener('load', scheduleStickyColumn, true);
  document.fonts.ready.then(scheduleStickyColumn);
  updateStickyColumn();
}
