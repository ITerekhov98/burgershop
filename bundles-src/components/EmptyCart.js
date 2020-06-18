import React, {Component} from 'react';

const EmptyCart = (props) =>{
  return(
    <div className="container-fluid">
      <center>
        <div className="empty-cart"></div>
        <h2>You cart is empty!</h2>
      </center>
    </div>
  )
};

export default EmptyCart;
