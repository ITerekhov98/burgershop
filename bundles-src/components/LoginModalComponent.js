import React, { Component } from 'react'
import Cookies from 'universal-cookie';
import {Redirect} from 'react-router-dom'
import { withRouter } from 'react-router'
import { Button } from 'react-bootstrap';
import {Modal} from 'react-bootstrap';


class LoginModalComponent extends Component{
  cookies = new Cookies();
  state = {
    auth_url: 'api-basictoken-auth/',
    jwt_url: 'api-jwttoken-auth/',
    username: "" ,
    password: ""
  }

  saveUsername = (event) => {
    const {target : {value}} = event;
    this.setState({
      username : value
    })
  }

  savePassword = (event) => {
    const {target : {value}} = event;
    this.setState({
      password : value
    })
  }

  submit = (e) => {
    e.preventDefault();
    this.login(this.state)
  }

  async login({username, password}){
    var formData  = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    try {
      let response = await fetch(this.state.jwt_url, {
        method: 'post',
        body: formData,
      });
      let myJson = await response.json();
      if ('token' in myJson){
        this.cookies.set('userJwtToken', myJson, { path: '/',expires: new Date(Date.now() + 2592000)} );
        this.cookies.set('username',formData.get('username'), {path : '/', expires: new Date(Date.now() + 2592000)})
        this.props.toggleisAuthenticated();
        this.props.handleLoginModalClose();
      }
      else{
        alert("Invalid Credentials");
      }
    } catch(e){
      console.log("Error occured in Login");
    };
  }

  render(){
    return (

      <Modal show={this.props.loginModalActive} onHide={this.props.handleLoginModalClose}>
        <Modal.Header closeButton>
          <h2>
            <center><Modal.Title>Login</Modal.Title></center>
          </h2>
        </Modal.Header>
        <Modal.Body>
          <div className="form-group container-fluid">
            <label htmlFor="username">Username:</label>
            <input onChange={this.saveUsername} id="username" type="text" className="form-control" placeholder="Enter username"/><br/>
            <label htmlFor="password">Password:</label>
            <input onChange={this.savePassword} type="password" className="form-control" placeholder="Enter Password"/><br/>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={this.submit} className="btn btn-primary" value="Login">Login</Button>
          <Button onClick={this.props.handleLoginModalClose}>Close</Button>
        </Modal.Footer>
      </Modal>
    )
  }
}

export default LoginModalComponent;
