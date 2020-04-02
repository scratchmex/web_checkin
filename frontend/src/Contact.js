import React from 'react';
import Container from 'react-bootstrap/Container';

function Contact() {
    return (
      <Container className="content">
        <h1>Ponte en Contacto</h1>
        <p>
          Si tienes alguna duda, comentario y/o sugerencia sobre la 
          web-app, no dudes en escribirnos a: 
        </p>
        <a href="mailto://ivan.golzalez@cimat.mx"><h2 className="contact-email">ivan.gonzalez@cimat.mx</h2></a>
        <a href="mailto://juan.bolanos@cimat.mx"><h2 className="contact-email">juan.bolanos@cimat.mx</h2></a>
      </Container>
    );
}

export default Contact;