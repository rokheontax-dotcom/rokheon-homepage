// 록헌 세무회계 — 메뉴, 스크롤 효과

// 모바일 메뉴
const burger = document.querySelector('.burger');
const menu = document.querySelector('.menu');
burger.addEventListener('click', () => {
  const open = menu.classList.toggle('open');
  burger.setAttribute('aria-expanded', open);
});

// 업무 분야 하위 메뉴: 모바일에서는 눌러서 펼침 (PC는 마우스 올리면 CSS로 열림)
const dd = document.querySelector('.dd');
const ddBtn = dd.querySelector('.dd-btn');
ddBtn.addEventListener('click', () => {
  const open = dd.classList.toggle('open');
  ddBtn.setAttribute('aria-expanded', open);
});
menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  menu.classList.remove('open');
  burger.setAttribute('aria-expanded', false);
}));

// 화면에 들어오면 등장
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));

// 스크롤 위치에 따라 움직이는 요소들 (페이지마다 있는 것만 동작)
const root = document.documentElement;
const header = document.querySelector('header.site');
const hero = document.querySelector('.hero, .page-hero');
const statement = document.getElementById('statement');
const words = statement ? statement.querySelectorAll('.w') : [];
const rows = document.querySelectorAll('.marquee .row');
const stepsList = document.querySelectorAll('.steps');
const mbar = document.querySelector('.mbar');
const isHome = !!document.querySelector('.hero');
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;

// 질문 카드가 화면 폭의 3배가 될 때까지 복제해서 빈 공간이 보이지 않게
// (복제본은 화면 읽기·탭 이동에서 제외)
rows.forEach(row => {
  const items = [...row.children];
  while (row.scrollWidth < innerWidth * 3) {
    items.forEach(n => {
      const c = n.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      c.tabIndex = -1;
      row.appendChild(c);
    });
  }
});

function update() {
  const y = scrollY, vh = innerHeight;

  header.classList.toggle('scrolled', y > 20);
  header.style.setProperty('--sp', clamp(y / (root.scrollHeight - vh)));
  if (mbar) mbar.classList.toggle('show', !isHome || y > vh * 0.6);

  if (still) {
    words.forEach(w => w.classList.add('on'));
    if (statement) { statement.style.setProperty('--strike', 1); statement.style.setProperty('--tail', 1); }
    stepsList.forEach(s => s.style.setProperty('--lp', 1));
    return;
  }

  // 머리 영역: 사진·도형이 서로 다른 속도로 움직임
  if (hero) hero.style.setProperty('--hp', clamp(y / hero.offsetHeight));

  // 원칙 문장: 고정된 동안 줄긋기 → 단어 채우기 → 설명 등장
  if (statement) {
    const r = statement.getBoundingClientRect();
    const p = clamp(-r.top / (r.height - vh));
    statement.style.setProperty('--strike', clamp(p / 0.22));
    words.forEach((w, i) => w.classList.toggle('on', p > 0.25 + (i / words.length) * 0.5));
    statement.style.setProperty('--tail', clamp((p - 0.8) / 0.15));
  }

  // 키워드 띠: 가운데 정렬 기준으로 스크롤 따라 좌우로 흐름
  rows.forEach(row => {
    const shift = (row.getBoundingClientRect().top - vh / 2) * parseFloat(row.dataset.speed);
    row.style.transform = `translateX(${-(row.scrollWidth - innerWidth) / 2 + shift}px)`;
  });

  // 단계 위쪽 선이 그려짐
  stepsList.forEach(s => {
    const sr = s.getBoundingClientRect();
    s.style.setProperty('--lp', clamp((vh * 0.85 - sr.top) / (vh * 0.5)));
  });
}

let ticking = false;
addEventListener('scroll', () => {
  if (!ticking) { requestAnimationFrame(() => { update(); ticking = false; }); ticking = true; }
}, { passive: true });
addEventListener('resize', update);
update();
