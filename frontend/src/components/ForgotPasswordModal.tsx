import React, { useState } from 'react';
import { Modal, Form, Input, Button, Typography, message, Alert, Steps } from 'antd';
import { MailOutlined, LockOutlined, CheckCircleOutlined, SafetyOutlined, NumberOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Text, Title } = Typography;

interface ForgotPasswordModalProps {
    visible: boolean;
    onClose: () => void;
}

const ForgotPasswordModal: React.FC<ForgotPasswordModalProps> = ({ visible, onClose }) => {
    const [loading, setLoading] = useState(false);
    const [step, setStep] = useState(0); // 0: email, 1: code verification, 2: new password, 3: success
    const [email, setEmail] = useState('');
    const [verificationCode, setVerificationCode] = useState('');
    const [generatedCode, setGeneratedCode] = useState('');
    const [form] = Form.useForm();

    // Step 1: Send verification code
    const handleSendCode = async (values: { email: string }) => {
        setLoading(true);
        try {
            // Check if email exists in the system
            const response = await axios.post('http://localhost:8000/api/auth/request-reset', {
                email: values.email
            });

            setEmail(values.email);
            setGeneratedCode(response.data.code); // In production, this would be sent via email
            setStep(1);
            message.success('Code de vérification envoyé! (Voir la console pour le code de démonstration)');
            console.log('🔐 Code de vérification:', response.data.code);
        } catch (error: any) {
            const errorMessage = error.response?.data?.detail || 'Erreur lors de l\'envoi du code';
            message.error(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    // Step 2: Verify code
    const handleVerifyCode = async (values: { code: string }) => {
        if (values.code !== generatedCode) {
            message.error('Code de vérification incorrect');
            return;
        }
        setVerificationCode(values.code);
        setStep(2);
        message.success('Code vérifié avec succès!');
    };

    // Step 3: Reset password
    const handleResetPassword = async (values: { newPassword: string; confirmPassword: string }) => {
        if (values.newPassword !== values.confirmPassword) {
            message.error('Les mots de passe ne correspondent pas');
            return;
        }

        setLoading(true);
        try {
            await axios.post('http://localhost:8000/api/auth/reset-password', {
                email: email,
                new_password: values.newPassword,
                verification_code: verificationCode
            });
            setStep(3);
            message.success('Mot de passe réinitialisé avec succès!');
        } catch (error: any) {
            const errorMessage = error.response?.data?.detail || 'Erreur lors de la réinitialisation';
            message.error(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const handleClose = () => {
        form.resetFields();
        setStep(0);
        setEmail('');
        setVerificationCode('');
        setGeneratedCode('');
        onClose();
    };

    const renderStep = () => {
        switch (step) {
            case 0:
                return (
                    <>
                        <Text type="secondary" style={{ display: 'block', marginBottom: 24, textAlign: 'center' }}>
                            Entrez votre email pour recevoir un code de vérification
                        </Text>
                        <Form form={form} layout="vertical" onFinish={handleSendCode}>
                            <Form.Item
                                name="email"
                                rules={[
                                    { required: true, message: 'Veuillez saisir votre email' },
                                    { type: 'email', message: 'Email invalide' }
                                ]}
                            >
                                <Input
                                    prefix={<MailOutlined style={{ color: '#9ca3af' }} />}
                                    placeholder="Adresse email"
                                    size="large"
                                    style={{ borderRadius: 10 }}
                                />
                            </Form.Item>
                            <Form.Item style={{ marginBottom: 0 }}>
                                <Button
                                    type="primary"
                                    htmlType="submit"
                                    loading={loading}
                                    block
                                    style={{
                                        height: 44,
                                        borderRadius: 10,
                                        background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                                        border: 'none',
                                        fontWeight: 600,
                                    }}
                                >
                                    {loading ? 'Envoi...' : 'Envoyer le code'}
                                </Button>
                            </Form.Item>
                        </Form>
                    </>
                );

            case 1:
                return (
                    <>
                        <Alert
                            message="Code envoyé!"
                            description={`Un code de vérification a été envoyé à ${email}. (Pour la démonstration, le code est affiché dans la console du navigateur)`}
                            type="info"
                            showIcon
                            style={{ marginBottom: 20 }}
                        />
                        <Form form={form} layout="vertical" onFinish={handleVerifyCode}>
                            <Form.Item
                                name="code"
                                rules={[
                                    { required: true, message: 'Veuillez saisir le code' },
                                    { len: 6, message: 'Le code doit contenir 6 chiffres' }
                                ]}
                            >
                                <Input
                                    prefix={<NumberOutlined style={{ color: '#9ca3af' }} />}
                                    placeholder="Code à 6 chiffres"
                                    size="large"
                                    maxLength={6}
                                    style={{ borderRadius: 10, letterSpacing: 8, textAlign: 'center', fontSize: 20 }}
                                />
                            </Form.Item>
                            <Form.Item style={{ marginBottom: 0 }}>
                                <Button
                                    type="primary"
                                    htmlType="submit"
                                    block
                                    style={{
                                        height: 44,
                                        borderRadius: 10,
                                        background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                                        border: 'none',
                                        fontWeight: 600,
                                    }}
                                >
                                    Vérifier le code
                                </Button>
                            </Form.Item>
                        </Form>
                        <Button type="link" onClick={() => setStep(0)} style={{ marginTop: 10 }}>
                            ← Changer d'email
                        </Button>
                    </>
                );

            case 2:
                return (
                    <>
                        <Alert
                            message="Identité vérifiée ✓"
                            description="Vous pouvez maintenant créer un nouveau mot de passe."
                            type="success"
                            showIcon
                            style={{ marginBottom: 20 }}
                        />
                        <Form form={form} layout="vertical" onFinish={handleResetPassword}>
                            <Form.Item
                                name="newPassword"
                                rules={[
                                    { required: true, message: 'Veuillez saisir le nouveau mot de passe' },
                                    { min: 6, message: 'Minimum 6 caractères' }
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
                                rules={[{ required: true, message: 'Confirmez le mot de passe' }]}
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
                                    loading={loading}
                                    block
                                    style={{
                                        height: 44,
                                        borderRadius: 10,
                                        background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                                        border: 'none',
                                        fontWeight: 600,
                                    }}
                                >
                                    {loading ? 'Réinitialisation...' : 'Réinitialiser le mot de passe'}
                                </Button>
                            </Form.Item>
                        </Form>
                    </>
                );

            case 3:
                return (
                    <>
                        <div style={{ textAlign: 'center', padding: '20px 0' }}>
                            <CheckCircleOutlined style={{ fontSize: 64, color: '#10b981', marginBottom: 20 }} />
                            <Title level={4} style={{ color: '#10b981' }}>Mot de passe réinitialisé!</Title>
                            <Text type="secondary">
                                Votre mot de passe a été changé avec succès. Vous pouvez maintenant vous connecter.
                            </Text>
                        </div>
                        <Button
                            type="primary"
                            onClick={handleClose}
                            block
                            style={{
                                height: 44,
                                borderRadius: 10,
                                background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                                border: 'none',
                                fontWeight: 600,
                                marginTop: 20,
                            }}
                        >
                            Retour à la connexion
                        </Button>
                    </>
                );

            default:
                return null;
        }
    };

    return (
        <Modal
            open={visible}
            onCancel={handleClose}
            footer={null}
            centered
            width={440}
        >
            <div style={{ padding: '20px 0' }}>
                <div style={{ textAlign: 'center', marginBottom: 24 }}>
                    <div style={{
                        width: 64,
                        height: 64,
                        background: step === 3
                            ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                            : 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                        borderRadius: '16px',
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        marginBottom: 16,
                    }}>
                        {step === 3 ? (
                            <CheckCircleOutlined style={{ fontSize: 32, color: 'white' }} />
                        ) : (
                            <SafetyOutlined style={{ fontSize: 32, color: 'white' }} />
                        )}
                    </div>
                    <Title level={4} style={{ marginBottom: 0 }}>
                        {step === 3 ? 'Succès!' : 'Réinitialisation sécurisée'}
                    </Title>
                </div>

                {step < 3 && (
                    <Steps
                        current={step}
                        size="small"
                        style={{ marginBottom: 24 }}
                        items={[
                            { title: 'Email' },
                            { title: 'Vérification' },
                            { title: 'Nouveau MDP' },
                        ]}
                    />
                )}

                {renderStep()}
            </div>
        </Modal>
    );
};

export default ForgotPasswordModal;
