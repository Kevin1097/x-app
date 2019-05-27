import React, { Component } from 'react';  // nuevo
import ReactDOM from 'react-dom';
import axios from 'axios';
import UsersList from './components/UsersList';
import AddUser from './components/AddUser';
 
 
// nuevo
class App extends Component {
  constructor() {
		super();
		this.state = {
			users: []
		};
		this.addUser = this.addUser.bind(this);
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
	addUser(event) {
		event.preventDefault();
		console.log('sanity check!');
	};

  render() {
	return (
  	<section className="section">
    	<div className="container">
      	<div className="columns">
        	<div className="column is-one-third">
          	<br/>
          	<h1 className="title is-1">Todos los Usuarios</h1>
          	<hr/><br/>
						<AddUser addUser={this.addUser}/> {/* nuevo */}
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
