import React from 'react';
import "../styles/global.css";

interface NavbarProps {
	title: string
};

export default function NavBar(props: NavbarProps) {
	return (
		<header className="centered">
			<h1>
				{props.title}
			</h1>
		</header>
	);
}
