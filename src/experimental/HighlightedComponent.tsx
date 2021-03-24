import React from "react";
import ContentPage from "./ContentPage";

interface HighlightedCompProps {
    sub: string,    // subject
    msg?: string
};

export default function HighlightedComponent(props:HighlightedCompProps) {
    return <ContentPage title={props.sub} dirPath={`highlighted/${props.sub}/`} msg={props.msg} />;
}
