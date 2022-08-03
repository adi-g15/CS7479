# This and `create_zips.js` will be in HOME directory of Cloud Shell

cd ~
gsutil -m cp "Lecture*pdf" gs://assignment-7d2c8.appspot.com/cs4401/
gsutil -m cp -r gs://assignment-7d2c8.appspot.com/cs4401 .

cd cs4401
zip -u CS4401_COA_All.zip Lecture*		# Creating zip of All Lectures

node create_zips.js						# This javascript script creates the zip files for Unit-I, Unit-II, ...

gsutil mv *.zip gs://assignment-7d2c8.appspot.com/cs4401/
