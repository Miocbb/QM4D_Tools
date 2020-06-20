#include <cstddef>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using std::string;
using std::vector;

void show_vector(const vector<double> &vec)
{
    for (size_t i = 0; i < vec.size(); ++i) {
        // std::cout << vec[i] << " ";
        printf("%20.10e ", vec[i]);
        if ((i + 1) % 4 == 0)
            std::cout << std::endl;
    }
    std::cout << std::endl;
}

vector<string> str_split(const string &line, char token = ' ')
{
    vector<string> tokens;
    std::istringstream check(line);
    string find_str;
    while (std::getline(check, find_str, token)) {
        if (find_str.size() != 0) {
            tokens.push_back(find_str);
        }
    }
    return tokens;
}

vector<double> extract_vector(std::ifstream &fchk, size_t num_elements)
{
    vector<double> vec;
    string line;
    size_t n = 0;
    while (n < num_elements) {
        std::getline(fchk, line);
        vector<string> line_split = str_split(line);
        for (size_t i = 0; i < line_split.size(); ++i) {
            vec.push_back(std::stod(line_split[i]));
            ++n;
        }
    }
    return vec;
}

/**
 * How to run: executable fchk spin fbin [-v]
 * fchk: gaussian fchk file.
 * spin: 1 for restricted and 2 for unrestricted
 * fbin: output binary file
 * [-v]: if print verbose
 */
int main(int argc, const char **argv)
{
    // parse arguments
    if (argc <= 1) {
        std::cout << "Error: no fchk file is given.";
        std::exit(EXIT_FAILURE);
    } else if (argc <= 2) {
        std::cout << "Error: no spin setting is given.";
        std::exit(EXIT_FAILURE);
    } else if (argc <= 3) {
        std::cout << "Error: no binary file name is given.";
        std::exit(EXIT_FAILURE);
    }
    std::ifstream fchk(argv[1]);
    if (fchk.peek() == std::ifstream::traits_type::eof()) {
        std::cout << "Error: fchk is empty. It may be not existed or formed "
                     "with error.";
        std::exit(EXIT_FAILURE);
    }

    const int nspin = std::stoi(argv[2]);
    const string fbin = argv[3];
    bool verbose = false;
    if (argc >= 5) {
        for (size_t i = 4; i < argc; ++i) {
            if (argv[i] == string("-v"))
                verbose = true;
            else if (argv[i] == string("-h")) {
                std::cout
                    << "Extrat the MO information from Gaussian fchk file."
                    << std::endl;
                std::cout << "How to use: executable fchk spin fbin [-v] [-h]"
                          << std::endl;
                std::cout << "fchk: Gaussian fchk file path" << std::endl;
                std::cout << "spin: 1 for restricted and 2 for unrestricted."
                          << std::endl;
                std::cout << "fbin: MO binary file that will be generated."
                          << std::endl;
                exit(EXIT_SUCCESS);
            }
        }
    }

    // start to read MO information from fchk file.
    size_t nbasis = 0;
    int num_elec[2] = {0, 0};
    vector<vector<double>> occ;
    vector<vector<double>> coef(2);
    vector<vector<double>> eigs(2);

    std::string line;
    while (std::getline(fchk, line)) {
        // number of alpha electrons
        if (line.find("Number of alpha electrons") != string::npos) {
            vector<string> line_split = str_split(line);
            num_elec[0] = std::stoi(line_split.back());
            if (verbose)
                std::cout << "number of alpha electrons: " << num_elec[0]
                          << std::endl;
        }
        // number of beta electrons
        else if (line.find("Number of beta electrons") != string::npos) {
            vector<string> line_split = str_split(line);
            num_elec[1] = std::stoi(line_split.back());
            if (verbose)
                std::cout << "number of beta electrons: " << num_elec[1]
                          << std::endl;
        }
        // number of basis functions
        else if (line.find("Number of basis functions") != string::npos) {
            vector<string> line_split = str_split(line);
            nbasis = std::stoi(line_split.back());
            if (verbose)
                std::cout << "number of basis function: " << nbasis
                          << std::endl;
        }
        // Alpha eigenvalues
        else if (line.find("Alpha Orbital Energies") != string::npos) {
            size_t num_elements = std::stoi(str_split(line).back());
            eigs[0] = extract_vector(fchk, num_elements);
            if (verbose) {
                std::cout << "Alpha Eigenvalues:" << std::endl;
                show_vector(eigs[0]);
            }
        }
        // Beta eigenvalues
        else if (line.find("Beta Orbital Energies") != string::npos) {
            size_t num_elements = std::stoi(str_split(line).back());
            eigs[1] = extract_vector(fchk, num_elements);
            if (verbose) {
                std::cout << "Beta Eigenvalues:" << std::endl;
                show_vector(eigs[1]);
            }
        }
        // Alpha MO coefficients
        else if (line.find("Alpha MO coefficients") != string::npos) {
            size_t num_elements = std::stoi(str_split(line).back());
            coef[0] = extract_vector(fchk, num_elements);
            if (verbose) {
                std::cout << "Alpha MO coefficient:" << std::endl;
                show_vector(coef[0]);
            }
        }
        // Beta MO coefficients
        else if (line.find("Beta MO coefficients") != string::npos) {
            size_t num_elements = std::stoi(str_split(line).back());
            coef[1] = extract_vector(fchk, num_elements);
            if (verbose) {
                std::cout << "Beta MO coefficient:" << std::endl;
                show_vector(coef[1]);
            }
        }
    }
    // form occupation number array
    for (size_t is = 0; is < nspin; ++is) {
        vector<double> t(nbasis, 0.0);
        occ.push_back(t);
        for (size_t i = 0; i < num_elec[is]; ++i) {
            occ[is][i] = 1.0;
        }
        if (verbose) {
            std::cout << "Occpuation number: spin=" << is << std::endl;
            show_vector(occ[is]);
        }
    }

    // start to write MO information into binary file
    FILE *fpt = fopen(fbin.c_str(), "wb");
    /* write molecular orbitals */
    for (size_t is = 0; is < nspin; is++) {
        if (fwrite((void *)coef[is].data(), sizeof(double), coef[is].size(),
                   fpt) != coef[is].size()) {
            printf("Error: fail to write CoefMatrix[%2d]\n", is);
            exit(EXIT_FAILURE);
        }
    }
    /* write eigenvalues */
    for (size_t is = 0; is < nspin; is++) {
        if (fwrite((void *)eigs[is].data(), sizeof(double), eigs[is].size(),
                   fpt) != eigs[is].size()) {
            printf("Error: fail tp write eigValue[%2d]\n", is);
            exit(EXIT_FAILURE);
        }
    }
    /* write occupation numbers */
    for (size_t is = 0; is < nspin; is++) {
        if (fwrite((void *)occ[is].data(), sizeof(double), occ[is].size(),
                   fpt) != occ[is].size()) {
            printf("Error: fail tp write occupation number[%2d]\n", is);
            exit(EXIT_FAILURE);
        }
    }
    /* write nOcc */
    if (fwrite((void *)num_elec, sizeof(int), nspin, fpt) != nspin) {
        printf("Error: fail to write number of occupied orbitals\n");
        exit(EXIT_FAILURE);
    }
    std::cout << "write mo into binary file: " << fbin << std::endl;

    return 0;
}
