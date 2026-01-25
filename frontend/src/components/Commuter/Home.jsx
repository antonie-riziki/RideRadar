import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getVehicles, getTickets } from '../../api/api'

export default function CommuterHome(){
  const [nextVehicle, setNextVehicle] = useState(null)
  const [tickets, setTickets] = useState([])

  useEffect(()=>{
    let mounted = true
    async function load(){
      try{
        const vs = await getVehicles()
        if(!mounted) return
        setNextVehicle(vs && vs.length ? vs[0] : null)
      }catch(e){ console.warn(e) }
      try{ const t = await getTickets(); if(mounted) setTickets(t) }catch(e){}
    }
    load()
    return ()=>{ mounted = false }
  },[])

  return (
    <div>
      <section className="card">
        <h2>Good morning 👋</h2>
        <div style={{marginTop:12}}>
          <input placeholder="Search destination or choose..." style={{width:'100%', padding:10, borderRadius:8}} />
        </div>
        <div style={{display:'flex', gap:8, marginTop:12}}>
          <button className="large-cta">Nearest Stop</button>
          <button className="large-cta">My Usual Route</button>
        </div>
      </section>

      <section className="card">
        <h3>Live status</h3>
        {nextVehicle ? (
          <div>
            <p>Route {nextVehicle.route} — arriving in {nextVehicle.eta_minutes} mins 🚐</p>
            <div style={{marginTop:8}}>
              <Link to="/map" className="large-cta">Track Vehicle</Link>
            </div>
          </div>
        ) : (
          <p>Loading nearby vehicles...</p>
        )}
      </section>

      <section className="card">
        <h3>Your tickets</h3>
        {tickets && tickets.length ? (
          <div>
            <div style={{fontWeight:600}}>Active</div>
            <div style={{marginTop:8}}>{tickets[0].route} — expires in {tickets[0].expires_in_min} min</div>
            <div style={{marginTop:8}}><Link to="/tickets">View all</Link></div>
          </div>
        ) : (
          <div>No active tickets</div>
        )}
      </section>
    </div>
  )
}
