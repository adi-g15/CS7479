cd ~
# gsutil ls gs://assignment-7d2c8.appspot.com/cs4401/
gsutil -m cp "Lecture*pdf" gs://assignment-7d2c8.appspot.com/cs4401/
gsutil -m cp -r gs://assignment-7d2c8.appspot.com/cs4401 .
cd cs4401
zip -u CS4401_COA_All.zip Lecture*


/// create_zips.js
// Must be executed INSIDE the directory having these files

const SUB_CODE = 'CS4401_COA';

const fs = require('fs')
const { exec } = require("child_process");

const files = fs.readdirSync('.').filter(file => file.includes('Lecture') && file.includes('.pdf') && file.includes('Unit'))

const units = {'I': [], 'II': [], 'III': [], 'IV': []};

for(n in units) {
	units[n] = files.filter(file => file.includes('Unit ' + n +' -'))

	fs.mkdirSync(`${SUB_CODE}_Unit_${n}`)

	_a =exec(`zip -u ${SUB_CODE}_Unit_${n}.zip *"Unit ${n} -"*`, (err, stdout, stderr) => console.log(err,stdout, stderr))
}

/// END


gsutil mv *.zip gs://assignment-7d2c8.appspot.com/cs4401/

exit

