import React from 'react';
import {Navbar,
        NavDropdown,
        Nav,
        Button
} from 'react-bootstrap';
import {MdPerson,
        MdPersonAdd
} from 'react-icons/md';
import {GiSwordsPower} from 'react-icons/gi';
import {FaCalendarAlt,
        FaCalendarPlus
} from 'react-icons/fa';

import './assets/main.css';

export default function AdminNavbar() {
    return (
        <Navbar className="navbar-custom" variant="dark" expand="lg">
        <Navbar.Brand href="/admin">Administrador - Web Checkin</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
            <NavDropdown title="Usuarios" id="users-dropdown">
                <NavDropdown.Item href="/admin/users"><MdPerson/> Ver Usuarios</NavDropdown.Item>
                <NavDropdown.Item href="/admin/create_user"><MdPersonAdd /> Crear Usuario</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="Eventos" id="events-dropdown">
                <NavDropdown.Item href="/admin/events"><FaCalendarAlt/> Ver Eventos</NavDropdown.Item>
                <NavDropdown.Item href="/admin/create_event"><FaCalendarPlus/> Crear Evento</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="Admins" id="admins-dropdown">
                <NavDropdown.Item href="/admin/admins"><GiSwordsPower/>  Ver Admins</NavDropdown.Item>
                <NavDropdown.Item href="/admin/create_admin"><GiSwordsPower/>+ Crear Admin</NavDropdown.Item>
            </NavDropdown>
            </Nav>
            <Button variant="outline-primary" onClick={logout}>Salir</Button>
        </Navbar.Collapse>
        </Navbar>
    );
}

function logout() {
    window.location.href = "/";
}