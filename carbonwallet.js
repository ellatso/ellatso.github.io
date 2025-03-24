// carbonwallet.js
document.addEventListener('DOMContentLoaded', () => {
    // 訂閱表單處理
    const subscribeForm = document.getElementById('subscribeForm');
    const emailInput = document.getElementById('emailInput');
    const subscribeMessage = document.getElementById('subscribeMessage');

    subscribeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = emailInput.value;
        
        if (validateEmail(email)) {
            subscribeMessage.textContent = '感謝訂閱！我們將與您分享最新的碳減排進展。';
            subscribeMessage.style.color = 'green';
            emailInput.value = '';
        } else {
            subscribeMessage.textContent = '請輸入有效的電子郵件地址。';
            subscribeMessage.style.color = 'red';
        }
    });

    // Email 驗證函數
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // 數字動畫效果
    function animateValue(id, start, end, duration) {
        const element = document.getElementById(id);
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            element.textContent = Math.floor(progress * (end - start) + start).toLocaleString();
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // 初始化數字動畫
    animateValue('carbonReduction', 0, 245620, 2000);
    animateValue('brandCount', 0, 47, 1500);
    animateValue('userCount', 0, 12500, 2500);

    // 支持按鈕互動
    const supportBtn = document.getElementById('supportBtn');
    supportBtn.addEventListener('click', () => {
        alert('感謝您對減碳行動的支持！我們將很快與您聯繫。');
    });
});
