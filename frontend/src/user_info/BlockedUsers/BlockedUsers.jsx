import React, { useState, useEffect } from 'react';

import NavBar from '../../Shared_Components/NavBar';
import Sidebar from '../../Shared_Components/Sidebar/Sidebar';
import Feed from "../../Shared_Components/Feed/Feed";

export default function BlockedUsers(){	
	
	return (
	    <div>
		<NavBar />
			<div className="settings-container">
				<Sidebar />	
				<Feed route="blockedusers/" elementType="profile"/>
			</div>
		</div>
	);

}