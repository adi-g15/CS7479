export function GetListService(storageRef: firebase.storage.Reference) {
    return new Promise((resolve, reject) => {
        try{
            storageRef.root.listAll().then(result => {
                return resolve(result.items.map(item => {
                    return({
                        name: item.name,
                        link: item.getDownloadURL()
                    });
                }));
            });
        } catch {
            return reject();
        }
    })
  // future -> Use node fs module to get list
}
