import * as React from 'react';
import './App.css';
// import Box from '@mui/material/Box';
// import Bar from './components/Assets/Bar';
import { Routes, Route } from 'react-router-dom';

import Dashboard from './components/Dashboard';
import Measures from './components/Measures';
import Profile from './components/Profile';
import Reminder from './components/Reminder';
import Layout from './components/Layout';

function App() {
    return (
        <div>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/measures" element={<Measures />} />
                    <Route path="/profile" element={<Profile />} />
                    <Route path="/reminder" element={<Reminder />} />
                </Route>
            </Routes>
            {/*<Box sx={{ display: 'flex' }}>
                <Box component="main" sx={{ flexGrow: 1, p: 2 }}>
                    <Outlet />
                    
                </Box>
    </Box>*/}
        </div>
    );
}

export default App;
