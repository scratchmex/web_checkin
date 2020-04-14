import React, {useState} from 'react';
import {Form,
        Card,
        Button,
        Alert
} from 'react-bootstrap';
import {MdErrorOutline} from 'react-icons/md';

import cookieTokenCheck from './cookieTokenCheck';
import apiBaseUrl from './apiBaseUrl';

export default function Login() {
  let [check, setCheck] = useState(false);

  async function checkCookie() {
    setCheck(await cookieTokenCheck());
    if(check === true) {
      window.location.href = "/admin";
    }
  }
  
  checkCookie();

  let [alertShow, setAlertShow] = useState(false);
  let [usrShow, setUsrShow] = useState(false);
  let [passShow, setPassShow] = useState(false);
  
  async function sendLogin() {
    let usrVal = document.getElementById('user').value;
    let usrPass = document.getElementById('pass').value;
    let cancel = false;
  
    if(usrVal === '') {
      cancel = true;
      setUsrShow(true);
    } else {
      setUsrShow(false);
    }
    if(usrPass === '') {
      cancel = true;
      setPassShow(true);
    } else {
      setPassShow(false);
    }
    if(cancel) {
      return
    }
  
    let details = {
      'username': usrVal,
      'password': usrPass
    };
    
    let formBody = [];
    for (let property in details) {
      let encodedKey = encodeURIComponent(property);
      let encodedValue = encodeURIComponent(details[property]);
      formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");
    const url = apiBaseUrl + '/token/auth';
    const params = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formBody
    };
  
    const resp = await fetch(url, params)
    if(resp.ok) {
      const jsonBody = await resp.json()
      let d = new Date();
      d.setTime(d.getTime() + (jsonBody.expires_in*1000));
      document.cookie = `access_token=${jsonBody.access_token}; expires=${d.toUTCString()}; `;
      window.location.href = "/admin";
    } else {
      setAlertShow(true);
    }
  }

  return (
    <Card className="mx-auto card-admin" variant="primary" style={{ width: '18rem' }}>
    <Card.Body>
      <Card.Title>Iniciar Sesión</Card.Title>
      <Form >
        <Form.Group>
        <Form.Label>Nombre de Usuario</Form.Label>
        <Alert variant="warning" show={usrShow}>Campo requerido</Alert>
        <Form.Control id="user" size="lg" type="text" placeholder="Escribe tu Nombre de Usuario" />
        <br></br>
        <Form.Label>Contraseña</Form.Label>
        <Alert variant="warning" show={passShow}>Campo requerido</Alert>
        <Form.Control id="pass" size="lg" type="password" placeholder="Escribe tu Contraseña" />
        </Form.Group>
        <Alert show={alertShow} variant="danger">
          <MdErrorOutline/> Ha habido un error de autenticación :c
        </Alert>
        <Button className="btn-block" onClick={sendLogin}>Iniciar Sesión</Button>
      </Form>
    </Card.Body>
    </Card>
  );
}