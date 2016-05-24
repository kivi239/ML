#include <cstdio>
#include <iostream>
#include <cstring>
#include <string>
#include <algorithm>
#include <sstream>
#include <fstream>
#include <set>
#include <vector>
#include <thread>


using namespace std;

const string path = "../../OK/Parts_norm/part-r-000";
const string out_path = "files/";


string intToStr(int x) {
	string s;
	while (x > 0) {
		s += (x % 10) + '0';
		x /= 10;
	}
	
	while (s.size() < 2) {
		s += '0';
	}

	reverse(s.begin(), s.end());

	return s;
}


void do_it(int file_num) {
	set<pair<string, string> > pairs;
  string file_name = path + intToStr(file_num);

  ifstream file(file_name.c_str());
	string seq;

	string out_file_name = out_path + intToStr(file_num);
	ofstream res(out_file_name.c_str());

	while (getline(file, seq)) {
		istringstream iss(seq);
		string word;
		vector<string> l;
		while (iss >> word) {
			l.push_back(word);
		}
		                       
		for (int i = 0; i < (int)l.size(); i++) {
		  for (int j = i + 1; j < (int)l.size(); j++) {
		   	pairs.insert(make_pair(l[i], l[j]));
		   	pairs.insert(make_pair(l[j], l[i]));
		  }
		}
	}

	for (set<pair<string, string> >::iterator it = pairs.begin(); it != pairs.end(); it++) {
	  res << (*it).first << ' ' << (*it).second << endl;
	}

	cerr << pairs.size() << endl;

	file.close();
	res.close();

}


int main() {
  for (int file = 1; file < 1; file += 4) {
		do_it(file);
	}

	return 0;
}