import React from "react";
import "../styles/global.css";

export default function NotFound() {
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                height: `100vh`,
                alignItems: 'center',
                justifyContent: 'center'    // horizontal
            }}
        >
            <h1 style={{fontStretch: "expanded"}}>404</h1>
            <h2>Galat jagah aa gya patra... Ja Wapas !!</h2>
        </div>
    )
}