## Scripts to automate decrypting

> ### **[DEPRECATED]**
> See `code.py` for a single script capable of automating everything, from fetching pdfs from google drive, decrypting, and uploading to google cloud bucket

This was the original way in which...

1. Download pdf from Lecture Handouts folder on google drive
2. Run `decrypt.cpp` (compiled), it then called a program (qpdf) to decrypt the pdf
3. Upload decrypted pdf to Cloud Shell (Google Cloud Console provides it)
4. Run `./cloud_shell_script.sh` in cloud shell

> The `cloud_shell_script.sh` itself also called `create_zips.js`

A three language endeavour :D

> The above way may seem long, but it still was only `some seconds` to complete, given you actively used Cloud Shell


## Updated way

Now the process is:

1. Run `./code.py`

DONE, it automatically gets the folder id for the folder name with the lecture pdfs, downloads the pdfs inside it, decrypts then, upload to Google Cloud Bucket which is used by `https://cs4401.netlify.app` to show the decrypted lectures


### simple_decrypt.py

This is a part of /code.py, that only deals with downloading and decrypting pdfs from the google drive folder.

Ye simply koi bhi naya file jo us folder me add ho but aapke pas na ho, usko download krke decrypt karega, NO UPLOADING, NOR CREATING ZIP

Helpful for MOST of the people who don't need to maintain this site
