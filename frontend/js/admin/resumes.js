function initResumes() {
    if (!requireAdmin()) return;
    initLogout();
    loadResumes();
    document.getElementById('refreshResumes').addEventListener('click', loadResumes);
    document.getElementById('resumeSearch').addEventListener('input', debounce((e) => loadResumes({ search: e.target.value }), 300));
}

async function loadResumes(params = {}) {
    try {
        const data = await api.admin.resumes(params);
        const container = document.getElementById('resumesTable');
        if (!data || data.length === 0) {
            container.innerHTML = emptyStateHtml('document', 'No resumes found', 'Try adjusting your search');
            return;
        }
        container.innerHTML = '<table class="data-table"><thead><tr><th>File</th><th>User</th><th>ATS Score</th><th>Status</th><th>Actions</th></tr></thead><tbody>' +
            data.map(r => {
                const score = (r.ats_score ?? 0).toFixed(1);
                const scoreColor = score >= 80 ? 'var(--success)' : score >= 60 ? 'var(--warning)' : 'var(--danger)';
                return `<tr>
                    <td><strong>${r.filename}</strong></td>
                    <td>${r.user_email || 'Unknown'}</td>
                    <td><span style="color: ${scoreColor}; font-weight: 700;">${score}</span></td>
                    <td><span class="badge badge-${r.status === 'completed' ? 'success' : r.status === 'processing' ? 'warning' : 'danger'}">${r.status}</span></td>
                    <td><button class="btn btn-danger btn-sm" onclick="deleteResume('${r.id}')">Delete</button></td>
                </tr>`;
            }).join('') +
            '</tbody></table>';
    } catch (err) {
        console.error(err);
        showToast('Failed to load resumes', 'error');
    }
}

async function deleteResume(id) {
    if (!confirm('Are you sure you want to delete this resume?')) return;
    try {
        await api.admin.deleteResume(id);
        showToast('Resume deleted successfully', 'success');
        loadResumes();
    } catch (err) {
        showToast(err.message, 'error');
    }
}
