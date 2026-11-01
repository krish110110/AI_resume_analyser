function initLogout() {
    const btn = document.getElementById('logoutBtn');
    if (!btn) return;
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        clearToken();
        clearUser();
        showToast('You have been logged out', 'info');
        setTimeout(() => {
            window.location.href = '../index.html';
        }, 500);
    });
}
