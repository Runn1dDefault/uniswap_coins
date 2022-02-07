import {Routes, Route, BrowserRouter, Navigate, Outlet} from "react-router-dom";
import React from 'react';
import DashboardContent from './pages/Dashboard';
import Login from './pages/SignIn';


function PrivateOutlet() {
  const auth = localStorage.getItem("jwtToken");
  return auth ? <Outlet /> : <Navigate to="/login" />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<PrivateOutlet />}>
          <Route path="" element={<DashboardContent/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
