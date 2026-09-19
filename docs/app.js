document.documentElement.classList.add('js');
const menuButton = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('#main-nav');
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
  mainNav.querySelectorAll('a').forEach(item => item.removeAttribute('aria-current'));
  if (link.hash) link.setAttribute('aria-current', 'location');
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && mainNav.classList.contains('open')) closeMenu(true);
});
window.matchMedia('(max-width: 760px)').addEventListener('change', () => closeMenu());
