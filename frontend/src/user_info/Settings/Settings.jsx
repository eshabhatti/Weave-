import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import NavBar from '../../Shared_Components/NavBar';
import Sidebar from '../../Shared_Components/Sidebar/Sidebar';
import './settings.css';

export default function Settings(){

	const [currPass, updateCurrPass] = useState("");
	const [newPass, updateNewPass] = useState("");
	const [newUser, updateNewUser] = useState("");
	const [newEmail, updateNewEmail] = useState("");
	const [setPrivate, updatePrivacyCheck] = useState(false)
	const [deleteErrorMessage, updateDeleteErrorMessage] = useState("");
	const [normalErrorMessage, updateNormalErrorMessage] = useState("");
	const [successMessage, updateSuccessMessage] = useState("");
	const [access_token, updateToken] = useState(localStorage.getItem('access_token'));
	if (access_token == null) {
		window.location = '/login';
	}

	// Delete Account Function
	const DeleteAccount = (event) => {
		
		event.preventDefault();
		const JSONbody = {
			password: currPass,
		}

		const deletepoint = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/deleteaccount/";
		fetch(deletepoint, {
      		method: 'POST',
      		headers: {
        		'Content-Type': 'application/json',
        		'Authorization': 'Bearer ' + access_token
			  },
			  body: JSON.stringify(JSONbody)
    	}).then(response => response.json()).then(data => {
			
			// Catches errors
			const errorMessage = data.error_message || data.msg;
      		if (errorMessage) {
				updateDeleteErrorMessage(data.error_message);
			}
			else {
				
				// Blacklists the current JWT tokens; mirrors logout.
				const access_token = localStorage.getItem('access_token');
				const logoutEndpoint = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/logout";
				fetch(logoutEndpoint, {
				method: "DELETE",
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + access_token
				},
				}).then(response => response.json()).then(data => {
				const { refresh_token } = data;
				const endpoint2 = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/logout2";
				fetch(endpoint2, {
					method: "DELETE",
					headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + refresh_token
					},
				}).then(response => response.json()).then(data => {
					localStorage.clear("access_token");
					localStorage.clear("refresh_token");
					// window.location = "/login";
				}).catch(err => {
					console.error(err);
					alert("error: check console for details");
				});
				}).catch(err => {
				console.error(err);
				alert("error: check console for details");
				});
				// End JWT Blacklist
			
			}  

    	}).catch(err => {
      		console.error(err);
    	});
	}
	// End Delete Account

	// Update settings Function
	const UpdateSettings = (event) => {
		
		event.preventDefault();
		const JSONbody = {
			currentpass: currPass,
			newemail: newEmail,
			newpass: newPass,
			newusername: newUser,
			privacy: setPrivate,
		}

		const endpoint = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/editsettings/";
		fetch(endpoint, {
      		method: 'POST',
      		headers: {
        		'Content-Type': 'application/json',
        		'Authorization': 'Bearer ' + access_token
			},
			body: JSON.stringify(JSONbody)
		}).then(response => response.json()).then(data => {
			
			// Catches errors
			const errorMessage = data.error_message || data.msg;
			if (errorMessage) {
				updateNormalErrorMessage(data.error_message);
			}
			else {
				const { access_token, refresh_token } = data;
				localStorage.setItem('access_token', access_token);
				localStorage.setItem('refresh_token', refresh_token);
				updateToken(localStorage.getItem('access_token'));
				updateSuccessMessage("Settings updated!");
			}

		}).catch(err => {
			console.error(err);
		});
		// End Update Settings Function
	}

	const deleteErrObject = deleteErrorMessage !== "" ? <ErrorBubble message={deleteErrorMessage} /> : null;
	const normalErrObject = normalErrorMessage !== "" ? <ErrorBubble message={normalErrorMessage} /> : null;
	const succObject = successMessage !== "" ? <SuccessBubble message={successMessage} /> : null;

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
							<input 
								value={currPass}
								onChange={e => {
									updateCurrPass(e.target.value);
									updateDeleteErrorMessage("");
									updateNormalErrorMessage("");
									updateSuccessMessage("");
								}}
								type="password"
								className="settings-input" 
							/>

							<hr className="settings-divider"/>

							<label className="settings-label">Enter a new password:</label>
							<input 
								value={newPass}
								onChange={e => {
									updateNewPass(e.target.value);
									updateDeleteErrorMessage("");
									updateNormalErrorMessage("");
									updateSuccessMessage("");
								}}
								type="password"
								className="settings-input" 
							/>

							<label className="settings-label">Enter a new username:</label>
							<input 
								value={newUser}
								onChange={e => {
									updateNewUser(e.target.value);
									updateDeleteErrorMessage("");
									updateNormalErrorMessage("");
									updateSuccessMessage("");
								}}
								className="settings-input" 
							/>

							<label className="settings-label">Enter a new email:</label>
							<input 
								value={newEmail}
								onChange={e => {
									updateNewEmail(e.target.value);
									updateDeleteErrorMessage("");
									updateNormalErrorMessage("");
									updateSuccessMessage("");
								}}
								className="settings-input" 
							/>
							
							<hr className="settings-divider-special"/>
							
							<a className="settings-link" href="/blockedusers" >Blocked Users</a> <br />
							
							<hr className="settings-divider-special"/>
							
							<input
								type="checkbox"
								className="settings-checkbox"
								checked={setPrivate}
								onChange={e => {
									updatePrivacyCheck(!setPrivate);
									updateDeleteErrorMessage("");
									updateNormalErrorMessage("");
									updateSuccessMessage("");
								}}
							/>
							<label className="settings-label-header">Activate privacy mode</label>
							<label className="settings-label">When privacy mode is activated, you will not receieve direct messages from anyone but the users you have followed.</label>


							<button className="settings-button" onClick={(e) => UpdateSettings(e)}>Update Settings</button>
							{normalErrObject}
							{succObject}

							<hr className="settings-divider"/>

							<label className="delete-label">If you are ready to end your time here on Weave, enter your password and then click the button below. THIS ACTION CANNOT BE UNDONE.</label>

							<button className="delete-button" onClick={(e) => DeleteAccount(e)}>Delete My Account</button>
							{deleteErrObject}
						</form>
					</div>
				</div>
			</div>
		</div>
	);
} 

function ErrorBubble({ message }) {
	return (
	  <div className="edit-error-bubble">
		<p className="edit-error-message">{message}</p>
	  </div>
	)
}

function SuccessBubble({ message }) {
	return (
		<div className="edit-success-bubble">
			<p className="edit-error-message">{message}</p>
		</div>
	)
}
