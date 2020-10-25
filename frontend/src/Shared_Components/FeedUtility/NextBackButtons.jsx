import React, { useState, useEffect } from "react";

import "./nextbackbuttons.css";

export default function NextBackButtons({
    actualValue, setFunction
}) {
	return (
		<div>
		{(actualValue > 0) ? (
			<button onClick={() => setFunction(actualValue - 5)}>Back</button>
		) : ( <p></p>)
		}
		<button onClick={() => setFunction(actualValue + 5)}>Next</button>
		</div>
	);
}