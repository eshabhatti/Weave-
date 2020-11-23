import React, { useState, useEffect } from "react";
import Chat from "./Chat"

export default function Test() {
    const [errorMessage, updateErrorMessage] = useState("");
    const access_token = localStorage.getItem('access_token');
    if (access_token == null) {
        window.location = "/login"
    }

	return (
        <Chat sender={"schikyal"} receiver={"receiver"} />
	);
}