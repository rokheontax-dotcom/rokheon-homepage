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
// IntersectionObserver가 일부 모바일 환경에서 반응하지 않아 콘텐츠가 안 보이는 일이 있어,
// 스크롤할 때 위치를 직접 확인하는 방식(revealCheck)을 함께 쓴다. 둘 중 먼저 걸리는 쪽이 보여준다.
let pending = [...document.querySelectorAll('[data-reveal]')];
const show = el => { el.classList.add('in'); pending = pending.filter(p => p !== el); };
const io = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { show(e.target); io.unobserve(e.target); } });
}, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }) : null;
if (io) pending.forEach(el => io.observe(el));
function revealCheck() {
  const limit = innerHeight * 0.92;
  pending.forEach(el => { if (el.getBoundingClientRect().top < limit) show(el); });
}

// 스크롤 위치에 따라 움직이는 요소들 (페이지마다 있는 것만 동작)
const root = document.documentElement;
const header = document.querySelector('header.site');
const hero = document.querySelector('.hero, .page-hero');
const statement = document.getElementById('statement');
const words = statement ? statement.querySelectorAll('.w') : [];
const stepsList = document.querySelectorAll('.steps');
const mbar = document.querySelector('.mbar');
const isHome = !!document.querySelector('.hero');
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;

function update() {
  const y = scrollY, vh = innerHeight;
  if (pending.length) revealCheck();

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

// 탭 (업무 페이지의 개인/법인 구분). JS가 없으면 모든 탭 내용이 그대로 보인다.
document.querySelectorAll('.tabs').forEach(tabs => {
  const btns = tabs.querySelectorAll('button');
  btns.forEach(btn => btn.addEventListener('click', () => {
    btns.forEach(b => {
      const on = b === btn;
      b.setAttribute('aria-selected', on);
      const panel = document.getElementById(b.dataset.tab);
      panel.classList.toggle('on', on);
      if (on) panel.querySelectorAll('[data-reveal]').forEach(show);
    });
  }));
});
