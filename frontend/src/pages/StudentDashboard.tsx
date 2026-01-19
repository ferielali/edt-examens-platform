import React, { useEffect, useState } from 'react';
import {
    Row,
    Col,
    Card,
    Calendar,
    Badge,
    Typography,
    List,
    Tag,
    Space,
    Spin,
    Empty,
    Button,
    message,
} from 'antd';
import {
    CalendarOutlined,
    ClockCircleOutlined,
    EnvironmentOutlined,
    BookOutlined,
    DownloadOutlined,
} from '@ant-design/icons';
import type { Dayjs } from 'dayjs';
import dayjs from 'dayjs';
import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';
import { examensApi, Examen } from '../services/api';

const { Title, Text } = Typography;

const StudentDashboard: React.FC = () => {
    const [loading, setLoading] = useState(true);
    const [examens, setExamens] = useState<Examen[]>([]);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const response = await examensApi.list({ size: 100 });
            setExamens(response.items.filter(e => e.statut === 'confirmed'));
        } catch (error) {
            console.error('Error loading examens:', error);
        } finally {
            setLoading(false);
        }
    };

    // Handle PDF Export
    const handleExportPDF = () => {
        const doc = new jsPDF();

        // Title
        doc.setFontSize(20);
        doc.setTextColor(30, 58, 95);
        doc.text('Planning des Examens', 105, 20, { align: 'center' });

        // Subtitle
        doc.setFontSize(12);
        doc.setTextColor(100, 100, 100);
        doc.text(`Généré le ${dayjs().format('DD MMMM YYYY à HH:mm')}`, 105, 28, { align: 'center' });

        // Prepare table data
        const tableData = examens
            .sort((a, b) => new Date(a.date_heure).getTime() - new Date(b.date_heure).getTime())
            .map(exam => [
                exam.module?.nom || `Module ${exam.module_id}`,
                dayjs(exam.date_heure).format('DD/MM/YYYY'),
                dayjs(exam.date_heure).format('HH:mm'),
                `${exam.duree_minutes} min`,
                exam.salle?.nom || '-',
                exam.statut === 'confirmed' ? 'Confirmé' : 'Planifié'
            ]);

        // Add table
        autoTable(doc, {
            startY: 40,
            head: [['Module', 'Date', 'Heure', 'Durée', 'Salle', 'Statut']],
            body: tableData,
            styles: {
                fontSize: 10,
                cellPadding: 4,
            },
            headStyles: {
                fillColor: [30, 58, 95],
                textColor: [255, 255, 255],
                fontStyle: 'bold',
            },
            alternateRowStyles: {
                fillColor: [240, 242, 245],
            },
            columnStyles: {
                0: { cellWidth: 50 },
                1: { cellWidth: 25 },
                2: { cellWidth: 20 },
                3: { cellWidth: 20 },
                4: { cellWidth: 35 },
                5: { cellWidth: 25 },
            },
        });

        // Footer
        const pageCount = doc.getNumberOfPages();
        for (let i = 1; i <= pageCount; i++) {
            doc.setPage(i);
            doc.setFontSize(10);
            doc.setTextColor(150, 150, 150);
            doc.text(
                `Plateforme EDT Examens - Page ${i} / ${pageCount}`,
                105,
                doc.internal.pageSize.height - 10,
                { align: 'center' }
            );
        }

        // Save PDF
        doc.save(`planning-examens-${dayjs().format('YYYY-MM-DD')}.pdf`);
        message.success('PDF exporté avec succès !');
    };

    // Get examens for a specific date
    const getExamensForDate = (date: Dayjs) => {
        return examens.filter(e =>
            dayjs(e.date_heure).format('YYYY-MM-DD') === date.format('YYYY-MM-DD')
        );
    };

    // Calendar cell renderer
    const dateCellRender = (value: Dayjs) => {
        const dayExamens = getExamensForDate(value);

        if (dayExamens.length === 0) return null;

        return (
            <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                {dayExamens.slice(0, 2).map(exam => (
                    <li key={exam.id}>
                        <Badge
                            status={exam.statut === 'confirmed' ? 'success' : 'processing'}
                            text={
                                <Text style={{ fontSize: 11 }} ellipsis>
                                    {exam.module?.nom || `Examen ${exam.id}`}
                                </Text>
                            }
                        />
                    </li>
                ))}
                {dayExamens.length > 2 && (
                    <li>
                        <Text type="secondary" style={{ fontSize: 10 }}>
                            +{dayExamens.length - 2} autres
                        </Text>
                    </li>
                )}
            </ul>
        );
    };

    // Upcoming examens (next 30 days)
    const upcomingExamens = examens
        .filter(e => dayjs(e.date_heure).isAfter(dayjs()))
        .sort((a, b) => new Date(a.date_heure).getTime() - new Date(b.date_heure).getTime())
        .slice(0, 10);

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
                <Spin size="large" tip="Chargement de votre planning..." />
            </div>
        );
    }

    return (
        <div className="fade-in">
            <div style={{ marginBottom: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <Title level={4} style={{ marginBottom: 4 }}>
                        Mon Planning d'Examens
                    </Title>
                    <Text type="secondary">
                        Consultez vos examens et téléchargez votre planning personnalisé
                    </Text>
                </div>
                <Button type="primary" icon={<DownloadOutlined />} onClick={handleExportPDF}>
                    Exporter PDF
                </Button>
            </div>

            <Row gutter={[24, 24]}>
                {/* Calendar View */}
                <Col xs={24} lg={16}>
                    <Card className="exam-calendar">
                        <Calendar
                            dateCellRender={dateCellRender}
                            headerRender={({ value, onChange }) => (
                                <div style={{ padding: '8px 16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <Title level={5} style={{ margin: 0 }}>
                                        {value.format('MMMM YYYY')}
                                    </Title>
                                    <Space>
                                        <Button onClick={() => onChange(value.subtract(1, 'month'))}>
                                            &lt;
                                        </Button>
                                        <Button onClick={() => onChange(dayjs())}>
                                            Aujourd'hui
                                        </Button>
                                        <Button onClick={() => onChange(value.add(1, 'month'))}>
                                            &gt;
                                        </Button>
                                    </Space>
                                </div>
                            )}
                        />
                    </Card>
                </Col>

                {/* Upcoming Examens */}
                <Col xs={24} lg={8}>
                    <Card
                        title={
                            <Space>
                                <CalendarOutlined />
                                <span>Prochains Examens</span>
                            </Space>
                        }
                        style={{ height: '100%' }}
                    >
                        {upcomingExamens.length === 0 ? (
                            <Empty description="Aucun examen à venir" />
                        ) : (
                            <List
                                itemLayout="vertical"
                                dataSource={upcomingExamens}
                                renderItem={(exam) => (
                                    <List.Item
                                        style={{
                                            padding: '12px',
                                            marginBottom: 8,
                                            background: '#fafafa',
                                            borderRadius: 8,
                                            border: `1px solid ${exam.statut === 'confirmed' ? '#b7eb8f' : '#91d5ff'}`,
                                        }}
                                    >
                                        <div>
                                            <Text strong style={{ fontSize: 14 }}>
                                                {exam.module?.nom || `Module ${exam.module_id}`}
                                            </Text>
                                            <Tag
                                                color={exam.statut === 'confirmed' ? 'success' : 'processing'}
                                                style={{ marginLeft: 8, fontSize: 10 }}
                                            >
                                                {exam.statut === 'confirmed' ? 'Confirmé' : 'Planifié'}
                                            </Tag>
                                        </div>

                                        <Space direction="vertical" size={4} style={{ marginTop: 8 }}>
                                            <Text type="secondary" style={{ fontSize: 12 }}>
                                                <CalendarOutlined style={{ marginRight: 6 }} />
                                                {dayjs(exam.date_heure).format('dddd D MMMM YYYY')}
                                            </Text>
                                            <Text type="secondary" style={{ fontSize: 12 }}>
                                                <ClockCircleOutlined style={{ marginRight: 6 }} />
                                                {dayjs(exam.date_heure).format('HH:mm')} - {exam.duree_minutes} min
                                            </Text>
                                            {exam.salle && (
                                                <Text type="secondary" style={{ fontSize: 12 }}>
                                                    <EnvironmentOutlined style={{ marginRight: 6 }} />
                                                    {exam.salle.nom} - {exam.salle.batiment}
                                                </Text>
                                            )}
                                        </Space>
                                    </List.Item>
                                )}
                            />
                        )}
                    </Card>
                </Col>
            </Row>

            {/* Stats */}
            <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
                <Col xs={24} sm={8}>
                    <Card>
                        <Space>
                            <BookOutlined style={{ fontSize: 32, color: '#1890ff' }} />
                            <div>
                                <Text type="secondary">Total Examens</Text>
                                <Title level={3} style={{ margin: 0 }}>{examens.length}</Title>
                            </div>
                        </Space>
                    </Card>
                </Col>
                <Col xs={24} sm={8}>
                    <Card>
                        <Space>
                            <CalendarOutlined style={{ fontSize: 32, color: '#52c41a' }} />
                            <div>
                                <Text type="secondary">À Venir</Text>
                                <Title level={3} style={{ margin: 0 }}>{upcomingExamens.length}</Title>
                            </div>
                        </Space>
                    </Card>
                </Col>
                <Col xs={24} sm={8}>
                    <Card>
                        <Space>
                            <ClockCircleOutlined style={{ fontSize: 32, color: '#faad14' }} />
                            <div>
                                <Text type="secondary">Cette Semaine</Text>
                                <Title level={3} style={{ margin: 0 }}>
                                    {examens.filter(e =>
                                        dayjs(e.date_heure).isAfter(dayjs()) &&
                                        dayjs(e.date_heure).isBefore(dayjs().add(7, 'day'))
                                    ).length}
                                </Title>
                            </div>
                        </Space>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default StudentDashboard;
