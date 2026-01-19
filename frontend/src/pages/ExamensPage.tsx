import React, { useEffect, useState } from 'react';
import {
    Card,
    Table,
    Button,
    Space,
    Tag,
    Typography,
    Input,
    Select,
    DatePicker,
    Row,
    Col,
    Modal,
    Form,
    message,
    Popconfirm,
    TimePicker,
} from 'antd';
import {
    PlusOutlined,
    SearchOutlined,
    EditOutlined,
    DeleteOutlined,
    CheckCircleOutlined,
    CloseCircleOutlined,
    ReloadOutlined,
} from '@ant-design/icons';
import dayjs from 'dayjs';
import { examensApi, dashboardApi, Examen, Module, PaginatedResponse } from '../services/api';
import { useAuth } from '../context/AuthContext';

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;

const ExamensPage: React.FC = () => {
    const { user } = useAuth();
    const [form] = Form.useForm();
    const [loading, setLoading] = useState(true);
    const [examens, setExamens] = useState<Examen[]>([]);
    const [modules, setModules] = useState<Module[]>([]);
    const [pagination, setPagination] = useState({ current: 1, pageSize: 20, total: 0 });
    const [filters, setFilters] = useState<any>({});
    const [modalVisible, setModalVisible] = useState(false);
    const [creating, setCreating] = useState(false);
    const [editingExam, setEditingExam] = useState<Examen | null>(null);

    useEffect(() => {
        loadData();
        loadModules();
    }, [pagination.current, filters]);

    const loadModules = async () => {
        try {
            const response = await dashboardApi.getModules();
            setModules(response.items);
        } catch (error) {
            console.error('Error loading modules:', error);
        }
    };

    const loadData = async () => {
        try {
            setLoading(true);
            const response = await examensApi.list({
                page: pagination.current,
                size: pagination.pageSize,
                ...filters,
            });
            setExamens(response.items);
            setPagination(prev => ({ ...prev, total: response.total }));
        } catch (error) {
            console.error('Error loading examens:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleConfirm = async (id: number) => {
        try {
            await examensApi.confirm(id);
            message.success('Examen confirmé');
            loadData();
        } catch (error: any) {
            message.error(error.response?.data?.detail || 'Erreur');
        }
    };

    const handleCancel = async (id: number) => {
        try {
            await examensApi.cancel(id);
            message.success('Examen annulé');
            loadData();
        } catch (error: any) {
            message.error(error.response?.data?.detail || 'Erreur');
        }
    };

    const handleDelete = async (id: number) => {
        try {
            await examensApi.delete(id);
            message.success('Examen supprimé');
            loadData();
        } catch (error: any) {
            message.error(error.response?.data?.detail || 'Erreur');
        }
    };

    const handleEdit = (exam: Examen) => {
        setEditingExam(exam);
        form.setFieldsValue({
            module_id: exam.module_id,
            date: dayjs(exam.date_heure),
            time: dayjs(exam.date_heure),
            duree_minutes: exam.duree_minutes,
        });
        setModalVisible(true);
    };

    const handleCreateOrUpdate = async (values: any) => {
        try {
            setCreating(true);
            const dateHeure = values.date
                .hour(values.time.hour())
                .minute(values.time.minute())
                .toISOString();

            if (editingExam) {
                await examensApi.update(editingExam.id, {
                    module_id: values.module_id,
                    date_heure: dateHeure,
                    duree_minutes: values.duree_minutes,
                });
                message.success('Examen mis à jour avec succès');
            } else {
                await examensApi.create({
                    module_id: values.module_id,
                    date_heure: dateHeure,
                    duree_minutes: values.duree_minutes,
                    statut: 'draft',
                });
                message.success('Examen créé avec succès');
            }

            setModalVisible(false);
            setEditingExam(null);
            form.resetFields();
            loadData();
        } catch (error: any) {
            message.error(error.response?.data?.detail || 'Erreur lors de l\'opération');
        } finally {
            setCreating(false);
        }
    };

    const columns = [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id',
            width: 60,
        },
        {
            title: 'Module',
            key: 'module',
            render: (_: any, record: Examen) => (
                <div>
                    <Text strong>{record.module?.nom || `Module ${record.module_id}`}</Text>
                    <br />
                    <Text type="secondary" style={{ fontSize: 11 }}>
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
                    <Text>{dayjs(date).format('DD/MM/YYYY')}</Text>
                    <br />
                    <Text type="secondary">{dayjs(date).format('HH:mm')}</Text>
                </div>
            ),
            sorter: true,
        },
        {
            title: 'Durée',
            dataIndex: 'duree_minutes',
            key: 'duree_minutes',
            render: (value: number) => `${value} min`,
            width: 80,
        },
        {
            title: 'Salle',
            key: 'salle',
            render: (_: any, record: Examen) => (
                record.salle ? (
                    <div>
                        <Text>{record.salle.nom}</Text>
                        <br />
                        <Text type="secondary" style={{ fontSize: 11 }}>
                            {record.salle.batiment}
                        </Text>
                    </div>
                ) : <Text type="secondary">-</Text>
            ),
        },
        {
            title: 'Surveillant',
            key: 'professeur',
            render: (_: any, record: Examen) => (
                record.professeur ? (
                    `${record.professeur.prenom} ${record.professeur.nom}`
                ) : <Text type="secondary">-</Text>
            ),
        },
        {
            title: 'Inscrits',
            dataIndex: 'nb_inscrits',
            key: 'nb_inscrits',
            width: 80,
            render: (value: number) => <Tag color="blue">{value}</Tag>,
        },
        {
            title: 'Statut',
            dataIndex: 'statut',
            key: 'statut',
            width: 100,
            render: (statut: string) => {
                const config: Record<string, { color: string; label: string }> = {
                    draft: { color: 'default', label: 'Brouillon' },
                    scheduled: { color: 'processing', label: 'Planifié' },
                    confirmed: { color: 'success', label: 'Confirmé' },
                    completed: { color: 'cyan', label: 'Terminé' },
                    cancelled: { color: 'error', label: 'Annulé' },
                };
                const { color, label } = config[statut] || { color: 'default', label: statut };
                return <Tag color={color}>{label}</Tag>;
            },
            filters: [
                { text: 'Brouillon', value: 'draft' },
                { text: 'Planifié', value: 'scheduled' },
                { text: 'Confirmé', value: 'confirmed' },
                { text: 'Terminé', value: 'completed' },
                { text: 'Annulé', value: 'cancelled' },
            ],
        },
        {
            title: 'Actions',
            key: 'actions',
            width: 180,
            render: (_: any, record: Examen) => (
                <Space size="small">
                    {['draft', 'scheduled'].includes(record.statut) &&
                        ['director', 'administrator', 'department_head'].includes(user?.role || '') && (
                            <Button
                                type="primary"
                                size="small"
                                icon={<CheckCircleOutlined />}
                                onClick={() => handleConfirm(record.id)}
                                title="Confirmer"
                            />
                        )}
                    {['draft', 'scheduled'].includes(record.statut) &&
                        ['director', 'administrator'].includes(user?.role || '') && (
                            <Button
                                size="small"
                                icon={<EditOutlined />}
                                onClick={() => handleEdit(record)}
                                title="Modifier"
                            />
                        )}
                    {['draft', 'scheduled', 'confirmed'].includes(record.statut) &&
                        ['director', 'administrator'].includes(user?.role || '') && (
                            <Button
                                size="small"
                                danger
                                icon={<CloseCircleOutlined />}
                                onClick={() => handleCancel(record.id)}
                                title="Annuler"
                            />
                        )}
                    {['director', 'administrator'].includes(user?.role || '') && (
                        <Popconfirm
                            title="Supprimer cet examen?"
                            onConfirm={() => handleDelete(record.id)}
                        >
                            <Button size="small" danger icon={<DeleteOutlined />} title="Supprimer" />
                        </Popconfirm>
                    )}
                </Space>
            ),
        },
    ];

    return (
        <div className="fade-in">
            <div style={{ marginBottom: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <Title level={4} style={{ marginBottom: 4 }}>
                        Gestion des Examens
                    </Title>
                    <Text type="secondary">
                        Consultez et gérez tous les examens planifiés
                    </Text>
                </div>
                <Space>
                    <Button icon={<ReloadOutlined />} onClick={loadData}>
                        Actualiser
                    </Button>
                    {['director', 'administrator'].includes(user?.role || '') && (
                        <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
                            Nouvel Examen
                        </Button>
                    )}
                </Space>
            </div>

            {/* Filters */}
            <Card style={{ marginBottom: 24 }}>
                <Row gutter={16}>
                    <Col xs={24} sm={12} md={6}>
                        <Input
                            placeholder="Rechercher..."
                            prefix={<SearchOutlined />}
                            allowClear
                            onChange={(e) => setFilters((prev: any) => ({ ...prev, search: e.target.value || undefined }))}
                        />
                    </Col>
                    <Col xs={24} sm={12} md={6}>
                        <Select
                            placeholder="Statut"
                            style={{ width: '100%' }}
                            allowClear
                            onChange={(value) => setFilters((prev: any) => ({ ...prev, statut: value }))}
                            options={[
                                { value: 'draft', label: 'Brouillon' },
                                { value: 'scheduled', label: 'Planifié' },
                                { value: 'confirmed', label: 'Confirmé' },
                                { value: 'completed', label: 'Terminé' },
                                { value: 'cancelled', label: 'Annulé' },
                            ]}
                        />
                    </Col>
                    <Col xs={24} sm={12} md={8}>
                        <RangePicker
                            style={{ width: '100%' }}
                            placeholder={['Date début', 'Date fin']}
                            format="DD/MM/YYYY"
                            onChange={(dates) => {
                                if (dates) {
                                    setFilters((prev: any) => ({
                                        ...prev,
                                        date_debut: dates[0]?.toISOString(),
                                        date_fin: dates[1]?.toISOString(),
                                    }));
                                } else {
                                    setFilters((prev: any) => {
                                        const { date_debut, date_fin, ...rest } = prev;
                                        return rest;
                                    });
                                }
                            }}
                        />
                    </Col>
                </Row>
            </Card>

            {/* Table */}
            <Card>
                <Table
                    dataSource={examens}
                    columns={columns}
                    rowKey="id"
                    loading={loading}
                    onChange={(paginationInfo, tableFilters, sorter: any) => {
                        // Handle pagination
                        setPagination(prev => ({
                            ...prev,
                            current: paginationInfo.current || 1,
                            pageSize: paginationInfo.pageSize || 20,
                        }));

                        // Handle filters from column headers
                        if (tableFilters.statut && tableFilters.statut.length > 0) {
                            setFilters((prev: any) => ({
                                ...prev,
                                statut: tableFilters.statut?.[0] as string,
                            }));
                        } else {
                            setFilters((prev: any) => {
                                const { statut, ...rest } = prev;
                                return rest;
                            });
                        }

                        // Handle sorting
                        if (sorter.field === 'date_heure') {
                            setFilters((prev: any) => ({
                                ...prev,
                                sort_order: sorter.order === 'descend' ? 'desc' : 'asc',
                            }));
                        }
                    }}
                    pagination={{
                        ...pagination,
                        showSizeChanger: true,
                        showTotal: (total) => `${total} examens`,
                    }}
                />
            </Card>

            {/* New/Edit Exam Modal */}
            <Modal
                title={editingExam ? "Modifier l'Examen" : "Créer un Nouvel Examen"}
                open={modalVisible}
                onCancel={() => {
                    setModalVisible(false);
                    setEditingExam(null);
                    form.resetFields();
                }}
                footer={null}
                width={500}
            >
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleCreateOrUpdate}
                >
                    <Form.Item
                        name="module_id"
                        label="Module"
                        rules={[{ required: true, message: 'Veuillez sélectionner un module' }]}
                    >
                        <Select
                            placeholder="Sélectionner un module"
                            showSearch
                            optionFilterProp="children"
                            filterOption={(input, option) =>
                                (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
                            }
                            options={modules.map(m => ({
                                value: m.id,
                                label: `${m.nom} (${m.code})`,
                            }))}
                        />
                    </Form.Item>

                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item
                                name="date"
                                label="Date"
                                rules={[{ required: true, message: 'Veuillez sélectionner une date' }]}
                            >
                                <DatePicker
                                    format="DD/MM/YYYY"
                                    style={{ width: '100%' }}
                                    placeholder="Sélectionner la date"
                                />
                            </Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item
                                name="time"
                                label="Heure"
                                rules={[{ required: true, message: 'Veuillez sélectionner une heure' }]}
                            >
                                <TimePicker
                                    format="HH:mm"
                                    style={{ width: '100%' }}
                                    placeholder="Sélectionner l'heure"
                                    minuteStep={15}
                                />
                            </Form.Item>
                        </Col>
                    </Row>

                    <Form.Item
                        name="duree_minutes"
                        label="Durée (minutes)"
                        rules={[{ required: true, message: 'Veuillez entrer la durée' }]}
                        initialValue={120}
                    >
                        <Select
                            options={[
                                { value: 60, label: '1 heure' },
                                { value: 90, label: '1h30' },
                                { value: 120, label: '2 heures' },
                                { value: 150, label: '2h30' },
                                { value: 180, label: '3 heures' },
                            ]}
                        />
                    </Form.Item>

                    <Form.Item style={{ marginBottom: 0, marginTop: 24 }}>
                        <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
                            <Button onClick={() => {
                                setModalVisible(false);
                                setEditingExam(null);
                                form.resetFields();
                            }}>
                                Annuler
                            </Button>
                            <Button type="primary" htmlType="submit" loading={creating}>
                                {editingExam ? "Mettre à jour" : "Créer l'Examen"}
                            </Button>
                        </Space>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default ExamensPage;

