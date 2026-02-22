import { useEffect, useState } from 'react'
import { Navigate, Route, Routes, Link, useNavigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import ProductsPage from './pages/ProductsPage'
import BillingPage from './pages/BillingPage'
import api from './api/client'

interface User {
  id: string
  email: string
  role: string
  shop_id: string
}

function App() {
  const [user, setUser] = useState<User | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) return
    api.get<User>('/auth/me').then(res => setUser(res.data)).catch(() => {
      localStorage.removeItem('token')
    })
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    setUser(null)
    navigate('/login')
  }

  if (!user && !localStorage.getItem('token')) {
    return (
      <Routes>
        <Route path="/login" element={<LoginPage onLogin={setUser} />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    )
  }

  return (
    <div>
      <header style={{ padding: '12px 20px', background: '#0f172a', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ fontWeight: 700 }}>Retail ERP</div>
        <nav style={{ display: 'flex', gap: '12px' }}>
          <Link to="/" style={{ color: '#fff' }}>Dashboard</Link>
          <Link to="/products" style={{ color: '#fff' }}>Products</Link>
          <Link to="/billing" style={{ color: '#fff' }}>Billing</Link>
        </nav>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <span style={{ fontSize: 14 }}>{user?.email}</span>
          <button className="btn" onClick={handleLogout}>Logout</button>
        </div>
      </header>
      <div className="container" style={{ paddingTop: 24 }}>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/products" element={<ProductsPage />} />
          <Route path="/billing" element={<BillingPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </div>
  )
}

export default App
