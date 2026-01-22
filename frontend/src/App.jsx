import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import CommuterHome from './components/Commuter/Home'
import MapScreen from './components/Commuter/Map'
import Tickets from './components/Commuter/Tickets'
import AdminDashboard from './components/Admin/Dashboard'

export default function App(){
  return (
    <div className="app-root">
      <header className="app-header">
        <Link to="/">Commuter</Link>
        <Link to="/admin">Admin</Link>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<CommuterHome/>} />
          <Route path="/map" element={<MapScreen/>} />
          <Route path="/tickets" element={<Tickets/>} />
          <Route path="/admin" element={<AdminDashboard/>} />
        </Routes>
      </main>
    </div>
  )
}
