import React, { useState, useEffect } from 'react';

export default function ProfilePreview({username}){	
  
	let access_token = localStorage.getItem('access_token');
	if (!access_token) {
		access_token = "";
	}
	let profile_link = "/profile/" + username + "/";
  	return (
	    <div>
			<a href={profile_link} >{username}</a> <br />
		</div>
	);

}