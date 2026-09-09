(() => {
  const burger = document.querySelector('.nav-burger');
  const links = document.getElementById('primary-nav');
  if (!burger || !links) return;

  const close = () => {
    burger.setAttribute('aria-expanded', 'false');
    links.classList.remove('is-open');
    document.body.classList.remove('nav-open');
  };

  burger.addEventListener('click', () => {
    const open = burger.getAttribute('aria-expanded') === 'true';
    burger.setAttribute('aria-expanded', String(!open));
    links.classList.toggle('is-open', !open);
    document.body.classList.toggle('nav-open', !open);
  });

  links.querySelectorAll('a').forEach((a) => a.addEventListener('click', close));

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) close();
  });
})();
