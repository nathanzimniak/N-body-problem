#include "io.hpp"
#include <hdf5.h>
#include <filesystem>
#include <cstdio>
#include <vector>
#include <string>


void save_state_hdf5(
    const State& U,
    int step,
    double t,
    const std::string& path
) {
    // Create the directory if it doesn't exist (does nothing if it already exists).
    std::filesystem::create_directories(path);

    // Construct the complete file path.
    char filename[64];
    std::snprintf(filename, sizeof(filename), "output_%06d.h5", step);
    std::string filepath = path + "/" + filename;

    // Open (create) the file for this iteration.
    hid_t file_id = H5Fcreate(filepath.c_str(), H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);

    // Size of the arrays to write.
    hsize_t N = U.x.size();
    hid_t dataspace_id = H5Screate_simple(1, &N, nullptr);

    // Local lambda function to write a dataset.
    auto write_dataset = [&](const std::string& name, const std::vector<double>& data) {
        hid_t dataset_id = H5Dcreate2(file_id, name.c_str(),
                                       H5T_NATIVE_DOUBLE, dataspace_id,
                                       H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        H5Dwrite(dataset_id, H5T_NATIVE_DOUBLE,
                 H5S_ALL, H5S_ALL, H5P_DEFAULT, data.data());
        H5Dclose(dataset_id);
    };

    // Write each component of the state.
    write_dataset("x",  U.x);
    write_dataset("y",  U.y);
    write_dataset("z",  U.z);
    write_dataset("vx", U.vx);
    write_dataset("vy", U.vy);
    write_dataset("vz", U.vz);

    // Write the current time as an attribute of the file.
    hsize_t scalar = 1;
    hid_t scalar_space = H5Screate_simple(1, &scalar, nullptr);
    hid_t attr_id = H5Acreate2(file_id, "time",
                                H5T_NATIVE_DOUBLE, scalar_space,
                                H5P_DEFAULT, H5P_DEFAULT);
    H5Awrite(attr_id, H5T_NATIVE_DOUBLE, &t);
    H5Aclose(attr_id);
    H5Sclose(scalar_space);

    // Close the resources.
    H5Sclose(dataspace_id);
    H5Fclose(file_id);
}
