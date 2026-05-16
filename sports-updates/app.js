'use strict';

// ── DATA ──────────────────────────────────────────────────────────────────────

const TICKER_SCORES = [
  { home: 'Real Madrid', away: 'Man City',   scoreH: 4, scoreA: 2, sport: '⚽', time: "90'" },
  { home: 'Lakers',      away: 'Warriors',   scoreH: 112, scoreA: 108, sport: '🏀', time: "Q4 3:21" },
  { home: 'Djokovic',    away: 'Alcaraz',    scoreH: 2, scoreA: 1, sport: '🎾', time: 'Set 3' },
  { home: 'Arsenal',     away: 'Chelsea',    scoreH: 1, scoreA: 1, sport: '⚽', time: "67'" },
  { home: 'Celtics',     away: 'Heat',       scoreH: 98, scoreA: 94, sport: '🏀', time: "Q3 8:44" },
  { home: 'Federer',     away: 'Medvedev',   scoreH: 1, scoreA: 0, sport: '🎾', time: 'Set 2' },
  { home: 'Bayern',      away: 'PSG',        scoreH: 3, scoreA: 1, sport: '⚽', time: "78'" },
  { home: 'Nuggets',     away: 'Clippers',   scoreH: 87, scoreA: 90, sport: '🏀', time: "Q4 1:12" },
];

const NEWS_ARTICLES = [
  {
    id: 1, filter: 'football',
    badge: 'FOOTBALL', badgeColor: 'badge--red',
    icon: '⚽', iconBg: '#1A1A24',
    title: "Mbappe Breaks Record as Champions League's All-Time Top Scorer",
    excerpt: "The French forward surpassed Cristiano Ronaldo's long-standing record during last night's quarter-final clash.",
    author: 'James Mitchell', time: '2 hours ago',
  },
  {
    id: 2, filter: 'basketball',
    badge: 'NBA', badgeColor: 'badge--blue',
    icon: '🏀', iconBg: '#0D1B2A',
    title: "LeBron James Announces Historic 22nd Season — 'I Still Have More to Give'",
    excerpt: "The ageless superstar shocked the sporting world by signing another two-year extension with the Lakers.",
    author: 'Sarah Chen', time: '4 hours ago',
  },
  {
    id: 3, filter: 'tennis',
    badge: 'TENNIS', badgeColor: 'badge--green',
    icon: '🎾', iconBg: '#0D1F14',
    title: "Alcaraz Edges Djokovic in Five-Set Wimbledon Epic to Claim Second Title",
    excerpt: "In one of the greatest matches ever played at the All England Club, the young Spaniard triumphed 7-6.",
    author: 'Emma Thornton', time: '6 hours ago',
  },
  {
    id: 4, filter: 'athletics',
    badge: 'ATHLETICS', badgeColor: 'badge--yellow',
    icon: '🏃', iconBg: '#1F1A00',
    title: "World Record Shattered: 100m Barrier Broken at World Championships",
    excerpt: "Sprinting history was made in Budapest as a stunning 9.53s left the crowd — and commentators — speechless.",
    author: 'Marcus Williams', time: '8 hours ago',
  },
  {
    id: 5, filter: 'cricket',
    badge: 'CRICKET', badgeColor: 'badge--green',
    icon: '🏏', iconBg: '#0D1F14',
    title: "India Clinch World Cup with Last-Ball Thriller Against Australia",
    excerpt: "Needing 7 runs off the final over, Hardik Pandya delivered in extraordinary fashion to seal a famous victory.",
    author: 'Priya Sharma', time: '10 hours ago',
  },
  {
    id: 6, filter: 'football',
    badge: 'PREMIER LEAGUE', badgeColor: 'badge--red',
    icon: '⚽', iconBg: '#1A1A24',
    title: "Arsenal Clinch Premier League Title for First Time in 20 Years",
    excerpt: "The Gunners ended their long wait at the Emirates, beating Chelsea 3-1 in front of a jubilant home crowd.",
    author: 'Tom Bradley', time: '1 day ago',
  },
  {
    id: 7, filter: 'rugby',
    badge: 'RUGBY', badgeColor: 'badge--yellow',
    icon: '🏉', iconBg: '#1F1500',
    title: "New Zealand Storm Back to Win Rugby World Cup in Paris",
    excerpt: "The All Blacks trailed by 10 points at half-time before a stunning second-half performance secured glory.",
    author: 'Liam O\'Brien', time: '1 day ago',
  },
  {
    id: 8, filter: 'basketball',
    badge: 'NBA FINALS', badgeColor: 'badge--blue',
    icon: '🏀', iconBg: '#0D1B2A',
    title: "Stephen Curry Scores 51 Points to Rescue Warriors in Game 7",
    excerpt: "Down by 18 points entering the fourth quarter, Curry's historic performance kept Golden State's dynasty alive.",
    author: 'Dana Jackson', time: '2 days ago',
  },
];

const LIVE_SCORES = [
  { league: 'UEFA Champions League', sport: '⚽', homeTeam: 'Real Madrid', awayTeam: 'Man City', homeIcon: '👑', awayIcon: '🌆', homeScore: 4, awayScore: 2, status: 'live', minute: "FT" },
  { league: 'NBA Playoffs', sport: '🏀', homeTeam: 'LA Lakers', awayTeam: 'Warriors', homeIcon: '💜', awayIcon: '💛', homeScore: 112, awayScore: 108, status: 'live', minute: "Q4 3:21" },
  { league: 'Premier League', sport: '⚽', homeTeam: 'Arsenal', awayTeam: 'Chelsea', homeIcon: '🔴', awayIcon: '🔵', homeScore: 1, awayScore: 1, status: 'live', minute: "67'" },
  { league: 'La Liga', sport: '⚽', homeTeam: 'Barcelona', awayTeam: 'Atletico', homeIcon: '🔵🔴', awayIcon: '🔴⬜', homeScore: 2, awayScore: 0, status: 'live', minute: "45+2'" },
  { league: 'NBA Playoffs', sport: '🏀', homeTeam: 'Celtics', awayTeam: 'Heat', homeIcon: '🍀', awayIcon: '🔥', homeScore: 98, awayScore: 94, status: 'live', minute: "Q3 8:44" },
  { league: 'Bundesliga', sport: '⚽', homeTeam: 'Bayern', awayTeam: 'Dortmund', homeIcon: '🔴', awayIcon: '⚫🟡', homeScore: 3, awayScore: 1, status: 'finished', minute: "FT" },
  { league: 'Serie A', sport: '⚽', homeTeam: 'AC Milan', awayTeam: 'Juventus', homeIcon: '⚫🔴', awayIcon: '⚫⬜', homeScore: 0, awayScore: 0, status: 'upcoming', minute: "19:45" },
  { league: 'Ligue 1', sport: '⚽', homeTeam: 'PSG', awayTeam: 'Lyon', homeIcon: '🔵🔴', awayIcon: '🔵⬜', homeScore: 2, awayScore: 1, status: 'live', minute: "82'" },
];

const VIDEOS = [
  { icon: '⚽', bg: 'linear-gradient(135deg,#1a1a24,#2E1B1B)', title: "Mbappe Hat-Trick Goals — All Three in Full", duration: '4:32', views: '2.4M', time: '3 hours ago', category: 'Football' },
  { icon: '🏀', bg: 'linear-gradient(135deg,#0D1B2A,#1B2A3A)', title: "Curry's Legendary 51-Point Game 7 Performance", duration: '8:15', views: '1.8M', time: '1 day ago', category: 'Basketball' },
  { icon: '🎾', bg: 'linear-gradient(135deg,#0D1F14,#1A2E1A)', title: "Epic 5th Set Tiebreak — Alcaraz vs Djokovic Wimbledon Final", duration: '12:04', views: '3.1M', time: '6 hours ago', category: 'Tennis' },
  { icon: '🏃', bg: 'linear-gradient(135deg,#1F1A00,#2E2A00)', title: "World Record 9.53s — Full Race Replay & Slow Motion", duration: '3:45', views: '5.7M', time: '8 hours ago', category: 'Athletics' },
  { icon: '🏏', bg: 'linear-gradient(135deg,#0D1F14,#1E2E1E)', title: "Last Ball Thriller — India's World Cup Winning Moment", duration: '6:20', views: '8.2M', time: '10 hours ago', category: 'Cricket' },
  { icon: '🏉', bg: 'linear-gradient(135deg,#1A1200,#2A2000)', title: "All Blacks' Incredible Second-Half Comeback in Full", duration: '9:58', views: '1.2M', time: '1 day ago', category: 'Rugby' },
];

const TOP_STORIES = [
  { title: "Djokovic Pulls Out of French Open Citing Knee Injury", meta: "Tennis • 30 min ago" },
  { title: "Premier League Unveils New 2026/27 Season Fixtures", meta: "Football • 1 hour ago" },
  { title: "Olympic Committee Confirms Paris Legacy Games for 2030", meta: "Athletics • 2 hours ago" },
  { title: "Tiger Woods Eyes Masters Return After Two-Year Absence", meta: "Golf • 3 hours ago" },
];

// ── RENDER ────────────────────────────────────────────────────────────────────

function buildTicker() {
  const content = document.getElementById('tickerContent');
  const doubled = [...TICKER_SCORES, ...TICKER_SCORES]; // seamless loop
  content.innerHTML = doubled.map(s =>
    `<span class="ticker__item">
      ${s.sport} <strong>${s.home}</strong>
      <span class="ticker__score">${s.scoreH} – ${s.scoreA}</span>
      <strong>${s.away}</strong>
      <span style="color:rgba(255,255,255,0.5);font-size:11px">${s.time}</span>
    </span>`
  ).join('');
}

function buildTopStories() {
  const container = document.getElementById('topStories');
  container.innerHTML = TOP_STORIES.map((s, i) =>
    `<div class="sidebar__item">
      <span class="sidebar__item-num">0${i + 1}</span>
      <div>
        <div class="sidebar__item-title">${s.title}</div>
        <div class="sidebar__item-meta">${s.meta}</div>
      </div>
    </div>`
  ).join('');
}

function buildNews() {
  const grid = document.getElementById('newsGrid');
  grid.innerHTML = NEWS_ARTICLES.map(a =>
    `<article class="news-card" data-filter="${a.filter}">
      <div class="news-card__img-placeholder" style="background:${a.iconBg}">${a.icon}</div>
      <div class="news-card__body">
        <div class="news-card__badge"><span class="badge ${a.badgeColor}">${a.badge}</span></div>
        <h3 class="news-card__title">${a.title}</h3>
        <p class="news-card__excerpt">${a.excerpt}</p>
        <div class="news-card__footer">
          <span class="news-card__author">${a.author}</span>
          <span>${a.time}</span>
        </div>
      </div>
    </article>`
  ).join('');
}

function buildScores() {
  const grid = document.getElementById('scoresGrid');
  grid.innerHTML = LIVE_SCORES.map(m => {
    const statusClass = m.status === 'live' ? '' : m.status;
    const statusLabel = m.status === 'live' ? '🔴 LIVE' : m.status === 'finished' ? 'FINISHED' : '🕐 UPCOMING';
    return `<div class="score-card">
      <div class="score-card__header">
        <span>${m.sport} ${m.league}</span>
        <span class="score-card__status ${statusClass}">${statusLabel}</span>
      </div>
      <div class="score-card__match">
        <div class="score-card__team">
          <span class="score-card__team-icon">${m.homeIcon}</span>
          <span class="score-card__team-name">${m.homeTeam}</span>
        </div>
        <div class="score-card__scores">
          <span class="score-card__score">${m.homeScore}</span>
          <span class="score-card__divider">–</span>
          <span class="score-card__score">${m.awayScore}</span>
        </div>
        <div class="score-card__team">
          <span class="score-card__team-icon">${m.awayIcon}</span>
          <span class="score-card__team-name">${m.awayTeam}</span>
        </div>
      </div>
      <div class="score-card__minute">${m.minute}</div>
    </div>`;
  }).join('');
}

function buildVideos() {
  const grid = document.getElementById('videosGrid');
  grid.innerHTML = VIDEOS.map(v =>
    `<div class="video-card">
      <div class="video-card__thumb">
        <div class="video-card__thumb-bg" style="background:${v.bg}">${v.icon}</div>
        <div class="video-card__play">
          <div class="video-card__play-btn">&#9654;</div>
        </div>
        <span class="video-card__duration">${v.duration}</span>
      </div>
      <div class="video-card__body">
        <div class="news-card__badge" style="margin-bottom:8px">
          <span class="badge badge--red" style="font-size:10px">${v.category}</span>
        </div>
        <div class="video-card__title">${v.title}</div>
        <div class="video-card__meta">${v.views} views &bull; ${v.time}</div>
      </div>
    </div>`
  ).join('');
}

// ── CATEGORY FILTER ───────────────────────────────────────────────────────────

function initCategoryFilter() {
  document.querySelectorAll('.cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      document.querySelectorAll('.news-card').forEach(card => {
        if (filter === 'all' || card.dataset.filter === filter) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

// ── COUNTER ANIMATION ─────────────────────────────────────────────────────────

function animateCounters() {
  const counters = document.querySelectorAll('.stat__number');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseInt(el.dataset.target, 10);
      const duration = 1800;
      const step = target / (duration / 16);
      let current = 0;
      const timer = setInterval(() => {
        current = Math.min(current + step, target);
        el.textContent = target >= 1000000
          ? (current / 1000000).toFixed(1) + 'M'
          : target >= 1000
          ? Math.round(current).toLocaleString()
          : Math.round(current);
        if (current >= target) clearInterval(timer);
      }, 16);
      observer.unobserve(el);
    });
  }, { threshold: 0.3 });
  counters.forEach(c => observer.observe(c));
}

// ── NEWSLETTER ────────────────────────────────────────────────────────────────

function initNewsletter() {
  document.getElementById('newsletterForm').addEventListener('submit', e => {
    e.preventDefault();
    const msg = document.getElementById('newsletterMsg');
    msg.textContent = '✓ You\'re subscribed! Check your inbox for a confirmation.';
    e.target.reset();
    setTimeout(() => { msg.textContent = ''; }, 5000);
  });
}

// ── HAMBURGER ─────────────────────────────────────────────────────────────────

function initHamburger() {
  document.getElementById('hamburger').addEventListener('click', () => {
    document.querySelector('.nav').classList.toggle('open');
  });
}

// ── DATE ──────────────────────────────────────────────────────────────────────

function setDate() {
  const el = document.getElementById('currentDate');
  if (el) {
    el.textContent = new Date().toLocaleDateString('en-US', {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
    });
  }
}

// ── LIVE SCORE UPDATES (simulated) ───────────────────────────────────────────

function simulateLiveUpdates() {
  setInterval(() => {
    const cards = document.querySelectorAll('.score-card');
    const liveCards = [...cards].filter(c => c.querySelector('.score-card__status:not(.finished):not(.upcoming)'));
    if (!liveCards.length) return;
    const card = liveCards[Math.floor(Math.random() * liveCards.length)];
    const scores = card.querySelectorAll('.score-card__score');
    if (!scores.length) return;
    const idx = Math.random() > 0.5 ? 0 : 1;
    scores[idx].textContent = parseInt(scores[idx].textContent) + 1;
    scores[idx].style.color = 'var(--yellow)';
    setTimeout(() => { scores[idx].style.color = ''; }, 800);
  }, 12000);
}

// ── INIT ──────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  setDate();
  buildTicker();
  buildTopStories();
  buildNews();
  buildScores();
  buildVideos();
  initCategoryFilter();
  animateCounters();
  initNewsletter();
  initHamburger();
  simulateLiveUpdates();
});
