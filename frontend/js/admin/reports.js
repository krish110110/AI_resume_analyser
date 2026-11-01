function initAdminReports() {
    if (!requireAdmin()) return;
    initLogout();
    loadReports();
    document.getElementById('refreshReports')?.addEventListener('click', loadReports);
    document.getElementById('reportSearch')?.addEventListener('input', debounce(loadReports, 300));
}

async function loadReports() {
    try {
        const search = document.getElementById('reportSearch')?.value || '';
        const data = await api.admin.reports({ search });
        const container = document.getElementById('reportsTable');
        if (!data || data.length === 0) {
            container.innerHTML = '<p class="text-muted" style="padding:20px;">No reports found.</p>';
            return;
        }
        container.innerHTML = '<table class="admin-data-table"><thead><tr><th>File</th><th>User</th><th>ATS Score</th><th>Skill Match</th><th>Category</th><th>Level</th><th>Date</th></tr></thead><tbody>' +
            data.map(r => {
                const score = (r.ats_score ?? 0).toFixed(1);
                const skillMatch = (r.skill_match_percentage ?? 0).toFixed(1) + '%';
                const user = r.user_name || r.user_email || r.user_id || 'Unknown';
                return `<tr class="admin-row-clickable" onclick="openReportDetails('${r.id}')" title="Click to view resume details">
                    <td><button type="button" class="resume-link" onclick="event.stopPropagation(); openReportDetails('${r.id}')">${escapeAdminHtml(r.filename || 'N/A')}</button></td>
                    <td>${escapeAdminHtml(user)}</td>
                    <td>${score}</td>
                    <td>${skillMatch}</td>
                    <td>${escapeAdminHtml(r.category || 'N/A')}</td>
                    <td>${escapeAdminHtml(r.level || 'N/A')}</td>
                    <td>${formatDate(r.created_at)}</td>
                </tr>`;
            }).join('') +
            '</tbody></table>';
    } catch (err) {
        console.error(err);
        showToast('Failed to load reports', 'error');
    }
}
