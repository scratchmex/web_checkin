import React from 'react';
import {Form,
        Card,
        Button
} from 'react-bootstrap';

import getCookie from './getCookie'

function Login() {
  let cookie = getCookie('access_token');
  if(cookie !== "") {
    window.location.href="/admin";
  }
  return (
    <Card className="mx-auto card-admin" variant="primary" style={{ width: '18rem' }}>
    <Card.Body>
      <Card.Title>Iniciar Sesión</Card.Title>
      <Form >
        <Form.Group>
        <Form.Label>Nombre de Usuario</Form.Label>
        <Form.Control id="user" size="lg" type="text" placeholder="Escribe tu Nombre de Usuario" />
        <br></br>
        <Form.Label>Contraseña</Form.Label>
        <Form.Control id="pass" size="lg" type="password" placeholder="Escribe tu Contraseña" />
        </Form.Group>
        <Button className="btn-block" onClick={sendLogin}>Iniciar Sesión</Button>
      </Form>
    </Card.Body>
    </Card>
  );
}

function sendLogin() {
  let details = {
      'username': document.getElementById('user').value,
      'password': document.getElementById('pass').value,
  };
  
  let formBody = [];
  for (let property in details) {
    let encodedKey = encodeURIComponent(property);
    let encodedValue = encodeURIComponent(details[property]);
    formBody.push(encodedKey + "=" + encodedValue);
  }
  formBody = formBody.join("&");
  console.log("The sent urlenc is: ", formBody);
  
  fetch('http://localhost:8000/token/auth', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: formBody
  }).then(resp => {
    if(resp.ok) {
      return resp.json()
    } else {
      return {err: true};
    }
  })
  .then(json => {
    console.log(json);
    if(json.err === true){
      console.log("There's been an error!");
    } else {
      document.cookie = `access_token=${json.access_token}`;
      window.location.href = "/admin";
    }
  });
}

export default Login;