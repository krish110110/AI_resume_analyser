function initAnalytics() {
    if (!requireAdmin()) return;
    initLogout();
    loadAnalytics();
}

async function loadAnalytics() {
    try {
        const data = await api.admin.analytics();
        renderAdminCharts(data);
        showToast('Analytics data loaded', 'success');
    } catch (err) {
        console.error(err);
        showToast('Failed to load analytics', 'error');
    }
}
