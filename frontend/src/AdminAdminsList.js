import React from 'react';
import Table from 'react-bootstrap/Table';

import apiBaseUrl from './apiBaseUrl';

export default class AdminAdminsList extends React.Component {
    constructor() {
        super();
        this.state = {
            adminsList: []
        }
    }

    componentDidMount() {
        let url = apiBaseUrl + "/admins";
        fetch(url)
            .then(resp => resp.json())
            .then(json => {
                this.setState({adminsList: json});
            });
    }

    render() {
        let tableRows = this.state.adminsList.map(admin => {
            return (
                <tr key={admin.id} >
                    <td>{admin.id}</td>
                    <td>{admin.name}</td>
                    <td>{admin.username}</td>
                </tr>
            );
        });
        return (
            <Table responsive striped hover size="sm">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Username</th>
                </tr>
            </thead>
            <tbody>
                {tableRows}
            </tbody>
            </Table>
        )
    }
}