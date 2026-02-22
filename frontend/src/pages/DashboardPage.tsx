import { useEffect, useState } from 'react'
import api from '../api/client'

interface DailyReport {
  date: string
  total_sales: number
  total_discount: number
  total_gst: number
  total_orders: number
}

export default function DashboardPage() {
  const [report, setReport] = useState<DailyReport | null>(null)

  useEffect(() => {
    api
      .get<DailyReport>('/reports/daily')
      .then(res => {
        const r = res.data
        // Backend may return decimals as strings; normalize to numbers for safe toFixed.
        setReport({
          date: r.date,
          total_sales: Number(r.total_sales) || 0,
          total_discount: Number(r.total_discount) || 0,
          total_gst: Number(r.total_gst) || 0,
          total_orders: Number(r.total_orders) || 0,
        })
      })
      .catch(() => setReport(null))
  }, [])

  return (
    <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit,minmax(220px,1fr))' }}>
      <div className="card">
        <div>Today Sales</div>
        <strong style={{ fontSize: 24 }}>
          ₹ {report ? report.total_sales.toFixed(2) : '0.00'}
        </strong>
      </div>
      <div className="card">
        <div>Orders</div>
        <strong style={{ fontSize: 24 }}>{report ? report.total_orders : 0}</strong>
      </div>
      <div className="card">
        <div>GST</div>
        <strong style={{ fontSize: 24 }}>
          ₹ {report ? report.total_gst.toFixed(2) : '0.00'}
        </strong>
      </div>
      <div className="card">
        <div>Discount</div>
        <strong style={{ fontSize: 24 }}>
          ₹ {report ? report.total_discount.toFixed(2) : '0.00'}
        </strong>
      </div>
    </div>
  )
}
