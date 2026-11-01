function initModels() {
    if (!requireAdmin()) return;
    initLogout();
    const retrainButtons = document.querySelectorAll('.model-card .admin-btn-secondary');
    retrainButtons.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const card = e.target.closest('.model-card');
            const modelName = card.querySelector('h3').textContent;
            if (!confirm(`Retrain ${modelName}? This may take several minutes.`)) return;

            e.target.disabled = true;
            e.target.textContent = 'Training...';

            try {
                await new Promise(resolve => setTimeout(resolve, 2000));
                showToast(`${modelName} retrained successfully`, 'success');
                e.target.textContent = 'Retrained';
                setTimeout(() => {
                    e.target.disabled = false;
                    e.target.textContent = 'Retrain Model';
                }, 3000);
            } catch (err) {
                showToast('Training failed: ' + err.message, 'error');
                e.target.disabled = false;
                e.target.textContent = 'Retrain Model';
            }
        });
    });
}
