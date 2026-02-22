import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'

interface User {
  id: string
  email: string
  role: string
  shop_id: string
}

interface Props {
  onLogin: (u: User) => void
}

export default function LoginPage({ onLogin }: Props) {
  const [email, setEmail] = useState('owner@example.com')
  const [password, setPassword] = useState('changeme123')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await api.post<{ access_token: string }>('/auth/login', { email, password })
      localStorage.setItem('token', data.access_token)
      const me = await api.get<User>('/auth/me')
      onLogin(me.data)
      navigate('/')
    } catch (err) {
      setError('Invalid credentials')
    }
  }

  return (
    <div className="container" style={{ maxWidth: 420, paddingTop: 80 }}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>Sign in</h2>
        <form onSubmit={handleSubmit}>
          <label>Email</label>
          <input className="input" value={email} onChange={e => setEmail(e.target.value)} />
          <label>Password</label>
          <input className="input" type="password" value={password} onChange={e => setPassword(e.target.value)} />
          {error && <div style={{ color: 'red', marginBottom: 12 }}>{error}</div>}
          <button className="btn primary" style={{ width: '100%' }} type="submit">Login</button>
        </form>
      </div>
    </div>
  )
}
