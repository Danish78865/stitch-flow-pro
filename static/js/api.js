class ApiService {
    constructor() {
        this.baseURL = 'http://localhost:8000';
        this.token = localStorage.getItem('authToken');
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        if (this.token) {
            config.headers.Authorization = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                let errorMessage = `HTTP error! status: ${response.status}`;
                
                if (response.status === 401) {
                    // Token expired or invalid
                    this.logout();
                    throw new Error('Authentication required');
                }
                
                if (response.status === 400) {
                    // Bad request - try to get error details
                    try {
                        const errorData = await response.json();
                        errorMessage = errorData.detail || errorMessage;
                    } catch {
                        // If can't parse JSON, use default message
                    }
                }
                
                throw new Error(errorMessage);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Authentication methods
    async login(username, password) {
        const data = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        });
        this.token = data.access_token;
        localStorage.setItem('authToken', this.token);
        return data;
    }

    async register(userData) {
        return await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData),
        });
    }

    logout() {
        this.token = null;
        localStorage.removeItem('authToken');
        window.location.href = 'login.html';
    }

    // Dashboard methods
    async getDashboardStats() {
        return await this.request('/dashboard/stats');
    }

    // Project methods
    async getProjects() {
        return await this.request('/projects');
    }

    async createProject(projectData) {
        return await this.request('/projects', {
            method: 'POST',
            body: JSON.stringify(projectData),
        });
    }

    async getProject(projectId) {
        return await this.request(`/projects/${projectId}`);
    }

    // Task methods
    async getTasks(projectId = null, status = null) {
        const params = new URLSearchParams();
        if (projectId) params.append('project_id', projectId);
        if (status) params.append('status', status);
        
        const endpoint = params.toString() ? `/tasks?${params}` : '/tasks';
        return await this.request(endpoint);
    }

    async createTask(taskData) {
        return await this.request('/tasks', {
            method: 'POST',
            body: JSON.stringify(taskData),
        });
    }

    async updateTask(taskId, taskData) {
        return await this.request(`/tasks/${taskId}`, {
            method: 'PUT',
            body: JSON.stringify(taskData),
        });
    }

    // Team methods
    async getTeamMembers() {
        return await this.request('/team');
    }

    async addTeamMember(memberData) {
        return await this.request('/team', {
            method: 'POST',
            body: JSON.stringify(memberData),
        });
    }

    // Analytics methods
    async getAnalytics() {
        return await this.request('/analytics');
    }

    async getWorkloadData() {
        return await this.request('/analytics/workload');
    }

    async getTaskVelocity() {
        return await this.request('/analytics/velocity');
    }

    async getTeamDistribution() {
        return await this.request('/analytics/team-distribution');
    }

    // WebSocket connection for real-time updates
    connectWebSocket() {
        if (this.ws) {
            this.ws.close();
        }

        const wsURL = this.baseURL.replace('http', 'ws') + '/ws';
        this.ws = new WebSocket(wsURL);

        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
        };

        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.attemptReconnect();
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    handleWebSocketMessage(data) {
        // Emit custom events for different message types
        const event = new CustomEvent('realtime-update', { detail: data });
        document.dispatchEvent(event);

        // Handle specific message types
        switch (data.type) {
            case 'project_created':
                console.log('New project created:', data.data);
                break;
            case 'task_completed':
                console.log('Task completed:', data.data);
                break;
            case 'team_member_added':
                console.log('Team member added:', data.data);
                break;
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
            
            console.log(`Attempting to reconnect in ${delay}ms...`);
            setTimeout(() => {
                this.connectWebSocket();
            }, delay);
        } else {
            console.error('Max reconnection attempts reached');
        }
    }

    disconnectWebSocket() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }

    // Advanced API methods
    async duplicateProject(projectId) {
        return await this.request(`/projects/${projectId}/duplicate`, {
            method: 'POST'
        });
    }

    async completeTask(taskId) {
        return await this.request(`/tasks/${taskId}/complete`, {
            method: 'POST'
        });
    }

    async getSystemInfo() {
        return await this.request('/system/info');
    }

    async healthCheck() {
        return await this.request('/health');
    }
}

// Global API instance
const api = new ApiService();

// Utility functions for UI updates
function updateElementContent(selector, content) {
    const element = document.querySelector(selector);
    if (element) {
        element.textContent = content;
    }
}

function updateElementHTML(selector, html) {
    const element = document.querySelector(selector);
    if (element) {
        element.innerHTML = html;
    }
}

function showLoading(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.innerHTML = '<div class="text-center text-primary">Loading...</div>';
    }
}

function showError(selector, message) {
    const element = document.querySelector(selector);
    if (element) {
        element.innerHTML = `<div class="text-center text-error">Error: ${message}</div>`;
    }
}

// Authentication check
function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token && !window.location.pathname.includes('login.html')) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Format dates
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Calculate progress percentage
function calculateProgress(completed, total) {
    if (total === 0) return 0;
    return Math.round((completed / total) * 100);
}

// Status color mapping
function getStatusColor(status) {
    const colors = {
        'active': 'text-primary border-primary',
        'completed': 'text-emerald-400 border-emerald-400',
        'on_hold': 'text-amber-400 border-amber-400',
        'cancelled': 'text-error border-error',
        'todo': 'text-outline border-outline',
        'in_progress': 'text-secondary border-secondary',
        'review': 'text-tertiary border-tertiary',
        'delayed': 'text-error border-error'
    };
    return colors[status] || 'text-outline border-outline';
}

// Priority color mapping
function getPriorityColor(priority) {
    const colors = {
        'low': 'text-outline',
        'medium': 'text-secondary',
        'high': 'text-primary',
        'critical': 'text-error'
    };
    return colors[priority] || 'text-outline';
}
