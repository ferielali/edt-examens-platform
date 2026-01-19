import axios, { AxiosInstance, AxiosError } from 'axios';

// Types
export interface User {
    id: number;
    email: string;
    nom: string | null;
    prenom: string | null;
    role: string;
    nom_complet: string;
}

export interface LoginResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
}

export interface DashboardStats {
    total_etudiants: number;
    total_professeurs: number;
    total_formations: number;
    total_modules: number;
    total_examens_planifies: number;
    total_salles: number;
    taux_occupation_salles: number;
    nb_conflits_actifs: number;
}

export interface DepartementKPI {
    departement_id: number;
    departement_nom: string;
    nb_etudiants: number;
    nb_professeurs: number;
    nb_examens: number;
    taux_planification: number;
    nb_conflits: number;
}

export interface Departement {
    id: number;
    nom: string;
    code: string;
    batiment: string | null;
    nb_formations?: number;
    nb_etudiants?: number;
    nb_professeurs?: number;
}

export interface Formation {
    id: number;
    nom: string;
    code: string;
    dept_id: number;
    niveau: string | null;
    type_formation: string | null;
}

export interface Module {
    id: number;
    nom: string;
    code: string;
    formation_id: number;
    credits: number;
    semestre: number;
    duree_examen_min: number;
}

export interface Examen {
    id: number;
    module_id: number;
    prof_id: number | null;
    salle_id: number | null;
    date_heure: string;
    duree_minutes: number;
    statut: string;
    nb_inscrits: number;
    module?: {
        nom: string;
        code: string;
    };
    professeur?: {
        nom: string;
        prenom: string;
    };
    salle?: {
        nom: string;
        batiment: string;
    };
}

export interface Salle {
    id: number;
    nom: string;
    code: string;
    capacite: number;
    capacite_examen: number;
    type: string;
    batiment: string;
    disponible: boolean;
}

export interface EDTGenerationRequest {
    date_debut: string;
    date_fin: string;
    dept_ids?: number[];
    formation_ids?: number[];
    force_regenerate?: boolean;
}

export interface EDTGenerationResponse {
    session_id: number;
    statut: string;
    nb_examens_planifies: number;
    nb_conflits_resolus: number;
    temps_execution_ms: number;
    message: string;
}

export interface ConflictInfo {
    type: string;
    description: string;
    examens_ids: number[];
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    size: number;
    pages: number;
}

// API instance
const api: AxiosInstance = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor for token refresh
api.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const originalRequest = error.config as any;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
                try {
                    const response = await axios.post('/api/auth/refresh', {
                        refresh_token: refreshToken,
                    });

                    localStorage.setItem('access_token', response.data.access_token);
                    localStorage.setItem('refresh_token', response.data.refresh_token);

                    originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
                    return api(originalRequest);
                } catch (refreshError) {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    window.location.href = '/login';
                }
            }
        }

        return Promise.reject(error);
    }
);

// Auth API
export const authApi = {
    login: async (email: string, password: string): Promise<LoginResponse> => {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await api.post('/auth/login', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
        return response.data;
    },

    getProfile: async (): Promise<User> => {
        const response = await api.get('/auth/me');
        return response.data;
    },

    logout: async (): Promise<void> => {
        await api.post('/auth/logout');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },
};

// Dashboard API
export const dashboardApi = {
    getStats: async (): Promise<DashboardStats> => {
        const response = await api.get('/dashboard/stats');
        return response.data;
    },

    getDepartementKPIs: async (): Promise<DepartementKPI[]> => {
        const response = await api.get('/dashboard/kpi/departements');
        return response.data;
    },

    getDepartements: async (): Promise<Departement[]> => {
        const response = await api.get('/dashboard/departements');
        return response.data;
    },

    getFormations: async (params?: { dept_id?: number; niveau?: string }): Promise<PaginatedResponse<Formation>> => {
        const response = await api.get('/dashboard/formations', { params });
        return response.data;
    },

    getSalles: async (): Promise<Salle[]> => {
        const response = await api.get('/dashboard/salles');
        return response.data;
    },

    getOccupationSalles: async () => {
        const response = await api.get('/dashboard/salles/occupation');
        return response.data;
    },

    getModules: async (params?: { formation_id?: number; semestre?: number }): Promise<PaginatedResponse<Module>> => {
        const response = await api.get('/dashboard/modules', { params: { ...params, size: 100 } });
        return response.data;
    },
};

// Examens API
export const examensApi = {
    list: async (params?: {
        page?: number;
        size?: number;
        dept_id?: number;
        formation_id?: number;
        statut?: string;
        date_debut?: string;
        date_fin?: string;
    }): Promise<PaginatedResponse<Examen>> => {
        const response = await api.get('/examens/', { params });
        return response.data;
    },

    get: async (id: number): Promise<Examen> => {
        const response = await api.get(`/examens/${id}`);
        return response.data;
    },

    create: async (data: Partial<Examen>): Promise<Examen> => {
        const response = await api.post('/examens/', data);
        return response.data;
    },

    update: async (id: number, data: Partial<Examen>): Promise<Examen> => {
        const response = await api.put(`/examens/${id}`, data);
        return response.data;
    },

    delete: async (id: number): Promise<void> => {
        await api.delete(`/examens/${id}`);
    },

    generateEDT: async (data: EDTGenerationRequest): Promise<EDTGenerationResponse> => {
        const response = await api.post('/examens/generate', data);
        return response.data;
    },

    detectConflicts: async (): Promise<ConflictInfo[]> => {
        const response = await api.get('/examens/conflicts/detect');
        return response.data;
    },

    confirm: async (id: number): Promise<void> => {
        await api.post(`/examens/${id}/confirm`);
    },

    cancel: async (id: number): Promise<void> => {
        await api.post(`/examens/${id}/cancel`);
    },
};

export default api;
