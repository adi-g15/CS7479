import React, { useEffect, useRef } from "react";
import "../styles/pdf_down.css";

interface PdfProps {
    name: string,
    linkPromise: Promise<string>,
    metaPromise: Promise<any>
};

export default function PdfDown(props: PdfProps) {
    const anchorRef = useRef(null);
    const sizeRef = useRef(null);

    useEffect(() => {
        props.linkPromise.then(url => {
            anchorRef.current.setAttribute("href", url);
        })
        props.metaPromise.then(metadata => {
            sizeRef.current.innerText = metadata.size/1000 + ' KB';
        })
    }, []);

    return (
        <tr className="pdf_down">
            <td>
                <span className="download_logo">
                    ⏬
                </span>
            </td>
            <td>
                <span className="pdf_name">
                    <a ref={anchorRef} href={"?"}>
                        {props.name}
                    </a>
                </span>
            </td>
            <td>
                <p ref={sizeRef} />
            </td>
        </tr>
    )
}
