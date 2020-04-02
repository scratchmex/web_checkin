import React from "react";
import 'bootstrap/dist/css/bootstrap.css';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

import './assets/main.css';

import MainNavbar from './MainNavbar';
import Home from './Home';
import Checkin from './Checkin';
import Contact from './Contact';
import Info from './Info';
import Login from './Login';
import Admin from './Admin';
import AdminNavbar from './AdminNavbar';

export default function App() {
  return (
    <Router>
      <div>
        <Switch>
          <Route path="/info">
            <MainNavbar />
            <Info />
          </Route>
          <Route path="/checkin">
            <MainNavbar />
            <Checkin />
          </Route>
          <Route path="/contact">
            <MainNavbar />
            <Contact />
          </Route>
          <Route path="/login">
            <MainNavbar />
            <Login />
          </Route>
          <Route path="/admin">
            <AdminNavbar />
            <Admin />
          </Route>
          <Route path="/">
            <MainNavbar />
            <Home />
          </Route>
          <Route path="/home">
            <MainNavbar />
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}