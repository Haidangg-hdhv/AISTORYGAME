const API_BASE = localStorage.getItem('story_api_base') || 'http://127.0.0.1:8000';

const storage = {
  get selectedWorld() {
    const raw = localStorage.getItem('story_selected_world');
    return raw ? JSON.parse(raw) : null;
  },
  set selectedWorld(value) {
    localStorage.setItem('story_selected_world', JSON.stringify(value));
  },
  get draftCharacter() {
    const raw = localStorage.getItem('story_character_draft');
    return raw ? JSON.parse(raw) : null;
  },
  set draftCharacter(value) {
    localStorage.setItem('story_character_draft', JSON.stringify(value));
  },
  get sessionId() {
    return sessionStorage.getItem('story_session_id') || null;
  },
  set sessionId(value) {
    if (value) sessionStorage.setItem('story_session_id', value);
    else sessionStorage.removeItem('story_session_id');
  },
  get theme() {
    return localStorage.getItem('story_theme') || 'light';
  },
  set theme(value) {
    if (value === 'dark') localStorage.setItem('story_theme', 'dark');
    else localStorage.setItem('story_theme', 'light');
  },
  clearGameSession() {
    sessionStorage.removeItem('story_session_id');
  }
  
};
function applyTheme() {
  document.body.classList.remove('theme-light', 'theme-dark');
  document.body.classList.add(storage.theme === 'dark' ? 'theme-dark' : 'theme-light');
}

function toggleTheme() {
  storage.theme = storage.theme === 'dark' ? 'light' : 'dark';
  applyTheme();
  updateThemeButtons();
}
function updateThemeButtons() {
  qsa('[data-theme-toggle]').forEach(btn => {
    btn.textContent = storage.theme === 'dark' ? '☀ Chế độ sáng' : '🌙 Chế độ tối';
  });
}

function qs(selector, root = document) { return root.querySelector(selector); }
function qsa(selector, root = document) { return [...root.querySelectorAll(selector)]; }
function esc(str) {
  return String(str ?? '')
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;')
    .replace(/'/g,'&#39;');
}
// Dán đoạn này đè lên hàm safeFetch cũ trong shared.js
async function safeFetch(path, options = {}) {
    options.headers = options.headers || {};
    options.headers['Content-Type'] = 'application/json';

    // 1. ÉP TRÌNH DUYỆT ĐỨNG YÊN CHỜ LẤY THẺ UID
    const uid = await new Promise((resolve) => {
        const unsubscribe = firebase.auth().onAuthStateChanged((user) => {
            unsubscribe(); // Lấy xong là ngắt máy quét luôn
            resolve(user ? user.uid : "anonymous");
        });
    });

    // 2. Dán đúng thẻ UID vào gói hàng
    options.headers['X-User-ID'] = uid;

    // 3. Gắn thẻ xong xuôi mới được phóng đi
    // (Lưu ý: Chỗ "http://127.0.0.1:8000" nếu code gốc của bạn xài biến API_BASE thì sửa lại thành API_BASE nhé)
    return fetch("http://127.0.0.1:8000" + path, options).then(async res => {
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Lỗi API");
        return data;
    });
}
function go(url) { window.location.href = url; }
document.addEventListener('DOMContentLoaded', () => {
  applyTheme();
  updateThemeButtons();

  qsa('[data-theme-toggle]').forEach(btn => {
    btn.addEventListener('click', () => {
      toggleTheme();
      updateThemeButtons();
    });
  });
});
function updateThemeButtons() {
  qsa('[data-theme-toggle]').forEach(btn => {
    btn.textContent =
      storage.theme === 'dark'
        ? '☀ Chế độ sáng'
        : '🌙 Chế độ tối';
  });
}


// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBdv3lxueUVBmWa8177Y8m6b8mO3aG8rJ8",
  authDomain: "ai-story-game-8c5f3.firebaseapp.com",
  projectId: "ai-story-game-8c5f3",
  storageBucket: "ai-story-game-8c5f3.firebasestorage.app",
  messagingSenderId: "578743195829",
  appId: "1:578743195829:web:ed581d8aacdd04ea2ec6fc",
  measurementId: "G-XVEV45JT4T"
};
// Phải có dòng này để bật Firebase lên nè
firebase.initializeApp(firebaseConfig);