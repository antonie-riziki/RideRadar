const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

async function request(path, {method='GET', body=null, token=null} = {}){
  const headers = { 'Content-Type': 'application/json' }
  if(token) headers['Authorization'] = `Bearer ${token}`
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
}

export { API_BASE, request }
