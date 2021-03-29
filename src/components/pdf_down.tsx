import React, { useEffect, useRef, useState } from "react";
import byteSize from "byte-size";
import "../styles/pdf_down.css";

/**
 * The file object, we get from firebase looks like this
 * 
 * NOTE-  the `link` and `metadata` are NOT returned by firebase, you have to call another function to get them, that's why we have promises here
 */
interface PdfProps {
    name: string,
    linkPromise: Promise<string>,
    metaPromise: Promise<any>,
    selectOn: boolean,
    selectNotify?: Function
};

export default function PdfDown(props: PdfProps) {
    const [link, setLink] = useState(null);
    const [size, setSize] = useState(0);

    useEffect(() => {
        props.linkPromise.then(url => setLink(url))
        props.metaPromise.then(meta => setSize(byteSize(meta.size)));
    }, [props.name]);

    return (
        <tr className="pdf_down">
            {props.selectOn && (
                <td>
                    <input type="" />
                </td>)}
            <td>
                <span className="pdf_name">
                    <a download href={link}>
                        {props.name}
                    </a>
                </span>
            </td>
            <td>
                <p>{size.toString()}</p>
            </td>
        </tr>
    )
}
