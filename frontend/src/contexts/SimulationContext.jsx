import { createContext, useContext, useState, useEffect } from 'react'
import api from '../api/client'

const SimulationContext = createContext()

export function SimulationProvider({ children }) {
  const [scenario, setScenario] = useState('NORMAL')
  const [scenarioData, setScenarioData] = useState({})
  const [scenarioList, setScenarioList] = useState([])

  useEffect(() => {
    api.get('/simulate/scenarios').then(r => setScenarioList(r.data)).catch(() => {})
    // Preload all scenario data
    ;['TRUCK_STRIKE', 'HEATWAVE', 'EARLY_MONSOON'].forEach(id => {
      api.get(`/simulate/scenario/${id}/data`).then(r => {
        setScenarioData(prev => ({ ...prev, [id]: r.data }))
      }).catch(() => {})
    })
  }, [])

  // Reset on idle (5 min)
  useEffect(() => {
    let timer
    const reset = () => {
      clearTimeout(timer)
      timer = setTimeout(() => setScenario('NORMAL'), 5 * 60 * 1000)
    }
    window.addEventListener('mousemove', reset)
    window.addEventListener('keydown', reset)
    reset()
    return () => {
      clearTimeout(timer)
      window.removeEventListener('mousemove', reset)
      window.removeEventListener('keydown', reset)
    }
  }, [])

  const currentData = scenario === 'NORMAL' ? null : scenarioData[scenario]

  return (
    <SimulationContext.Provider value={{ scenario, setScenario, currentData, scenarioList }}>
      {children}
    </SimulationContext.Provider>
  )
}

export const useSimulation = () => useContext(SimulationContext)
