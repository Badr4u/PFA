import React, { Component } from "react";
import { Navbar, Nav, NavDropdown, Modal } from "react-bootstrap";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import * as actions from "../../Store/Actions/auth";
import axios from "axios";
import { FaShoppingCart } from "react-icons/fa";
import ShoppingCart from "./ShoppingCart";
import { ToastContainer, toast } from "react-toastify";

export class NavBarComp extends Component {
  constructor(props) {
    super(props);

    this.state = {
      Info: {
        Userid: null,
        isAdmin: null,
        username: null,
      },
      loading: true,
      showmodalPanier: false,
      modalInfo: {},
      ModalisFetched: false,
      TotalPrice: null,
    };
    this.handleLogout = this.handleLogout.bind(this);
    this.ApiCall = this.ApiCall.bind(this);
    this.PanierHandler = this.PanierHandler.bind(this);
    this.quitmodal = this.quitmodal.bind(this);
    this.handlePayement = this.handlePayement.bind(this);
  }

  async PanierHandler() {
    await axios
      .post("http://127.0.0.1:8000/api/OrderView/", {
        pk: this.state.Info.Userid,
      })
      .then(({ data }) =>
        this.setState({
          modalInfo: data,
          ModalisFetched: true,
          showmodalPanier: true,
        })
      );
    // await this.setState({});
  }

  ApiCall() {
    const token = localStorage.getItem("token");
    axios
      .post("http://127.0.0.1:8000/api/TokenView/", {
        token: token,
      })
      .then(({ data }) =>
        this.setState({
          Info: {
            Userid: data.user,
            isAdmin: data.is_admin,
            username: data.user_name,
          },
          loading: false,
        })
      )
      .catch((err) => console.log(err));
  }
  async handleLogout() {
    await this.props.logout();
    await this.setState({
      Info: {
        Userid: null,
        isAdmin: null,
        username: null,
      },
      loading: true,
      showmodalPanier: false,

      ModalisFetched: false,
    });
  }
  // handleTotalPrice() {}
  quitmodal() {
    toast.error("Produit Supprimer du Panier", {
      position: "top-right",
      autoClose: 2000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });
    this.setState({ showmodalPanier: false });

    return <ToastContainer />;
  }

  handlePayement() {
    axios
      .post("http://127.0.0.1:8000/api/payment/", {
        pk: this.state.modalInfo.id,
        user: this.state.Info.Userid,
      })
      .then((res) =>
        toast.error(`${res.data.message}`, {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        })
      )
      .then(this.setState({ showmodalPanier: false }))

      .catch((err) => console.log(err));
    return <ToastContainer />;
  }

  render() {
    return (
      <>
        <Navbar bg="light" expand="lg">
          <Link className="navbar-brand" to="/">
            MyFood
          </Link>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ml-auto">
              {this.props.isAuthenticated ? (
                <>
                  {this.state.loading ? (
                    this.ApiCall()
                  ) : (
                    <>
                      <span className="mx-4 lead my-auto">
                        Bonjour ,{this.state.Info.username}
                      </span>
                      {this.state.Info.isAdmin ? null : (
                        <button
                          onClick={this.PanierHandler}
                          className="btn btn-dark"
                        >
                          <FaShoppingCart className="m-1" />
                          Panier
                        </button>
                      )}

                      {this.state.ModalisFetched ? (
                        <>
                          <Modal
                            show={this.state.showmodalPanier}
                            onHide={() =>
                              this.setState({ showmodalPanier: false })
                            }
                            size="lg"
                          >
                            <div className="modal-content">
                              <div className="modal-header border-bottom-0">
                                <h5
                                  className="modal-title"
                                  id="exampleModalLabel"
                                >
                                  Panier
                                </h5>
                                <button
                                  type="button"
                                  className="close"
                                  data-dismiss="modal"
                                  aria-label="Close"
                                  onClick={() =>
                                    this.setState({ showmodalPanier: false })
                                  }
                                >
                                  <span aria-hidden="true">&times;</span>
                                </button>
                              </div>
                              <div className="modal-body">
                                <table className="table table-image">
                                  <thead>
                                    <tr>
                                      <th scope="col"></th>
                                      <th scope="col">Produit</th>
                                      <th scope="col">Prix</th>
                                      <th scope="col">Quantité</th>
                                      <th scope="col">Total</th>
                                      <th scope="col">Supprimé</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {this.state.modalInfo.product.map(
                                      (item) => (
                                        <ShoppingCart
                                          item={item}
                                          key={item.id}
                                          user={this.state.modalInfo.user}
                                          quit={this.quitmodal}
                                        />
                                      )
                                    )}
                                  </tbody>
                                </table>
                                {this.state.TotalPrice != null ? (
                                  <div className="d-flex justify-content-end">
                                    <h5>
                                      Total:{" "}
                                      <span className="price text-success">
                                        {this.state.TotalPrice}
                                      </span>
                                    </h5>
                                  </div>
                                ) : null}
                              </div>
                              <div className="modal-footer border-top-0 d-flex justify-content-between">
                                <button
                                  type="button"
                                  className="btn btn-secondary"
                                  onClick={() =>
                                    this.setState({ showmodalPanier: false })
                                  }
                                >
                                  Fermé
                                </button>
                                {this.state.modalInfo.product.length > 0 ? (
                                  <button
                                    type="button"
                                    className="btn btn-success"
                                    onClick={this.handlePayement}
                                  >
                                    Payer
                                  </button>
                                ) : (
                                  <button
                                    type="button"
                                    className="btn btn-success "
                                    disabled
                                  >
                                    Payer
                                  </button>
                                )}
                              </div>
                            </div>
                          </Modal>
                        </>
                      ) : null}
                      <NavDropdown title="Menu" id="nav-dropdown">
                        {this.state.Info.isAdmin ? (
                          <Link
                            to="/admin"
                            className=" text-reset text-decoration-none d-block mx-auto"
                          >
                            Panneau Admin
                          </Link>
                        ) : (
                          <Link
                            to={`/Client/${this.state.Info.Userid}/Pannel`}
                            className="text-reset text-decoration-none d-block mx-auto "
                          >
                            Panneau Client
                          </Link>
                        )}

                        <Link
                          to={`${this.state.Info.Userid}/Profile`}
                          className="text-reset text-decoration-none"
                        >
                          Profile
                        </Link>
                      </NavDropdown>
                    </>
                  )}
                  <button
                    className="btn btn-outline-secondary mx-2"
                    // onClick={this.props.logout}
                    onClick={this.handleLogout}
                  >
                    déconnecter
                  </button>
                </>
              ) : (
                <>
                  <Link className="btn btn-outline-secondary mx-2" to="/SignUp">
                    {" "}
                    S'inscrire / Se connecter{" "}
                  </Link>
                </>
              )}
            </Nav>
          </Navbar.Collapse>
        </Navbar>
      </>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.token !== null,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    logout: () => dispatch(actions.logout()),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(NavBarComp);
