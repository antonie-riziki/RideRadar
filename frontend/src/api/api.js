const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

async function request(path, {method='GET', body=null, token=null} = {}){
  const headers = { 'Content-Type': 'application/json' }
  if(token) headers['Authorization'] = `Bearer ${token}`
  try{
    const res = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null,
    })
    if(!res.ok){
      const text = await res.text()
      throw new Error(`${res.status} ${text}`)
    }
    return res.json().catch(()=>null)
  }catch(err){
    // rethrow for callers to decide; caller can fallback to mock data
    throw err
  }
}

// High level API helpers with graceful fallbacks
async function getVehicles(){
  try{ return await request('/vehicles/') }
  catch(_){
    // mock fallback
    return [
      { id: 'KAA-123A', route: '46', lat: -1.2921, lon: 36.8219, dir: 'NW', occupancy: 'medium', eta_minutes: 6, fare: 40 },
      { id: 'KAB-456B', route: '23', lat: -1.3000, lon: 36.8200, dir: 'E', occupancy: 'low', eta_minutes: 12, fare: 30 }
    ]
  }
}

async function getTickets(){
  try{ return await request('/tickets/') }
  catch(_){
    return [ { id: 'TCK-001', route: '46', expires_in_min: 28, code: 'ABC123' } ]
  }
}

async function getOverview(){
  try{ return await request('/overview/') }
  catch(_){
    return { active_vehicles: 24, commuters_today: 1482, revenue_today: 34120, avg_wait_min: 6 }
  }
}

async function getAnalytics(){
  try{ return await request('/analytics/') }
  catch(_){
    return { peak_hours: [{hour:'17:00', demand:1200}], route_performance: [{route:'46', score:78}] }
  }
}

export { API_BASE, request, getVehicles, getTickets, getOverview, getAnalytics }
