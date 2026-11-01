function initHistory() {
    if (!requireUser()) return;
    hideUploadForAdmin();
    initLogout();
    const user = getUser();
    const debugEl = document.getElementById('historyDebug');
    if (debugEl && user) {
        debugEl.textContent = `Logged in as: ${user.email}`;
    }
    loadHistory();
    const searchInput = document.getElementById('historySearch');
    if (searchInput) {
        searchInput.addEventListener('input', debounce((e) => {
            const term = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('#historyList table tbody tr');
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(term) ? '' : 'none';
            });
        }, 300));
    }
}

async function loadHistory() {
    try {
        const [resumes, reports] = await Promise.all([
            api.resumes.list(),
            api.reports.list()
        ]);
        const reportMap = {};
        reports.forEach(r => {
            if (r.resume_id) reportMap[r.resume_id] = r.id;
        });
        const container = document.getElementById('historyList');
        if (!resumes || resumes.length === 0) {
            container.innerHTML = emptyStateHtml('list', 'No history yet', 'Upload a resume to see your analysis history');
            return;
        }
        container.innerHTML = '<table class="data-table"><thead><tr><th>File</th><th>ATS Score</th><th>Status</th><th>Date</th><th>Action</th></tr></thead><tbody>' +
            resumes.map(r => {
                const score = (r.ats_score ?? 0).toFixed(1);
                const scoreColor = score >= 80 ? 'var(--success)' : score >= 60 ? 'var(--warning)' : 'var(--danger)';
                const reportId = reportMap[r.id];
                return `<tr>
                    <td><strong>${r.filename}</strong></td>
                    <td><span style="color: ${scoreColor}; font-weight: 700;">${score}</span></td>
                    <td><span class="badge badge-${r.status === 'completed' ? 'success' : r.status === 'processing' ? 'warning' : 'danger'}">${r.status}</span></td>
                    <td>${formatDate(r.created_at)}</td>
                    <td>${reportId ? `<a href="report.html?id=${reportId}" class="btn btn-primary btn-sm">View Report</a>` : '<span class="text-muted">Processing</span>'}</td>
                </tr>`;
            }).join('') +
            '</tbody></table>';
    } catch (err) {
        console.error(err);
        showToast('Failed to load history', 'error');
    }
}
