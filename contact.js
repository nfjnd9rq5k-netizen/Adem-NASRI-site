(() => {
  const form = document.getElementById('contact-form');
  const sent = document.getElementById('contact-sent');
  const reset = document.getElementById('contact-reset');
  if (!form || !sent || !reset) return;

  const subjects = form.querySelectorAll('.subject');
  const subjectInput = form.querySelector('input[name="subject"]');
  subjects.forEach((b) => {
    b.addEventListener('click', () => {
      subjects.forEach((x) => x.classList.remove('is-active'));
      b.classList.add('is-active');
      subjectInput.value = b.dataset.value;
    });
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    form.hidden = true;
    sent.hidden = false;
  });

  reset.addEventListener('click', () => {
    form.reset();
    subjects.forEach((x) => x.classList.remove('is-active'));
    subjects[0].classList.add('is-active');
    subjectInput.value = subjects[0].dataset.value;
    sent.hidden = true;
    form.hidden = false;
  });
})();
