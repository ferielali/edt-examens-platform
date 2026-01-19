import React, { useState } from 'react';
import { Modal, Form, Input, Button, Typography, message, Tabs, Alert } from 'antd';
import { MailOutlined, LockOutlined, SettingOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Text } = Typography;

interface SettingsModalProps {
    visible: boolean;
    onClose: () => void;
    userEmail: string;
    token: string;
}

const SettingsModal: React.FC<SettingsModalProps> = ({ visible, onClose, userEmail, token }) => {
    const [emailLoading, setEmailLoading] = useState(false);
    const [passwordLoading, setPasswordLoading] = useState(false);
    const [emailForm] = Form.useForm();
    const [passwordForm] = Form.useForm();

    const handleEmailChange = async (values: { newEmail: string; password: string }) => {
        setEmailLoading(true);
        try {
            await axios.put('http://localhost:8000/api/auth/change-email', {
                new_email: values.newEmail,
                password: values.password
            }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            message.success('Email modifié avec succès! Veuillez vous reconnecter.');
            emailForm.resetFields();
            setTimeout(() => {
                window.location.href = '/login';
            }, 1500);
        } catch (error: any) {
            const errorMessage = error.response?.data?.detail || 'Erreur lors du changement d\'email';
            message.error(errorMessage);
        } finally {
            setEmailLoading(false);
        }
    };

    const handlePasswordChange = async (values: { oldPassword: string; newPassword: string; confirmPassword: string }) => {
        if (values.newPassword !== values.confirmPassword) {
            message.error('Les mots de passe ne correspondent pas');
            return;
        }

        setPasswordLoading(true);
        try {
            await axios.put(`http://localhost:8000/api/auth/change-password?old_password=${encodeURIComponent(values.oldPassword)}&new_password=${encodeURIComponent(values.newPassword)}`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            });
            message.success('Mot de passe modifié avec succès!');
            passwordForm.resetFields();
        } catch (error: any) {
            const errorMessage = error.response?.data?.detail || 'Erreur lors du changement de mot de passe';
            message.error(errorMessage);
        } finally {
            setPasswordLoading(false);
        }
    };

    const handleClose = () => {
        emailForm.resetFields();
        passwordForm.resetFields();
        onClose();
    };

    const items = [
        {
            key: 'email',
            label: '📧 Changer Email',
            children: (
                <div style={{ padding: '16px 0' }}>
                    <Alert
                        message="Attention"
                        description="Après avoir changé votre email, vous devrez vous reconnecter avec le nouvel email."
                        type="warning"
                        showIcon
                        style={{ marginBottom: 20 }}
                    />

                    <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
                        Email actuel: <strong>{userEmail}</strong>
                    </Text>

                    <Form
                        form={emailForm}
                        layout="vertical"
                        onFinish={handleEmailChange}
                    >
                        <Form.Item
                            name="newEmail"
                            label="Nouvel email"
                            rules={[
                                { required: true, message: 'Veuillez saisir le nouvel email' },
                                { type: 'email', message: 'Email invalide' }
                            ]}
                        >
                            <Input
                                prefix={<MailOutlined style={{ color: '#9ca3af' }} />}
                                placeholder="Nouvel email"
                                size="large"
                                style={{ borderRadius: 10 }}
                            />
                        </Form.Item>

                        <Form.Item
                            name="password"
                            label="Mot de passe actuel"
                            rules={[{ required: true, message: 'Veuillez saisir votre mot de passe' }]}
                        >
                            <Input.Password
                                prefix={<LockOutlined style={{ color: '#9ca3af' }} />}
                                placeholder="Mot de passe pour confirmer"
                                size="large"
                                style={{ borderRadius: 10 }}
                            />
                        </Form.Item>

                        <Form.Item style={{ marginBottom: 0 }}>
                            <Button
                                type="primary"
                                htmlType="submit"
                                loading={emailLoading}
                                block
                                style={{
                                    height: 44,
                                    borderRadius: 10,
                                    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                                    border: 'none',
                                    fontWeight: 600,
                                }}
                            >
                                {emailLoading ? 'Modification...' : 'Changer l\'email'}
                            </Button>
                        </Form.Item>
                    </Form>
                </div>
            )
        },
        {
            key: 'password',
            label: '🔐 Changer Mot de passe',
            children: (
                <div style={{ padding: '16px 0' }}>
                    <Form
                        form={passwordForm}
                        layout="vertical"
                        onFinish={handlePasswordChange}
                    >
                        <Form.Item
                            name="oldPassword"
                            label="Mot de passe actuel"
                            rules={[{ required: true, message: 'Veuillez saisir votre mot de passe actuel' }]}
                        >
                            <Input.Password
                                prefix={<LockOutlined style={{ color: '#9ca3af' }} />}
                                placeholder="Mot de passe actuel"
                                size="large"
                                style={{ borderRadius: 10 }}
                            />
                        </Form.Item>

                        <Form.Item
                            name="newPassword"
                            label="Nouveau mot de passe"
                            rules={[
                                { required: true, message: 'Veuillez saisir le nouveau mot de passe' },
                                { min: 6, message: 'Le mot de passe doit contenir au moins 6 caractères' }
                            ]}
                        >
                            <Input.Password
                                prefix={<LockOutlined style={{ color: '#9ca3af' }} />}
                                placeholder="Nouveau mot de passe"
                                size="large"
                                style={{ borderRadius: 10 }}
                            />
                        </Form.Item>

                        <Form.Item
                            name="confirmPassword"
                            label="Confirmer le mot de passe"
                            rules={[{ required: true, message: 'Veuillez confirmer le mot de passe' }]}
                        >
                            <Input.Password
                                prefix={<LockOutlined style={{ color: '#9ca3af' }} />}
                                placeholder="Confirmer le mot de passe"
                                size="large"
                                style={{ borderRadius: 10 }}
                            />
                        </Form.Item>

                        <Form.Item style={{ marginBottom: 0 }}>
                            <Button
                                type="primary"
                                htmlType="submit"
                                loading={passwordLoading}
                                block
                                style={{
                                    height: 44,
                                    borderRadius: 10,
                                    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                                    border: 'none',
                                    fontWeight: 600,
                                }}
                            >
                                {passwordLoading ? 'Modification...' : 'Changer le mot de passe'}
                            </Button>
                        </Form.Item>
                    </Form>
                </div>
            )
        }
    ];

    return (
        <Modal
            open={visible}
            onCancel={handleClose}
            footer={null}
            centered
            width={480}
            title={
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <SettingOutlined style={{ fontSize: 20, color: '#6366f1' }} />
                    <span>Paramètres du compte</span>
                </div>
            }
        >
            <Tabs items={items} />
        </Modal>
    );
};

export default SettingsModal;
