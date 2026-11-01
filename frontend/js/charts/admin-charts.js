function renderAdminCharts(data) {
    if (!data) return;
    applyChartDefaults();

    const labels = data.labels || [];
    const ats = data.ats_scores || [];
    const volumes = data.report_volumes || [];
    const skills = data.skill_gaps || [];
    const users = data.user_growth || [];

    new Chart(document.getElementById('atsScoreChart'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Avg ATS Score',
                data: ats,
                backgroundColor: CHART_PALETTE[0],
                borderRadius: 6,
                borderSkipped: false,
                maxBarThickness: 42
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false }, title: chartTitle('ATS Score Distribution') },
            scales: { y: linearScale(100), x: categoryScale() }
        }
    });

    new Chart(document.getElementById('resumeVolumeChart'), {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Reports',
                data: volumes,
                borderColor: CHART_PALETTE[2],
                backgroundColor: 'rgba(4, 120, 87, 0.10)',
                fill: true,
                tension: 0.35,
                borderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 5,
                pointBackgroundColor: CHART_PALETTE[2],
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false }, title: chartTitle('Report Volume') },
            scales: { y: linearScale(null, 1), x: categoryScale() }
        }
    });

    new Chart(document.getElementById('skillGapChart'), {
        type: 'doughnut',
        data: {
            labels: skills.map(s => s.skill),
            datasets: [{
                data: skills.map(s => s.count),
                backgroundColor: CHART_PALETTE,
                borderColor: '#ffffff',
                borderWidth: 2,
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '62%',
            plugins: { legend: chartLegend('right'), title: chartTitle('Top Skill Gaps') }
        }
    });

    new Chart(document.getElementById('userGrowthChart'), {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'New Users',
                data: users,
                borderColor: CHART_PALETTE[3],
                backgroundColor: 'rgba(217, 119, 6, 0.10)',
                fill: true,
                tension: 0.35,
                borderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 5,
                pointBackgroundColor: CHART_PALETTE[3],
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false }, title: chartTitle('User Growth') },
            scales: { y: linearScale(null, 1), x: categoryScale() }
        }
    });
}