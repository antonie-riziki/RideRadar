import React, { useEffect, useState } from 'react'
import { getVehicles } from '../../api/api'

export default function MapScreen(){
  const [vehicles, setVehicles] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    let mounted = true
    async function load(){
      setLoading(true)
      try{
        const vs = await getVehicles()
        if(mounted) setVehicles(vs)
      }catch(e){ console.warn(e); if(mounted) setVehicles([]) }
      if(mounted) setLoading(false)
    }
    load()
    const t = setInterval(load, 10000) // poll every 10s
    return ()=>{ mounted = false; clearInterval(t) }
  },[])

  return (
    <div>
      <section className="card">
        <h3>Live Map & Tracking</h3>
        <p>Map placeholder — integrate Mapbox/Leaflet for production.</p>
        {loading ? <p>Loading vehicles...</p> : (
          <div>
            {vehicles.length ? (
              vehicles.map(v => (
                <div key={v.id} style={{padding:8, borderBottom:'1px solid #eee'}}>
                  <div style={{fontWeight:700}}>{v.id} — Route {v.route}</div>
                  <div>ETA: {v.eta_minutes} mins · Occupancy: {v.occupancy} · Fare: KES {v.fare}</div>
                </div>
              ))
            ) : (
              <p>No active vehicles found.</p>
            )}
          </div>
        )}
      </section>
    </div>
  )
}
