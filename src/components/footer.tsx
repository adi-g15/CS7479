import React from 'react';
import "../styles/global.css";

interface FooterProps {
	msg: string
};

export default function NavBar(props: FooterProps) {
	return (
		<footer className="centered">
			<div style={{padding: '5px', fontSize: 'large'}}>
				<a href="https://drive.google.com/drive/folders/1oGKKT1DVB__792WIMvARUSFJkUqy2jWu?usp=sharing">Original Drive Link</a>
			</div>
			<div>
				{props.msg}
			</div>
		</footer>
	);
}
