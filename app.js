const storageKey = 'cwUser';

function loadUser() {
    const data = localStorage.getItem(storageKey);
    return data ? JSON.parse(data) : {
        points: 0,
        totalPoints: 0,
        totalCO2: 0,
        streak: 0,
        level: 1,
        lastActionDate: null
    };
}

function saveUser(user) {
    localStorage.setItem(storageKey, JSON.stringify(user));
}

const user = loadUser();

function updateDashboard() {
    if (document.getElementById('availablePts')) {
        document.getElementById('availablePts').textContent = user.points;
        document.getElementById('totalPts').textContent = user.totalPoints;
    }
    if (document.getElementById('totalCO2')) {
        document.getElementById('totalCO2').textContent = user.totalCO2.toFixed(1);
    }
    if (document.getElementById('level')) {
        document.getElementById('level').textContent = user.level;
    }
    if (document.getElementById('levelProgress')) {
        const progress = (user.totalPoints % 100) / 100 * 100;
        document.getElementById('levelProgress').style.width = progress + '%';
    }
}

function updateStreak() {
    const container = document.getElementById('streakContainer');
    if (!container) return;
    container.innerHTML = '';
    for (let i = 0; i < 5; i++) {
        const div = document.createElement('div');
        div.className = 'streak-circle' + (i < user.streak ? ' streak-filled' : '');
        container.appendChild(div);
    }
}

function logAction(type) {
    let pts = 0, co2 = 0;
    if (type === 'transport') { pts = 10; co2 = 0.5; }
    if (type === 'cup') { pts = 5; co2 = 0.2; }
    const today = new Date().toISOString().split('T')[0];
    if (user.lastActionDate !== today) {
        if (user.lastActionDate && new Date(today) - new Date(user.lastActionDate) === 86400000) {
            user.streak += 1;
        } else {
            user.streak = 1;
        }
        user.lastActionDate = today;
        if (user.streak === 5) {
            pts += 10; // bonus
            alert('5-day streak! +10 bonus points!');
            user.streak = 0;
        }
    }
    user.points += pts;
    user.totalPoints += pts;
    user.totalCO2 += co2;
    user.level = Math.floor(user.totalPoints / 100) + 1;
    saveUser(user);
    updateDashboard();
    updateStreak();
}

document.addEventListener('DOMContentLoaded', () => {
    updateDashboard();
    updateStreak();
    const transportBtn = document.getElementById('publicTransportBtn');
    if (transportBtn) transportBtn.addEventListener('click', () => logAction('transport'));
    const cupBtn = document.getElementById('reusableCupBtn');
    if (cupBtn) cupBtn.addEventListener('click', () => logAction('cup'));
});
