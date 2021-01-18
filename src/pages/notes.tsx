import React from "react";
import NavBar from "../components/navbar";
import "../styles/global.css";

export default function NotesPage() {

    return (
        <>
            <NavBar title="CSE {2k19 - 2k23}" />

            <hr className="separation" />
			<div className="centered">
                Better use `https://nitp-notes.web.app`. Waha pe sab courses ka notes daalne ka koshish hoga jinka milta h
			</div>
			<hr className="separation" />
			<br />

        </>
    );
}