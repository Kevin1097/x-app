import React, { Component } from 'react';  // nuevo
import ReactDOM from 'react-dom';
 
 
// nuevo
class App extends Component {
  constructor() {
	super();
  }
  render() {
	return (
  	<section className="section">
    	<div className="container">
      	<div className="columns">
        	<div className="column is-one-third">
          	<br/>
          	<h1 className="title is-1">Todos los Usuarios</h1>
          	<hr/><br/>
        	</div>
      	</div>
    	</div>
  	</section>
	)
  }
};
 
ReactDOM.render(
  <App />,
  document.getElementById('root')
);
