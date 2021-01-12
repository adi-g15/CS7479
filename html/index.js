function handleZipClick(event) {
    document.getElementById("zip_anchor").click();
}

function GetListService(params) {
    
}

GetListService(storageRef).then(data => {
    console.debug(data);

    setFiles(data.storedFiles);
    if(data.zipped) {
        data.zipped.link.then(link => setZipLink(link));
        data.zipped.meta.then(metadata => setZipSize(metadata.size));

        document.getElementById("zip_btn");
    }
});