import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import NavBar from '../../Shared_Components/NavBar';
import Sidebar from '../../Shared_Components/Sidebar/Sidebar';

import './settings.css';



export default function Settings(){
	const access_token = localStorage.getItem('access_token');
	if (access_token == null) {
		window.location = '/login';
	}
	const DeleteAccount = () => {
		fetch('http://localhost:5000/deleteaccount/', {
      		method: 'GET',
      		headers: {
        		'Content-Type': 'application/json',
        		'Authorization': 'Bearer ' + access_token
      		},
    	}).then(response => response.json()).then(data => {
      		const errorMessage = data.error_message || data.msg;
      		if (errorMessage) {
        		alert(errorMessage);
	  		}
			  
			// Blacklists the current JWT tokens; mirrors logout.
			const access_token = localStorage.getItem('access_token');
			const logoutEndpoint = "http://localhost:5000/logout";
			fetch(logoutEndpoint, {
			  method: "DELETE",
			  headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + access_token
			  },
			}).then(response => response.json()).then(data => {
			  const { refresh_token } = data;
			  const endpoint2 = "http://localhost:5000/logout2";
			  fetch(endpoint2, {
				method: "DELETE",
				headers: {
				  'Content-Type': 'application/json',
				  'Authorization': 'Bearer ' + refresh_token
				},
			  }).then(response => response.json()).then(data => {
				localStorage.clear("access_token");
				localStorage.clear("refresh_token");
				window.location = "/login";
			  }).catch(err => {
				console.error(err);
				alert("error: check console for details");
			  });
			}).catch(err => {
			  console.error(err);
			  alert("error: check console for details");
			});
    	}).catch(err => {
      		console.error(err);
    	});
	}

	return (
	    <div>
		<NavBar />
			<div className="settings-container">
				<Sidebar />	
				<div className="settings-display">
				<button onClick={(e) => DeleteAccount(e)}>Delete My Account</button>
				</div>
			</div>
		</div>
	);

} 
