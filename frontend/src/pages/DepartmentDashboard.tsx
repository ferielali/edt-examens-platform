import React, { useEffect, useState } from 'react';
import {
    Row,
    Col,
    Card,
    Table,
    Tag,
    Space,
    Typography,
    Statistic,
    Button,
    Spin,
    Progress,
} from 'antd';
import {
    TeamOutlined,
    BookOutlined,
    CheckCircleOutlined,
    ClockCircleOutlined,
    FileSearchOutlined,
} from '@ant-design/icons';
import { dashboardApi, examensApi, Examen, PaginatedResponse } from '../services/api';
import { useAuth } from '../context/AuthContext';

const { Title, Text } = Typography;

const DepartmentDashboard: React.FC = () => {
    const { user } = useAuth();
    const [loading, setLoading] = useState(true);
    const [examens, setExamens] = useState<Examen[]>([]);
    const [stats, setStats] = useState({
        total_examens: 0,
        confirmes: 0,
        en_attente: 0,
    });

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const response = await examensApi.list({ size: 50 });
            setExamens(response.items);

            // Calculate stats
            const confirmes = response.items.filter(e => e.statut === 'confirmed').length;
            const en_attente = response.items.filter(e => e.statut === 'scheduled').length;

            setStats({
                total_examens: response.total,
                confirmes,
                en_attente,
            });
        } catch (error) {
            console.error('Error loading data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleConfirm = async (id: number) => {
        try {
            await examensApi.confirm(id);
            loadData();
        } catch (error) {
            console.error('Error confirming exam:', error);
        }
    };

    const columns = [
        {
            title: 'Module',
            dataIndex: ['module', 'nom'],
            key: 'module',
            render: (_: any, record: Examen) => (
                <div>
                    <Text strong>{record.module?.nom || `Module ${record.module_id}`}</Text>
                    <br />
                    <Text type="secondary" style={{ fontSize: 12 }}>
                        {record.module?.code || ''}
                    </Text>
                </div>
            ),
        },
        {
            title: 'Date & Heure',
            dataIndex: 'date_heure',
            key: 'date_heure',
            render: (date: string) => (
                <div>
                    <Text>{new Date(date).toLocaleDateString('fr-FR')}</Text>
                    <br />
                    <Text type="secondary">
                        {new Date(date).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                    </Text>
                </div>
            ),
        },
        {
            title: 'Salle',
            dataIndex: ['salle', 'nom'],
            key: 'salle',
            render: (_: any, record: Examen) => record.salle?.nom || '-',
        },
        {
            title: 'Inscrits',
            dataIndex: 'nb_inscrits',
            key: 'nb_inscrits',
            render: (value: number) => <Tag color="blue">{value}</Tag>,
        },
        {
            title: 'Statut',
            dataIndex: 'statut',
            key: 'statut',
            render: (statut: string) => {
                const colors: Record<string, string> = {
                    draft: 'default',
                    scheduled: 'processing',
                    confirmed: 'success',
                    completed: 'cyan',
                    cancelled: 'error',
                };
                const labels: Record<string, string> = {
                    draft: 'Brouillon',
                    scheduled: 'Planifié',
                    confirmed: 'Confirmé',
                    completed: 'Terminé',
                    cancelled: 'Annulé',
                };
                return <Tag color={colors[statut]}>{labels[statut] || statut}</Tag>;
            },
        },
        {
            title: 'Actions',
            key: 'actions',
            render: (_: any, record: Examen) => (
                <Space>
                    {record.statut === 'scheduled' && (
                        <Button
                            type="primary"
                            size="small"
                            icon={<CheckCircleOutlined />}
                            onClick={() => handleConfirm(record.id)}
                        >
                            Valider
                        </Button>
                    )}
                    <Button size="small" icon={<FileSearchOutlined />}>
                        Détails
                    </Button>
                </Space>
            ),
        },
    ];

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
                <Spin size="large" tip="Chargement..." />
            </div>
        );
    }

    return (
        <div className="fade-in">
            <div style={{ marginBottom: 24 }}>
                <Title level={4} style={{ marginBottom: 4 }}>
                    Gestion du Département
                </Title>
                <Text type="secondary">
                    Validation et suivi des examens de votre département
                </Text>
            </div>

            {/* Stats Cards */}
            <Row gutter={[24, 24]}>
                <Col xs={24} sm={8}>
                    <Card>
                        <Statistic
                            title="Total Examens"
                            value={stats.total_examens}
                            prefix={<BookOutlined style={{ color: '#1890ff' }} />}
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={8}>
                    <Card>
                        <Statistic
                            title="Confirmés"
                            value={stats.confirmes}
                            prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
                            valueStyle={{ color: '#52c41a' }}
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={8}>
                    <Card>
                        <Statistic
                            title="En Attente de Validation"
                            value={stats.en_attente}
                            prefix={<ClockCircleOutlined style={{ color: '#faad14' }} />}
                            valueStyle={{ color: '#faad14' }}
                        />
                    </Card>
                </Col>
            </Row>

            {/* Progress */}
            <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
                <Col span={24}>
                    <Card title="Progression de la Validation">
                        <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
                            <Progress
                                type="circle"
                                percent={Math.round((stats.confirmes / (stats.total_examens || 1)) * 100)}
                                strokeColor={{ '0%': '#108ee9', '100%': '#87d068' }}
                            />
                            <div>
                                <Text strong style={{ fontSize: 16 }}>
                                    {stats.confirmes} sur {stats.total_examens} examens validés
                                </Text>
                                <br />
                                <Text type="secondary">
                                    {stats.en_attente} examens en attente de votre validation
                                </Text>
                            </div>
                        </div>
                    </Card>
                </Col>
            </Row>

            {/* Examens Table */}
            <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
                <Col span={24}>
                    <Card
                        title="Examens à Valider"
                        extra={
                            <Button type="primary" onClick={loadData}>
                                Actualiser
                            </Button>
                        }
                    >
                        <Table
                            dataSource={examens}
                            columns={columns}
                            rowKey="id"
                            pagination={{ pageSize: 10 }}
                        />
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default DepartmentDashboard;
