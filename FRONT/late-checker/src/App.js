import React, { Fragment } from "react";
import { Route, BrowserRouter as Router, Link, Switch } from "react-router-dom";
import "./App.css";
import VideoFeed from "./Components/VideoFeed/VideoFeed";
import FacedTesting from "./Components/face-api-testing/faced";
import AdminBlock from "./Components/AdminBlock/AdminBlock";
function App() {
  // * ---------- STYLE ---------- *

  return (
    <Fragment>
      <Router>
        <div className="App">
          <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <a className="navbar-brand" href="#">
              IMTMA
            </a>
            <button
              className="navbar-toggler"
              type="button"
              data-toggle="collapse"
              data-target="#navbarSupportedContent"
              aria-controls="navbarSupportedContent"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <ul className="navbar-nav mr-auto">
              <li className="nav-item">
                <Link to="/" className="nav-link">
                  Home
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/admin_module" className="nav-link">
                  Admin module
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/staff_enrollment" className="nav-link">
                  Staff Enrollment
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/facial_test_link" className="nav-link">
                  Facial Test
                </Link>
              </li>
            </ul>
          </nav>
          <div className="container">
            <Switch>
              <Route exact path="/"></Route>
              <Route path="/staff_enrollment" component={VideoFeed}></Route>
              <Route path="/admin_module" component={AdminBlock}></Route>
              <Route path="/facial_test_link" component={FacedTesting}></Route>
            </Switch>
          </div>
        </div>
      </Router>

      {/* <SearchBar />
				<LastArrivalList />
				<AdminBlock /> */}
    </Fragment>
  );
}

export default App;
