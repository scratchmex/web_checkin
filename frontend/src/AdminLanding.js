import React from 'react';

export default function AdminLanding () {
    return (
        <p>
            Bienvenido al panel de administrador. Aquí podrás
            <a href='/admin/validate-checkin'> validar checkins</a>, así
            como editar eventos, usuarios y admins en el base
            de datos.
        </p>
    )
}