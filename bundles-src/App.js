import React, { Component } from 'react';
import './css/App.css';
import NavBarComponent from './components/NavBarComponent';
import CartModalComponent from './components/CartModalComponent';
import BannerComponent from './components/BannerComponent';
import Products from './components/Products';
import QuickView from './components/QuickView';
import FooterComponent from './components/FooterComponent';
import SpecialsComponent from './components/SpecialsComponent';
import CheckoutModal from './components/CheckoutModalComponent';

class App extends Component {

  constructor(props){
    super();
    this.state = {
      products: [],
      cart: [],
      totalItems: 0,  // FIXME заменить на вычисляемые свойства
      totalAmount: 0,  // FIXME заменить на вычисляемые свойства
      term: '',
      categoryId: null,
      quickViewProduct: {},
      showCart: false,
      quickViewModalActive: false,
      quantity: 1,  // FIXME что здесь хранится?
      banners: [],
      checkoutModalActive: false,
    };
    this.handleSearch = this.handleSearch.bind(this);
    this.handleCategory = this.handleCategory.bind(this);
    this.handleAddToCart = this.handleAddToCart.bind(this);
    this.sumTotalItems = this.sumTotalItems.bind(this);
    this.sumTotalAmount = this.sumTotalAmount.bind(this);
    this.checkProduct = this.checkProduct.bind(this);
    this.handleRemoveProduct = this.handleRemoveProduct.bind(this);
    this.handleCartShow = this.handleCartShow.bind(this);
    this.handleCartClose = this.handleCartClose.bind(this);
    this.handleQuickViewModalClose = this.handleQuickViewModalClose.bind(this);
    this.handleQuickViewModalShow = this.handleQuickViewModalShow.bind(this);
    this.updateQuantity=this.updateQuantity.bind(this);
    this.handleCheckout=this.handleCheckout.bind(this);
    this.handleCheckoutModalShow=this.handleCheckoutModalShow.bind(this);
    this.handleCheckoutModalClose=this.handleCheckoutModalClose.bind(this);
  }

  handleCheckoutModalShow(){
    this.setState({checkoutModalActive: true});
  }

  handleCheckoutModalClose(){
    this.setState({checkoutModalActive: false});
  }

  async handleCheckout({firstname, lastname, phonenumber, address}){
    const url = "api/order/";
    let data = {
      'products': this.state.cart,
      firstname,
      lastname,
      phonenumber,
      address
    };

    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
      let response = await fetch(url, {
        method: 'post',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok){
        alert('Ошибка при оформлении заказа. Попробуйте ещё раз или свяжитесь с нами по телефону.');
        return;
      }
      let responseData = await response.json();

      this.setState({
        totalAmount: 0,
        totalItems: 0,
        cart: []
      });

      alert("Заказ оформлен. Вам перезвонят в течение 10 минут.");

      this.handleCartClose();
    } catch(error){
      alert('Ошибка при оформлении заказа. Попробуйте ещё раз или свяжитесь с нами по телефону.');
      throw error;
    };
  }


  updateToken(NewToken){

    this.setState({
      token:NewToken
    })
  }


  async getProducts(){
    const url = "/api/products/";

    let response = await fetch(url, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok){
      return;
    }

    let data = await response.json();
    this.setState({
      products : data
    });
  }

  async getBanners(){
    const url = "/api/banners/";

    let response = await fetch(url, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok){
      return;
    }

    let data = await response.json();
    this.setState({
      banners : data
    });
  }

  componentWillMount(){
    this.getProducts();
    this.getBanners();
  }


  // Search by Keyword
  handleSearch(event){
    this.setState({term: event.target.value});
  }
  // Filter by Category
  handleCategory(event){
    this.setState({categoryId: event.target.value});
  }

  handleCartClose() {
    this.setState({ showCart: false });
  }

  handleCartShow() {
    this.setState({ showCart: true });
  }

  updateQuantity(qty){
    this.setState({
        quantity: qty
    })
  }

  // Add to Cart
  handleAddToCart(selectedProducts){

    let cartItems = this.state.cart;
    let productID = selectedProducts.id;
    let productQty = selectedProducts.quantity;

    if (this.checkProduct(productID)){
      let index = cartItems.findIndex((x => x.id == productID));
      cartItems[index].quantity = parseFloat(cartItems[index].quantity) + parseFloat(productQty);
      this.setState({
        cart: cartItems
      })
    }
    else {
      cartItems.push(selectedProducts);
    }

    this.setState({
      cart : cartItems,
    });


    setTimeout(() => {
      // FIXME протестировать этот код, он работает?
      this.setState({
        quantity: 1
      });
    }, 1000);

    this.sumTotalItems(this.state.cart);
    this.sumTotalAmount(this.state.cart);

  }


  handleRemoveProduct(id, e){
    let cart = this.state.cart;
    let index = cart.findIndex((x => x.id == id));
    cart.splice(index, 1);
    this.setState({
      cart: cart
    })
    this.sumTotalItems(this.state.cart);
    this.sumTotalAmount(this.state.cart);
    e.preventDefault();
  }


  checkProduct(productID){
    let cart = this.state.cart;
    return cart.some(function(item) {
      return item.id === productID;
    });
  }

  sumTotalItems(){
        let total = 0;
        let cart = this.state.cart;
    total = cart.length;
    this.setState({
      totalItems: total
    })
  }


  sumTotalAmount(){
        let total = 0;
        let cart = this.state.cart;
        for (var i=0; i<cart.length; i++) {
            total += cart[i].price * parseFloat(cart[i].quantity);
        }
    this.setState({
      totalAmount: total
    })
  }

  // Open Modal
  handleQuickViewModalShow(product){
    this.setState({
      quickViewProduct: product,
      quickViewModalActive: true
    })
  }
  // Close Modal
  handleQuickViewModalClose(){
    this.setState({
      quickViewModalActive: false
    })
  }

  render() {
    return (

      <React.Fragment>
        <NavBarComponent
          totalItems= {this.state.totalItems}
          totalAmount ={this.state.totalAmount}
          handleCartShow={this.handleCartShow}
        />

        <CartModalComponent
          cartItems={this.state.cart}
          showCart={this.state.showCart}
          removeProduct={this.handleRemoveProduct}
          handleCartClose={this.handleCartClose}
          handleProceed={this.handleCheckoutModalShow}
        />

        <QuickView
          product={this.state.quickViewProduct}
          quickViewModalActive={this.state.quickViewModalActive}
          handleQuickViewModalShow={this.handleQuickViewModalShow}
          handleQuickViewModalClose={this.handleQuickViewModalClose}
        />

        <BannerComponent banners={this.state.banners}/>

        <div id="what_we_do" className="container-fluid"></div>

        <div id="restaurants" className="container-fluid"></div>

        <div id="foodcart_specials" className="container-fluid">
          <div className="row">
            <div className="col-md-3  col-lg-3"></div>
            <div className="col-md-6 col-sm-12 col-lg-6">
              <center></center>
              <br/>
              <div className="input-group">
                <input type="text" onChange={this.handleSearch} className="form-control"/>
                <span className="input-group-addon" style={{marginTop:"40px"}}>
                  <span className="glyphicon glyphicon-search"></span>
                </span>
              </div>
            </div>
            <div className="col-md-3 col-lg-3"></div>
          </div>

          <br/>
          <br/>
          <br/>

          <center>
            <b style={{fontFamily:"Times New Roman"}}><h2>Foodcart Specials</h2></b>
            <hr/>
          </center>

          <SpecialsComponent
            productsList={this.state.products}
            term={this.state.term}
            addToCart={this.handleAddToCart}
            productQuantity={this.state.quantity}
            updateQuantity={this.updateQuantity}
            openModal={this.handleQuickViewModalShow}
          />
        </div>

        <div id="products" style={{marginTop:"20px"}} className="form-group">
          <center>
            <h2>Choose your Favourite Fooooood</h2>
          </center>

          <hr/>

          <div className="container">
            <Products
              productsList={this.state.products}
              term={this.state.term}
              addToCart={this.handleAddToCart}
              productQuantity={this.state.quantity}
              updateQuantity={this.updateQuantity}
              openModal={this.handleQuickViewModalShow}
            />
          </div>
        </div>

        <div id="contact_us" className="container-fluid" style={{backgroundColor:"black",width:"100%"}}>
          <FooterComponent/>
        </div>

        <CheckoutModal
          checkoutModalActive={true}
          checkoutModalActive={this.state.checkoutModalActive}
          handleCheckoutModalShow={this.handleCheckoutModalShow}
          handleCheckoutModalClose={this.handleCheckoutModalClose}
          handleCheckout={this.handleCheckout}
        />

      </React.Fragment>
    );
  }
}

export default App;
