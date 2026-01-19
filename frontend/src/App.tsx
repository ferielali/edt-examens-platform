import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Spin } from 'antd';
import { useAuth } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import DashboardLayout from './components/DashboardLayout';
import DirectorDashboard from './pages/DirectorDashboard';
import AdminDashboard from './pages/AdminDashboard';
import DepartmentDashboard from './pages/DepartmentDashboard';
import StudentDashboard from './pages/StudentDashboard';
import ExamensPage from './pages/ExamensPage';
import SallesPage from './pages/SallesPage';

// Protected route component
const ProtectedRoute: React.FC<{ children: React.ReactNode; allowedRoles?: string[] }> = ({
    children,
    allowedRoles,
}) => {
    const { isAuthenticated, isLoading, user } = useAuth();

    if (isLoading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <Spin size="large" tip="Chargement..." />
            </div>
        );
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    if (allowedRoles && user && !allowedRoles.includes(user.role)) {
        // Redirect to appropriate dashboard based on role
        return <Navigate to={getDefaultRoute(user.role)} replace />;
    }

    return <>{children}</>;
};

// Get default route based on user role
const getDefaultRoute = (role: string): string => {
    switch (role) {
        case 'director':
            return '/director';
        case 'administrator':
            return '/admin';
        case 'department_head':
            return '/department';
        case 'professor':
        case 'student':
            return '/student';
        default:
            return '/login';
    }
};

const App: React.FC = () => {
    const { user, isAuthenticated, isLoading } = useAuth();

    if (isLoading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <Spin size="large" tip="Chargement..." />
            </div>
        );
    }

    return (
        <Routes>
            {/* Public routes */}
            <Route
                path="/login"
                element={isAuthenticated ? <Navigate to={getDefaultRoute(user?.role || '')} replace /> : <LoginPage />}
            />

            {/* Protected routes with dashboard layout */}
            <Route
                path="/"
                element={
                    <ProtectedRoute>
                        <DashboardLayout />
                    </ProtectedRoute>
                }
            >
                {/* Director Dashboard */}
                <Route
                    path="director"
                    element={
                        <ProtectedRoute allowedRoles={['director']}>
                            <DirectorDashboard />
                        </ProtectedRoute>
                    }
                />

                {/* Admin Dashboard */}
                <Route
                    path="admin"
                    element={
                        <ProtectedRoute allowedRoles={['director', 'administrator']}>
                            <AdminDashboard />
                        </ProtectedRoute>
                    }
                />

                {/* Department Head Dashboard */}
                <Route
                    path="department"
                    element={
                        <ProtectedRoute allowedRoles={['director', 'administrator', 'department_head']}>
                            <DepartmentDashboard />
                        </ProtectedRoute>
                    }
                />

                {/* Student/Professor Dashboard */}
                <Route
                    path="student"
                    element={
                        <ProtectedRoute allowedRoles={['director', 'administrator', 'department_head', 'professor', 'student']}>
                            <StudentDashboard />
                        </ProtectedRoute>
                    }
                />

                {/* Examens Management */}
                <Route
                    path="examens"
                    element={
                        <ProtectedRoute allowedRoles={['director', 'administrator', 'department_head', 'professor', 'student']}>
                            <ExamensPage />
                        </ProtectedRoute>
                    }
                />

                {/* Salles Management */}
                <Route
                    path="salles"
                    element={
                        <ProtectedRoute allowedRoles={['director', 'administrator']}>
                            <SallesPage />
                        </ProtectedRoute>
                    }
                />

                {/* Default redirect */}
                <Route
                    index
                    element={<Navigate to={user ? getDefaultRoute(user.role) : '/login'} replace />}
                />
            </Route>

            {/* Catch all - redirect to login */}
            <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
    );
};

export default App;
