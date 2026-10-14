/* Formularze: tryb podglądu (placeholder action), prefill województwa z ?woj=, honeypot. */
(function () {
  'use strict';
  var params = new URLSearchParams(window.location.search);
  var woj = params.get('woj');
  if (woj) {
    document.querySelectorAll('select[data-prefill="woj"]').forEach(function (sel) {
      for (var i = 0; i < sel.options.length; i++) {
        if (sel.options[i].value === woj) { sel.selectedIndex = i; break; }
      }
    });
  }
  document.querySelectorAll('form[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      var status = form.querySelector('.form-status');
      var hp = form.querySelector('input[name="www"]');
      if (hp && hp.value) { e.preventDefault(); return; }
      if (!form.checkValidity()) {
        e.preventDefault();
        form.reportValidity();
        return;
      }
      if (form.getAttribute('data-placeholder') === 'true') {
        e.preventDefault();
        if (status) {
          status.textContent = 'Tryb podglądu: formularz nie jest jeszcze podłączony, dane nie zostały wysłane.';
        }
      }
    });
  });
})();
