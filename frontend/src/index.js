import React, { useState, useEffect } from 'react';
import './index.css';
import ReactDOM from 'react-dom';

import Login from "./Login/Login";

function App() {
  return (
    <div>
      <Login />
    </div>
  );
}

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
