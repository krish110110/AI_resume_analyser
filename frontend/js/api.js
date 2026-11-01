const api = {
    auth: {
        login: (payload) => request('/auth/login', { method: 'POST', body: JSON.stringify(payload) }),
        register: (payload) => request('/auth/register', { method: 'POST', body: JSON.stringify(payload) }),
        refresh: (payload) => request('/auth/refresh', { method: 'POST', body: JSON.stringify(payload) }),
        forgotPassword: (payload) => request('/auth/forgot-password', { method: 'POST', body: JSON.stringify(payload) }),
    },
    users: {
        me: () => request('/users/me'),
        updateMe: (payload) => request('/users/me', { method: 'PUT', body: JSON.stringify(payload) }),
    },
    admin: {
        stats: () => request('/admin/stats'),
        users: (params) => request(`/admin/users?${new URLSearchParams(params)}`),
        createUser: (payload) => request('/admin/users', { method: 'POST', body: JSON.stringify(payload) }),
        deleteUser: (id) => request(`/admin/users/${id}`, { method: 'DELETE' }),
        getUserAnalytics: (id) => request(`/admin/users/${id}/analytics`),
        reports: (params) => request(`/admin/reports?${new URLSearchParams(params)}`),
        getReport: (id) => request(`/admin/reports/${id}`),
        deleteResume: (id) => request(`/admin/resumes/${id}`, { method: 'DELETE' }),
        analytics: () => request('/admin/analytics'),
    },
    resumes: {
        upload: async (formData) => {
            const url = `${API_BASE}/resumes/upload`;
            const token = getToken();
            const headers = {};
            if (token) headers['Authorization'] = `Bearer ${token}`;
            const res = await fetch(url, { method: 'POST', body: formData, headers });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) throw new Error(data.detail || 'Upload failed');
            return data;
        },
        list: () => request('/resumes'),
        get: (id) => request(`/resumes/${id}`),
        delete: (id) => request(`/resumes/${id}`, { method: 'DELETE' }),
    },
    analysis: {
        create: (payload) => request('/analysis', { method: 'POST', body: JSON.stringify(payload) }),
        get: (id) => request(`/analysis/${id}`),
    },
    jobs: {
        create: (payload) => request('/jobs', { method: 'POST', body: JSON.stringify(payload) }),
        list: () => request('/jobs'),
        get: (id) => request(`/jobs/${id}`),
    },
    reports: {
        get: (id) => request(`/reports/${id}`),
        getByResume: (resumeId) => request(`/reports/by-resume/${resumeId}`),
        list: () => request('/reports'),
    },
    interview: {
        byResume: (resumeId) => request(`/interview-questions/by-resume/${resumeId}`),
        generate: (skills, perSkill) => request('/interview-questions/generate', { method: 'POST', body: JSON.stringify({ skills, per_skill: perSkill || 2 }) }),
        stats: () => request('/interview-questions/stats'),
        list: () => request('/interview-questions/'),
        bySkill: (skill) => request(`/interview-questions/by-skill/${encodeURIComponent(skill)}`),
        seed: (force) => request('/interview-questions/seed', { method: 'POST', body: JSON.stringify({ force: !!force }) }),
    },
    dashboard: {
        user: () => request('/dashboard/user'),
        admin: () => request('/dashboard/admin'),
    }
};
