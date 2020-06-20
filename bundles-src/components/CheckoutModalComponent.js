import React,{Component} from 'react';
import {Modal} from 'react-bootstrap';
import {Button} from 'react-bootstrap';

class CheckoutModal extends Component{
  state = {
    firstname:"",
    lastname:"",
    phonenumber:"",
    address:""
  }

  saveFirstname = event => {
    const {target : {value}}  = event;
    this.setState({
      firstname : value
    });
  }

  saveLastname = event => {
    const {target : {value}}  = event;
    this.setState({
      lastname : value
    });
  }

  savePhonenumber = (event) => {
    const {target : {value}} = event;
    this.setState({
      phonenumber : value
    });
  }

  saveAddress = event => {
    const {target : {value}} = event;
    this.setState({
      address : value
    });
  }

  submit = e => {
    e.preventDefault();
    this.props.handleCheckout(this.state);
  }

  render(){
    return (
      <Modal show={this.props.checkoutModalActive} onHide={this.props.handleCheckoutModalClose}>
        <Modal.Header closeButton>
          <h2>
            <center>
              <Modal.Title>Оформление заказа</Modal.Title>
            </center>
          </h2>
        </Modal.Header>
        <Modal.Body>
          <div className="form-group container-fluid">
            <label htmlFor="firstname">Имя:</label>
            <input onChange={this.saveFirstname} required id="firstname" type="text" className="form-control"/><br/>
            <label htmlFor="lastname">Фамилия:</label>
            <input onChange={this.saveLastname} required id="lastname" type="text" className="form-control"/><br/>
            <label htmlFor="phonenumber">Телефон:</label>
            <input onChange={this.savePhonenumber} required id="phonenumber" maxLength="10" type="text" className="form-control" placeholder="+7 901 ..."/><br/>
            <label htmlFor="address">Адрес доставки:</label>
            <input onChange={this.saveAddress} required id="address" type="text" maxLength="256" className="form-control" placeholder="Город, улица, дом"/><br/>
          </div>
        </Modal.Body>
        <Modal.Footer>
           <Button id="order-submit-btn" onClick={(events)=>{
               document.getElementById("order-submit-btn").setAttribute("disabled","disabled");
               this.submit(events);
               document.getElementById("order-submit-btn").removeAttribute("disabled");
            }} className="btn btn-primary">
              Отправить
            </Button>
          <Button onClick={this.props.handleCheckoutModalClose}>Закрыть</Button>
        </Modal.Footer>
      </Modal>
    );
  }
}

export default CheckoutModal;
