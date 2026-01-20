import React, { useState } from 'react';
import { Form, Input, Button, Typography, Checkbox, Divider } from 'antd';
import { UserOutlined, LockOutlined, CalendarOutlined, SafetyOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ForgotPasswordModal from '../components/ForgotPasswordModal';

const { Title, Text, Paragraph } = Typography;

const LoginPage: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [forgotPasswordVisible, setForgotPasswordVisible] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const onFinish = async (values: { email: string; password: string }) => {
        setLoading(true);
        const success = await login(values.email, values.password);
        setLoading(false);

        if (success) {
            navigate('/');
        }
    };

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            background: 'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)',
            position: 'relative',
            overflow: 'hidden',
        }}>
            {/* Animated background elements */}
            <div style={{
                position: 'absolute',
                width: '100%',
                height: '100%',
                overflow: 'hidden',
            }}>
                {[...Array(20)].map((_, i) => (
                    <div
                        key={i}
                        style={{
                            position: 'absolute',
                            width: `${Math.random() * 300 + 50}px`,
                            height: `${Math.random() * 300 + 50}px`,
                            background: `radial-gradient(circle, rgba(99, 102, 241, ${Math.random() * 0.1 + 0.05}) 0%, transparent 70%)`,
                            borderRadius: '50%',
                            left: `${Math.random() * 100}%`,
                            top: `${Math.random() * 100}%`,
                            animation: `float ${Math.random() * 10 + 10}s ease-in-out infinite`,
                        }}
                    />
                ))}
            </div>

            {/* Left Panel - Branding */}
            <div style={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                padding: '60px',
                position: 'relative',
                zIndex: 1,
            }}>
                <div style={{ textAlign: 'center', maxWidth: '500px' }}>
                    <div style={{
                        width: '100px',
                        height: '100px',
                        background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                        borderRadius: '24px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        margin: '0 auto 32px',
                        boxShadow: '0 20px 60px rgba(99, 102, 241, 0.4)',
                    }}>
                        <CalendarOutlined style={{ fontSize: 48, color: 'white' }} />
                    </div>

                    <Title level={1} style={{ color: 'white', marginBottom: 16, fontSize: '42px', fontWeight: 700 }}>
                        ExamScheduler
                    </Title>

                    <Paragraph style={{ color: 'rgba(255,255,255,0.7)', fontSize: '18px', lineHeight: 1.8 }}>
                        Plateforme d'Optimisation Intelligente des Emplois du Temps d'Examens Universitaires
                    </Paragraph>

                    <Divider style={{ borderColor: 'rgba(255,255,255,0.1)', margin: '40px 0' }} />

                    <div style={{ display: 'flex', gap: '24px', justifyContent: 'center', flexWrap: 'wrap' }}>
                        {[
                            { icon: '⚡', text: 'Génération < 45s' },
                            { icon: '🎯', text: '13 000+ étudiants' },
                            { icon: '🔒', text: 'Sécurisé JWT' },
                        ].map((item, i) => (
                            <div key={i} style={{
                                background: 'rgba(255,255,255,0.05)',
                                borderRadius: '12px',
                                padding: '16px 20px',
                                backdropFilter: 'blur(10px)',
                                border: '1px solid rgba(255,255,255,0.1)',
                            }}>
                                <span style={{ fontSize: 24 }}>{item.icon}</span>
                                <Text style={{ color: 'rgba(255,255,255,0.8)', display: 'block', marginTop: 8, fontSize: 13 }}>
                                    {item.text}
                                </Text>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Right Panel - Login Form */}
            <div style={{
                width: '480px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '40px',
                position: 'relative',
                zIndex: 1,
            }}>
                <div style={{
                    width: '100%',
                    background: 'rgba(255, 255, 255, 0.98)',
                    borderRadius: '24px',
                    padding: '48px',
                    boxShadow: '0 30px 100px rgba(0, 0, 0, 0.3)',
                }}>
                    <div style={{ textAlign: 'center', marginBottom: 40 }}>
                        <div style={{
                            width: 56,
                            height: 56,
                            background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                            borderRadius: '16px',
                            display: 'inline-flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            marginBottom: 20,
                        }}>
                            <SafetyOutlined style={{ fontSize: 28, color: 'white' }} />
                        </div>
                        <Title level={3} style={{ marginBottom: 8, color: '#1e1b4b' }}>
                            Connexion Sécurisée
                        </Title>
                        <Text type="secondary">
                            Accédez à votre espace de gestion des examens
                        </Text>
                    </div>

                    <Form
                        name="login"
                        initialValues={{ remember: true }}
                        onFinish={onFinish}
                        layout="vertical"
                        size="large"
                    >
                        <Form.Item
                            name="email"
                            rules={[
                                { required: true, message: 'Veuillez saisir votre email' },
                                { type: 'email', message: 'Email invalide' },
                            ]}
                        >
                            <Input
                                prefix={<UserOutlined style={{ color: '#9ca3af' }} />}
                                placeholder="Adresse email"
                                autoComplete="email"
                                style={{
                                    height: 52,
                                    borderRadius: 12,
                                    border: '2px solid #e5e7eb',
                                    fontSize: 15,
                                }}
                            />
                        </Form.Item>

                        <Form.Item
                            name="password"
                            rules={[{ required: true, message: 'Veuillez saisir votre mot de passe' }]}
                        >
                            <Input.Password
                                prefix={<LockOutlined style={{ color: '#9ca3af' }} />}
                                placeholder="Mot de passe"
                                autoComplete="current-password"
                                style={{
                                    height: 52,
                                    borderRadius: 12,
                                    border: '2px solid #e5e7eb',
                                    fontSize: 15,
                                }}
                            />
                        </Form.Item>

                        <Form.Item>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <Form.Item name="remember" valuePropName="checked" noStyle>
                                    <Checkbox style={{ color: '#6b7280' }}>Se souvenir de moi</Checkbox>
                                </Form.Item>
                                <a
                                    style={{ color: '#6366f1', fontWeight: 500, cursor: 'pointer' }}
                                    onClick={() => setForgotPasswordVisible(true)}
                                >
                                    Mot de passe oublié?
                                </a>
                            </div>
                        </Form.Item>

                        <Form.Item style={{ marginBottom: 16 }}>
                            <Button
                                type="primary"
                                htmlType="submit"
                                loading={loading}
                                block
                                style={{
                                    height: 52,
                                    fontSize: 16,
                                    fontWeight: 600,
                                    borderRadius: 12,
                                    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                                    border: 'none',
                                    boxShadow: '0 8px 24px rgba(99, 102, 241, 0.35)',
                                }}
                            >
                                {loading ? 'Connexion...' : 'Se connecter'}
                            </Button>
                        </Form.Item>
                    </Form>

                    <Divider style={{ margin: '24px 0' }}>
                        <Text type="secondary" style={{ fontSize: 12 }}>Comptes de démonstration</Text>
                    </Divider>

                    <div style={{
                        background: '#f8fafc',
                        borderRadius: 12,
                        padding: 16,
                        border: '1px solid #e2e8f0',
                    }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                            <Text style={{ color: '#64748b', fontSize: 13 }}>👔 Directeur</Text>
                            <Text code style={{ fontSize: 11 }}>admin@univ.edu</Text>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                            <Text style={{ color: '#64748b', fontSize: 13 }}>⚙️ Admin</Text>
                            <Text code style={{ fontSize: 11 }}>admin.scolarite@univ.edu</Text>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                            <Text style={{ color: '#64748b', fontSize: 13 }}>🏫 Chef Dept.</Text>
                            <Text code style={{ fontSize: 11 }}>chef.info@univ.edu</Text>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Text style={{ color: '#64748b', fontSize: 13 }}>👨‍🏫 Professeur</Text>
                            <Text code style={{ fontSize: 11 }}>prof.math@univ.edu</Text>
                        </div>
                    </div>
                </div>
            </div>

            <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(5deg); }
        }
        
        .ant-input:focus, .ant-input-affix-wrapper:focus, 
        .ant-input-affix-wrapper-focused {
          border-color: #6366f1 !important;
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
        }
        
        .ant-input-affix-wrapper:hover {
          border-color: #6366f1 !important;
        }
        
        .ant-btn-primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 12px 32px rgba(99, 102, 241, 0.45) !important;
        }
        
        .ant-checkbox-checked .ant-checkbox-inner {
          background-color: #6366f1 !important;
          border-color: #6366f1 !important;
        }
      `}</style>

            <ForgotPasswordModal
                visible={forgotPasswordVisible}
                onClose={() => setForgotPasswordVisible(false)}
            />
        </div>
    );
};

export default LoginPage;
