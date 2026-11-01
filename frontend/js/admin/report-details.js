const reportDetailCache = new Map();

function escapeAdminHtml(value) {
    if (value === null || value === undefined) return '';
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function cacheReportDetail(report) {
    if (report && report.id) reportDetailCache.set(report.id, report);
}

function formatResumeMetaValue(value, suffix = '') {
    if (value === null || value === undefined || value === '') return 'N/A';
    if (typeof value === 'number') {
        return suffix === 'bytes' ? `${(value / 1024).toFixed(1)} KB` : `${value}${suffix}`;
    }
    return `${value}${suffix}`;
}

function renderResumeFileMeta(resume) {
    if (!resume) return '';
    const type = (resume.file_type || '').toUpperCase();
    const size = formatResumeMetaValue(resume.file_size, 'bytes');
    const status = resume.status ? resume.status.toString() : 'N/A';
    return `<div class="resume-preview-meta">
        <span class="admin-badge admin-badge-primary">${escapeAdminHtml(type || 'FILE')}</span>
        <span class="admin-badge admin-badge-success">${escapeAdminHtml(size)}</span>
        <span class="admin-badge admin-badge-warning">${escapeAdminHtml(status)}</span>
    </div>`;
}

function renderResumeTextSection(report) {
    const resume = report.resume || null;
    const text = (resume && resume.text) || '';

    const header = `<div class="report-detail-actions">
        <h4 style="margin:0;flex:1;">Resume Content</h4>
        <button class="admin-btn admin-btn-secondary btn-sm" type="button" onclick="copyResumeText()">Copy Text</button>
        <button class="admin-btn admin-btn-secondary btn-sm" type="button" onclick="downloadResumeText()">Download</button>
    </div>`;

    if (!text) {
        return `<div class="report-detail-section" style="grid-column: 1 / -1;">
            ${header}
            <p class="text-muted">Resume text is not available for this report.</p>
        </div>`;
    }

    const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
    return `<div class="report-detail-section" style="grid-column: 1 / -1;">
        ${header}
        ${renderResumeFileMeta(resume)}
        <div class="resume-preview" id="resumeTextPreview">${escapeAdminHtml(text)}</div>
        <p class="text-muted" style="margin-top:10px;font-size:12px;">${wordCount} words &middot; ${text.length} characters extracted</p>
    </div>`;
}

function currentResumeText() {
    const el = document.getElementById('resumeTextPreview');
    return el ? el.textContent : '';
}

function currentResumeFilename() {
    const title = document.getElementById('reportDetailTitle');
    const name = title ? title.textContent : 'resume';
    return name.replace(/[^a-zA-Z0-9._-]+/g, '_');
}

async function copyResumeText() {
    const text = currentResumeText();
    if (!text) {
        showToast('No resume text to copy', 'error');
        return;
    }
    try {
        await navigator.clipboard.writeText(text);
        showToast('Resume text copied to clipboard', 'success');
    } catch (err) {
        showToast('Could not copy resume text', 'error');
    }
}

function downloadResumeText() {
    const text = currentResumeText();
    if (!text) {
        showToast('No resume text to download', 'error');
        return;
    }
    const name = currentResumeFilename();
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${name.replace(/\.[^.]+$/, '')}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

function renderReportDetailBody(report) {
    const parsed = report.parsed_data || {};
    const classification = report.classification || {};
    const scores = report.scores || {};

    const skills = (report.skills || []).join(', ') || 'None';
    const missing = (report.missing_keywords || []).join(', ') || 'None';
    const recommendations = (report.recommendations || []).join('  |  ') || 'None';

    const name = parsed.name || 'Not detected';
    const email = parsed.email || 'Not detected';
    const phone = parsed.phone || 'Not detected';
    const experience = parsed.experience ? JSON.stringify(parsed.experience) : 'N/A';
    const education = parsed.education ? JSON.stringify(parsed.education) : 'N/A';

    return `
        <div class="report-detail-grid">
            <div class="report-detail-section">
                <h4>Overview</h4>
                <table class="report-detail-table">
                    <tr><td>Candidate</td><td>${escapeAdminHtml(name)}</td></tr>
                    <tr><td>Owner</td><td>${escapeAdminHtml(report.user_name || report.user_id || 'Unknown')}</td></tr>
                    <tr><td>Owner Email</td><td>${escapeAdminHtml(report.user_email || 'N/A')}</td></tr>
                    <tr><td>ATS Score</td><td>${report.ats_score ?? 0}</td></tr>
                    <tr><td>Similarity Score</td><td>${report.similarity_score ?? 0}</td></tr>
                    <tr><td>Skill Match</td><td>${report.skill_match_percentage ?? 0}%</td></tr>
                    <tr><td>Quality Score</td><td>${scores.quality_score ?? 'N/A'}</td></tr>
                    <tr><td>Category</td><td>${escapeAdminHtml(classification.category || 'N/A')}</td></tr>
                    <tr><td>Level</td><td>${escapeAdminHtml(classification.level || 'N/A')}</td></tr>
                    <tr><td>Analyzed On</td><td>${report.created_at ? formatDate(report.created_at) : 'N/A'}</td></tr>
                </table>
            </div>
            <div class="report-detail-section">
                <h4>Candidate Details</h4>
                <table class="report-detail-table">
                    <tr><td>Name</td><td>${escapeAdminHtml(name)}</td></tr>
                    <tr><td>Email</td><td>${escapeAdminHtml(email)}</td></tr>
                    <tr><td>Phone</td><td>${escapeAdminHtml(phone)}</td></tr>
                    <tr><td>Experience</td><td>${escapeAdminHtml(experience)}</td></tr>
                    <tr><td>Education</td><td>${escapeAdminHtml(education)}</td></tr>
                </table>
            </div>
            <div class="report-detail-section">
                <h4>Detected Skills</h4>
                <p>${escapeAdminHtml(skills)}</p>
            </div>
            <div class="report-detail-section">
                <h4>Missing Keywords</h4>
                <p>${escapeAdminHtml(missing)}</p>
            </div>
            <div class="report-detail-section" style="grid-column: 1 / -1;">
                <h4>Recommendations</h4>
                <p>${escapeAdminHtml(recommendations)}</p>
            </div>
            ${renderResumeTextSection(report)}
            <div class="report-detail-section" style="grid-column: 1 / -1;">
                <h4>Interview Questions</h4>
                ${renderAdminModalInterviewQuestions(report.interview_questions)}
            </div>
        </div>
    `;
}

function renderAdminModalInterviewQuestions(groups) {
    if (!Array.isArray(groups) || groups.length === 0) {
        return '<p class="text-muted">No interview questions available for this report.</p>';
    }
    return groups.map((group, gi) => `
        <div class="interview-group open" data-group-index="modal-${gi}">
            <button type="button" class="interview-group-header" onclick="toggleModalInterviewGroup('modal-${gi}')">
                <span class="interview-group-header-left">
                    <span class="interview-skill-name">${escapeAdminHtml(group.skill || 'Skill')}</span>
                    <span class="interview-category">${escapeAdminHtml(group.category || 'General')}</span>
                </span>
                <span class="interview-group-header-left">
                    <span class="interview-count-badge">${(group.questions || []).length} questions</span>
                    <span class="interview-chevron">&#9662;</span>
                </span>
            </button>
            <ul class="interview-question-list">
                ${(group.questions || []).map((q, qi) => `
                    <li class="interview-question-item">
                        <div class="interview-question-text">
                            <span class="interview-question-index">Q${qi + 1}.</span>
                            <span>${escapeAdminHtml(q.question)}</span>
                        </div>
                        <span class="difficulty-badge ${escapeAdminHtml(q.difficulty || 'medium')}">${escapeAdminHtml(q.difficulty || 'medium')}</span>
                        ${q.answer ? `<div class="interview-answer"><strong>What to cover:</strong> ${escapeAdminHtml(q.answer)}</div>` : ''}
                    </li>
                `).join('')}
            </ul>
        </div>
    `).join('');
}

function toggleModalInterviewGroup(index) {
    const group = document.querySelector(`#reportDetailBody .interview-group[data-group-index="${index}"]`);
    if (group) group.classList.toggle('open');
}

async function openReportDetails(reportId, preset) {
    const modal = document.getElementById('reportDetailsModal');
    if (!modal || !reportId) return;

    const titleEl = modal.querySelector('#reportDetailTitle');
    const bodyEl = modal.querySelector('#reportDetailBody');

    if (preset) cacheReportDetail(preset);

    modal.style.display = 'block';
    bodyEl.innerHTML = '<p class="text-muted">Loading resume details...</p>';

    let report = reportDetailCache.get(reportId);
    if (!report) {
        try {
            report = await api.admin.getReport(reportId);
            cacheReportDetail(report);
        } catch (err) {
            console.error(err);
            bodyEl.innerHTML = '<p class="text-muted">Failed to load report details.</p>';
            showToast('Failed to load report details', 'error');
            return;
        }
    }

    const parsed = report.parsed_data || {};
    titleEl.textContent = `${report.filename || 'Report'}${parsed.name ? ` — ${parsed.name}` : ''}`;
    bodyEl.innerHTML = renderReportDetailBody(report);
}

function closeReportDetails() {
    const modal = document.getElementById('reportDetailsModal');
    if (modal) modal.style.display = 'none';
}

window.escapeAdminHtml = escapeAdminHtml;
window.openReportDetails = openReportDetails;
window.closeReportDetails = closeReportDetails;
window.cacheReportDetail = cacheReportDetail;
window.toggleModalInterviewGroup = toggleModalInterviewGroup;
window.copyResumeText = copyResumeText;
window.downloadResumeText = downloadResumeText;