/* Quiz „Sprawdź, czy się kwalifikujesz” – czysty JS, bez wysyłania danych.
   Warunki: ustawa z 20.03.2025 o rynku pracy i służbach zatrudnienia, art. 147–148,
   oraz typowe zapisy regulaminów PUP (docs/jak-dziala-dotacja-2026.md). */
(function () {
  'use strict';

  var cfgEl = document.getElementById('quiz-config');
  var root = document.getElementById('quiz');
  if (!cfgEl || !root) return;
  var CFG = JSON.parse(cfgEl.textContent);

  var form = document.getElementById('quiz-form');
  var stepBox = document.getElementById('quiz-step');
  var errBox = document.getElementById('quiz-err');
  var btnBack = document.getElementById('quiz-back');
  var btnNext = document.getElementById('quiz-next');
  var bar = document.getElementById('quiz-bar');
  var count = document.getElementById('quiz-count');
  var resultBox = document.getElementById('quiz-result');

  var ans = {};
  var idx = 0;

  /* ---------- pytania ---------- */
  var BEZ_ETATU = ['bezrobotny', 'rejestracja', 'opiekun'];
  var Q = [
    {
      id: 'status',
      q: 'Jaki masz dziś status?',
      hint: 'Dofinansowanie z PUP przysługuje trzem grupom osób (art. 147 ustawy o rynku pracy).',
      opts: [
        ['bezrobotny', 'Jestem zarejestrowany(-a) w urzędzie pracy jako osoba bezrobotna'],
        ['rejestracja', 'Nie pracuję i nie jestem jeszcze zarejestrowany(-a), ale mogę się zarejestrować'],
        ['opiekun', 'Jestem opiekunem(-ką) osoby niepełnosprawnej, nie pracuję i szukam pracy'],
        ['cis', 'Jestem absolwentem(-ką) CIS lub KIS (centrum lub klubu integracji społecznej)'],
        ['etat', 'Pracuję (etat, zlecenie) albo prowadzę firmę']
      ]
    },
    {
      id: 'firma',
      q: function (a) {
        return a.status === 'opiekun'
          ? 'Czy obecnie prowadzisz firmę albo masz ją zawieszoną?'
          : 'Czy w ciągu ostatnich 12 miesięcy miałeś(-aś) zarejestrowaną firmę – także zawieszoną?';
      },
      hint: function (a) {
        return a.status === 'opiekun' ? '' : 'Urząd sprawdza to w CEIDG. Liczy się też działalność prowadzona za granicą.';
      },
      opts: function (a) {
        return a.status === 'opiekun'
          ? [['nie', 'Nie'], ['tak', 'Tak, prowadzę albo mam zawieszoną firmę']]
          : [['nie', 'Nie'], ['tak12', 'Tak, w ostatnich 12 miesiącach (także zawieszoną)'],
             ['zagranica', 'Prowadzę albo mam zawieszoną firmę za granicą'],
             ['niewiem', 'Zamknąłem(-am) firmę, ale nie pamiętam dokładnej daty']];
      }
    },
    {
      id: 'przerwanie',
      show: function (a) { return BEZ_ETATU.indexOf(a.status) !== -1; },
      q: 'Czy w ostatnich 12 miesiącach przerwałeś(-aś) z własnej winy staż, szkolenie lub inną formę pomocy z urzędu pracy?',
      opts: [['nie', 'Nie'], ['tak', 'Tak'], ['niewiem', 'Nie jestem pewien(-na)']]
    },
    {
      id: 'dotacja',
      q: 'Czy kiedykolwiek dostałeś(-aś) bezzwrotne środki publiczne na założenie firmy lub spółdzielni socjalnej?',
      hint: 'Chodzi o dotację z PUP, PFRON, projektu unijnego, LGD albo umorzenie pożyczki z urzędu pracy. Przepis nie ma limitu czasu.',
      opts: [['nie', 'Nie'], ['tak', 'Tak'], ['niewiem', 'Nie wiem (np. dostałem(-am) wsparcie, ale nie pamiętam jakie)']]
    },
    {
      id: 'innypup',
      q: 'Czy złożyłeś(-aś) wniosek o dofinansowanie w innym urzędzie pracy?',
      opts: [['nie', 'Nie'], ['oczekuje', 'Tak, i ten wniosek jest jeszcze rozpatrywany'],
             ['rozpatrzony', 'Tak, ale został rozpatrzony i umowy nie zawarto (i nie zostanie zawarta)']]
    },
    {
      id: 'karalnosc',
      q: 'Czy w ostatnich 2 latach zostałeś(-aś) prawomocnie skazany(-a) za przestępstwo przeciwko obrotowi gospodarczemu, dokumentom albo przestępstwo skarbowe?',
      hint: 'Warunek potwierdzasz we wniosku oświadczeniem pod rygorem odpowiedzialności karnej.',
      opts: [['nie', 'Nie'], ['tak', 'Tak']]
    },
    {
      id: 'branza',
      q: 'Jaką działalność planujesz?',
      hint: 'Urzędy mogą wykluczać niektóre rodzaje działalności w swoim regulaminie.',
      opts: [
        ['uslugi', 'Usługi w lokalu (np. salon, warsztat, gabinet)'],
        ['mobilne', 'Usługi mobilne u klienta (np. sprzątanie, remonty)'],
        ['handel', 'Handel w sklepie stacjonarnym'],
        ['online', 'Sklep internetowy'],
        ['gastro', 'Gastronomia w lokalu'],
        ['foodtruck', 'Food truck lub gastronomia obwoźna'],
        ['obwozny', 'Handel obwoźny, na targowisku lub bazarze'],
        ['sezonowa', 'Działalność sezonowa (np. tylko latem)'],
        ['rolnictwo', 'Rolnictwo, hodowla, rybołówstwo'],
        ['komis', 'Komis, lombard, skup, handel samochodami'],
        ['spolka', 'Spółka z inną osobą albo przejęcie firmy po członku rodziny'],
        ['produkcja', 'Produkcja (np. stolarnia, rękodzieło)'],
        ['inne', 'Inna działalność']
      ]
    },
    {
      id: 'zabezp',
      q: 'Czym zabezpieczysz zwrot dotacji?',
      hint: 'Zabezpieczenie jest obowiązkowe. Bez niego urząd nie podpisze umowy. Najczęściej to poręczenie 2 osób.',
      opts: [
        ['dwa', 'Mam 2 osoby, które mogą poręczyć (stały dochód ok. 4–5 tys. zł netto, bez dużych kredytów)'],
        ['jeden', 'Mam 1 taką osobę'],
        ['blokada', 'Mam oszczędności większe niż kwota dotacji (blokada środków na koncie)'],
        ['majatek', 'Mam nieruchomość albo wartościowy samochód lub maszynę'],
        ['niewiem', 'Jeszcze tego nie sprawdzałem(-am)'],
        ['brak', 'Nie mam żadnej z tych możliwości']
      ]
    },
    {
      id: 'wklad',
      q: 'Ile własnych pieniędzy możesz dołożyć na start?',
      hint: 'Ustawa nie wymaga wkładu własnego, ale część urzędów go punktuje, a dotacja nie pokrywa kosztów bieżących.',
      opts: [['duzo', 'Ponad 10% kwoty dotacji'], ['malo', 'Trochę, mniej niż 10%'], ['nic', 'Nie mam własnych środków']]
    },
    {
      id: 'woj',
      type: 'select',
      q: 'W jakim województwie mieszkasz?',
      hint: 'Wniosek składasz w urzędzie pracy właściwym dla miejsca zamieszkania.'
    },
    {
      id: 'nabor',
      q: 'Czy Twój urząd ogłosił nabór wniosków?',
      opts: [['trwa', 'Tak, nabór trwa teraz'], ['wkrotce', 'Jest zapowiedziany, startuje wkrótce'], ['brak', 'Nie ma naboru albo nie wiem']]
    }
  ];

  function val(x) { return typeof x === 'function' ? x(ans) : x; }
  function aktywne() { return Q.filter(function (q) { return !q.show || q.show(ans); }); }

  /* ---------- ocena ---------- */
  function ocen(a) {
    var blok = [], spr = [], info = [];
    switch (a.status) {
      case 'etat':
        blok.push(['Masz pracę lub prowadzisz firmę.', 'Dofinansowanie z PUP przysługuje osobom bezrobotnym, absolwentom CIS/KIS i niepracującym opiekunom osób niepełnosprawnych. Jeśli planujesz odejść z pracy, po rejestracji jako osoba bezrobotna możesz złożyć wniosek. Inne ścieżki to np. pożyczka na start firmy albo premia z LGD – sprawdź ich warunki u operatora.']);
        break;
      case 'rejestracja':
        spr.push(['Najpierw zarejestruj się jako osoba bezrobotna.', 'Status musisz mieć w dniu złożenia wniosku. Przy rejestracji zapytaj doradcę o wpisanie dotacji do Indywidualnego Planu Działania – część urzędów tego wymaga.']);
        break;
      case 'opiekun':
        spr.push(['Sprawdź, czy nabór obejmuje opiekunów osób niepełnosprawnych.', 'Ustawa dopuszcza opiekuna, który poszukuje pracy, nie jest zatrudniony i nie wykonuje innej pracy zarobkowej. Projekty z EFS+ mają jednak własne grupy docelowe.']);
        break;
      case 'cis':
        spr.push(['Sprawdź, czy nabór obejmuje absolwentów CIS/KIS.', 'Ustawa dopuszcza tę grupę (art. 147), ale nabory z EFS+ mają własne grupy docelowe. Przygotuj dokument potwierdzający ukończenie zajęć.']);
        break;
      default:
        info.push('Zapytaj doradcę, czy dotacja jest wpisana w Twój Indywidualny Plan Działania – niektóre urzędy tego wymagają.');
    }
    if (a.firma === 'tak12') blok.push(['W ostatnich 12 miesiącach miałeś(-aś) zarejestrowaną firmę.', 'Wróć, gdy minie 12 miesięcy od wykreślenia firmy z CEIDG. Zapisz się na alert, żeby nie przegapić naborów po tym terminie.']);
    if (a.firma === 'zagranica') blok.push(['Masz firmę za granicą.', 'Nie możesz prowadzić ani mieć zawieszonej działalności za granicą w dniu złożenia wniosku.']);
    if (a.firma === 'tak') blok.push(['Prowadzisz lub masz zawieszoną firmę.', 'Opiekun osoby niepełnosprawnej nie może w dniu złożenia wniosku prowadzić ani mieć zawieszonej działalności.']);
    if (a.firma === 'niewiem') spr.push(['Sprawdź datę wykreślenia firmy w CEIDG.', 'Od wykreślenia musi minąć 12 miesięcy. Urząd sprawdza to w rejestrze.']);
    if (a.przerwanie === 'tak') blok.push(['W ostatnich 12 miesiącach przerwałeś(-aś) z własnej winy formę pomocy z urzędu.', 'Wróć po upływie 12 miesięcy od przerwania. Urząd sprawdza to w swoim systemie.']);
    if (a.przerwanie === 'niewiem') spr.push(['Zapytaj w urzędzie, czy przerwanie stażu lub szkolenia uznano za zawinione.', 'Tylko przerwanie z własnej winy w ostatnich 12 miesiącach wyklucza wniosek.']);
    if (a.dotacja === 'tak') blok.push(['Dostałeś(-aś) już bezzwrotne środki na założenie firmy.', 'Ustawa wyklucza osoby, które kiedykolwiek otrzymały bezzwrotne środki publiczne na podjęcie działalności lub spółdzielnię socjalną – bez limitu czasu. Zostają inne formy finansowania, np. pożyczka na start.']);
    if (a.dotacja === 'niewiem') spr.push(['Ustal, jakie wsparcie dostałeś(-aś) wcześniej.', 'Wyklucza tylko bezzwrotna dotacja na założenie firmy lub spółdzielni socjalnej (albo umorzona pożyczka). Szkolenie czy staż nie wykluczają.']);
    if (a.innypup === 'oczekuje') blok.push(['Masz wniosek rozpatrywany w innym urzędzie pracy.', 'Nie można jednocześnie ubiegać się o dotację w dwóch urzędach. Poczekaj na rozpatrzenie tamtego wniosku.']);
    if (a.innypup === 'rozpatrzony') info.push('Wniosek rozpatrzony w innym urzędzie, po którym umowy nie zawarto i nie zostanie zawarta, nie blokuje nowego wniosku.');
    if (a.karalnosc === 'tak') blok.push(['Prawomocne skazanie w ostatnich 2 latach.', 'Wyklucza wniosek. Wróć, gdy miną 2 lata od uprawomocnienia wyroku.']);

    var br = {
      foodtruck: 'Część urzędów wyklucza gastronomię obwoźną. Sprawdź regulamin swojego PUP, zanim przygotujesz wniosek.',
      obwozny: 'Część urzędów wyklucza handel obwoźny i na targowiskach. Sprawdź regulamin swojego PUP.',
      sezonowa: 'Część urzędów wyklucza działalność sezonową. Pokaż przychody przez cały rok albo sprawdź regulamin.',
      komis: 'Część urzędów nie finansuje towaru handlowego w komisach, lombardach i skupach, a sprzedaż pojazdów bywa wykluczona.',
      spolka: 'Część urzędów finansuje tylko jednoosobową działalność i wyklucza przejęcie firmy po członku rodziny.'
    };
    if (br[a.branza]) spr.push(['Sprawdź, czy regulamin nie wyklucza Twojej branży.', br[a.branza]]);
    if (a.branza === 'rolnictwo') blok.push(['Rolnictwo, hodowla i rybołówstwo są wyłączone.', 'Dotacja jest pomocą de minimis, która nie obejmuje produkcji podstawowej produktów rolnych ani rybołówstwa. Sprawdź programy dla rolników (np. ARiMR, LGD).']);
    if (a.branza === 'online') info.push('Sklep internetowy: towar ma zwykle limit 10–30% kwoty, a część urzędów wymaga własnego sklepu (nie tylko aukcji).');
    if (a.branza === 'handel') info.push('Handel: towar ma zwykle limit 10–30% kwoty dotacji, więc kosztorys opieramy na wyposażeniu.');
    if (a.branza === 'gastro') info.push('Gastronomia: lokal musi przejść zatwierdzenie sanepidu, a kasa fiskalna jest obowiązkowa od pierwszej sprzedaży.');
    if (a.branza === 'mobilne') info.push('Przy pracy mobilnej podajesz we wniosku miejsce przechowywania sprzętu i obszar działania.');
    if (a.branza === 'produkcja') info.push('W części kart oceny produkcja dostaje więcej punktów niż usługi i handel.');

    if (a.zabezp === 'brak') blok.push(['Nie masz zabezpieczenia zwrotu.', 'Bez niego urząd nie podpisze umowy, nawet po pozytywnej ocenie. Porozmawiaj z rodziną lub znajomymi o poręczeniu (rodzic, rodzeństwo, znajomy – nie małżonek we wspólności majątkowej). Wymogi wobec poręczycieli są w regulaminie urzędu.']);
    if (a.zabezp === 'jeden') spr.push(['Sprawdź, czy wystarczy 1 poręczyciel.', 'Większość urzędów wymaga 2 poręczycieli. Niektóre akceptują 1 przy niższej kwocie (np. do 35 tys. zł) albo przy wyższym dochodzie poręczyciela.']);
    if (a.zabezp === 'majatek') spr.push(['Sprawdź, jak urząd przyjmuje zabezpieczenie majątkiem.', 'Akt notarialny i weksel in blanco nie wystarczą same – potrzebna jest druga forma. Zastaw wymaga wyceny rzeczoznawcy (zwykle 125–160% kwoty) na Twój koszt.']);
    if (a.zabezp === 'niewiem') spr.push(['Ustal zabezpieczenie przed zamówieniem.', 'To najczęstszy powód, dla którego wniosek kończy się bez umowy. Najczęściej potrzeba 2 poręczycieli z dochodem ok. 4–5 tys. zł netto (umowa na czas nieokreślony lub emerytura).']);
    if (a.zabezp === 'blokada') info.push('Blokada środków to zwykle 125–150% kwoty dotacji na 18–24 miesiące.');
    if (a.zabezp === 'dwa') info.push('Poręczyciel nie może mieć zajęcia komorniczego, a jego małżonek zwykle musi wyrazić zgodę. Urzędy mają też limity wieku (np. 70–75 lat).');

    if (a.wklad === 'duzo') info.push('Wkład własny bywa punktowany (np. powyżej 10% kosztów = więcej punktów). Opiszemy go tak, żeby komisja go policzyła.');
    if (a.wklad === 'nic') spr.push(['Zaplanuj, z czego pokryjesz pierwsze miesiące.', 'Dotacja nie pokrywa ZUS, czynszu, mediów ani kasy fiskalnej. Komisja ocenia też, czy firma przetrwa start.']);

    var poziom = blok.length ? 'c' : (spr.length ? 'b' : 'a');
    return { poziom: poziom, blok: blok, spr: spr, info: info };
  }

  /* ---------- render pytań ---------- */
  function h(tag, attrs, kids) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'text') e.textContent = attrs[k];
      else if (k === 'html') e.innerHTML = attrs[k];
      else e.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c) e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return e;
  }

  function renderStep(focus) {
    var list = aktywne();
    if (idx >= list.length) idx = list.length - 1;
    var q = list[idx];
    errBox.textContent = '';
    stepBox.innerHTML = '';
    var fs = h('fieldset', { 'aria-describedby': 'q-hint' });
    var legend = h('legend', { id: 'q-legend', tabindex: '-1', text: val(q.q) });
    fs.appendChild(legend);
    var hint = val(q.hint);
    fs.appendChild(h('p', { id: 'q-hint', class: 'quiz__hint', text: hint || '' }));
    if (q.type === 'select') {
      var lab = h('label', { for: 'q-select', class: 'sr-only', text: val(q.q) });
      var sel = h('select', { id: 'q-select', name: q.id });
      sel.appendChild(h('option', { value: '', text: 'Wybierz województwo…' }));
      CFG.wojewodztwa.forEach(function (w) {
        var o = h('option', { value: w, text: w });
        if (ans[q.id] === w) o.selected = true;
        sel.appendChild(o);
      });
      fs.appendChild(lab);
      fs.appendChild(sel);
    } else {
      var box = h('div', { class: 'opts' });
      val(q.opts).forEach(function (o, i) {
        var id = 'q-' + q.id + '-' + i;
        var inp = h('input', { type: 'radio', name: q.id, id: id, value: o[0] });
        if (ans[q.id] === o[0]) inp.checked = true;
        box.appendChild(h('div', { class: 'opt' }, [inp, h('label', { for: id, text: o[1] })]));
      });
      fs.appendChild(box);
    }
    stepBox.appendChild(fs);
    var pct = Math.round((idx / list.length) * 100);
    bar.style.width = pct + '%';
    count.textContent = 'Pytanie ' + (idx + 1) + ' z ' + list.length;
    btnBack.hidden = idx === 0;
    btnNext.firstChild.textContent = idx === list.length - 1 ? 'Pokaż wynik ' : 'Dalej ';
    if (focus) legend.focus();
  }

  function odczytaj() {
    var q = aktywne()[idx];
    if (q.type === 'select') {
      var s = document.getElementById('q-select');
      return s && s.value ? s.value : null;
    }
    var c = form.querySelector('input[name="' + q.id + '"]:checked');
    return c ? c.value : null;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var q = aktywne()[idx];
    var v = odczytaj();
    if (!v) {
      errBox.textContent = q.type === 'select' ? 'Wybierz województwo, żeby przejść dalej.' : 'Zaznacz jedną odpowiedź, żeby przejść dalej.';
      var first = stepBox.querySelector('input, select');
      if (first) first.focus();
      return;
    }
    ans[q.id] = v;
    if (q.id === 'status') { delete ans.firma; delete ans.przerwanie; }
    if (idx < aktywne().length - 1) { idx++; renderStep(true); }
    else pokazWynik();
  });
  btnBack.addEventListener('click', function () { if (idx > 0) { idx--; renderStep(true); } });

  /* ---------- wynik ---------- */
  var IK = {
    a: '<path d="M5 12.5l4.5 4.5L19 7"/>',
    b: '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.01"/>',
    c: '<circle cx="12" cy="12" r="9"/><path d="M8 8l8 8M16 8l-8 8"/>',
    pobierz: '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>'
  };
  function svg(name) {
    return '<svg class="ik" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + IK[name] + '</svg>';
  }
  var TYT = {
    a: ['Spełniasz podstawowe warunki', 'Na podstawie Twoich odpowiedzi nic nie wyklucza złożenia wniosku. Teraz liczy się dobrze napisany wniosek i termin naboru.'],
    b: ['Prawdopodobnie tak – sprawdź kilka rzeczy', 'Nie widzimy wykluczeń, ale zanim zapłacisz za wniosek, wyjaśnij poniższe punkty.'],
    c: ['Na dziś raczej nie', 'Twoje odpowiedzi wskazują na przeszkodę, która blokuje wniosek. Poniżej piszemy, co z nią zrobić.']
  };

  function alertUrl() {
    var b = CFG.linki.alert.split('#')[0];
    return b + (ans.woj ? '?woj=' + encodeURIComponent(ans.woj) : '') + '#alerty';
  }

  function kroki(r) {
    var k = [];
    if (r.poziom === 'c') {
      k.push('Zapisz się na alert o naborach – przypomnimy o sobie, gdy przeszkoda zniknie.');
      k.push('Masz pytania o swoją sytuację? Napisz do nas, zanim cokolwiek kupisz.');
      return k;
    }
    if (r.poziom === 'b') k.push('Najpierw wyjaśnij punkty z listy „Do sprawdzenia” – w urzędzie albo w regulaminie naboru.');
    if (ans.nabor === 'trwa') k.push('Nabór trwa, więc liczy się czas. Pakiet Premium albo ekspres: treści w 24 h robocze od kompletu danych.');
    else if (ans.nabor === 'wkrotce') k.push('Zamów teraz, żeby mieć gotowy wniosek w dniu otwarcia naboru. Nabory trwają często 1–2 dni.');
    else k.push('Zapisz się na alert o naborach. Wniosek możesz przygotować wcześniej – pracujemy na aktualnym regulaminie, a po zmianie formularza dopasujemy treści.');
    k.push('Pobierz z urzędu regulamin i formularz wniosku – dołączysz je do kwestionariusza.');
    return k;
  }

  function pokazWynik() {
    var r = ocen(ans);
    bar.style.width = '100%';
    count.textContent = 'Wynik';
    form.hidden = true;
    var t = TYT[r.poziom];
    var parts = [];
    parts.push('<div class="res__head">' + svg(r.poziom) + '<div><h2>' + t[0] + '</h2><p>' + t[1] + '</p></div></div>');
    function sekcja(tytul, items, fmt) {
      if (!items.length) return;
      parts.push('<div class="res__sec"><h3>' + tytul + '</h3><ul class="res__list">' + items.map(fmt).join('') + '</ul></div>');
    }
    var two = function (x) { return '<li><strong>' + x[0] + '</strong> ' + x[1] + '</li>'; };
    sekcja('Dlaczego nie teraz', r.blok, two);
    sekcja('Do sprawdzenia', r.spr, two);
    sekcja('Warto wiedzieć', r.info, function (x) { return '<li>' + x + '</li>'; });
    sekcja('Następny krok', kroki(r), function (x) { return '<li>' + x + '</li>'; });

    var pupy = CFG.pupy.filter(function (p) { return p.woj === ans.woj; });
    var urz = '<p class="small">Urzędy w bazie (' + ans.woj + '): ';
    urz += pupy.length
      ? pupy.map(function (p) { return '<a href="' + p.url + '">' + p.nazwa + '</a>'; }).join(', ')
      : 'jeszcze ich nie mamy – <a href="' + CFG.linki.urzedy + '?woj=' + encodeURIComponent(ans.woj) + '">zobacz listę</a>. Pracujemy z każdym urzędem: regulamin i formularz dołączasz do kwestionariusza.';
    urz += '</p>';

    var btns = '<div class="res__btns">';
    if (r.poziom === 'c') {
      btns += '<a class="btn btn-primary btn-lg" href="' + alertUrl() + '">Zapisz się na alert</a>';
      btns += '<a class="btn btn-secondary" href="' + CFG.linki.kontakt + '">Zapytaj o swoją sytuację</a>';
    } else if (ans.nabor === 'brak') {
      btns += '<a class="btn btn-primary btn-lg" href="' + alertUrl() + '">Zapisz się na alert</a>';
      btns += '<a class="btn btn-secondary" href="' + CFG.linki.zamow + '">Zamów treści do wniosku</a>';
    } else {
      btns += '<a class="btn btn-primary btn-lg" href="' + CFG.linki.zamow + '">Zamów treści do wniosku</a>';
      btns += '<a class="btn btn-secondary" href="' + CFG.linki.cennik + '">Zobacz cennik</a>';
      if (ans.nabor === 'wkrotce') btns += '<a class="btn btn-ghost" href="' + alertUrl() + '">Alert o naborze</a>';
    }
    btns += '</div>';
    parts.push(urz + btns);
    parts.push('<div class="res__btns"><button type="button" class="btn btn-ghost" id="quiz-dl">' + svg('pobierz') + ' Pobierz wynik (.txt)</button><button type="button" class="btn btn-ghost" id="quiz-reset">Zacznij od nowa</button></div>');
    parts.push('<p class="small muted">Twoje odpowiedzi nie zostały nigdzie wysłane. Wynik jest orientacyjny – o kwalifikacji decyduje urząd.</p>');

    resultBox.className = 'quiz__result res--' + r.poziom;
    resultBox.innerHTML = parts.join('');
    resultBox.hidden = false;
    resultBox.focus();
    document.getElementById('quiz-dl').addEventListener('click', function () { pobierz(r); });
    document.getElementById('quiz-reset').addEventListener('click', function () {
      ans = {}; idx = 0; resultBox.hidden = true; form.hidden = false; renderStep(true);
    });
  }

  function pobierz(r) {
    var L = [];
    L.push('WYNIK QUIZU: CZY KWALIFIKUJESZ SIĘ DO DOTACJI Z URZĘDU PRACY');
    L.push('Data: ' + new Date().toLocaleDateString('pl-PL') + ' (stan prawny: ' + CFG.stan_na + ')');
    L.push('');
    L.push('WYNIK: ' + TYT[r.poziom][0].toUpperCase());
    L.push(TYT[r.poziom][1]);
    function blok(t, items, two) {
      if (!items.length) return;
      L.push(''); L.push(t.toUpperCase());
      items.forEach(function (x) { L.push('- ' + (two ? x[0] + ' ' + x[1] : x)); });
    }
    blok('Dlaczego nie teraz', r.blok, true);
    blok('Do sprawdzenia', r.spr, true);
    blok('Warto wiedzieć', r.info, false);
    blok('Następny krok', kroki(r), false);
    L.push(''); L.push('TWOJE ODPOWIEDZI');
    aktywne().forEach(function (q) {
      var v = ans[q.id];
      var label = v;
      if (q.type !== 'select') {
        val(q.opts).forEach(function (o) { if (o[0] === v) label = o[1]; });
      }
      L.push('- ' + val(q.q) + ' ' + label);
    });
    L.push('');
    L.push('Quiz ma charakter orientacyjny. O kwalifikacji decyduje urząd na podstawie swojego regulaminu.');
    L.push('Warunki: ustawa z 20.03.2025 o rynku pracy i służbach zatrudnienia, art. 147-148.');
    var blob = new Blob([L.join('\r\n')], { type: 'text/plain;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'wynik-quizu-dotacja-pup.txt';
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  form.hidden = false;
  root.setAttribute('data-ready', 'true');
  renderStep(false);
})();
