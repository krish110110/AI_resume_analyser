const CHART_PALETTE = ['#2563eb', '#0891b2', '#047857', '#d97706', '#7c3aed', '#be185d', '#475569', '#4d7c0f', '#b91c1c', '#0f766e'];
const CHART_COLORS = {
    grid: '#e2e8f0',
    tick: '#5b6b7f',
    title: '#0f172a',
    legend: '#475569'
};

function applyChartDefaults() {
    if (typeof Chart === 'undefined') return;
    Chart.defaults.font.family = "'Inter', system-ui, -apple-system, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = CHART_COLORS.tick;
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15, 23, 42, 0.95)';
    Chart.defaults.plugins.tooltip.titleColor = '#ffffff';
    Chart.defaults.plugins.tooltip.bodyColor = '#e2e8f0';
    Chart.defaults.plugins.tooltip.padding = 12;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    Chart.defaults.plugins.tooltip.boxPadding = 6;
}

function chartTitle(text) {
    return { display: true, text, color: CHART_COLORS.title, font: { size: 14, weight: '600' }, padding: { bottom: 16 } };
}

function chartLegend(position = 'right') {
    return {
        position,
        labels: { color: CHART_COLORS.legend, usePointStyle: true, pointStyle: 'circle', padding: 14, font: { size: 12 } }
    };
}

function linearScale(max, stepSize) {
    return {
        beginAtZero: true,
        ...(max ? { max } : {}),
        grid: { color: CHART_COLORS.grid, drawTicks: false },
        border: { display: false },
        ticks: { color: CHART_COLORS.tick, ...(stepSize ? { stepSize, precision: 0 } : {}) }
    };
}

function categoryScale() {
    return {
        grid: { display: false },
        border: { display: false },
        ticks: { color: CHART_COLORS.tick }
    };
}