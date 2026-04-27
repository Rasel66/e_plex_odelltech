// Hero Carousel
(function() {
  const slides = document.querySelectorAll('.slide');
  const dots   = document.querySelectorAll('.cdot');
  const bar    = document.getElementById('heroProgress');
  const DURATION = 4000;
  let current = 0, timer;

  function goTo(n) {
    slides[current].classList.remove('active');
    dots[current].classList.remove('active');
    current = (n + slides.length) % slides.length;
    slides[current].classList.add('active');
    dots[current].classList.add('active');
    restartBar();
  }
  function restartBar() {
    bar.style.transition = 'none';
    bar.style.width = '0%';
    requestAnimationFrame(() => requestAnimationFrame(() => {
      bar.style.transition = `width ${DURATION}ms linear`;
      bar.style.width = '100%';
    }));
  }
  function startAuto() {
    clearInterval(timer);
    timer = setInterval(() => goTo(current + 1), DURATION);
  }
  document.getElementById('heroNext').addEventListener('click', () => { goTo(current + 1); startAuto(); });
  document.getElementById('heroPrev').addEventListener('click', () => { goTo(current - 1); startAuto(); });
  dots.forEach((d, i) => d.addEventListener('click', () => { goTo(i); startAuto(); }));
  restartBar(); startAuto();
})();