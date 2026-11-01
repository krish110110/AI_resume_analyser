function requireAuth() {
    const token = getToken();
    if (!token) { window.location.href = '../auth/login.html'; return false; }
    return true;
}

function requireAdmin() {
    if (!requireAuth()) return false;
    const user = getUser();
    if (!user || user.role !== 'admin') { window.location.href = '../auth/login.html'; return false; }
    return true;
}

function requireUser() {
    if (!requireAuth()) return false;
    const user = getUser();
    if (user && user.role === 'admin') { window.location.href = '../admin/dashboard.html'; return false; }
    return true;
}

function initLogout() {
    const btn = document.getElementById('logoutBtn');
    if (!btn) return;
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        clearToken();
        clearUser();
        window.location.href = '../index.html';
    });
}

function hideUploadForAdmin() {
    const user = getUser();
    if (user && user.role === 'admin') {
        const uploadLinks = document.querySelectorAll('a[href*="upload"]');
        uploadLinks.forEach(link => link.style.display = 'none');
    }
}
