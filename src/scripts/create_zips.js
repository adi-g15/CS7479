// This and `cloud_shell_script.sh` will be in HOME directory of Cloud Shell
// Tumko ye file execute karne ka jaroorat nahi hai, cloud_shell_script does it for you

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
