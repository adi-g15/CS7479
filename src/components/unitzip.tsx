import React, { useEffect, useRef, useState } from "react";
import byteSize from "byte-size";
import "../styles/pdf_down.css";

/**
 * The file object, we get from firebase looks like this
 * 
 * NOTE-  the `link` and `metadata` are NOT returned by firebase, you have to call another function to get them, that's why we have promises here
 */
interface ZipProps {
    name: string,
    linkPromise: Promise<string>,
    metaPromise: Promise<any>,
    gridWidth?: [number, number]
};

export default function UnitZip(props: ZipProps) {
    const [link, setLink] = useState("?");
    const [size, setSize] = useState(0);

    const anchor = useRef();
    useEffect(() => {
        props.linkPromise.then(link => setLink(link));
        props.metaPromise.then(meta => setSize(meta.size));
    }, []);

    return (
        <div className="unit_zip" style={ props.gridWidth ? {gridColumnStart: props.gridWidth[0], gridColumnEnd: props.gridWidth[1]} : {} }>
            <button
				onClick={() => anchor.current?.click()}
				disabled={link === '?'}
			>
				<a download href={link} ref={anchor}>
					{props.name}
				</a>
				<p>
					{ `( ${byteSize(size).toString()} )`}
				</p>
			</button>
        </div>
    )
}
