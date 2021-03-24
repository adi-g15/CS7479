import React, { useEffect, useState } from 'react';
import NavBar from "../components/navbar";
import Footer from "../components/footer";
import PDFDown from "../components/pdf_down";
import {GetListService} from "../services/files";
import "../styles/global.css";
import UnitZip from "../components/unitzip";

import firebase from "firebase/app";
import firebaseConfig from "../config/firebase";
import "firebase/storage";
import dayjs from "dayjs";

try{
	firebase.initializeApp(firebaseConfig);
} catch(err) {
	console.error(err.msg || "Error");
}

const storage = firebase.storage();
const storageRef = storage.ref();

export default function CS4401() {
	const [files, setFiles] = useState([]);
	const [allZip, setZip] = useState(null);
	const [unitZips, setUnitZips] = useState([]);
	const [selectOn, setSelect] = useState(false);
	const [updated_time, setUpdatedTime] = useState(null);
	const [ascendingOrder, setAscendingOrder] = useState(true);

	if( ascendingOrder === true )
		files.sort((a,b) => a.name === b.name ? 0: (a.name < b.name ? -1:1 ));
	else if( ascendingOrder === false )
		files.sort((a,b) => a.name === b.name ? 0: (a.name < b.name ? 1:-1 ));

	useEffect(() => {
		GetListService(storageRef.child("cs4401/")).then(data => {
			console.debug(data);

			const all_zip = data.zipped.find(zip => !zip.name.startsWith('Unit'));
			setZip(all_zip);

			all_zip.meta.then(meta => {
				console.debug("List Updated: ", meta.updated);
				setUpdatedTime( dayjs(meta.updated).format('DD MMM YYYY') );
			});

			setUnitZips(data.zipped.filter(zip => zip.name.startsWith('Unit')));
			setFiles(data.storedFiles);
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
			<div className="container">
				<div className="unit_container">
					{
						[( allZip && <UnitZip key={0} gridWidth={[1,3]} name={"Download All as ZIP"} linkPromise={allZip.link} metaPromise={allZip.meta} />)]
							.concat(unitZips.map((zip, index) => (
								<UnitZip key={index+1} name={zip.name} linkPromise={zip.link} metaPromise={zip.meta} />
							)))
					}
				</div>

				<table>
					<thead>
						<tr>
							{selectOn && (<td>Select</td>)}
							<td style={{cursor: 'pointer'}} onClick={() => ascendingOrder === null ? setAscendingOrder(false): setAscendingOrder(order => !order) }>
								<span>Name</span>
								<span style={{paddingLeft: '15px'}}>{ascendingOrder ? '👇': '👆'}</span>
							</td>
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
			<Footer msg={`Updated: ${updated_time}`}/>
		</>
	);
}
