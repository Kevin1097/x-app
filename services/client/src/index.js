import React, { Component } from 'react';  // nuevo
import ReactDOM from 'react-dom';
import axios from 'axios';
import UsersList from './components/UserList';
 
 
// nuevo
class App extends Component {
  constructor() {
		super();
		this.state = {
			users: []
		};
	};
	//nuevo
	componentDidMount() {
		this.getUser();
	};
	
	getUser(){
		axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
		.then((res) => { this.setState({users: res.data.data.users});})
		.catch((err) => { console.log(err); });
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
						{/* new */}
						<UsersList users={this.state.users}/>
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
