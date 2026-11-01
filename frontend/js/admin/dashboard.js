function initAdminDashboard() {
    if (!requireAdmin()) return;
    initLogout();
    const user = getUser();
    document.getElementById('adminName').textContent = user?.name || 'Admin';
    loadAdminStats();
    loadRecentActivity();
}

async function loadAdminStats() {
    try {
        const data = await api.dashboard.admin();
        const usersEl = document.getElementById('statUsers');
        const reportsEl = document.getElementById('statReports');
        const scoreEl = document.getElementById('statAvgScore');
        const healthEl = document.getElementById('statHealth');

        if (usersEl) animateCounter(usersEl, data.total_users ?? 0);
        if (reportsEl) animateCounter(reportsEl, data.total_reports ?? 0);
        if (scoreEl) {
            const score = (data.avg_ats_score ?? 0);
            scoreEl.textContent = score.toFixed(1);
        }
        if (healthEl) {
            healthEl.textContent = data.system_health || 'OK';
            if (data.system_health === 'OK') {
                healthEl.style.color = 'var(--success)';
            }
        }
    } catch (err) {
        console.error(err);
        showToast('Failed to load admin stats', 'error');
    }
}

async function loadRecentActivity() {
    try {
        const data = await api.admin.reports();
        const container = document.getElementById('recentActivity');
        if (!data || data.length === 0) {
            container.innerHTML = '<p class="text-muted">No recent activity.</p>';
            return;
        }
        container.innerHTML = '<table class="admin-data-table"><thead><tr><th>File</th><th>User</th><th>Score</th><th>Date</th></tr></thead><tbody>' +
            data.slice(0, 8).map(r => {
                const score = (r.ats_score ?? 0).toFixed(1);
                const user = r.user_name || r.user_email || r.user_id || 'Unknown';
                return `<tr class="admin-row-clickable" onclick="openReportDetails('${r.id}')">
                    <td><button type="button" class="resume-link" onclick="event.stopPropagation(); openReportDetails('${r.id}')">${escapeAdminHtml(r.filename || 'N/A')}</button></td>
                    <td>${escapeAdminHtml(user)}</td>
                    <td>${score}</td>
                    <td>${formatDate(r.created_at)}</td>
                </tr>`;
            }).join('') +
            '</tbody></table>';
    } catch (err) {
        console.error(err);
    }
}
