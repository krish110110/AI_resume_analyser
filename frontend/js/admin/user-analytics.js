function initUserAnalytics() {
    if (!requireAdmin()) return;
    initLogout();
    hideUploadForAdmin();

    const params = new URLSearchParams(window.location.search);
    const userId = params.get('userId');
    if (!userId) {
        window.location.href = 'users.html';
        return;
    }

    loadUserAnalytics(userId);
}

async function loadUserAnalytics(userId) {
    try {
        const data = await api.admin.getUserAnalytics(userId);
        const user = data.user;

        document.getElementById('userName').textContent = user.name || 'Unknown User';
        document.getElementById('userEmail').textContent = user.email || user.id;

        document.getElementById('statTotalReports').textContent = data.total_reports;
        document.getElementById('statAvgAts').textContent = data.avg_ats_score || 0;
        document.getElementById('statAvgSimilarity').textContent = data.avg_similarity_score || 0;
        document.getElementById('statAvgSkillMatch').textContent = (data.avg_skill_match || 0) + '%';

        // Build aggregated skill gaps across all reports
        const gapContainer = document.getElementById('skillGapsContainer');
        const allMissing = {};
        for (const r of data.reports) {
            for (const kw of r.missing_keywords || []) {
                allMissing[kw] = (allMissing[kw] || 0) + 1;
            }
        }
        const sortedGaps = Object.entries(allMissing).sort((a, b) => b[1] - a[1]);
        if (sortedGaps.length === 0) {
            gapContainer.innerHTML = emptyStateHtml('target', 'No skill gaps detected', 'All recommended skills are present in this user\'s resumes');
        } else {
            gapContainer.innerHTML = '<table class="admin-data-table"><thead><tr><th>Missing Skill</th><th>Occurrences</th></tr></thead><tbody>' +
                sortedGaps.map(([skill, count]) => `<tr><td><span class="skill-tag missing">${skill}</span></td><td>${count}</td></tr>`).join('') +
                '</tbody></table>';
        }

        renderInterviewQuestions(data.reports || []);

        const container = document.getElementById('reportsTable');
        if (!data.reports || data.reports.length === 0) {
            container.innerHTML = emptyStateHtml('list', 'No reports found', 'This user has not submitted any resumes');
            return;
        }

let html = '<table class="admin-data-table"><thead><tr><th>Candidate</th><th>File</th><th>ATS Score</th><th>Similarity</th><th>Skill Match</th><th>Category</th><th>Level</th><th>Date</th><th>Details</th></tr></thead><tbody>';
        for (const r of data.reports) {
            cacheReportDetail(r);
            const score = (r.ats_score ?? 0).toFixed(1);
            const similarity = (r.similarity_score ?? 0).toFixed(1);
            const skillMatch = (r.skill_match_percentage ?? 0).toFixed(1) + '%';
            const category = (r.classification && r.classification.category) || 'N/A';
            const level = (r.classification && r.classification.level) || 'N/A';
            const date = r.created_at ? new Date(r.created_at).toLocaleDateString() : 'N/A';
            const candidate = (r.parsed_data && r.parsed_data.name) || 'Not detected';

            html += `<tr class="admin-row-clickable" onclick="openReportDetails('${r.id}')" title="Click to view resume details">
                <td><button type="button" class="resume-link" onclick="event.stopPropagation(); openReportDetails('${r.id}')">${escapeHtml(candidate)}</button></td>
                <td>${escapeHtml(r.filename || 'N/A')}</td>
                <td>${score}</td>
                <td>${similarity}</td>
                <td>${skillMatch}</td>
                <td>${category}</td>
                <td>${level}</td>
                <td>${date}</td>
                <td><button class="admin-btn admin-btn-secondary btn-sm" onclick="event.stopPropagation(); openReportDetails('${r.id}')">View Resume</button></td>
            </tr>`;
        }
        html += '</tbody></table>';
        container.innerHTML = html;
    } catch (err) {
        console.error(err);
        showToast('Failed to load user analytics', 'error');
    }
}

function escapeHtml(value) {
    if (value === null || value === undefined) return '';
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function renderInterviewGroupHtml(group, index) {
    const questions = group.questions || [];
    const isOpen = index < 2;
    const questionHtml = questions.map((q, qi) => `
        <li class="interview-question-item">
            <div class="interview-question-text">
                <span class="interview-question-index">Q${qi + 1}.</span>
                <span>${escapeHtml(q.question)}</span>
            </div>
            <span class="difficulty-badge ${escapeHtml(q.difficulty || 'medium')}">${escapeHtml(q.difficulty || 'medium')}</span>
            ${q.answer ? `<div class="interview-answer"><strong>What to cover:</strong> ${escapeHtml(q.answer)}</div>` : ''}
        </li>
    `).join('');

    return `
        <div class="interview-group ${isOpen ? 'open' : ''}" data-group-index="${index}">
            <button type="button" class="interview-group-header" onclick="toggleInterviewGroup(${index})">
                <span class="interview-group-header-left">
                    <span class="interview-skill-name">${escapeHtml(group.skill || 'Skill')}</span>
                    <span class="interview-category">${escapeHtml(group.category || 'General')}</span>
                </span>
                <span class="interview-group-header-left">
                    <span class="interview-count-badge">${questions.length} questions</span>
                    <span class="interview-chevron">&#9662;</span>
                </span>
            </button>
            <ul class="interview-question-list">${questionHtml}</ul>
        </div>
    `;
}

function toggleInterviewGroup(index) {
    const group = document.querySelector(`#interviewQuestionsContainer .interview-group[data-group-index="${index}"]`);
    if (group) group.classList.toggle('open');
}

function renderInterviewQuestions(reports) {
    const container = document.getElementById('interviewQuestionsContainer');
    const summary = document.getElementById('interviewSummary');
    if (!container) return;

    // Use the most recent report that has interview questions attached.
    const withQuestions = (reports || []).filter(r => Array.isArray(r.interview_questions) && r.interview_questions.length > 0);

    if (withQuestions.length === 0) {
        if (summary) summary.innerHTML = '';
        container.innerHTML = emptyStateHtml('chat', 'No interview questions yet', 'Questions appear here after a resume is analysed and skills are extracted');
        return;
    }

    const latest = withQuestions[0];
    const groups = latest.interview_questions;
    const total = groups.reduce((sum, g) => sum + ((g.questions || []).length), 0);
    const hard = groups.reduce((sum, g) => sum + (g.questions || []).filter(q => q.difficulty === 'hard').length, 0);

    if (summary) {
        const parsed = latest.parsed_data || {};
        const candidate = parsed.name || 'Candidate name not detected';
        summary.innerHTML = `
            <span class="interview-count-badge">${escapeHtml(candidate)}</span>
            <span class="interview-count-badge">${escapeHtml(latest.filename || 'Latest resume')}</span>
            <span class="interview-count-badge">${groups.length} skills covered</span>
            <span class="interview-count-badge">${total} questions</span>
            <span class="interview-count-badge">${hard} hard questions</span>
        `;
    }

    container.innerHTML = groups.map((g, i) => renderInterviewGroupHtml(g, i)).join('');
}

function showReportDetails(reportId) {
    openReportDetails(reportId);
}

function downloadReport() {
    const container = document.getElementById('reportsTable');
    const rows = container.querySelectorAll('tbody tr');
    if (rows.length === 0) return;

    let csv = 'Filename,ATS Score,Similarity,Skill Match,Category,Level,Date\n';
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        csv += Array.from(cells).slice(0, 7).map(c => `"${c.textContent}"`).join(',') + '\n';
    });

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'user-analytics.csv';
    a.click();
    URL.revokeObjectURL(url);
}

window.showReportDetails = showReportDetails;
window.downloadReport = downloadReport;
window.toggleInterviewGroup = toggleInterviewGroup;
