function initDashboard() {
    if (!requireUser()) return;
    hideUploadForAdmin();
    initLogout();
    initLogout();
    const user = getUser();
    if (user) {
        document.getElementById('userName').textContent = user.name || 'User';
        const avatar = document.getElementById('userAvatar');
        if (avatar) avatar.textContent = (user.name || 'U').charAt(0).toUpperCase();
    }
    loadStats();
    loadRecent();
}

async function loadStats() {
    try {
        const data = await api.dashboard.user();
        const resumesEl = document.getElementById('statResumes');
        const scoreEl = document.getElementById('statAvgScore');
        const matchesEl = document.getElementById('statMatches');

        if (resumesEl) animateCounter(resumesEl, data.total_resumes ?? 0);
        if (scoreEl) {
            const score = (data.avg_ats_score ?? 0);
            scoreEl.textContent = score.toFixed(1);
        }
        if (matchesEl) animateCounter(matchesEl, data.total_matches ?? 0);
    } catch (err) {
        console.error(err);
        showToast('Failed to load dashboard stats', 'error');
    }
}

async function loadRecent() {
    try {
        const data = await api.resumes.list();
        const container = document.getElementById('recentAnalyses');
        if (!data || data.length === 0) {
            container.innerHTML = emptyStateHtml('list', 'No analyses yet', 'Upload a resume to get started');
            return;
        }
        container.innerHTML = '<table class="data-table"><thead><tr><th>File</th><th>ATS Score</th><th>Status</th><th>Date</th></tr></thead><tbody>' +
            data.slice(0, 5).map(r => {
                const score = (r.ats_score ?? 0).toFixed(1);
                const scoreColor = score >= 80 ? 'var(--success)' : score >= 60 ? 'var(--warning)' : 'var(--danger)';
                return `<tr>
                    <td><strong>${r.filename}</strong></td>
                    <td><span style="color: ${scoreColor}; font-weight: 700;">${score}</span></td>
                    <td><span class="badge badge-${r.status === 'completed' ? 'success' : r.status === 'processing' ? 'warning' : 'danger'}">${r.status}</span></td>
                    <td>${formatDate(r.created_at)}</td>
                </tr>`;
            }).join('') +
            '</tbody></table>';
    } catch (err) {
        console.error(err);
    }
}
