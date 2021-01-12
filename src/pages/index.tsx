import React, { useEffect, useRef, useState } from 'react';
import NavBar from "../components/navbar";
import PDFDown from "../components/pdf_down";
import {GetListService} from "../services/files"; 
import "../styles/global.css";

import firebase from "firebase/app";
import firebaseConfig from "../config/firebase";
import "firebase/storage";

firebase.initializeApp(firebaseConfig);
const storage = firebase.storage();
const storageRef = storage.ref();

export default function App() {
	const [files, setFiles] = useState([]);
	const [zipLink, setZipLink] = useState('?');
	const [zipSize, setZipSize] = useState(0);

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
			<NavBar />

			<hr className="separation" />
			<div className="centered">
				Decrypted Lecture Notes CS4401 :D, no password
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
					{ "( " + Math.round(zipSize/1000) + ' KB )'}
				</p>
			</button></div>

				<table>
					<tbody>
					{files.map((value, index) => (
						<PDFDown
							name={value.name}
							linkPromise={value.link}
							metaPromise={value.meta}
							key={index}
						/>
					)
					)}
					</tbody>
				</table>
			</div>
		</>
	);
}
