#include <filesystem>
#include <vector>
#include <string>
// #include <format>	// for std::format
#include <iomanip>	// for std::quoted
// #include <algorithm>
// #include <execution>

using namespace std;
using namespace filesystem;

const std::string password = "nitp_cs4401-Spr21";
const std::string path_to_qpdf = "C:\\Users\\adity\\Downloads\\qpdf-6.0.0\\qpdf";
const char* encrypted_pdf_directory = "encrypted";

string Command( path& in ){
	// return std::format("{}  --decrypt --password={} {} {}", path_to_qpdf, password, std::quoted(in.string()), std::quoted(in.filename().string()));
	return (path_to_qpdf + " --decrypt --password=" + password + " \"" + in.string() + "\" \"" + in.filename().string() + "\"");
}

int main(){
	vector<path> vec;

	for( auto& p: directory_iterator(encrypted_pdf_directory) ){
		if( p.path().has_filename() && p.path().extension().string() == ".pdf" ) 
			vec.push_back( p.path() );
	}

	// system() call likely should not be parallelized like this, can do through pipes though
	// for_each(execution::par_unseq, vec.begin(), vec.end(), [](auto& filepath){
	// 	system( Command(filepath).c_str() );
	// });
	for(auto& filepath: vec){
		system( Command(filepath).c_str() );
	}

	remove_all(encrypted_pdf_directory);
	create_directory(encrypted_pdf_directory);	// keep the directory, remove only 

	return 0;
}
