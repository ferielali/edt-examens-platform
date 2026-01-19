import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
    Layout,
    Menu,
    Avatar,
    Dropdown,
    Typography,
    Badge,
    Space,
    List,
    Popover,
    Button,
    message,
    Modal,
} from 'antd';
import {
    DashboardOutlined,
    CalendarOutlined,
    TeamOutlined,
    BookOutlined,
    SettingOutlined,
    LogoutOutlined,
    UserOutlined,
    BellOutlined,
    MenuFoldOutlined,
    MenuUnfoldOutlined,
    ScheduleOutlined,
    BankOutlined,
} from '@ant-design/icons';
import { useAuth } from '../context/AuthContext';
import SettingsModal from './SettingsModal';

const { Header, Sider, Content } = Layout;
const { Text } = Typography;

const DashboardLayout: React.FC = () => {
    const [collapsed, setCollapsed] = useState(false);
    const [showAllNotifications, setShowAllNotifications] = useState(false);
    const [showSettings, setShowSettings] = useState(false);
    const [notifications, setNotifications] = useState([
        {
            id: 1,
            title: 'Nouvel examen planifié',
            description: 'Mathématiques L2 - 23 Dec 2025',
            time: 'Il y a 5 min',
            read: false,
        },
        {
            id: 2,
            title: 'Conflit détecté',
            description: 'Chevauchement salle A101 détecté',
            time: 'Il y a 1 heure',
            read: false,
        },
        {
            id: 3,
            title: 'EDT généré avec succès',
            description: 'Session Décembre 2025 complète',
            time: 'Il y a 2 heures',
            read: true,
        },
    ]);
    const { user, logout, token } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    // Menu items based on user role
    const getMenuItems = () => {
        const baseItems = [];

        // Director-only items
        if (user?.role === 'director') {
            baseItems.push({
                key: '/director',
                icon: <DashboardOutlined />,
                label: 'Vue Stratégique',
            });
        }

        // Admin items
        if (['director', 'administrator'].includes(user?.role || '')) {
            baseItems.push(
                {
                    key: '/admin',
                    icon: <ScheduleOutlined />,
                    label: 'Génération EDT',
                },
                {
                    key: '/salles',
                    icon: <BankOutlined />,
                    label: 'Salles',
                }
            );
        }

        // Department head items
        if (['director', 'administrator', 'department_head'].includes(user?.role || '')) {
            baseItems.push({
                key: '/department',
                icon: <TeamOutlined />,
                label: 'Mon Département',
            });
        }

        // Common items for all
        baseItems.push(
            {
                key: '/examens',
                icon: <CalendarOutlined />,
                label: 'Examens',
            },
            {
                key: '/student',
                icon: <BookOutlined />,
                label: 'Mon Planning',
            }
        );

        return baseItems;
    };

    const handleMenuClick = (info: { key: string }) => {
        navigate(info.key);
    };

    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    const userMenuItems = [
        {
            key: 'profile',
            icon: <UserOutlined />,
            label: 'Mon Profil',
        },
        {
            key: 'settings',
            icon: <SettingOutlined />,
            label: 'Paramètres',
            onClick: () => setShowSettings(true),
        },
        {
            type: 'divider' as const,
        },
        {
            key: 'logout',
            icon: <LogoutOutlined />,
            label: 'Déconnexion',
            danger: true,
            onClick: handleLogout,
        },
    ];

    const getRoleLabel = (role: string) => {
        const labels: Record<string, string> = {
            director: 'Directeur',
            administrator: 'Administrateur',
            department_head: 'Chef de Département',
            professor: 'Professeur',
            student: 'Étudiant',
        };
        return labels[role] || role;
    };

    // Mark all notifications as read
    const handleMarkAllRead = () => {
        setNotifications(notifications.map(n => ({ ...n, read: true })));
        message.success('Toutes les notifications ont été marquées comme lues');
    };

    // Mark single notification as read
    const handleNotificationClick = (id: number) => {
        setNotifications(notifications.map(n =>
            n.id === id ? { ...n, read: true } : n
        ));
    };

    // Notification dropdown content
    const notificationContent = (
        <div style={{ width: 320 }}>
            <div style={{
                padding: '12px 16px',
                borderBottom: '1px solid #f0f0f0',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}>
                <Text strong style={{ fontSize: 16 }}>Notifications</Text>
                <Button type="link" size="small" onClick={handleMarkAllRead}>Tout marquer lu</Button>
            </div>
            <List
                dataSource={notifications}
                renderItem={(item) => (
                    <List.Item
                        style={{
                            padding: '12px 16px',
                            cursor: 'pointer',
                            background: item.read ? 'transparent' : '#f0f7ff'
                        }}
                        onClick={() => handleNotificationClick(item.id)}
                    >
                        <List.Item.Meta
                            title={<Text strong={!item.read}>{item.title}</Text>}
                            description={
                                <div>
                                    <Text type="secondary" style={{ fontSize: 12 }}>{item.description}</Text>
                                    <br />
                                    <Text type="secondary" style={{ fontSize: 11 }}>{item.time}</Text>
                                </div>
                            }
                        />
                    </List.Item>
                )}
            />
            <div style={{ padding: '8px 16px', borderTop: '1px solid #f0f0f0', textAlign: 'center' }}>
                <Button type="link" onClick={() => setShowAllNotifications(true)}>Voir toutes les notifications</Button>
            </div>
        </div>
    );

    return (
        <Layout className="dashboard-layout">
            <Sider
                trigger={null}
                collapsible
                collapsed={collapsed}
                style={{
                    overflow: 'auto',
                    height: '100vh',
                    position: 'fixed',
                    left: 0,
                    top: 0,
                    bottom: 0,
                }}
            >
                <div
                    style={{
                        height: 64,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        borderBottom: '1px solid rgba(255,255,255,0.1)',
                    }}
                >
                    <div className="dashboard-logo">
                        <CalendarOutlined style={{ fontSize: 24, color: '#1890ff' }} />
                        {!collapsed && (
                            <span style={{ color: 'white', marginLeft: 8, fontWeight: 600 }}>
                                ExamScheduler
                            </span>
                        )}
                    </div>
                </div>

                <Menu
                    theme="dark"
                    mode="inline"
                    selectedKeys={[location.pathname]}
                    items={getMenuItems()}
                    onClick={handleMenuClick}
                    style={{ marginTop: 16 }}
                />
            </Sider>

            <Layout style={{ marginLeft: collapsed ? 80 : 200, transition: 'all 0.2s' }}>
                <Header
                    className="dashboard-header"
                    style={{
                        padding: '0 24px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        background: 'linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%)',
                        boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
                    }}
                >
                    <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                        {React.createElement(collapsed ? MenuUnfoldOutlined : MenuFoldOutlined, {
                            style: { fontSize: 20, cursor: 'pointer', color: 'white' },
                            onClick: () => setCollapsed(!collapsed),
                        })}
                        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                            <CalendarOutlined style={{ fontSize: 24, color: '#60a5fa' }} />
                            <span style={{
                                fontSize: 20,
                                fontWeight: 700,
                                color: 'white',
                                letterSpacing: '-0.5px',
                                textShadow: '0 1px 2px rgba(0,0,0,0.2)',
                            }}>
                                Plateforme EDT Examens
                            </span>
                        </div>
                    </div>

                    <div className="header-right" style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
                        <Popover
                            content={notificationContent}
                            trigger="click"
                            placement="bottomRight"
                            overlayStyle={{ padding: 0 }}
                        >
                            <Badge count={notifications.filter(n => !n.read).length} size="small">
                                <BellOutlined style={{ fontSize: 20, cursor: 'pointer', color: '#fbbf24' }} />
                            </Badge>
                        </Popover>

                        <Dropdown menu={{ items: userMenuItems }} trigger={['click']}>
                            <Space style={{ cursor: 'pointer' }}>
                                <Avatar
                                    style={{ backgroundColor: '#60a5fa' }}
                                    icon={<UserOutlined />}
                                />
                                <div style={{ lineHeight: 1.3 }}>
                                    <Text strong style={{ display: 'block', fontSize: 14, color: 'white' }}>
                                        {user?.nom_complet}
                                    </Text>
                                    <Text style={{ fontSize: 12, color: '#93c5fd' }}>
                                        {getRoleLabel(user?.role || '')}
                                    </Text>
                                </div>
                            </Space>
                        </Dropdown>
                    </div>
                </Header>

                <Content
                    style={{
                        margin: 24,
                        padding: 24,
                        minHeight: 'calc(100vh - 112px)',
                        background: '#f0f2f5',
                    }}
                >
                    <Outlet />
                </Content>
            </Layout>

            {/* All Notifications Modal */}
            <Modal
                title="Toutes les Notifications"
                open={showAllNotifications}
                onCancel={() => setShowAllNotifications(false)}
                footer={[
                    <Button key="markAll" onClick={handleMarkAllRead}>
                        Tout marquer lu
                    </Button>,
                    <Button key="close" type="primary" onClick={() => setShowAllNotifications(false)}>
                        Fermer
                    </Button>
                ]}
                width={500}
            >
                <List
                    dataSource={notifications}
                    renderItem={(item) => (
                        <List.Item
                            style={{
                                padding: '12px 16px',
                                cursor: 'pointer',
                                background: item.read ? 'transparent' : '#f0f7ff',
                                borderRadius: 8,
                                marginBottom: 8
                            }}
                            onClick={() => handleNotificationClick(item.id)}
                        >
                            <List.Item.Meta
                                title={<Text strong={!item.read}>{item.title}</Text>}
                                description={
                                    <div>
                                        <Text type="secondary" style={{ fontSize: 12 }}>{item.description}</Text>
                                        <br />
                                        <Text type="secondary" style={{ fontSize: 11 }}>{item.time}</Text>
                                    </div>
                                }
                            />
                            {!item.read && (
                                <Badge status="processing" />
                            )}
                        </List.Item>
                    )}
                />
            </Modal>

            {/* Settings Modal */}
            <SettingsModal
                visible={showSettings}
                onClose={() => setShowSettings(false)}
                userEmail={user?.email || ''}
                token={token || ''}
            />
        </Layout>
    );
};

export default DashboardLayout;
