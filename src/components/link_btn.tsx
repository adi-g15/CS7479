import React, { useRef } from "react";

export default function LinkBtn({name, link}) {
    const anchorRef = useRef(null);

    return (
        <button style={{cursor: 'pointer'}} onClick={() => anchorRef.current.click()}>
            <a
            ref={anchorRef}
            href = {link}
            style = {{textDecoration: 'none'}}
            >
                {name}
            </a>
        </button>
    );
}
