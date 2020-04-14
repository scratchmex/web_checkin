import React, {useState} from 'react';
import {Form,
        Card,
        Button,
        Modal
} from 'react-bootstrap';
import qrcode from 'qrcode-generator';
import apiBaseUrl from './apiBaseUrl';

function Checkin() {
    let [qrModalShow, setQrModalShow] = useState(false);
    let [qrData, setQrData] = useState('');

    const handleClose = () => setQrModalShow(false);
    
    function generateQR() {
        const typeNumber = 0;
        const errorCorrectionLevel = 'L'
        let qr = qrcode(typeNumber, errorCorrectionLevel);
        qr.addData(qrData);
        qr.make();
        document.getElementById('qr-div').innerHTML = qr.createSvgTag({
            cellSize: 4,
            scalable: true
        });
        console.log(qrData);
    }
    
    async function doCheckin() {
        const url = apiBaseUrl + '/token/checkins';
        let postBody = {};
        postBody.user = {};
        postBody.user.name = document.getElementById('nameInput').value;
        postBody.user.id = document.getElementById('nuaInput').value;
        postBody.event_id = document.getElementById('eventIdInput').value;
        const params = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(postBody)
        }
        const resp = await fetch(url, params);
        const jsonResp = await resp.json();
        if(resp.ok) {
            setQrModalShow(true);
            setQrData(jsonResp.access_token);
            generateQR();
        }
    }

    return (
        <>
        <Modal show={qrModalShow} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Completar Checkin</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                Para completar el Checkin, muestra el siguiente código QR al encargado
                <div id='qr-div'></div>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="primary" onClick={handleClose}>
                    Terminar
                </Button>
                <Button variant="danger" onClick={handleClose}>
                    Cancelar
                </Button>
            </Modal.Footer>
        </Modal>

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
        </Form>
        <Button className="btn-block" onClick={doCheckin} variant="primary" >
        Enviar
        </Button>
        </Card.Body>
        </Card>
        </>
    );
}

export default Checkin;