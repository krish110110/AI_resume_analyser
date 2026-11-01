function initUsers() {
    if (!requireAdmin()) return;
    initLogout();
    loadUsers();
    document.getElementById('refreshUsers').addEventListener('click', loadUsers);
    document.getElementById('userSearch').addEventListener('input', debounce((e) => loadUsers({ search: e.target.value }), 300));
    document.getElementById('addUserBtn').addEventListener('click', () => {
        document.getElementById('addUserModal').style.display = 'block';
    });
}

function closeAddUserModal() {
    document.getElementById('addUserModal').style.display = 'none';
}

async function submitAddUser() {
    const name = document.getElementById('addUserName').value;
    const email = document.getElementById('addUserEmail').value;
    const password = document.getElementById('addUserPassword').value;
    const role = document.getElementById('addUserRole').value;

    if (!name || !email || !password) {
        showToast('Name, email, and password are required', 'error');
        return;
    }

    try {
        await api.admin.createUser({ name, email, password, role });
        showToast('User created successfully', 'success');
        closeAddUserModal();
        document.getElementById('addUserForm').reset();
        loadUsers();
    } catch (err) {
        showToast(err.message, 'error');
    }
}

async function loadUsers(params = {}) {
    try {
        const data = await api.admin.users(params);
        const container = document.getElementById('usersTable');
        if (!data || data.length === 0) {
            container.innerHTML = emptyStateHtml('users', 'No users found', 'Try adjusting your search');
            return;
        }
        container.innerHTML = '<table class="admin-data-table"><thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Actions</th></tr></thead><tbody>' +
            data.map(u => `<tr>
                <td><strong>${u.name}</strong></td>
                <td>${u.email}</td>
                <td><span class="admin-badge admin-badge-primary">${u.role}</span></td>
                <td><span class="admin-badge admin-badge-${u.is_active ? 'success' : 'danger'}">${u.is_active ? 'Active' : 'Inactive'}</span></td>
                <td><button class="admin-btn admin-btn-danger btn-sm" onclick="deleteUser('${u.id}')">Delete</button></td>
            </tr>`).join('') +
            '</tbody></table>';

        const rows = container.querySelectorAll('tbody tr');
        rows.forEach((row, idx) => {
            const userId = data[idx].id;
            row.querySelector('td:first-child').style.cursor = 'pointer';
            row.querySelector('td:first-child').onclick = () => window.location.href = `user-analytics.html?userId=${userId}`;
        });
    } catch (err) {
        console.error(err);
        showToast('Failed to load users', 'error');
    }
}

async function deleteUser(id) {
    if (!confirm('Are you sure you want to delete this user?')) return;
    try {
        await api.admin.deleteUser(id);
        showToast('User deleted successfully', 'success');
        loadUsers();
    } catch (err) {
        showToast(err.message, 'error');
    }
}

window.closeAddUserModal = closeAddUserModal;
window.submitAddUser = submitAddUser;
window.deleteUser = deleteUser;
