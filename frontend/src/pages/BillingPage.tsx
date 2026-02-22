import { useEffect, useMemo, useState } from 'react'
import api from '../api/client'

interface Product {
  id: string
  name: string
  selling_price: number | string
  stock_quantity: number | string
}

interface CartItem {
  product: Product
  quantity: number
}

export default function BillingPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [cart, setCart] = useState<CartItem[]>([])
  const [discount, setDiscount] = useState(0)
  const [gst, setGst] = useState(0)
  const [paymentMode, setPaymentMode] = useState('cash')
  const [shopId, setShopId] = useState<string>('')

  useEffect(() => {
    api.get<Product[]>('/products/').then(res => {
      const normalized = res.data.map(p => ({
        ...p,
        selling_price: Number(p.selling_price),
        stock_quantity: Number(p.stock_quantity),
      }))
      setProducts(normalized)
    })
    api.get<{ id: string; shop_id: string }>('/auth/me').then(res => setShopId(res.data.shop_id))
  }, [])

  const addToCart = (product: Product) => {
    setCart(prev => {
      const existing = prev.find(c => c.product.id === product.id)
      if (existing) {
        return prev.map(c => c.product.id === product.id ? { ...c, quantity: c.quantity + 1 } : c)
      }
      return [...prev, { product, quantity: 1 }]
    })
  }

  const updateQty = (id: string, qty: number) => {
    setCart(prev => prev.map(c => c.product.id === id ? { ...c, quantity: qty } : c))
  }

  const total = useMemo(() => cart.reduce((sum, item) => sum + item.product.selling_price * item.quantity, 0), [cart])
  const gstAmount = useMemo(() => total * (gst / 100), [total, gst])
  const grandTotal = useMemo(() => total + gstAmount - discount, [total, gstAmount, discount])

  const submitSale = async () => {
    if (!shopId) return
    const items = cart.map(c => ({
      product_id: c.product.id,
      quantity: c.quantity,
      unit_price: c.product.selling_price
    }))
    await api.post('/sales/', {
      shop_id: shopId,
      discount,
      payment_mode: paymentMode,
      gst_percentage: gst,
      items
    })
    setCart([])
    setDiscount(0)
    setGst(0)
    alert('Sale recorded')
  }

  return (
    <div className="grid" style={{ gridTemplateColumns: '1.3fr 1fr' }}>
      <div className="card">
        <div style={{ marginBottom: 12, fontWeight: 600 }}>Products</div>
        <div style={{ display: 'grid', gap: 8, gridTemplateColumns: 'repeat(auto-fit,minmax(160px,1fr))' }}>
          {products.map(p => (
            <button key={p.id} className="card" style={{ textAlign: 'left', cursor: 'pointer' }} onClick={() => addToCart(p)}>
              <div style={{ fontWeight: 600 }}>{p.name}</div>
              <div style={{ fontSize: 12, color: '#555' }}>₹ {p.selling_price.toFixed(2)}</div>
              <div style={{ fontSize: 12, color: p.stock_quantity <= 3 ? 'crimson' : '#555' }}>Stock: {p.stock_quantity}</div>
            </button>
          ))}
        </div>
      </div>

      <div className="card">
        <div style={{ marginBottom: 12, fontWeight: 600 }}>Cart</div>
        <div className="grid" style={{ gap: 10 }}>
          {cart.map(item => (
            <div key={item.product.id} className="flex" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontWeight: 600 }}>{item.product.name}</div>
                <div style={{ fontSize: 12, color: '#555' }}>₹ {item.product.selling_price.toFixed(2)}</div>
              </div>
              <input
                type="number"
                min={1}
                className="input"
                style={{ width: 80 }}
                value={item.quantity}
                onChange={e => updateQty(item.product.id, Number(e.target.value))}
              />
            </div>
          ))}
        </div>

        <div className="grid" style={{ marginTop: 16 }}>
          <label>Discount</label>
          <input type="number" className="input" value={discount} onChange={e => setDiscount(Number(e.target.value))} />
          <label>GST %</label>
          <input type="number" className="input" value={gst} onChange={e => setGst(Number(e.target.value))} />
          <label>Payment Mode</label>
          <select className="input" value={paymentMode} onChange={e => setPaymentMode(e.target.value)}>
            <option value="cash">Cash</option>
            <option value="upi">UPI</option>
            <option value="card">Card</option>
          </select>
        </div>

        <div style={{ marginTop: 16, fontWeight: 700 }}>
          Subtotal: ₹ {total.toFixed(2)}
        </div>
        <div>GST: ₹ {gstAmount.toFixed(2)}</div>
        <div>Discount: ₹ {discount.toFixed(2)}</div>
        <div style={{ fontSize: 20, marginTop: 8 }}>Total: ₹ {grandTotal.toFixed(2)}</div>

        <button className="btn primary" style={{ marginTop: 16, width: '100%' }} onClick={submitSale} disabled={!cart.length}>
          Complete Sale
        </button>
      </div>
    </div>
  )
}
