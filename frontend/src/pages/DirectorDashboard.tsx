import React, { useEffect, useState } from 'react';
import {
    Row,
    Col,
    Card,
    Statistic,
    Progress,
    Table,
    Typography,
    Tag,
    Space,
    Spin,
} from 'antd';
import {
    TeamOutlined,
    BookOutlined,
    CalendarOutlined,
    BankOutlined,
    RiseOutlined,
    WarningOutlined,
    CheckCircleOutlined,
} from '@ant-design/icons';
import { dashboardApi, DashboardStats, DepartementKPI } from '../services/api';

const { Title, Text } = Typography;

const DirectorDashboard: React.FC = () => {
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [kpis, setKpis] = useState<DepartementKPI[]>([]);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const [statsData, kpisData] = await Promise.all([
                dashboardApi.getStats(),
                dashboardApi.getDepartementKPIs(),
            ]);
            setStats(statsData);
            setKpis(kpisData);
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        } finally {
            setLoading(false);
        }
    };

    const kpiColumns = [
        {
            title: 'Département',
            dataIndex: 'departement_nom',
            key: 'departement_nom',
            render: (text: string) => <Text strong>{text}</Text>,
        },
        {
            title: 'Étudiants',
            dataIndex: 'nb_etudiants',
            key: 'nb_etudiants',
            render: (value: number) => value.toLocaleString(),
        },
        {
            title: 'Professeurs',
            dataIndex: 'nb_professeurs',
            key: 'nb_professeurs',
        },
        {
            title: 'Examens',
            dataIndex: 'nb_examens',
            key: 'nb_examens',
        },
        {
            title: 'Taux Planification',
            dataIndex: 'taux_planification',
            key: 'taux_planification',
            render: (value: number) => (
                <Progress
                    percent={value}
                    size="small"
                    status={value >= 80 ? 'success' : value >= 50 ? 'normal' : 'exception'}
                    strokeWidth={8}
                    style={{ width: 120 }}
                />
            ),
        },
        {
            title: 'Conflits',
            dataIndex: 'nb_conflits',
            key: 'nb_conflits',
            render: (value: number) => (
                <Tag color={value === 0 ? 'green' : value < 5 ? 'orange' : 'red'}>
                    {value}
                </Tag>
            ),
        },
    ];

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
                <Spin size="large" tip="Chargement des données..." />
            </div>
        );
    }

    return (
        <div className="fade-in">
            <div style={{ marginBottom: 24 }}>
                <Title level={4} style={{ marginBottom: 4 }}>
                    Vue Stratégique
                </Title>
                <Text type="secondary">
                    Vue d'ensemble de la plateforme et KPIs académiques
                </Text>
            </div>

            {/* Statistics Cards */}
            <Row gutter={[24, 24]}>
                <Col xs={24} sm={12} lg={6}>
                    <Card className="stat-card" hoverable>
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
                            <TeamOutlined style={{ color: 'white' }} />
                        </div>
                        <Statistic
                            title="Total Étudiants"
                            value={stats?.total_etudiants || 0}
                            valueStyle={{ color: '#262626', fontWeight: 700 }}
                        />
                        <div className="stat-change positive">
                            <RiseOutlined /> +12% ce semestre
                        </div>
                    </Card>
                </Col>

                <Col xs={24} sm={12} lg={6}>
                    <Card className="stat-card" hoverable>
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
                            <BookOutlined style={{ color: 'white' }} />
                        </div>
                        <Statistic
                            title="Total Formations"
                            value={stats?.total_formations || 0}
                            valueStyle={{ color: '#262626', fontWeight: 700 }}
                        />
                    </Card>
                </Col>

                <Col xs={24} sm={12} lg={6}>
                    <Card className="stat-card" hoverable>
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
                            <CalendarOutlined style={{ color: 'white' }} />
                        </div>
                        <Statistic
                            title="Examens Planifiés"
                            value={stats?.total_examens_planifies || 0}
                            valueStyle={{ color: '#262626', fontWeight: 700 }}
                        />
                    </Card>
                </Col>

                <Col xs={24} sm={12} lg={6}>
                    <Card className="stat-card" hoverable>
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }}>
                            <BankOutlined style={{ color: 'white' }} />
                        </div>
                        <Statistic
                            title="Taux Occupation Salles"
                            value={stats?.taux_occupation_salles || 0}
                            suffix="%"
                            valueStyle={{ color: '#262626', fontWeight: 700 }}
                        />
                    </Card>
                </Col>
            </Row>

            {/* KPI by Department */}
            <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
                <Col span={24}>
                    <Card
                        title={
                            <Space>
                                <CalendarOutlined />
                                <span>KPIs par Département</span>
                            </Space>
                        }
                        className="chart-container"
                    >
                        <Table
                            dataSource={kpis}
                            columns={kpiColumns}
                            rowKey="departement_id"
                            pagination={false}
                            size="middle"
                        />
                    </Card>
                </Col>
            </Row>

            {/* Summary Cards */}
            <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
                <Col xs={24} md={12}>
                    <Card
                        title={
                            <Space>
                                <CheckCircleOutlined style={{ color: '#52c41a' }} />
                                <span>État de la Planification</span>
                            </Space>
                        }
                    >
                        <Space direction="vertical" style={{ width: '100%' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <Text>Modules planifiés</Text>
                                <Progress percent={75} size="small" style={{ width: 200 }} />
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <Text>Salles assignées</Text>
                                <Progress percent={82} size="small" style={{ width: 200 }} status="success" />
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <Text>Surveillants assignés</Text>
                                <Progress percent={68} size="small" style={{ width: 200 }} />
                            </div>
                        </Space>
                    </Card>
                </Col>

                <Col xs={24} md={12}>
                    <Card
                        title={
                            <Space>
                                <WarningOutlined style={{ color: '#faad14' }} />
                                <span>Alertes et Conflits</span>
                            </Space>
                        }
                    >
                        <Space direction="vertical" style={{ width: '100%' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid #f0f0f0' }}>
                                <Text>Conflits de salles</Text>
                                <Tag color="green">0</Tag>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid #f0f0f0' }}>
                                <Text>Surcharge professeurs</Text>
                                <Tag color="orange">2</Tag>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0' }}>
                                <Text>Capacité salles dépassée</Text>
                                <Tag color="green">0</Tag>
                            </div>
                        </Space>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default DirectorDashboard;
