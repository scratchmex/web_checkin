import React from 'react';
import {Navbar, Nav, Button} from 'react-bootstrap' 

function MainNavbar() {
    return (
        <Navbar className="navbar-custom" variant="dark" expand="lg">
        <Navbar.Brand href="/">Web-Checkin</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav" variant="dark">
            <Nav className="mr-auto">
                <Nav.Link href="/checkin">Registro</Nav.Link>
                <Nav.Link href="/info">Más Información</Nav.Link>
                <Nav.Link href="/contact">Contáctanos</Nav.Link>
            </Nav>
            <Nav>
                <Nav.Item>
                    <Button href="/login" variant="outline-danger">Administrador</Button>
                </Nav.Item>
            </Nav>
        </Navbar.Collapse>
        </Navbar>
    );
}

export default MainNavbar;