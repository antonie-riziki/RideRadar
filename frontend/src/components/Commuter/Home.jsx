import React from 'react'
import { Link } from 'react-router-dom'

export default function CommuterHome(){
  return (
    <div>
      <section className="card">
        <h2>Good morning 👋 Ready to head to Westlands?</h2>
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
        <p>Next vehicle arriving in 6 mins 🚐</p>
        <div style={{marginTop:8}}>
          <Link to="/map" className="large-cta">Track Vehicle</Link>
        </div>
      </section>

      <section className="card">
        <h3>Your tickets</h3>
        <Link to="/tickets">View active ticket</Link>
      </section>
    </div>
  )
}
