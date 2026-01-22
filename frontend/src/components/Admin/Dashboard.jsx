import React from 'react'

function StatCard({title, value}){return (<div style={{flex:1}} className="card"><h4>{title}</h4><div style={{fontSize:20, marginTop:6}}>{value}</div></div>)}

export default function AdminDashboard(){
  return (
    <div>
      <section style={{display:'flex', gap:12}}>
        <StatCard title="Active vehicles" value="24" />
        <StatCard title="Commuters today" value="1,482" />
        <StatCard title="Revenue (today)" value="KES 34,120" />
      </section>

      <section className="card" style={{marginTop:12}}>
        <h3>Live Fleet Monitoring</h3>
        <p>Map + vehicle overlays. Click vehicle to inspect telemetry.</p>
      </section>

      <section className="card" style={{marginTop:12}}>
        <h3>AI Recommendations</h3>
        <p>Example: Add 2 more vehicles to Route 46 between 5:30–7:30 PM.</p>
      </section>
    </div>
  )
}
