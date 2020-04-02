import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route
  } from "react-router-dom";

import AdminUsersList from './AdminUsersList';
import AdminEventsList from './AdminEventsList';
import AdminAdminsList from './AdminAdminsList';
import AdminCreateAdmin from './AdminCreateAdmin';

export default function AdminView() {
    return (
        <Router>
            <Switch>
                <Route path="/admin/users">
                    <AdminUsersList />
                </Route>
                <Route path="/admin/events">
                    <AdminEventsList />
                </Route>
                <Route path="/admin/admins">
                    <AdminAdminsList />
                </Route>
                <Route path="/admin/create_admin">
                    <AdminCreateAdmin />
                </Route>
                <Route path="/admin">
                    <h1>Admin, lel!</h1>
                </Route>
            </Switch>
        </Router>
    );
}