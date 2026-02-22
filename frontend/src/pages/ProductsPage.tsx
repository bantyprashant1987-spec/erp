import { useEffect, useState } from 'react'
import api from '../api/client'

interface Product {
  id: string
  name: string
  category?: string
    purchase_price: number | string
    selling_price: number | string
  stock_quantity: number
  low_stock_threshold: number
  shop_id: string
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [form, setForm] = useState({
    name: '',
    category: '',
    purchase_price: 0,
    selling_price: 0,
    stock_quantity: 0,
    low_stock_threshold: 5
  })

  const load = () => {
    api.get<Product[]>('/products/').then(res => {
      const normalized = res.data.map(p => ({
        ...p,
        purchase_price: Number(p.purchase_price),
        selling_price: Number(p.selling_price),
      }))
      setProducts(normalized)
    })
  }

  useEffect(() => {
    load()
  }, [])

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    await api.post('/products/', { ...form, shop_id: products[0]?.shop_id || '' })
    setForm({ name: '', category: '', purchase_price: 0, selling_price: 0, stock_quantity: 0, low_stock_threshold: 5 })
    load()
  }

  return (
    <div className="grid" style={{ gridTemplateColumns: '1.2fr 1fr' }}>
      <div className="card">
        <div style={{ marginBottom: 12, fontWeight: 600 }}>Products</div>
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Stock</th>
            </tr>
          </thead>
          <tbody>
            {products.map(p => (
              <tr key={p.id}>
                <td>{p.name}</td>
                <td>{p.category}</td>
                <td>₹ {p.selling_price.toFixed(2)}</td>
                <td style={{ color: p.stock_quantity <= p.low_stock_threshold ? 'crimson' : 'inherit' }}>{p.stock_quantity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="card">
        <div style={{ marginBottom: 12, fontWeight: 600 }}>Add Product</div>
        <form onSubmit={submit} className="grid" style={{ gap: 10 }}>
          <input className="input" placeholder="Name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} required />
          <input className="input" placeholder="Category" value={form.category} onChange={e => setForm({ ...form, category: e.target.value })} />
          <input className="input" type="number" placeholder="Purchase Price" value={form.purchase_price} onChange={e => setForm({ ...form, purchase_price: Number(e.target.value) })} required />
          <input className="input" type="number" placeholder="Selling Price" value={form.selling_price} onChange={e => setForm({ ...form, selling_price: Number(e.target.value) })} required />
          <input className="input" type="number" placeholder="Stock" value={form.stock_quantity} onChange={e => setForm({ ...form, stock_quantity: Number(e.target.value) })} required />
          <input className="input" type="number" placeholder="Low Stock Alert" value={form.low_stock_threshold} onChange={e => setForm({ ...form, low_stock_threshold: Number(e.target.value) })} />
          <button className="btn primary" type="submit">Save</button>
        </form>
      </div>
    </div>
  )
}
