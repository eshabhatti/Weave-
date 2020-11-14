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

	// Delete Account Function
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
	// End Delete Account

	return (
	    <div>
		<NavBar />
			<div className="settings-container">
				<Sidebar />	
				<div className="settings-display">
					<h1 className="settings-heading">Modify your settings</h1>
					<div className="settings-form-box">
						<form className="settings-form">

							<label className="settings-label">Enter your current password:</label>
							<input className="settings-input" />

							<hr className="settings-divider"/>

							<label className="settings-label">Enter a new password:</label>
							<input className="settings-input" />

							<label className="settings-label">Enter a new username:</label>
							<input className="settings-input" />

							<label className="settings-label">Enter a new email:</label>
							<input className="settings-input" />

							<button className="settings-button">Update Settings</button>

							<hr className="settings-divider"/>

							<label className="delete-label">If you are ready to end your time here on Weave, enter your password and then click the button below. THIS ACTION CANNOT BE UNDONE.</label>

							<button className="delete-button" onClick={(e) => DeleteAccount(e)}>Delete My Account</button>
						</form>
					</div>
				</div>
			</div>
		</div>
	);

} 
