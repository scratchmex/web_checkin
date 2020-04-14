import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route
} from "react-router-dom";

import AdminLanding from './AdminLanding';
import AdminUsersList from './AdminUsersList';
import AdminEventsList from './AdminEventsList';
import AdminAdminsList from './AdminAdminsList';
import AdminCreateAdmin from './AdminCreateAdmin';
import AdminValidateCheckin from './AdminValidateCheckin';

export default function AdminView() {
    return (
        <Router>
            <Switch>
                <Route path="/admin/validate-checkin">
                    <AdminValidateCheckin />
                </Route>
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
                    <AdminLanding />
                </Route>
            </Switch>
        </Router>
    );
}