import React from 'react';

import getCookie from './getCookie';
import AdminView from './AdminView';

export default function Admin() {
    if(getCookie('access_token') === "") {
        window.location.href = "/login"; 
    }
    return <AdminView />;
}