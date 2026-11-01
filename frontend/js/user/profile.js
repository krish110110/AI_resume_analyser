function initProfile() {
    if (!requireUser()) return;
    hideUploadForAdmin();
    initLogout();
    const user = getUser();
    if (user) {
        document.getElementById('name').value = user?.name || '';
        document.getElementById('email').value = user?.email || '';
    }
    document.getElementById('profileForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value.trim();
        const currentPassword = document.getElementById('currentPassword').value;
        const newPassword = document.getElementById('newPassword').value;
        const payload = { name };
        if (newPassword) {
            if (!currentPassword) {
                showToast('Current password is required', 'error');
                return;
            }
            payload.current_password = currentPassword;
            payload.new_password = newPassword;
        }

        const submitBtn = e.target.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Updating...';

        try {
            const updated = await api.users.updateMe(payload);
            setUser(updated);
            showToast('Profile updated successfully', 'success');
            document.getElementById('currentPassword').value = '';
            document.getElementById('newPassword').value = '';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Update Profile';
        } catch (err) {
            showToast(err.message, 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Update Profile';
        }
    });
}
