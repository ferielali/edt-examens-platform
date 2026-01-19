import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authApi, User } from '../services/api';
import { message } from 'antd';

interface AuthContextType {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (email: string, password: string) => Promise<boolean>;
    logout: () => Promise<void>;
    refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // Check for existing token on mount
    useEffect(() => {
        const initAuth = async () => {
            const token = localStorage.getItem('access_token');
            if (token) {
                try {
                    const userData = await authApi.getProfile();
                    setUser(userData);
                } catch (error) {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                }
            }
            setIsLoading(false);
        };

        initAuth();
    }, []);

    const login = async (email: string, password: string): Promise<boolean> => {
        try {
            setIsLoading(true);
            const response = await authApi.login(email, password);

            localStorage.setItem('access_token', response.access_token);
            localStorage.setItem('refresh_token', response.refresh_token);

            const userData = await authApi.getProfile();
            setUser(userData);

            message.success(`Bienvenue, ${userData.nom_complet}!`);
            return true;
        } catch (error: any) {
            const errorMessage = error.response?.data?.detail || 'Erreur de connexion';
            message.error(errorMessage);
            return false;
        } finally {
            setIsLoading(false);
        }
    };

    const logout = async () => {
        try {
            await authApi.logout();
        } catch (error) {
            // Ignore logout errors
        } finally {
            setUser(null);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            message.info('Déconnexion réussie');
        }
    };

    const refreshUser = async () => {
        try {
            const userData = await authApi.getProfile();
            setUser(userData);
        } catch (error) {
            setUser(null);
        }
    };

    const value: AuthContextType = {
        user,
        token: localStorage.getItem('access_token'),
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        refreshUser,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
