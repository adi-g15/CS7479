import React from 'react';
import "../styles/global.css";

interface FooterProps {
	msg: string
};

export default function NavBar(props: FooterProps) {
	return (
		<footer className="centered">
			{props.msg}
		</footer>
	);
}
