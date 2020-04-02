import React from 'react';
import {Container,
        Image,
        Button
} from 'react-bootstrap';
import {GoCalendar, GoLocation} from 'react-icons/go';
import ProfilePicture from './assets/seminario_junior.png';


function Home() {
    return (
      <Container fluid className='pp'>
        <Image src={ProfilePicture} fluid roundedCircle/>
        <h1>Seminario Jr.</h1>
        <p>  
          <GoCalendar/> Todos los miércoles 15:00hrs.<br></br>
          <GoLocation/> Salón de seminarios DEMAT
        </p>
        <Button href="/checkin" size="lg" variant="secondary">Hacer Checkin</Button>
      </Container>
    );
}

export default Home;