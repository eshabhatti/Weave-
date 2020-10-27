import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import NavBar from '../../Shared_Components/NavBar';
import Sidebar from '../../Shared_Components/Sidebar/Sidebar';

import './settings.css';

export default function Settings(){
	const DeleteAccount = () => {
		//TODO account deletion fetch
		
	}

	return (
	    <div>
		<NavBar />
			<div>
			<Sidebar />		
			<button onClick={(e) => DeleteAccount(e)}>Delete My Account</button>
			</div>
		</div>
	);

} 
