import React, { useEffect, useState } from 'react'
import { getOverview, getAnalytics, getVehicles } from '../../api/api'

function StatCard({title, value}){return (<div style={{flex:1}} className="card"><h4>{title}</h4><div style={{fontSize:20, marginTop:6}}>{value}</div></div>)}

export default function AdminDashboard(){
  const [overview, setOverview] = useState(null)
  const [analytics, setAnalytics] = useState(null)
  const [vehicles, setVehicles] = useState([])

  useEffect(()=>{
    let mounted = true
    async function load(){
      try{ const o = await getOverview(); if(mounted) setOverview(o) }catch(e){console.warn(e)}
      try{ const a = await getAnalytics(); if(mounted) setAnalytics(a) }catch(e){}
      try{ const v = await getVehicles(); if(mounted) setVehicles(v) }catch(e){}
    }
    load()
  },[])

  return (
    <div>
      <section style={{display:'flex', gap:12}}>
        <StatCard title="Active vehicles" value={overview ? overview.active_vehicles : '...'} />
        <StatCard title="Commuters today" value={overview ? overview.commuters_today : '...'} />
        <StatCard title="Revenue (today)" value={overview ? `KES ${overview.revenue_today}` : '...'} />
      </section>

      <section className="card" style={{marginTop:12}}>
        <h3>Live Fleet Monitoring</h3>
        <div>
          {vehicles && vehicles.length ? vehicles.slice(0,5).map(v => (
            <div key={v.id} style={{padding:6, borderBottom:'1px solid #eee'}}>{v.id} — Route {v.route} — ETA {v.eta_minutes}m</div>
          )) : <p>Loading vehicles...</p>}
        </div>
      </section>

      <section className="card" style={{marginTop:12}}>
        <h3>AI Recommendations</h3>
        <p>Example: Add 2 more vehicles to Route 46 between 5:30–7:30 PM.</p>
        <div style={{marginTop:8}}>
          <strong>Insights</strong>
          <pre style={{whiteSpace:'pre-wrap'}}>{analytics ? JSON.stringify(analytics, null, 2) : 'Loading analytics...'}</pre>
        </div>
      </section>
    </div>
  )
}
