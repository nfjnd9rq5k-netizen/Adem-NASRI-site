(() => {
  const form = document.getElementById('contact-form');
  const sent = document.getElementById('contact-sent');
  const reset = document.getElementById('contact-reset');
  const statut = document.getElementById('contact-status');
  if (!form || !sent || !reset) return;

  const MAIL = 'nasri.adem@hotmail.fr';
  const bouton = form.querySelector('button[type="submit"]');
  const libelleBouton = bouton ? bouton.textContent : '';

  // ── Choix du sujet ────────────────────────────────────────────────────────
  const subjects = form.querySelectorAll('.subject');
  const subjectInput = form.querySelector('input[name="subject"]');
  subjects.forEach((b) => {
    b.addEventListener('click', () => {
      subjects.forEach((x) => x.classList.remove('is-active'));
      b.classList.add('is-active');
      subjectInput.value = b.dataset.value;
    });
  });

  // ── Messages ──────────────────────────────────────────────────────────────
  const secours = `Écris-moi directement à <a href="mailto:${MAIL}">${MAIL}</a>, je réponds aussi vite.`;

  function afficher(html, ok) {
    if (!statut) return;
    statut.innerHTML = html;
    statut.classList.toggle('is-ok', !!ok);
    statut.hidden = false;
  }
  function cacher() {
    if (statut) { statut.hidden = true; statut.innerHTML = ''; }
    form.querySelectorAll('.is-invalid').forEach((el) => el.classList.remove('is-invalid'));
  }

  function erreur(code, data) {
    if (code === 422 && Array.isArray(data.champs)) {
      const noms = { name: 'ton nom', email: 'un email valide', message: 'ton message' };
      data.champs.forEach((c) => {
        const el = form.querySelector(`[name="${c}"]`);
        if (el) el.classList.add('is-invalid');
      });
      const manque = data.champs.map((c) => noms[c] || c).join(', ');
      afficher(`Il manque ${manque}.`);
      const premier = form.querySelector('.is-invalid');
      if (premier) premier.focus();
      return;
    }
    if (code === 429) {
      afficher(`Trop de messages envoyés depuis cette connexion. Réessaie dans une heure — ou ${secours}`);
      return;
    }
    afficher(`L'envoi a échoué de mon côté. ${secours}`);
  }

  // ── Envoi ─────────────────────────────────────────────────────────────────
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    cacher();
    if (bouton) { bouton.disabled = true; bouton.textContent = 'Envoi…'; }

    try {
      const r = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json', 'X-Requested-With': 'fetch' },
      });
      let data = {};
      try { data = await r.json(); } catch (_) { /* reponse non JSON */ }

      // La confirmation ne s'affiche qu'apres un accuse du serveur.
      if (r.ok && data.ok) {
        form.hidden = true;
        sent.hidden = false;
        sent.focus();
      } else {
        erreur(r.status, data);
      }
    } catch (_) {
      erreur(0, {});
    } finally {
      if (bouton) { bouton.disabled = false; bouton.textContent = libelleBouton; }
    }
  });

  reset.addEventListener('click', () => {
    form.reset();
    subjects.forEach((x) => x.classList.remove('is-active'));
    subjects[0].classList.add('is-active');
    subjectInput.value = subjects[0].dataset.value;
    cacher();
    sent.hidden = true;
    form.hidden = false;
    form.querySelector('input, textarea').focus();
  });

  // Retour du formulaire poste sans JavaScript : /contact/?envoye=1
  if (new URLSearchParams(location.search).get('envoye') === '1') {
    form.hidden = true;
    sent.hidden = false;
  }
})();
