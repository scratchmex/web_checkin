import React from 'react';
import {Form,
        Card,
        Button
} from 'react-bootstrap';

function Checkin() {
    return (
        <Card className="mx-auto card-admin" variant="primary" style={{ width: '18rem' }}>
        <Card.Body>
        <Card.Title>Hacer un Checkin</Card.Title>
        <Form>
            <Form.Group>
            <Form.Label>Nombre</Form.Label>
            <Form.Control id="nameInput" size="lg" type="text" placeholder="Escribe tu Nombre" />
            <br></br>
            <Form.Label>NUA</Form.Label>
            <Form.Control id="nuaInput" size="lg" type="number" placeholder="Escribe tu NUA" />
            <br></br>
            <Form.Label>ID de evento</Form.Label>
            <Form.Control id="eventIdInput" size="lg" type="text" placeholder="ID" />
            </Form.Group>
            <Button className="btn-block" onClick={doCheckin} variant="primary" >
            Enviar
            </Button>
        </Form>
        </Card.Body>
        </Card>
    );
}

function doCheckin() {
    let postBody = {};
    postBody.user = {};
    postBody.user.name = document.getElementById('nameInput').value;
    postBody.user.id = document.getElementById('nuaInput').value;
    postBody.event_id = document.getElementById('eventIdInput').value;
    fetch("http://localhost:8000/token/checkins", {
        method: 'POST',
        headers: {
        'Content-Type': 'text/plain'
        },
        body: JSON.stringify(postBody)
    }).then(resp => resp.json())
    .then(json => console.log(json))
    .catch(err => console.log(err));
}

export default Checkin;