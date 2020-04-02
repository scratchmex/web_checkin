import React from 'react';
import {Card,
        Button,
        Form
} from 'react-bootstrap';

import apiBaseUrl from './apiBaseUrl';
import getCookie from './getCookie';

export default function AdminCreateAdmin() {
    return (
        <Card className="mx-auto card-admin" variant="primary" style={{ width: '18rem' }}>
        <Card.Body>
            <Card.Title>Crear Admin</Card.Title>
            <Form>
                <Form.Group>
                    <Form.Label>Nombre</Form.Label>
                    <Form.Control id="name" type="text" placeholder="Nombre"></Form.Control> 
                    <br></br>
                    <Form.Label>Username</Form.Label>
                    <Form.Control id="username" type="text" placeholder="Username"></Form.Control>
                    <br></br>
                    <Form.Label>Password</Form.Label>
                    <Form.Control id="pass" type="password" placeholder="Password"></Form.Control>
                    <br></br>
                    <Button className="btn-block" onClick={postAdmin}>Crear Admin</Button>
                </Form.Group>
            </Form>
        </Card.Body>
        </Card>
    );
}

function postAdmin() {
    const data = {
        name: document.getElementById('name').value,
        username: document.getElementById('username').value,
        password: document.getElementById('pass').value
    }
    // console.log(data);
    const url = apiBaseUrl + "/admins";
    const params = {
        method: 'post',
        headers: {
            'Authorization': 'Bearer ' + getCookie('access_token'),
            'Content-Type': 'text/plain'
        },
        body: JSON.stringify(data)
    };
    fetch(url, params)
        .then(resp => resp.json())
        .then(json => console.log(json));
}