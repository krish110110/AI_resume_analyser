const API_BASE = 'http://localhost:8000/api/v1';

const getToken = () => localStorage.getItem('token');
const setToken = (token) => localStorage.setItem('token', token);
const clearToken = () => localStorage.removeItem('token');
const getUser = () => { try { return JSON.parse(localStorage.getItem('user')); } catch { return null; } };
const setUser = (user) => localStorage.setItem('user', JSON.stringify(user));
const clearUser = () => localStorage.removeItem('user');

async function request(path, options = {}) {
    const url = `${API_BASE}${path}`;
    const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(url, { ...options, headers });
    const data = await res.json().catch(() => ({}));
    if (res.status === 401) {
        clearToken();
        clearUser();
        if (path !== '/auth/login' && path !== '/auth/register') {
            window.location.href = '../auth/login.html';
        }
        return Promise.reject(new Error(data.detail || 'Unauthorized'));
    }
    if (!res.ok) throw new Error(data.detail || `Request failed with status ${res.status}`);
    return data;
}
