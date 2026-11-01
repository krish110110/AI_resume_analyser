let reportInitialized = false;

function initReport() {
    if (!requireUser()) return;
    if (reportInitialized) return;
    reportInitialized = true;
    hideUploadForAdmin();
    initLogout();
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    const container = document.getElementById('reportContent');
    if (!id || !container) {
        if (container) {
            container.innerHTML = emptyStateHtml('document', 'No report selected', 'Select a report from your history to view details');
        }
        return;
    }
    loadReport(id);
}

async function loadReport(id) {
    const container = document.getElementById('reportContent');
    if (!container) return;
    if (container.dataset.loaded === 'true') return;
    if (container.dataset.loading === 'true') return;

    container.dataset.loading = 'true';
    container.innerHTML = '<p>Loading report...</p>';

    try {
        let data;
        const cached = sessionStorage.getItem('report_' + id);
        if (cached) {
            try {
                data = JSON.parse(cached);
                // Refetch cached reports stored before interview questions existed.
                if (data && data.interview_questions === undefined) data = null;
            } catch (e) { data = null; }
        }
        if (!data) {
            try {
                data = await api.reports.get(id);
            } catch (e) {
                try {
                    data = await api.reports.getByResume(id);
                } catch (e2) {
                    const reports = await api.reports.list();
                    const match = reports.find(r => r.id === id || r.resume_id === id);
                    if (match) {
                        data = await api.reports.get(match.id);
                    } else {
                        throw new Error('Report not found');
                    }
                }
            }
            try { sessionStorage.setItem('report_' + id, JSON.stringify(data)); } catch (e) {}
        }

        const atsScore = (data.ats_score ?? 0).toFixed(0);
        const scoreColor = atsScore >= 80 ? 'var(--success)' : atsScore >= 60 ? 'var(--warning)' : 'var(--danger)';
        const borderColor = atsScore >= 80 ? 'var(--success)' : atsScore >= 60 ? 'var(--warning)' : 'var(--danger)';

        const features = data.features || {};
        const classification = data.classification || {};
        const scores = data.scores || {};
        const skills = (data.skills || []).slice(0, 20);
        const missingKeywords = (data.missing_keywords || []).slice(0, 20);
        const parsed = data.parsed_data || {};
        const candidateName = parsed.name || 'Name not detected';
        const candidateEmail = parsed.email || '';
        const candidatePhone = parsed.phone || '';
        const interviewGroups = Array.isArray(data.interview_questions) ? data.interview_questions : [];
        const interviewTotal = interviewGroups.reduce((sum, g) => sum + ((g.questions || []).length), 0);
        const hardTotal = interviewGroups.reduce(
            (sum, g) => sum + (g.questions || []).filter(q => q.difficulty === 'hard').length,
            0
        );

        container.innerHTML = `
            <div class="score-header">
                <div>
                    <h2>${escapeHtml(candidateName)}</h2>
                    <p class="date">${escapeHtml(data.filename || 'Resume Analysis')} &middot; ${formatDate(data.created_at)}</p>
                    ${candidateEmail || candidatePhone ? `<p class="date">${escapeHtml([candidateEmail, candidatePhone].filter(Boolean).join(' | '))}</p>` : ''}
                </div>
                <div class="score-circle" style="border-color: ${borderColor}; color: ${scoreColor};">${atsScore}</div>
            </div>
            <div class="score-details">
                <div class="score-card">
                    <strong>ATS Score</strong>
                    <div style="color: ${borderColor}">${(data.ats_score ?? 0).toFixed(1)}/100</div>
                </div>
                <div class="score-card">
                    <strong>Similarity</strong>
                    <div>${(data.similarity_score ?? 0).toFixed(1)}%</div>
                </div>
                <div class="score-card">
                    <strong>Skill Match</strong>
                    <div>${(data.skill_match_percentage ?? 0).toFixed(1)}%</div>
                </div>
                ${classification.category ? `
                <div class="score-card">
                    <strong>Category</strong>
                    <div>${classification.category}</div>
                </div>` : ''}
                ${classification.level ? `
                <div class="score-card">
                    <strong>Level</strong>
                    <div>${classification.level}</div>
                </div>` : ''}
                ${classification.quality_score != null ? `
                <div class="score-card">
                    <strong>Quality Score</strong>
                    <div>${classification.quality_score.toFixed(1)}/100</div>
                </div>` : ''}
            </div>

            <div class="report-grid">
                <div class="chart-container">
                    <canvas id="scoreChart"></canvas>
                </div>
                <div class="chart-container">
                    <canvas id="skillsChart"></canvas>
                </div>
            </div>

            <h3 class="section-title">Skills Found</h3>
            <div class="skill-tags">
                ${skills.map(s => `<span class="skill-tag">${s}</span>`).join('') || '<span class="text-muted">No skills extracted</span>'}
            </div>

            <h3 class="section-title">Missing Keywords</h3>
            <div class="skill-tags">
                ${missingKeywords.map(k => `<span class="skill-tag missing">${k}</span>`).join('') || '<span class="text-muted">No missing keywords</span>'}
            </div>

            ${data.recommendations && data.recommendations.length > 0 ? `
            <h3 class="section-title">Recommendations</h3>
            <ul class="recommendations-list">
                ${data.recommendations.map(r => `<li>${escapeHtml(r)}</li>`).join('')}
            </ul>` : ''}

            <h3 class="section-title">Interview Questions</h3>
            <div class="interview-summary">
                <span class="interview-count-badge">${interviewGroups.length} skills covered</span>
                <span class="interview-count-badge">${interviewTotal} questions</span>
                <span class="interview-count-badge">${hardTotal} hard questions</span>
            </div>
            ${interviewGroups.length > 0 ? interviewGroups.map((group, gi) => renderInterviewGroup(group, gi)).join('') : `
            <p class="text-muted" style="font-size: 13px; margin-top: 10px;">No interview questions available for this resume.</p>`}
            <p id="reportLoaded" class="text-muted" style="font-size: 12px; margin-top: 8px;">Report loaded</p>
        `;

        container.dataset.loaded = 'true';
        container.dataset.loading = 'false';
        try {
            if (typeof Chart !== 'undefined') {
                renderScoreChart(scores);
                renderSkillsChart(features, missingKeywords.length);
            } else {
                const warning = document.createElement('p');
                warning.className = 'text-muted';
                warning.style.marginTop = '12px';
                warning.textContent = 'Charts are unavailable because Chart.js did not load.';
                container.appendChild(warning);
            }
        } catch (chartError) {
            console.error('Report chart error:', chartError);
        }
    } catch (err) {
        container.dataset.loading = 'false';
        container.innerHTML = emptyStateHtml('document', 'Failed to load report', `${escapeHtml(err.message || String(err))} &middot; <a href="history.html">Back to History</a>`);
    }
}

function renderInterviewGroup(group, index) {
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
    const group = document.querySelector(`.interview-group[data-group-index="${index}"]`);
    if (group) group.classList.toggle('open');
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

function renderScoreChart(scores) {
    const ctx = document.getElementById('scoreChart');
    if (!ctx) return;
    applyChartDefaults();
    const ats = (scores.ats_score ?? 0).toFixed(1);
    const similarity = (scores.similarity_score ?? 0).toFixed(1);
    const skillMatch = (scores.skill_match_percentage ?? 0).toFixed(1);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['ATS Score', 'Similarity', 'Skill Match'],
            datasets: [{
                label: 'Score',
                data: [ats, similarity, skillMatch],
                backgroundColor: [CHART_PALETTE[0], CHART_PALETTE[2], CHART_PALETTE[3]],
                borderRadius: 6,
                borderSkipped: false,
                maxBarThickness: 56
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: chartTitle('Score Overview')
            },
            scales: {
                y: linearScale(100),
                x: categoryScale()
            }
        }
    });
}

function renderSkillsChart(features, missingCount) {
    const ctx = document.getElementById('skillsChart');
    if (!ctx) return;
    const skills = features.skills || [];
    const education = (features.education || []).length;
    const experience = (features.experience || []).length;
    const projects = (features.projects || []).length;
    const certifications = (features.certifications || []).length;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Skills', 'Education', 'Experience', 'Projects', 'Certifications', 'Missing Keywords'],
            datasets: [{
                data: [skills.length, education, experience, projects, certifications, missingCount],
                backgroundColor: [CHART_PALETTE[0], CHART_PALETTE[1], CHART_PALETTE[2], CHART_PALETTE[4], CHART_PALETTE[6], CHART_PALETTE[8]],
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: chartLegend('bottom'),
                title: chartTitle('Resume Composition')
            }
        }
    });
}
