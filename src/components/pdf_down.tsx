import React, { useEffect, useRef } from "react";
import "../styles/pdf_down.css";

interface PdfProps {
    name: string,
    linkPromise: Promise<string>,
    size: number    // in KB
};

export default function PdfDown(props: PdfProps) {
    const anchorRef = useRef(null);

    useEffect(() => {
        props.linkPromise.then(url => {
            anchorRef.current.setAttribute("href", url);
        })
    }, []);

    return (
        <div className="pdf_down">
            <span className="download_logo">
                ⏬
            </span>
            <span className="pdf_name">
                <a ref={anchorRef} href={"?"}>
                    {props.name}
                </a>
            </span>
        </div>
    )
}
