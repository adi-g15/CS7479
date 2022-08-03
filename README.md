# Decrypted Lecture Notes

![CS7479](https://socialify.git.ci/adi-g15/CS7479/image?description=1&descriptionEditable=Decrypted%20Lecture%20Notes%20for%20NITP%202k19%20batch&font=Inter&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2Fd%2Fda%2FGoogle_Drive_logo.png%2F268px-Google_Drive_logo.png&name=1&owner=1&pattern=Floating%20Cogs&theme=Dark)

<center>Workflow Status: <a href="https://github.com/adi-g15/CS7479/actions/workflows/python-app.yml"><img src="https://github.com/adi-g15/CS7479/actions/workflows/python-app.yml/badge.svg" /></a></center>

For the NITP 2k19-23 batch.

> Is baar public website nhi rkhenge, koshish hoga ki google drive ka link ho

Provides decrypted lecture notes, download and read, no need to always enter the password.

> See the `decrypt.py` file for code, it is the main code for fetching, decrypting and pushing the pdfs.

There are in-code comments, for any further issue/\`any\` doubt, create an issue here or dm.

## Decrypting and Updating data

This is totally automated to fetch new pdfs, decrypt and upload the files, with latest files added in the google drive folder.

This command handles it : 

```sh
python3 decrypt.py
```

After this everything is automated, the steps in brief are:

1. Downloading new files from google drive folder
2. Decrypting pdfs
3. Uploading updated files to google cloud storage/google drive

All of this is automated, see the `decrypt.py` file for more details and comments to how it is done :D

> TIP: scripts/ folder me kuchh aur mast cheeze hai, eg. uploading to a google cloud storage bucket

Made for anyone who wishes to make something easier for all :D

