document.documentElement.classList.add('js');

const menuButton = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('#main-nav');

if (menuButton && mainNav) {
  menuButton.hidden = false;

  function closeMenu(returnFocus = false) {
    mainNav.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.textContent = 'Menu';
    if (returnFocus) menuButton.focus();
  }

  menuButton.addEventListener('click', () => {
    const open = mainNav.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.textContent = open ? 'Close' : 'Menu';
  });

  mainNav.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link) return;
    closeMenu();
  });

  document.addEventListener('click', event => {
    if (mainNav.classList.contains('open') && !mainNav.contains(event.target) && !menuButton.contains(event.target)) {
      closeMenu();
    }
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && mainNav.classList.contains('open')) closeMenu(true);
  });

  window.matchMedia('(max-width: 760px)').addEventListener('change', () => closeMenu());
}

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!reduceMotion && 'IntersectionObserver' in window) {
  const revealTargets = document.querySelectorAll(
    '.section-head, .profile-grid, .capability-grid article, .career-case, .architecture-grid, .quality-workflow li, .ai-grid, .two-columns article, .api-practices article, .project-row, .toolkit > div, .contact-grid'
  );
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -35px 0px' });

  revealTargets.forEach((element, index) => {
    element.classList.add('reveal');
    element.style.setProperty('--reveal-index', index % 4);
    revealObserver.observe(element);
  });
}

const progressTrack = document.createElement('div');
progressTrack.className = 'scroll-progress';
progressTrack.setAttribute('aria-hidden', 'true');
progressTrack.innerHTML = '<span></span>';
document.body.append(progressTrack);
const progressFill = progressTrack.firstElementChild;
let scrollFrame = 0;

function updateScrollProgress() {
  const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = scrollableHeight > 0 ? Math.min(window.scrollY / scrollableHeight, 1) : 0;
  progressFill.style.transform = `scaleX(${progress})`;
  scrollFrame = 0;
}

window.addEventListener('scroll', () => {
  if (!scrollFrame) scrollFrame = window.requestAnimationFrame(updateScrollProgress);
}, { passive: true });
window.addEventListener('resize', updateScrollProgress, { passive: true });
updateScrollProgress();

const sectionLinks = new Map(
  [...document.querySelectorAll('#main-nav a[href^="#"]')]
    .map(link => [document.querySelector(link.getAttribute('href')), link])
    .filter(([section]) => section)
);

if ('IntersectionObserver' in window && sectionLinks.size) {
  const activeSectionObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      sectionLinks.forEach(link => link.removeAttribute('aria-current'));
      sectionLinks.get(entry.target)?.setAttribute('aria-current', 'location');
    });
  }, { rootMargin: '-18% 0px -68% 0px', threshold: 0 });
  sectionLinks.forEach((_, section) => activeSectionObserver.observe(section));
}
