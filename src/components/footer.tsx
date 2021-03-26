import React from 'react';
import LinkBtn from "./link_btn";
import "../styles/global.css";

interface FooterProps {
	msg: string
};

export default function NavBar(props: FooterProps) {
	return (
		<footer className="centered">
			<div style={{padding: '5px', fontSize: 'large'}}>
				<LinkBtn
					name="Original Drive Link"
					link="https://drive.google.com/drive/folders/1oGKKT1DVB__792WIMvARUSFJkUqy2jWu?usp=sharing"
				/>
			</div>
			<hr style={{width: '60%'}} />
			<div style={{padding: '5px', fontSize: 'large'}}>
				<LinkBtn
					name="CS4402 (FLAT)"
					link="https://patnanit.sharepoint.com/sites/CS4402FormalLanguagesAutomataTheory/Class%20Materials/Forms/AllItems.aspx"
				/>
				<LinkBtn
					name="CS4403 (Algo)"
					link="https://patnanit.sharepoint.com/sites/CS4403DesignAnalysisofAlgorithms/Shared%20Documents/General"
				/>
				<LinkBtn
					name="CS4404 (OS)"
					link="https://drive.google.com/drive/folders/1j_Owdu8srBdZbn-iTqzmj3ERKygEupgI"
				/>
				<LinkBtn
					name="CSL4404 (OS Lab)"
					link="https://patnanit.sharepoint.com/sites/CSL4404OperatingSystemslab/Class%20Materials/Forms/AllItems.aspx"
				/>
				<LinkBtn
					name="CS4460 (OOSD)"
					link="https://patnanit.sharepoint.com/sites/CS44602/Class%20Materials/Forms/AllItems.aspx"
				/>
			</div>
			<hr style={{width: '60%'}} />
			<div>
				{props.msg}
			</div>
		</footer>
	);
}
