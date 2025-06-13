/**
 * API Client for making requests to the backend
 */

class APIClient {
    constructor(baseURL = '/api/v1') {
        this.baseURL = baseURL;
        this.csrfToken = this.getCookie('csrftoken');
    }

    /**
     * Get CSRF token from cookies
     */
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Make an API request
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
                ...options.headers,
            },
            credentials: 'same-origin',
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'API request failed');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * GET request
     */
    get(endpoint, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        return this.request(url, { method: 'GET' });
    }

    /**
     * POST request
     */
    post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    /**
     * PUT request
     */
    put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    /**
     * PATCH request
     */
    patch(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    /**
     * DELETE request
     */
    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// Create global API client instance
const api = new APIClient();

// Example usage with Alpine.js
document.addEventListener('alpine:init', () => {
    Alpine.data('apiExample', () => ({
        stats: null,
        loading: false,
        error: null,

        async init() {
            await this.loadStats();
        },

        async loadStats() {
            this.loading = true;
            this.error = null;
            
            try {
                this.stats = await api.get('/dashboard/stats/');
            } catch (error) {
                this.error = error.message;
                console.error('Failed to load stats:', error);
            } finally {
                this.loading = false;
            }
        },

        async updateProfile(data) {
            try {
                const response = await api.patch('/users/profile/', data);
                Alpine.store('notifications').show('プロフィールが更新されました', 'success');
                return response;
            } catch (error) {
                Alpine.store('notifications').show('更新に失敗しました', 'error');
                throw error;
            }
        },

        async submitContact(formData) {
            try {
                const response = await api.post('/contacts/', formData);
                Alpine.store('notifications').show('お問い合わせを送信しました', 'success');
                return response;
            } catch (error) {
                Alpine.store('notifications').show('送信に失敗しました', 'error');
                throw error;
            }
        }
    }));
});