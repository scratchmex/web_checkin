import React, {useState} from 'react';
import {Card,
        Button,
        InputGroup,
        FormControl,
        Modal,
        Form,
} from 'react-bootstrap';
import QrReader from 'react-qr-reader';
import {AiOutlineQrcode} from 'react-icons/ai';

import apiBaseUrl from './apiBaseUrl';

export default function AdminValidateCheckin() {
    let [show, setShow] = useState(false);
    
    function handleClose() {
        setShow(false);
    }
    
    function openScanner() {
        setShow(true);
    }

    function handleError(err) {
        console.log(err);
    }

    async function handleScan(data) {
        console.log(data);
        if(data !== null) {
            document.getElementById('token-input').value = data;

            const url = apiBaseUrl + '/token';
            const params = {
                method: 'get',
                headers: {
                    'Authorization': `Bearer ${data}`
                }
            };
            
            const resp = await fetch(url, params);
            const jsonResp = await resp.json();
            console.log(jsonResp);
            document.getElementById('usr-id').value = jsonResp.iss.split(':')[1];
            document.getElementById('usr-name').value = jsonResp.data.name;
            document.getElementById('event-id').value = jsonResp.sub.split(':')[1];

            setShow(false);
        }
    }

    return (
        <>
        <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Escanear Código QR</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <QrReader
            delay={300}
            onError={handleError}
            onScan={handleScan}
            style={{ width: '100%' }}
            /> 
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={handleClose}>
            Cerrar
          </Button>
        </Modal.Footer>
        </Modal>
        
        <Card className="mx-auto card-admin" variant="primary" style={{ width: '18rem' }}>
            <Card.Body>
                <Card.Title>Ingresar Datos de Checkin</Card.Title>
                <Form>
                <Form.Label>Token de Checkin</Form.Label>
                <InputGroup className="mb-3">
                    <InputGroup.Prepend>
                        <Button variant="outline-secondary" onClick={openScanner}><AiOutlineQrcode/></Button>
                    </InputGroup.Prepend>
                    <FormControl aria-describedby="basic-addon1" placeholder="Token" id="token-input"/>
                </InputGroup>
                <Form.Label>ID de Usuario</Form.Label>
                <FormControl placeholder="ID de Usuario" id="usr-id" readOnly/>
                <br></br>
                <Form.Label>Nombre de Usuario</Form.Label>
                <FormControl placeholder="Nombre de Usuario" id="usr-name" readOnly/>
                <br></br>
                <Form.Label>ID de Evento</Form.Label>
                <FormControl placeholder="ID de Evento" id="event-id" readOnly/>
                <br></br>
                <Button className="btn-block" >Registrar</Button>
                </Form>
            </Card.Body>
        </Card>
        </>
    );
}