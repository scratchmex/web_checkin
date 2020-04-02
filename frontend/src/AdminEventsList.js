import React from 'react';
import Table from 'react-bootstrap/Table';

import apiBaseUrl from './apiBaseUrl';

export default class AdminEventsList extends React.Component {
    constructor() {
        super();
        this.state = {
            eventsList: []
        }
    }

    componentDidMount() {
        let url = apiBaseUrl + "/events";
        fetch(url)
            .then(resp => resp.json())
            .then(json => {
                this.setState({eventsList: json});
            });
    }

    render() {
        let tableRows = this.state.eventsList.map(event => {
            return (
                <tr key={event.id} >
                    <td>{event.id}</td>
                    <td>{event.title}</td>
                    <td>{event.date}</td>
                </tr>
            );
        });
        return (
            <Table responsive striped hover size="sm">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Título</th>
                    <th>Fecha</th>
                </tr>
            </thead>
            <tbody>
                {tableRows}
            </tbody>
            </Table>
        )
    }
}