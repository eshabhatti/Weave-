import React, { useState, useEffect } from "react";
import Chat from "./Chat"

export default function Timeline() {
	const [errorMessage, updateErrorMessage] = useState("");

	return (
        <Chat sender={"schikyal"} receiver={"receiver"} />
	);
}