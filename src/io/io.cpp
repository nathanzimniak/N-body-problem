#include "io.hpp"

#include <hdf5.h>

#include <cstdio>
#include <filesystem>
#include <string>
#include <vector>

void save_state_hdf5(
    const State& state,
    int step,
    double time,
    const std::string& output_path
) {
    // Create the output directory if it does not already exist.
    std::filesystem::create_directories(output_path);

    // Construct the output file path for the current step.
    char filename[64];
    std::snprintf(filename, sizeof(filename), "output_%06d.h5", step);
    const std::string file_path = output_path + "/" + filename;

    // Create the HDF5 file for this iteration.
    const hid_t file_id = H5Fcreate(file_path.c_str(), H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);

    // Define the dataspace shared by all state vectors.
    const hsize_t num_bodies = state.x.size();
    const hid_t dataspace_id = H5Screate_simple(1, &num_bodies, nullptr);

    // Write one vector-valued dataset to the file.
    const auto write_dataset = [&](const std::string& dataset_name, const std::vector<double>& data) {
        const hid_t dataset_id = H5Dcreate2(
            file_id,
            dataset_name.c_str(),
            H5T_NATIVE_DOUBLE,
            dataspace_id,
            H5P_DEFAULT,
            H5P_DEFAULT,
            H5P_DEFAULT
        );
        H5Dwrite(dataset_id, H5T_NATIVE_DOUBLE, H5S_ALL, H5S_ALL, H5P_DEFAULT, data.data());
        H5Dclose(dataset_id);
    };

    // Write each component of the state.
    write_dataset("x", state.x);
    write_dataset("y", state.y);
    write_dataset("z", state.z);
    write_dataset("vx", state.vx);
    write_dataset("vy", state.vy);
    write_dataset("vz", state.vz);

    // Write the current simulation time as a file attribute.
    const hsize_t attribute_size = 1;
    const hid_t attribute_space_id = H5Screate_simple(1, &attribute_size, nullptr);
    const hid_t attribute_id = H5Acreate2(
        file_id,
        "time",
        H5T_NATIVE_DOUBLE,
        attribute_space_id,
        H5P_DEFAULT,
        H5P_DEFAULT
    );
    H5Awrite(attribute_id, H5T_NATIVE_DOUBLE, &time);
    H5Aclose(attribute_id);
    H5Sclose(attribute_space_id);

    // Release HDF5 resources.
    H5Sclose(dataspace_id);
    H5Fclose(file_id);
}
