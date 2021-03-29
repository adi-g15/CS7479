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
import Helmet from "react-helmet";

try{
	firebase.initializeApp(firebaseConfig);
} catch(err) {
	console.error(err.msg || "Error");
}

const storage = firebase.storage();
const storageRef = storage.ref();

/**
 * This is the main page when you open https://cs4401.netlify.app
 * 
 * What it does ->
 * 	1. Get list of files from firebase (Using the GetListService function)
 *  2. Add all .zip files to unitZips array, and the "All lectures.zip" file to allZip
 *  3. Rest all pdf files added to files array
 *  4. Then for each zip we create a `UnitZip` component (which is mainly a simple "button")
 *  5. For each file, we create a `PDFDown` component (which is a "table row")
 * 
 * Note - There is also the sort ability, since jab tum site visit karoge, tum generally
 * 		  new pdfs upar dekhna chahoge/chahogi, that's why the additional functionality
 *        so you decide the order
 * 
 * Sorting - The `ascendingOrder` variable is used for this, when it is true, then sort in ascending order,
 * 			 else descending order (according to file name)
 * 
 * @returns {JSX.Element} The CS4401 lectures page
 */
export default function CS4401() {
	const [files, setFiles] = useState([]);			// array of pdfs (each being a File)
	const [allZip, setZip] = useState(null);		// All Lecture zip file
	const [unitZips, setUnitZips] = useState([]);	// UnitI, UnitII, UnitIII, ... zips
	const [selectOn, setSelect] = useState(false);	// NOT USED
	const [updated_time, setUpdatedTime] = useState(null);		// last updated time, bottom pe dikhta hai
	const [ascendingOrder, setAscendingOrder] = useState(true);	// sorting order, agar true then ascending nahi toh descending

	if( ascendingOrder === true )
		files.sort((a,b) => a.name === b.name ? 0: (a.name < b.name ? -1:1 ));
	else if( ascendingOrder === false )
		files.sort((a,b) => a.name === b.name ? 0: (a.name < b.name ? 1:-1 ));

	useEffect(() => {
		GetListService(storageRef.child("cs4401/")).then(data => {
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
			<div className="application">
				<Helmet>
					<meta charSet="utf-8" />
					<meta name="description" content="CS4401 bina password" />
					<meta name="theme-color" content="#20b2aa" />
					<meta name="lang" content="en" />
					<title>Decrypted CS4401</title>
				</Helmet>
			</div>
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
						/** 
						 * if allZip is not null, ie. there is a "All Lectures.zip",
						 * we set its gridWidth to use 2 columns, this is why it looks bigger
						 * For more information, ye padho - https://devdocs.io/css/grid-column-start
						 * 
						 * Then the unitZips.map call creates different buttons (`UnitZip` component)
						 * for each Unit-I, Unit-II, ... zip files
						*/
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
