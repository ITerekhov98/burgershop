import React, {Component} from 'react';
import Counter from './Counter';

class Product extends Component{
  constructor(props){
    super(props);
    this.state = {
      isAdded: false
    }
  }

  addToCart(quantity){
    let selectedProduct = {
      ...this.props.product,
      quantity: quantity,
    };

    this.props.addToCart(selectedProduct);

    this.setState({
      isAdded: true
    });
    this.props.updateQuantity(0);

    setTimeout(() => {
      this.setState({
        isAdded: false,
      });
    }, 1500);
  }

  quickView(){
    this.props.openModal(this.props.product);
  }

  render(){
    let image = this.props.product.image;
    let name = this.props.product.name;
    let price = this.props.product.price;
    let id = this.props.product.id;
    let quantity = this.props.productQuantity;
    return (
      <div className="product">
        <div className="product-image">
          <img src={image} alt={name} onClick={this.quickView.bind(this)}/>
        </div>
        <h4 className="product-name">{name}</h4>
        <p className="product-price currency">{price}</p>
        <Counter productQuantity={quantity} updateQuantity={this.props.updateQuantity} resetQuantity={this.resetQuantity}/>
        <div className="product-action">
          <button className={!this.state.isAdded ? "btn btn-primary" : "btn btn-success"} type="button" onClick={this.addToCart.bind(this, quantity)}>{!this.state.isAdded ? "В корзину" : "✔ Добавлено"}</button>
        </div>
      </div>
    )
  }
}

export default Product;
