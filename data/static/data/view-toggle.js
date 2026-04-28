/* view-toggle.js
 * Handles Cards/Table view switching with localStorage persistence.
 * Also initialises JS-based card pagination (9 per page) on artist_detail.
 * Tablesort is initialised in base.html's inline script (after Tablesort CDN).
 */

(function () {
  'use strict';

  function initViewToggles() {
    document.querySelectorAll('[data-view-toggle]').forEach(function (container) {
      var defaultView = container.dataset.defaultView || 'cards';
      var saved = localStorage.getItem('entry-view');
      // Only use saved value if it's a known option
      var active = (saved === 'cards' || saved === 'table') ? saved : defaultView;

      var cardsWrapper = document.querySelector('.entry-view-cards');
      var tableWrapper = document.querySelector('.entry-view-table');
      var cardBtn  = container.querySelector('[data-view="cards"]');
      var tableBtn = container.querySelector('[data-view="table"]');

      function setView(view) {
        if (cardsWrapper) cardsWrapper.style.display = (view === 'cards') ? '' : 'none';
        if (tableWrapper) tableWrapper.style.display = (view === 'table')  ? '' : 'none';

        if (cardBtn)  cardBtn.classList.toggle('view-toggle__btn--active',  view === 'cards');
        if (tableBtn) tableBtn.classList.toggle('view-toggle__btn--active', view === 'table');

        localStorage.setItem('entry-view', view);
      }

      setView(active);

      if (cardBtn)  cardBtn.addEventListener('click',  function () { setView('cards'); });
      if (tableBtn) tableBtn.addEventListener('click', function () { setView('table'); });

      // JS card pagination — only when we have an artist_detail (no server pagination)
      if (cardsWrapper && !cardsWrapper.hasAttribute('data-server-paginated')) {
        initCardPagination(cardsWrapper, 9);
      }
    });
  }

  function initCardPagination(container, perPage) {
    var cards = Array.prototype.slice.call(container.querySelectorAll('.entry-card'));
    if (cards.length <= perPage) return;

    var page = 1;
    var totalPages = Math.ceil(cards.length / perPage);

    function showPage(p) {
      page = p;
      cards.forEach(function (card, i) {
        card.style.display = (i >= (p - 1) * perPage && i < p * perPage) ? '' : 'none';
      });
      renderPagination();
    }

    function renderPagination() {
      var existing = container.querySelector('.card-pagination');
      if (existing) existing.parentNode.removeChild(existing);

      var nav = document.createElement('div');
      nav.className = 'pagination-nav card-pagination';

      if (page > 1) {
        nav.appendChild(makeBtn('First', function () { showPage(1); }));
        nav.appendChild(makeBtn('Previous', function () { showPage(page - 1); }));
      }

      // Show only pages within ±2 of current page (mirrors server-side pagination window)
      for (var i = 1; i <= totalPages; i++) {
        if (i >= page - 2 && i <= page + 2) {
          (function (n) {
            var btn = makeBtn(String(n), function () { showPage(n); });
            if (n === page) btn.classList.add('pagination-nav__btn--active');
            nav.appendChild(btn);
          })(i);
        }
      }

      if (page < totalPages) {
        nav.appendChild(makeBtn('Next', function () { showPage(page + 1); }));
        nav.appendChild(makeBtn('Last', function () { showPage(totalPages); }));
      }

      // Append inside the cards wrapper so it hides/shows with the cards view
      container.appendChild(nav);
    }

    function makeBtn(text, onClick) {
      var a = document.createElement('a');
      a.className = 'pagination-nav__btn';
      a.textContent = text;
      a.style.cursor = 'pointer';
      a.addEventListener('click', onClick);
      return a;
    }

    showPage(1);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initViewToggles);
  } else {
    initViewToggles();
  }
})();
