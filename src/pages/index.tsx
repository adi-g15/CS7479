import React, { useEffect, useState } from 'react';
import NavBar from "../components/navbar";
import PDFDown from "../components/pdf_down";
import byteSize from "byte-size";
import {GetListService} from "../services/files";
import "../styles/global.css";

import firebase from "firebase/app";
import firebaseConfig from "../config/firebase";
import "firebase/storage";

try{
	firebase.initializeApp(firebaseConfig);
} catch(err) {
	console.error(err.msg || "Error");
}

const storage = firebase.storage();
const storageRef = storage.ref();

export default function CS4401() {
	const [files, setFiles] = useState([]);
	const [zipLink, setZipLink] = useState('?');
	const [zipSize, setZipSize] = useState(0);
	const [selectOn, setSelect] = useState(false);

	useEffect(() => {
		GetListService(storageRef.child("cs4401/")).then(data => {
			console.debug(data);

			setFiles(data.storedFiles);
			if(data.zipped) {
				data.zipped.link.then(link => setZipLink(link));
				data.zipped.meta.then(metadata => setZipSize(metadata.size));
			}
		})
	}, []);

	// <></> is a react fragement
	return (
		<>
			<NavBar title="Decrypted CS4401"/>

			<hr className="separation" />
			<div className="centered">
				{"Decrypted Lecture Notes CS4401, bina password  :D"}
			</div>
			<hr className="separation" />
			<br />
			<div className="link_container">
			<div><button
				style={{
					backgroundColor: '#20b2aa30',
					width: '80%',
					marginLeft: '10%',
					borderRadius: '10px'
				}}
				onClick={() => document.getElementById("zip_anchor").click()}
				disabled={zipLink === '?'}
			>
				<a download id="zip_anchor" href={zipLink} style={{color: 'inherit', textDecoration: 'none'}}>
					Download All as ZIP
				</a>
				<p>
					{ `( ${byteSize(zipSize).toString()} )`}
				</p>
			</button></div>

				<table>
					<thead>
						<tr>
							{selectOn && (<td>Select</td>)}
							<td>Name</td>
							<td>Size</td>
						</tr>
					</thead>
					<tbody>
					{files.map((value, index) => (
						<PDFDown
							name={value.name}
							linkPromise={value.link}
							metaPromise={value.meta}
							key={index}
							selectOn={selectOn}
						/>
					)
					)}
					</tbody>
				</table>
			</div>
		</>
	);
}
