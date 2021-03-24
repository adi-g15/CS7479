import React from 'react';
import "../styles/global.css";

interface FooterProps {
	msg: string
};

export default function NavBar(props: FooterProps) {
	return (
		<footer className="centered">
			<div style={{padding: '5px', fontSize: 'large'}}>
				<button style={{cursor: 'pointer'}} onClick={()=>document.getElementById('org_drive_anchor').click()}>
					<a
					id="org_drive_anchor"
					href="https://drive.google.com/drive/folders/1oGKKT1DVB__792WIMvARUSFJkUqy2jWu?usp=sharing"
					style={{textDecoration: 'none'}}
					>
						Original Drive Link
					</a>
				</button>
			</div>
			<div>
				{props.msg}
			</div>
		</footer>
	);
}
