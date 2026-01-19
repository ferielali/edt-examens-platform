import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import frFR from 'antd/locale/fr_FR'
import App from './App'
import { AuthProvider } from './context/AuthContext'
import './index.css'

// Configuration du thème Ant Design
const theme = {
    token: {
        colorPrimary: '#1890ff',
        colorSuccess: '#52c41a',
        colorWarning: '#faad14',
        colorError: '#ff4d4f',
        colorInfo: '#1890ff',
        borderRadius: 8,
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    },
    components: {
        Layout: {
            headerBg: '#001529',
            siderBg: '#001529',
        },
        Menu: {
            darkItemBg: '#001529',
            darkItemSelectedBg: '#1890ff',
        },
    },
}

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <BrowserRouter>
            <ConfigProvider locale={frFR} theme={theme}>
                <AuthProvider>
                    <App />
                </AuthProvider>
            </ConfigProvider>
        </BrowserRouter>
    </React.StrictMode>,
)
