const ALLOWED_EXTENSIONS = ['pdf', 'docx', 'txt'];
const MAX_FILE_SIZE_MB = 10;

function initUpload() {
    if (!requireUser()) return;
    hideUploadForAdmin();
    initLogout();

    const form = document.getElementById('uploadForm');
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('resumeFile');
    const fileInfo = document.getElementById('fileInfo');
    const fileError = document.getElementById('fileError');
    const jobDescription = document.getElementById('jobDescription');
    const jobDescCount = document.getElementById('jobDescCount');
    const submitBtn = document.getElementById('analyzeBtn');

    function showFileError(message) {
        if (!message) {
            fileError.classList.add('hidden');
            fileError.textContent = '';
            uploadZone.classList.remove('invalid');
            return;
        }
        fileError.textContent = message;
        fileError.classList.remove('hidden');
        uploadZone.classList.add('invalid');
    }

    function validateFile(file) {
        if (!file) return 'Please select a resume file.';

        const ext = file.name.split('.').pop().toLowerCase();
        if (!ALLOWED_EXTENSIONS.includes(ext)) {
            return `"${ext.toUpperCase()}" files are not supported. Upload a PDF, DOCX, or TXT file.`;
        }
        if (file.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
            return `That file is ${(file.size / 1024 / 1024).toFixed(1)} MB. The maximum size is ${MAX_FILE_SIZE_MB} MB.`;
        }
        if (file.size === 0) {
            return 'That file is empty. Please upload a resume with content.';
        }
        return null;
    }

    function updateFileInfo(file) {
        if (!file) return;
        const error = validateFile(file);
        showFileError(error);
        if (error) return;

        const ext = file.name.split('.').pop().toUpperCase();
        document.getElementById('fileIcon').textContent = ext;
        document.getElementById('fileName').textContent = file.name;
        const sizeKb = file.size / 1024;
        document.getElementById('fileSize').textContent =
            sizeKb >= 1024 ? (sizeKb / 1024).toFixed(2) + ' MB' : sizeKb.toFixed(1) + ' KB';
        fileInfo.classList.add('visible');
    }

    function clearFile() {
        fileInput.value = '';
        fileInfo.classList.remove('visible');
        showFileError(null);
    }

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            updateFileInfo(e.target.files[0]);
        }
    });

    document.getElementById('fileRemove').addEventListener('click', clearFile);

    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            updateFileInfo(files[0]);
        }
    });

    uploadZone.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });

    jobDescription.addEventListener('input', () => {
        const length = jobDescription.value.trim().length;
        jobDescCount.textContent = `${length} character${length === 1 ? '' : 's'}`;
    });

    // Analysis type segmented control
    const segments = form.querySelectorAll('.segment');
    segments.forEach((segment) => {
        segment.addEventListener('click', () => {
            segments.forEach((s) => s.classList.remove('active'));
            segment.classList.add('active');
            segment.querySelector('input').checked = true;
        });
    });

    // Staged progress indicator
    const STAGES = [
        { key: 'upload', percent: 30, label: 'Uploading file...' },
        { key: 'extract', percent: 55, label: 'Extracting your skills...' },
        { key: 'score', percent: 80, label: 'Scoring your resume...' },
        { key: 'questions', percent: 95, label: 'Building interview questions...' },
    ];
    const progressSteps = Array.from(document.querySelectorAll('#progressSteps .progress-step'));
    let stageTimer = null;

    function setStage(index) {
        const stage = STAGES[index];
        if (!stage) return;
        document.getElementById('progressBar').style.width = stage.percent + '%';
        document.getElementById('progressPercent').textContent = stage.percent + '%';
        document.getElementById('progressText').textContent = stage.label;
        progressSteps.forEach((step, i) => {
            step.classList.toggle('done', i < index);
            step.classList.toggle('active', i === index);
        });
    }

    function startStages() {
        document.getElementById('uploadProgress').classList.remove('hidden');
        setStage(0);
        let index = 1;
        stageTimer = setInterval(() => {
            if (index >= STAGES.length) {
                clearInterval(stageTimer);
                stageTimer = null;
                return;
            }
            setStage(index);
            index += 1;
        }, 900);
    }

    function stopStages() {
        if (stageTimer) {
            clearInterval(stageTimer);
            stageTimer = null;
        }
    }

    function setSubmitting(isSubmitting) {
        submitBtn.disabled = isSubmitting;
        submitBtn.querySelector('.btn-label').textContent =
            isSubmitting ? 'Analyzing...' : 'Analyze Resume';
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const file = fileInput.files[0];
        const error = validateFile(file);
        if (error) {
            showFileError(error);
            showToast(error, 'error');
            uploadZone.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return;
        }

        const jobDescriptionText = jobDescription.value.trim();
        const formData = new FormData();
        formData.append('file', file);
        if (jobDescriptionText) formData.append('job_description', jobDescriptionText);
        const selectedSegment = form.querySelector('.segment.active input');
        formData.append('analysis_type', selectedSegment ? selectedSegment.value : 'full');

        setSubmitting(true);
        startStages();

        try {
            const data = await api.resumes.upload(formData);
            stopStages();
            document.getElementById('progressBar').style.width = '100%';
            document.getElementById('progressPercent').textContent = '100%';
            document.getElementById('progressText').textContent = 'Analysis complete!';
            progressSteps.forEach((step) => {
                step.classList.remove('active');
                step.classList.add('done');
            });
            showToast('Resume analyzed successfully', 'success');
            setTimeout(() => {
                window.location.href = `report.html?id=${data.report_id}`;
            }, 900);
        } catch (err) {
            stopStages();
            setSubmitting(false);
            document.getElementById('uploadProgress').classList.add('hidden');
            progressSteps.forEach((step) => {
                step.classList.remove('active', 'done');
            });
            showToast(err.message || 'Upload failed', 'error');
        }
    });
}