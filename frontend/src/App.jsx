import { Routes, Route, Navigate } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import AdminLayout from './layouts/AdminLayout'
import DealerLayout from './layouts/DealerLayout'
import CustomerLayout from './layouts/CustomerLayout'
import AdminDashboard from './pages/admin/Dashboard'
import DemandForecast from './pages/admin/DemandForecast'
import DeadStock from './pages/admin/DeadStock'
import Transfers from './pages/admin/Transfers'
import DealerPerformance from './pages/admin/DealerPerformance'
import DealerDashboard from './pages/dealer/Dashboard'
import SmartOrders from './pages/dealer/SmartOrders'
import OrderTracking from './pages/dealer/OrderTracking'
import ShadeCatalog from './pages/customer/ShadeCatalog'
import ShadeDetail from './pages/customer/ShadeDetail'
import FindNearMe from './pages/customer/FindNearMe'
import SnapAndFind from './pages/customer/SnapAndFind'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/admin" element={<AdminLayout />}>
        <Route index element={<AdminDashboard />} />
        <Route path="forecast" element={<DemandForecast />} />
        <Route path="dead-stock" element={<DeadStock />} />
        <Route path="transfers" element={<Transfers />} />
        <Route path="dealers" element={<DealerPerformance />} />
      </Route>
      <Route path="/dealer" element={<DealerLayout />}>
        <Route index element={<DealerDashboard />} />
        <Route path="smart-orders" element={<SmartOrders />} />
        <Route path="orders" element={<OrderTracking />} />
      </Route>
      <Route path="/customer" element={<CustomerLayout />}>
        <Route index element={<ShadeCatalog />} />
        <Route path="shade/:shadeId" element={<ShadeDetail />} />
        <Route path="find-near-me" element={<FindNearMe />} />
        <Route path="snap-find" element={<SnapAndFind />} />
      </Route>
    </Routes>
  )
}
