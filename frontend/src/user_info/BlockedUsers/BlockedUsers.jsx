import React, { useState, useEffect } from 'react';

import NavBar from '../../Shared_Components/NavBar';
import Sidebar from '../../Shared_Components/Sidebar/Sidebar';
import Feed from "../../Shared_Components/Feed/Feed";
import './blockedusers.css';

export default function BlockedUsers(){	
	
	return (
	    <div>
		<NavBar />
			<div className="settings-container">
				<Sidebar />
				<div className="blocked-feed">
					<Feed route="blockedusers/" elementType="profile"/>
				</div>
			</div>
		</div>
	);

}