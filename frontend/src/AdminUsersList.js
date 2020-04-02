import React from 'react';
import Table from 'react-bootstrap/Table';

import apiBaseUrl from './apiBaseUrl';

export default class AdminUsersList extends React.Component {
    constructor() {
        super();
        this.state = {
            usersList: []
        }
    }

    componentDidMount() {
        let url = apiBaseUrl + "/users";
        fetch(url)
            .then(resp => resp.json())
            .then(json => {
                this.setState({usersList: json});
            });
    }

    render() {
        let tableRows = this.state.usersList.map(user => {
            return (
                <tr key={user.id} >
                    <td>{user.id}</td>
                    <td>{user.name}</td>
                </tr>
            );
        });
        return (
            <Table responsive striped hover size="sm">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Name</th>
                </tr>
            </thead>
            <tbody>
                {tableRows}
            </tbody>
            </Table>
        )
    }
}