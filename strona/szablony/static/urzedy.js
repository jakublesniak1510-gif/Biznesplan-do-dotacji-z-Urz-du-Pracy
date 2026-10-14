/* Wyszukiwarka urzędów: filtr tekstowy + województwo (także z ?woj=). */
(function () {
  'use strict';
  var input = document.getElementById('szukaj-pup');
  var sel = document.getElementById('szukaj-woj');
  var wynik = document.getElementById('szukaj-wynik');
  var brak = document.getElementById('brak-wynikow');
  if (!input || !sel) return;
  var sekcje = Array.prototype.slice.call(document.querySelectorAll('#lista-pup .woj'));
  var norm = function (s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ł/g, 'l');
  };
  var params = new URLSearchParams(window.location.search);
  if (params.get('woj')) sel.value = params.get('woj');
  if (params.get('q')) input.value = params.get('q');

  function filtruj() {
    var q = norm(input.value.trim());
    var w = sel.value;
    var ile = 0;
    sekcje.forEach(function (sec) {
      var widocznych = 0;
      var zgodneWoj = !w || sec.getAttribute('data-woj') === w;
      sec.querySelectorAll('.pup').forEach(function (li) {
        var ok = zgodneWoj && (!q || norm(li.getAttribute('data-szukaj')).indexOf(q) !== -1);
        li.hidden = !ok;
        if (ok) widocznych++;
      });
      sec.hidden = widocznych === 0;
      ile += widocznych;
    });
    wynik.textContent = 'Znalezione urzędy: ' + ile + '.';
    brak.hidden = ile !== 0;
  }
  input.addEventListener('input', filtruj);
  sel.addEventListener('change', filtruj);
  filtruj();
})();
