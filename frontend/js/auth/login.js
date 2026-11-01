function initLogin() {
    clearToken();
    clearUser();
    const form = document.getElementById('loginForm');
    if (!form) return;
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = form.email.value.trim();
        const password = form.password.value;
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Signing in...';

        try {
            const data = await api.auth.login({ email, password });
            setToken(data.access_token);
            setUser(data.user);
            showToast('Welcome back! Redirecting...', 'success');
            setTimeout(() => {
                if (data.user.role === 'admin') {
                    window.location.href = '../admin/dashboard.html';
                } else {
                    window.location.href = '../user/dashboard.html';
                }
            }, 500);
        } catch (err) {
            showToast(err.message, 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Sign In';
        }
    });
}
