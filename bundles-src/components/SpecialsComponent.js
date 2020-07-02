import React, {Component} from 'react';
import Product from './Product';
import LoadingProducts from './loaders/LoadingProducts';
import NoResults from "./NoResults";
import {TransitionGroup, CSSTransition} from 'react-transition-group';

class SpecialsComponent extends Component{
  render(){
    let productsData;
    let term = this.props.term.toLowerCase();

    productsData = this.props.productsList.filter(x => {
      return x.name.toLowerCase().includes(term) || !term;
    }).filter(x => {
      return x.special_status == true;
    }).map(product =>{
      return (
        <CSSTransition
          classNames="fadeIn"
          className="products"
          timeout={{ enter:500, exit: 300 }}
          component="div"
          key={product.id}
        >
          <Product
            product={product}
            addToCart={this.props.addToCart}
            productQuantity={this.props.productQuantity}
            updateQuantity={this.props.updateQuantity}
            openModal={this.props.openModal}
          />
        </CSSTransition>
      )
    });

    // Empty and Loading States
    let view;
    if(productsData.length <= 0 && !term){
      view = <LoadingProducts />
    } else if(productsData.length <= 0 && term){
      view = '';
    } else{
      view = (
        <TransitionGroup className="products">
          {productsData}
        </TransitionGroup>
      )
    }
    return (
      <div className="products-wrapper">
        {view}
      </div>
    )
  }
}

export default SpecialsComponent;
