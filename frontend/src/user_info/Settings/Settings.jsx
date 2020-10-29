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
		//TODO account deletion fetch
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
      window.location = "/login";
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
