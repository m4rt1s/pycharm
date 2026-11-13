/* =============================================
   POKÉAPP — ANIMACE A INTERAKCE
   1. Samočinné částice na pozadí
   2. Záře reagující na kurzor
   3. Scroll reveal (s bezpečným fallbackem)
   4. Pokédex vyhledávání a filtrování
   5. Přesuny mezi sekcemi
   ============================================= */
'use strict';

// Soubor se načítá s defer, takže HTML prvky už existují.
// Každá funkce níže obstarává jednu část stránky.
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

createParticles();
startCursorGlow();
showSectionsOnScroll();
setupPokedex();
setupSectionLinks();

function createParticles() {
  // 1. Částice se pohybují SAMY, i když myš stojí.
  const field = document.getElementById('particleField');
  if (field && !reducedMotion) {
    // Vytvoříme 38 spanů. Výpočty s modulo rozmístí body po celé ploše.
    for (let i = 0; i < 38; i++) {
      const dot = document.createElement('span');
      dot.className = 'particle';
      dot.style.left = `${(i * 73.71) % 100}%`;
      dot.style.top = `${(i * 37.17) % 100}%`;
      // CSS proměnné nastaví délku cyklu a záporný začátek, aby částice nebyly synchronní.
      dot.style.setProperty('--duration', `${10 + (i % 11) * 1.7}s`);
      dot.style.setProperty('--delay', `${-i * 0.9}s`);
      field.appendChild(dot);
    }
  }

}

function startCursorGlow() {
  // 2. Volitelná jemná záře sleduje myš.
  const glow = document.querySelector('.cursor-glow');
  if (glow && !reducedMotion && window.matchMedia('(pointer:fine)').matches) {
    // x/y jsou aktuální souřadnice; targetX/targetY jsou cílové souřadnice od myši.
    let x = -1000;
    let y = -1000;
    let targetX = -1000;
    let targetY = -1000;
    window.addEventListener('pointermove', event => {
      // clientX a clientY měří polohu v okně. Odečítáme polovinu šířky záře (550 / 2).
      targetX = event.clientX - 275;
      targetY = event.clientY - 275;
    }, {passive:true});
    // Každý snímek překonáme 6,5 % zbývající vzdálenosti: záře měkce dojíždí.
    function animateGlow() {
      x += (targetX - x) * .065;
      y += (targetY - y) * .065;
      glow.style.transform = `translate3d(${x}px,${y}px,0)`;
      // Prohlížeč naplánuje další snímek; funkce tak průběžně aktualizuje transform.
      requestAnimationFrame(animateGlow);
    }
    animateGlow();
  }

}

function showSectionsOnScroll() {
  // 3. Sekce se objeví při scrollování. Bez podpory observeru zůstanou viditelné.
  if (!reducedMotion && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('js-motion');
    // Observer sleduje vstup prvků do oblasti obrazovky bez ručního počítání scrollu.
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          // Po prvním zobrazení prvek přestaneme sledovat; animace se nebude opakovat.
          observer.unobserve(entry.target);
        }
      });
    // Spuštění při viditelnosti 8 %; spodní okraj oblasti je rozšířen o 60 px.
    }, {threshold:0.08, rootMargin:'0px 0px 60px 0px'});
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  }

}

function setupPokedex() {
  // 4. Vyhledávání a filtry (kombinují se).
  const input = document.getElementById('pokemonSearch');
  // Na přihlašovací stránce Pokédex není, proto zde skončíme.
  if (!input) return;

  const cards = document.querySelectorAll('.pokemon-item');
  const buttons = document.querySelectorAll('.filter-chip');
  const empty = document.getElementById('noResults');
  const count = document.getElementById('resultCount');
  // Uchováváme zvolený typ mezi kliknutími. Na začátku zobrazujeme všechny typy.
  let activeFilter = 'all';
  // Jedna funkce kombinuje hledání a typový filtr a přepočítá výsledky.
  function updateCards() {
    // trim odstraní mezery kolem textu; lowercase sjednotí velikost písmen.
    const query = input.value.trim().toLocaleLowerCase();
    let shown = 0;
    cards.forEach(card => {
      // includes odpoví, zda daný údaj obsahuje hledaný text.
      // Operátor || znamená „nebo“: stačí shoda alespoň jednoho údaje.
      const matchesName = card.dataset.name.includes(query);
      const matchesNumber = card.dataset.id.includes(query);
      const matchesTypes = card.dataset.type.includes(query);
      const matchesText = matchesName || matchesNumber || matchesTypes;
      // Typ se hledá v celém seznamu, takže například Flying odpovídá i Fire · Flying.
      const matchesType = activeFilter === 'all' || (card.dataset.type || '').includes(activeFilter);
      // Karta musí splnit obě podmínky současně (operátor &&).
      const visible = matchesText && matchesType;
      // Nastavíme skrytí karty; display:none zároveň odstraní její místo v rozložení.
      card.hidden = !visible;
      card.style.display = visible ? '' : 'none';
      if (visible) {
        shown += 1;
      }
    });
    // Hláška se zobrazí pouze při nule výsledků; počítadlo se aktualizuje textContent.
    if (empty) empty.hidden = shown !== 0;
    if (count) count.textContent = `Zobrazeno ${shown} z ${cards.length} Pokémonů`;
  }
  // Událost input reaguje ihned při psaní, bez odeslání formuláře na server.
  input.addEventListener('input', updateCards);
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      // Kliknutí změní aktivní typ a zvýrazní jen právě stisknuté tlačítko.
      activeFilter = button.dataset.filter || 'all';
      buttons.forEach(filterButton => {
        const selected = filterButton === button;
        filterButton.classList.toggle('selected', selected);
        // aria-pressed informuje asistivní technologie o zvoleném filtru.
        filterButton.setAttribute('aria-pressed', String(selected));
      });
      updateCards();
    });
  });
  // Klávesa / přesune kurzor do hledání, pokud uživatel nepíše do jiného pole.
  document.addEventListener('keydown', event => {
    if (event.key === '/' && input && !['INPUT','TEXTAREA'].includes(document.activeElement?.tagName)) {
      // Zabráníme napsání lomítka a přesuneme focus do hledání.
      event.preventDefault();
      input.focus();
    }
  });

}

function setupSectionLinks() {
  // 5. Přesuny mezi sekcemi bez přidávání # do adresy prohlížeče.
  // href zachováme jako záložní navigaci; JavaScript převezme běžné kliknutí.
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    // Upravené kliknutí (Ctrl, Cmd, Shift, Alt) ponecháme prohlížeči.
    if (!link || event.defaultPrevented || event.button !== 0 ||
        event.ctrlKey || event.metaKey || event.shiftKey || event.altKey ||
        link.hasAttribute('download') || (link.target && link.target !== '_self')) return;
    const target = document.getElementById(link.getAttribute('href').slice(1));
    if (!target) return;
    event.preventDefault();
    // scroll-padding-top v CSS zajistí místo pro horní navigaci.
    target.scrollIntoView({behavior: reducedMotion ? 'instant' : 'smooth', block: 'start'});
    // Sekci zpřístupníme také uživateli klávesnice bez dalšího posunu.
    if (!target.hasAttribute('tabindex')) {
      target.setAttribute('tabindex', '-1');
      target.addEventListener('blur', () => target.removeAttribute('tabindex'), {once: true});
    }
    target.focus({preventScroll: true});
    // replaceState odstraní případný starší fragment bez znovunačtení stránky.
    if (window.location.hash) {
      history.replaceState(history.state, '', window.location.pathname + window.location.search);
    }
  });

  // Starší adresa s # se nejprve přesune k sekci a potom se vyčistí.
  if (window.location.hash) {
    const initialTarget = document.getElementById(window.location.hash.slice(1));
    if (initialTarget) {
      window.addEventListener('load', () => {
        initialTarget.scrollIntoView({behavior: 'instant', block: 'start'});
        history.replaceState(history.state, '', window.location.pathname + window.location.search);
      }, {once: true});
    }
  }
}
