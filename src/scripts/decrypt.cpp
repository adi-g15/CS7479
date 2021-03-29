// This file will be on your computer
// Similar scripts can be easily written in javascript or python

#include <filesystem>
#include <vector>
#include <string>
#include <iomanip>	// for quoted

using namespace std;
using namespace filesystem;

const string password = "nitp_cs4401-Spr21";
const string path_to_qpdf = "C:\\Users\\adity\\Downloads\\qpdf-6.0.0\\qpdf";
const char* encrypted_pdf_directory = "encrypted";

string Command( path& in ){
	return (path_to_qpdf + " --decrypt --password=" + password + " \"" + in.string() + "\" \"" + in.filename().string() + "\"");
}

int main(){
	vector<path> vec;

	for( auto& p: directory_iterator(encrypted_pdf_directory) ){
		if( p.path().has_filename() && p.path().extension().string() == ".pdf" ) 
			vec.push_back( p.path() );
	}

	for(auto& filepath: vec){
		system( Command(filepath).c_str() );
	}

	remove_all(encrypted_pdf_directory);
	create_directory(encrypted_pdf_directory);	// keep the directory, remove only 

	return 0;
}
