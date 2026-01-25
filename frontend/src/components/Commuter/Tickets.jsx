import React, { useEffect, useState } from 'react'
import { getTickets } from '../../api/api'

export default function Tickets(){
  const [tickets, setTickets] = useState([])

  useEffect(()=>{
    let mounted = true
    async function load(){
      try{ const t = await getTickets(); if(mounted) setTickets(t) }catch(e){ console.warn(e) }
    }
    load()
    return ()=>{ mounted = false }
  },[])

  return (
    <div>
      <section className="card">
        <h3>Active Ticket</h3>
        {tickets && tickets.length ? (
          <div>
            <div style={{fontWeight:700}}>{tickets[0].route} — {tickets[0].code}</div>
            <div>Expires in {tickets[0].expires_in_min} min</div>
          </div>
        ) : (
          <p>No active ticket. Buy one from a vehicle or the route page.</p>
        )}
      </section>

      <section className="card">
        <h3>Ticket history</h3>
        {tickets && tickets.length ? (
          <ul>
            {tickets.map(t => (
              <li key={t.id}>{t.id} — {t.route} — expires in {t.expires_in_min} min</li>
            ))}
          </ul>
        ) : (
          <p>History empty</p>
        )}
      </section>
    </div>
  )
}
