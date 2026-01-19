import React, { useEffect, useState } from 'react';
import {
    Card,
    Table,
    Button,
    Tag,
    Typography,
    Row,
    Col,
    Progress,
    Space,
    Spin,
} from 'antd';
import {
    BankOutlined,
    CheckCircleOutlined,
    CloseCircleOutlined,
    DesktopOutlined,
    ExperimentOutlined,
} from '@ant-design/icons';
import { dashboardApi, Salle } from '../services/api';

const { Title, Text } = Typography;

const SallesPage: React.FC = () => {
    const [loading, setLoading] = useState(true);
    const [salles, setSalles] = useState<Salle[]>([]);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const data = await dashboardApi.getSalles();
            setSalles(data);
        } catch (error) {
            console.error('Error loading salles:', error);
        } finally {
            setLoading(false);
        }
    };

    const getTypeIcon = (type: string) => {
        switch (type) {
            case 'amphi':
                return <BankOutlined />;
            case 'salle_info':
                return <DesktopOutlined />;
            case 'salle_tp':
                return <ExperimentOutlined />;
            default:
                return <BankOutlined />;
        }
    };

    const getTypeLabel = (type: string) => {
        const labels: Record<string, string> = {
            amphi: 'Amphithéâtre',
            salle_td: 'Salle TD',
            salle_tp: 'Salle TP',
            salle_info: 'Salle Info',
        };
        return labels[type] || type;
    };

    const columns = [
        {
            title: 'Salle',
            key: 'salle',
            render: (_: any, record: Salle) => (
                <Space>
                    {getTypeIcon(record.type)}
                    <div>
                        <Text strong>{record.nom}</Text>
                        <br />
                        <Text type="secondary" style={{ fontSize: 11 }}>{record.code}</Text>
                    </div>
                </Space>
            ),
        },
        {
            title: 'Type',
            dataIndex: 'type',
            key: 'type',
            render: (type: string) => (
                <Tag color="blue">{getTypeLabel(type)}</Tag>
            ),
            filters: [
                { text: 'Amphithéâtre', value: 'amphi' },
                { text: 'Salle TD', value: 'salle_td' },
                { text: 'Salle TP', value: 'salle_tp' },
                { text: 'Salle Info', value: 'salle_info' },
            ],
            onFilter: (value: boolean | React.Key, record: Salle) => record.type === value,
        },
        {
            title: 'Bâtiment',
            dataIndex: 'batiment',
            key: 'batiment',
        },
        {
            title: 'Capacité Normale',
            dataIndex: 'capacite',
            key: 'capacite',
            sorter: (a: Salle, b: Salle) => a.capacite - b.capacite,
        },
        {
            title: 'Capacité Examen',
            dataIndex: 'capacite_examen',
            key: 'capacite_examen',
            render: (value: number, record: Salle) => (
                <div>
                    <Text strong>{value}</Text>
                    <Text type="secondary"> places</Text>
                    <Progress
                        percent={Math.round((value / record.capacite) * 100)}
                        size="small"
                        showInfo={false}
                        strokeColor="#1890ff"
                    />
                </div>
            ),
        },
        {
            title: 'Disponibilité',
            dataIndex: 'disponible',
            key: 'disponible',
            render: (value: boolean) => (
                value ? (
                    <Tag icon={<CheckCircleOutlined />} color="success">
                        Disponible
                    </Tag>
                ) : (
                    <Tag icon={<CloseCircleOutlined />} color="error">
                        Indisponible
                    </Tag>
                )
            ),
            filters: [
                { text: 'Disponible', value: true },
                { text: 'Indisponible', value: false },
            ],
            onFilter: (value: boolean | React.Key, record: Salle) => record.disponible === value,
        },
        {
            title: 'PMR',
            key: 'pmr',
            render: (_: any, record: any) => (
                record.accessibilite_pmr ? (
                    <Tag color="green">Accessible</Tag>
                ) : (
                    <Tag color="default">-</Tag>
                )
            ),
        },
    ];

    // Statistics
    const totalCapacity = salles.reduce((sum, s) => sum + s.capacite_examen, 0);
    const totalSalles = salles.length;
    const sallesDisponibles = salles.filter(s => s.disponible).length;

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
                <Spin size="large" tip="Chargement des salles..." />
            </div>
        );
    }

    return (
        <div className="fade-in">
            <div style={{ marginBottom: 24 }}>
                <Title level={4} style={{ marginBottom: 4 }}>
                    Gestion des Salles
                </Title>
                <Text type="secondary">
                    Consultez la disponibilité et la capacité des salles d'examen
                </Text>
            </div>

            {/* Stats */}
            <Row gutter={[24, 24]} style={{ marginBottom: 24 }}>
                <Col xs={24} sm={8}>
                    <Card>
                        <Space>
                            <BankOutlined style={{ fontSize: 32, color: '#1890ff' }} />
                            <div>
                                <Text type="secondary">Total Salles</Text>
                                <Title level={3} style={{ margin: 0 }}>{totalSalles}</Title>
                            </div>
                        </Space>
                    </Card>
                </Col>
                <Col xs={24} sm={8}>
                    <Card>
                        <Space>
                            <CheckCircleOutlined style={{ fontSize: 32, color: '#52c41a' }} />
                            <div>
                                <Text type="secondary">Salles Disponibles</Text>
                                <Title level={3} style={{ margin: 0 }}>{sallesDisponibles}</Title>
                            </div>
                        </Space>
                    </Card>
                </Col>
                <Col xs={24} sm={8}>
                    <Card>
                        <Space>
                            <BankOutlined style={{ fontSize: 32, color: '#722ed1' }} />
                            <div>
                                <Text type="secondary">Capacité Totale (Examen)</Text>
                                <Title level={3} style={{ margin: 0 }}>{totalCapacity.toLocaleString()}</Title>
                            </div>
                        </Space>
                    </Card>
                </Col>
            </Row>

            {/* Table */}
            <Card>
                <Table
                    dataSource={salles}
                    columns={columns}
                    rowKey="id"
                    pagination={{ pageSize: 15, showSizeChanger: true }}
                />
            </Card>
        </div>
    );
};

export default SallesPage;
