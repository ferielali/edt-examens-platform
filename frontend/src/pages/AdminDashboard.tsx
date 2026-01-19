import React, { useState } from 'react';
import {
    Row,
    Col,
    Card,
    Button,
    DatePicker,
    Form,
    Select,
    Typography,
    Space,
    Alert,
    Progress,
    Steps,
    Divider,
    message,
    Modal,
    Result,
} from 'antd';
import {
    ThunderboltOutlined,
    CalendarOutlined,
    CheckCircleOutlined,
    ClockCircleOutlined,
    SettingOutlined,
} from '@ant-design/icons';
import dayjs from 'dayjs';
import { examensApi, EDTGenerationResponse } from '../services/api';

const { Title, Text, Paragraph } = Typography;
const { RangePicker } = DatePicker;

const AdminDashboard: React.FC = () => {
    const [form] = Form.useForm();
    const [generating, setGenerating] = useState(false);
    const [result, setResult] = useState<EDTGenerationResponse | null>(null);
    const [showResult, setShowResult] = useState(false);

    const handleGenerate = async (values: any) => {
        try {
            setGenerating(true);
            message.loading({ content: 'Génération de l\'EDT en cours...', key: 'generate' });

            const [dateDebut, dateFin] = values.periode;

            const response = await examensApi.generateEDT({
                date_debut: dateDebut.toISOString(),
                date_fin: dateFin.toISOString(),
                dept_ids: values.departements,
                force_regenerate: values.force_regenerate || false,
            });

            setResult(response);
            setShowResult(true);
            message.destroy('generate');

            if (response.statut === 'success') {
                message.success('EDT généré avec succès!');
            } else {
                message.warning('La génération a échoué. Vérifiez les paramètres.');
            }
        } catch (error: any) {
            message.destroy('generate');
            message.error(error.response?.data?.detail || 'Erreur lors de la génération');
        } finally {
            setGenerating(false);
        }
    };

    return (
        <div className="fade-in">
            <div style={{ marginBottom: 24 }}>
                <Title level={4} style={{ marginBottom: 4 }}>
                    Génération Automatique d'EDT
                </Title>
                <Text type="secondary">
                    Configurez et lancez la génération optimisée des emplois du temps d'examens
                </Text>
            </div>

            <Row gutter={[24, 24]}>
                {/* Configuration Panel */}
                <Col xs={24} lg={14}>
                    <Card
                        title={
                            <Space>
                                <SettingOutlined />
                                <span>Configuration de la Génération</span>
                            </Space>
                        }
                    >
                        <Form
                            form={form}
                            layout="vertical"
                            onFinish={handleGenerate}
                            initialValues={{
                                periode: [
                                    dayjs().add(1, 'month'),
                                    dayjs().add(1, 'month').add(2, 'weeks'),
                                ],
                            }}
                        >
                            <Form.Item
                                name="periode"
                                label="Période d'examens"
                                rules={[{ required: true, message: 'Sélectionnez une période' }]}
                            >
                                <RangePicker
                                    style={{ width: '100%' }}
                                    format="DD/MM/YYYY"
                                    placeholder={['Date de début', 'Date de fin']}
                                />
                            </Form.Item>

                            <Form.Item
                                name="departements"
                                label="Départements (laisser vide pour tous)"
                            >
                                <Select
                                    mode="multiple"
                                    placeholder="Tous les départements"
                                    options={[
                                        { value: 1, label: 'Informatique' },
                                        { value: 2, label: 'Mathématiques' },
                                        { value: 3, label: 'Physique' },
                                        { value: 4, label: 'Chimie' },
                                        { value: 5, label: 'Biologie' },
                                        { value: 6, label: 'Sciences Économiques' },
                                        { value: 7, label: 'Langues et Lettres' },
                                    ]}
                                />
                            </Form.Item>

                            <Divider />

                            <Alert
                                type="info"
                                showIcon
                                message="Contraintes appliquées automatiquement"
                                description={
                                    <ul style={{ marginBottom: 0, paddingLeft: 16 }}>
                                        <li>Maximum 1 examen par jour par étudiant</li>
                                        <li>Maximum 3 surveillances par jour par professeur</li>
                                        <li>Respect des capacités des salles</li>
                                        <li>Priorisation des examens par département</li>
                                    </ul>
                                }
                                style={{ marginBottom: 24 }}
                            />

                            <Form.Item>
                                <Button
                                    type="primary"
                                    htmlType="submit"
                                    loading={generating}
                                    icon={<ThunderboltOutlined />}
                                    size="large"
                                    block
                                    style={{ height: 48 }}
                                >
                                    {generating ? 'Génération en cours...' : 'Lancer la Génération'}
                                </Button>
                            </Form.Item>
                        </Form>
                    </Card>
                </Col>

                {/* Process Steps */}
                <Col xs={24} lg={10}>
                    <Card
                        title={
                            <Space>
                                <ClockCircleOutlined />
                                <span>Processus de Génération</span>
                            </Space>
                        }
                    >
                        <Steps
                            direction="vertical"
                            current={generating ? 1 : 0}
                            items={[
                                {
                                    title: 'Configuration',
                                    description: 'Définition des paramètres',
                                    icon: <SettingOutlined />,
                                },
                                {
                                    title: 'Analyse',
                                    description: 'Analyse des contraintes et ressources',
                                    icon: <CalendarOutlined />,
                                },
                                {
                                    title: 'Optimisation',
                                    description: 'Résolution OR-Tools (< 45s)',
                                    icon: <ThunderboltOutlined />,
                                },
                                {
                                    title: 'Validation',
                                    description: 'Vérification des conflits',
                                    icon: <CheckCircleOutlined />,
                                },
                            ]}
                        />

                        {generating && (
                            <div style={{ marginTop: 24 }}>
                                <Text type="secondary">Temps estimé:</Text>
                                <Progress
                                    percent={30}
                                    status="active"
                                    strokeColor={{ '0%': '#108ee9', '100%': '#87d068' }}
                                />
                            </div>
                        )}
                    </Card>

                    <Card style={{ marginTop: 24 }}>
                        <Paragraph>
                            <Text strong>Algorithme utilisé:</Text> Google OR-Tools
                            <br />
                            <Text type="secondary">
                                Programmation par contraintes pour l'optimisation multi-objectifs
                            </Text>
                        </Paragraph>
                        <Paragraph>
                            <Text strong>Temps maximum:</Text> 45 secondes
                            <br />
                            <Text type="secondary">
                                Configurable selon la complexité
                            </Text>
                        </Paragraph>
                    </Card>
                </Col>
            </Row>

            {/* Result Modal */}
            <Modal
                open={showResult}
                onCancel={() => setShowResult(false)}
                footer={[
                    <Button key="close" onClick={() => setShowResult(false)}>
                        Fermer
                    </Button>,
                    <Button key="view" type="primary" onClick={() => window.location.href = '/examens'}>
                        Voir les Examens
                    </Button>,
                ]}
                width={600}
            >
                {result && (
                    <Result
                        status={result.statut === 'success' ? 'success' : 'warning'}
                        title={result.statut === 'success' ? 'EDT Généré avec Succès!' : 'Génération Partielle'}
                        subTitle={result.message}
                        extra={[
                            <div key="stats" style={{ textAlign: 'left', background: '#fafafa', padding: 16, borderRadius: 8 }}>
                                <Row gutter={16}>
                                    <Col span={12}>
                                        <Text type="secondary">Examens planifiés:</Text>
                                        <br />
                                        <Text strong style={{ fontSize: 24 }}>{result.nb_examens_planifies}</Text>
                                    </Col>
                                    <Col span={12}>
                                        <Text type="secondary">Conflits résolus:</Text>
                                        <br />
                                        <Text strong style={{ fontSize: 24 }}>{result.nb_conflits_resolus}</Text>
                                    </Col>
                                </Row>
                                <Divider />
                                <Text type="secondary">Temps d'exécution:</Text>
                                <br />
                                <Text strong>{result.temps_execution_ms} ms</Text>
                            </div>,
                        ]}
                    />
                )}
            </Modal>
        </div>
    );
};

export default AdminDashboard;
