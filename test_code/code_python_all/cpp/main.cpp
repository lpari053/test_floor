#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include "Sensors.hpp" 
#include "FeaturesCalculator.hpp"
#include "Features.hpp" 

/**
 * @brief Splits a string into a vector of substrings using a specified delimiter.
 * 
 * This function takes a string input and splits it into substrings based on a specified delimiter.
 * 
 * @param str The string to split, containing substrings separated by the delimiter.
 * @param delimiter The character used to separate the substrings in the input string.
 * @return A vector containing the individual substrings extracted from the input string.
 */
std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> tokens; // Vector to store the extracted substrings
    std::stringstream ss(str); // String stream to process the input string
    std::string token; // Temporary variable to hold each substring

    // Iterate through each substring separated by the delimiter
    while (std::getline(ss, token, delimiter)) {
        tokens.push_back(token); // Add the substring to the vector
    }

    return tokens; // Return the vector of substrings
}


/**
 * @brief Main function that links all classes and is launched from a batch file in the command line.
 * 
 * arg[1] path to the input file
 * arg[2] path to the output file
 * 
 * @param argc Number of command-line arguments.
 * @param argv Array of C-style strings containing the command-line arguments.
 * 
 * @return Integer representing the exit status of the program.
 */
int main(int argc, char *argv[]) {

    // Class Feature Calculator that will calculate features
    FeaturesCalculator featureCalc;

    // Class Features where features will be stored
    Features* features;

    // Get the path of the output txt file
    std::string output_fichier = argv[2];
    
    int seuil_time = std::stoi(argv[3]);
    int seuil_step = std::stoi(argv[4]);

    // Get the file which we want to read the data from
    std::ifstream fichier(argv[1]);
	
    // Create the output file based on its path
    std::ofstream outputFile(output_fichier); 

    // Initialize the label of the data that represent the input file
    string mode;
    
    // Print the name of the output file
    std::cout  <<  argv[2]  <<  std::endl;

    // Write the header of the ouptut file
    outputFile 
        <<  "mode;"
     <<  "acc_arc;"

        <<  "gyr_arc;"
 
        <<  "mag_arc;"
 
        <<  "acc_x_aad;"
        <<  "acc_x_mean;"
        <<  "acc_x_std;"
        <<  "acc_x_kurt;"
        <<  "acc_x_skew;"
 
       <<  "acc_y_aad;"
       <<  "acc_y_mean;"
       <<  "acc_y_std;"
        <<  "acc_y_kurt;"
        <<  "acc_y_skew;"
 
       <<  "acc_z_aad;"
       <<  "acc_z_mean;"
       <<  "acc_z_std;"
       <<  "acc_z_kurt;"
       <<  "acc_z_skew;"
 
        <<  "gyr_x_aad;"
        <<  "gyr_x_mean;"
        <<  "gyr_x_std;"
        <<  "gyr_x_kurt;"
        <<  "gyr_x_skew;"
 
       <<  "gyr_y_aad;"
       <<  "gyr_y_mean;"
       <<  "gyr_y_std;"
        <<  "gyr_y_kurt;"
        <<  "gyr_y_skew;"
 
       <<  "gyr_z_aad;"
       <<  "gyr_z_mean;"
       <<  "gyr_z_std;"
       <<  "gyr_z_kurt;"
       <<  "gyr_z_skew;"
 
        <<  "mag_x_aad;"
        <<  "mag_x_mean;"
        <<  "mag_x_std;"
        <<  "mag_x_kurt;"
        <<  "mag_x_skew;"
 
       <<  "mag_y_aad;"
       <<  "mag_y_mean;"
       <<  "mag_y_std;"
        <<  "mag_y_kurt;"
        <<  "mag_y_skew;"
 
       <<  "mag_z_aad;"
       <<  "mag_z_mean;"
       <<  "mag_z_std;"
       <<  "mag_z_kurt;"
       <<  "mag_z_skew;" 
 
       <<  "baro_aad;"
       <<  "baro_mean;"
       <<  "baro_std;"
       <<  "baro_kurt;"
       <<  "baro_skew ;"

         <<  "nb_step;"

        <<  "aad_acc_norm;"
        <<  "mean_acc_norm;"
        <<  "std_acc_norm;"
        <<  "kurt_acc_norm;"
        <<  "skew_acc_norm;"
       
       
        <<  "aad_gyro_norm;"
        <<  "mean_gyro_norm;"
        <<  "std_gyro_norm;"
        <<  "kurtosis_gyro_norm;"
        <<  "skewness_gyro_norm;"
  
        <<  "aad_mag_norm;"
        <<  "mean_mag_norm;"
        <<  "std_mag_norm;"
        <<  "kurt_mag_norm;"
        <<  "skew_mag_norm ;"

        <<  "var_acc_norm;"
        <<  "var_gyro_norm;"
        <<  "var_mag_norm;"
        <<  "var_baro_norm;"

        <<  "time_diff \n" ;



    std::vector<std::string> lines;
    std::string ligne;
    
// Read the input file and push each line into the vector
    while (std::getline(fichier, ligne)) {
        lines.push_back(ligne);
    }

    // Close the input file
    fichier.close();

    // Initialize the index of the current line to read and the line of beginning to read
    int current_line = 0;
    int ll = 0;

    // While we are not at the end of the lines to read, continue to compute the features according to some condition
    while (current_line != lines.size() - 1) {

        // Define the delimiter for each sensor data in a line
        char delimiter = ',';

        // Get the data for each sensor in a vector of strings
        std::vector<std::string> result = split(lines[current_line], delimiter);

        // Assign to each sensor data its value transformed as float or int where needed
        float acc_x = std::stof(result[1]);
        float acc_y = std::stof(result[2]);
        float acc_z = std::stof(result[3]);
        float gyr_x = std::stof(result[4]);
        float gyr_y = std::stof(result[5]);
        float gyr_z = std::stof(result[6]);
        float mag_x = std::stof(result[7]);
        float mag_y = std::stof(result[8]);
        float mag_z = std::stof(result[9]);
        float baro = std::stof(result[10]);
        float temps = std::stof(result[11]);
        float step = std::stof(result[12]);
        mode = result[0];
 // Update the index to read the next time
        current_line = current_line + 1;

        float value;
        char delim;

        // Create an object of class sensor with the sensor data obtained from reading a line of the file
        Sensors sensors(
            temps,
            step,
            baro,
            acc_x,
            acc_y,
            acc_z,
            gyr_x,
            gyr_y,
            gyr_z,
            mag_x,
            mag_y,
            mag_z
        );

        // Calculate if the data meets the condition needed (time >= 3 or step >= 2) to calculate the feature to put in the output file or not
        bool stage = featureCalc.computeSensor(&sensors,seuil_time,seuil_step);


    // When the condition is fulfilled  
    if (stage){
        // Update the beginning of the reading 
        ll = ll + 1;

        // Start reading only 2 indices after the beginning of the reading of the previous stage
        current_line = ll;

        // Compute the features considering the sensor data that has been stored from the beginning of the reading to the index where the condition was fulfilled
        Features *features = featureCalc.computeFeatureVertical();

        // Write the compute feature in the output file


        outputFile  <<  mode      <<  ";";  //Label of the data 

            //ARC feature
        outputFile  <<  features->get_acc_arc()      <<  ";"; 
        outputFile  <<  features->get_gyr_arc()      <<  ";";
        outputFile  <<  features->get_mag_arc()      <<  ";";

            //Accelerometer features
                // X axis Accelerometer
        outputFile  <<  features->get_acc_x_aad()      <<  ";";
        outputFile  <<  features->get_acc_x_mean()      <<  ";";
        outputFile  <<  features->get_acc_x_std()      <<  ";";
        outputFile  <<  features->get_acc_x_kurt()      <<  ";";
        outputFile  <<  features->get_acc_x_skew()      <<  ";";
                // Y axis Accelerometer
        outputFile  <<   features->get_acc_y_aad()      <<  ";";
        outputFile  <<   features->get_acc_y_mean()      <<  ";";
        outputFile  <<   features->get_acc_y_std()      <<  ";";
        outputFile  <<  features->get_acc_y_kurt()      <<  ";";
        outputFile  <<  features->get_acc_y_skew()      <<  ";";
                // Z axis Accelerometer
        outputFile  <<   features->get_acc_z_aad()      <<  ";";
        outputFile  <<   features->get_acc_z_mean()      <<  ";";
        outputFile  <<   features->get_acc_z_std()      <<  ";";
        outputFile  <<   features->get_acc_z_kurt()      <<  ";";
        outputFile  <<   features->get_acc_z_skew()      <<  ";";

            //Gyroscope features
                // X axis Gyrosocope
        outputFile  <<  features->get_gyr_x_aad()      <<  ";";
        outputFile  <<  features->get_gyr_x_mean()      <<  ";";
        outputFile  <<  features->get_gyr_x_std()      <<  ";";
        outputFile  <<  features->get_gyr_x_kurt()      <<  ";";
        outputFile  <<  features->get_gyr_x_skew()      <<  ";";
                // Y axis Gyrosocope
        outputFile  <<   features->get_gyr_y_aad()      <<  ";";
        outputFile  <<   features->get_gyr_y_mean()      <<  ";";
        outputFile  <<   features->get_gyr_y_std()      <<  ";";
        outputFile  <<  features->get_gyr_y_kurt()      <<  ";";
        outputFile  <<  features->get_gyr_y_skew()      <<  ";";
                // Z axis Gyrosocope
        outputFile  <<   features->get_gyr_z_aad()      <<  ";";
        outputFile  <<   features->get_gyr_z_mean()      <<  ";";
        outputFile  <<   features->get_gyr_z_std()      <<  ";";
        outputFile  <<   features->get_gyr_z_kurt()      <<  ";";
        outputFile  <<   features->get_gyr_z_skew()      <<  ";";

            //Magnetometer features
                // X axis Magnetometer
        outputFile  <<  features->get_mag_x_aad()      <<  ";";
        outputFile  <<  features->get_mag_x_mean()      <<  ";";
        outputFile  <<  features->get_mag_x_std()      <<  ";";
        outputFile  <<  features->get_mag_x_kurt()      <<  ";";
        outputFile  <<  features->get_mag_x_skew()      <<  ";";

                // Y axis Magnetometer
        outputFile  <<   features->get_mag_y_aad()      <<  ";";
        outputFile  <<   features->get_mag_y_mean()      <<  ";";
        outputFile  <<   features->get_mag_y_std()      <<  ";";
        outputFile  <<  features->get_mag_y_kurt()      <<  ";";
        outputFile  <<  features->get_mag_y_skew()      <<  ";";

                // Z axis Magnetometer
        outputFile  <<   features->get_mag_z_aad()      <<  ";";
        outputFile  <<   features->get_mag_z_mean()      <<  ";";
        outputFile  <<   features->get_mag_z_std()      <<  ";";
        outputFile  <<   features->get_mag_z_kurt()      <<  ";";
        outputFile  <<   features->get_mag_z_skew()      <<  ";";

            // Barometer Features
        outputFile  <<   features->get_baro_aad()      <<  ";";
        outputFile  <<   features->get_baro_mean()      <<  ";";
        outputFile  <<   features->get_baro_std()      <<  ";";
        outputFile  <<   features->get_baro_kurt()      <<  ";";
        outputFile  <<   features->get_baro_skew()     <<  ";";

            // Extra fetaures
        outputFile  <<   features->get_nb_step()      <<  ";";

        // Features with the norm

            //Accelerometer Norm
        outputFile  <<   features->get_acc_norm_aad()      <<  ";";
        outputFile  <<   features->get_acc_norm_mean()      <<  ";";
        outputFile  <<   features->get_acc_norm_std()      <<  ";";
        outputFile  <<   features->get_acc_norm_kurt()      <<  ";";
        outputFile  <<   features->get_acc_norm_skew()      <<  ";";

            //Gyroscope  Norm
        outputFile  <<   features->get_gyro_norm_aad()      <<  ";";
        outputFile  <<   features->get_gyro_norm_mean()      <<  ";";
        outputFile  <<   features->get_gyro_norm_std()      <<  ";";
        outputFile  <<   features->get_gyro_norm_kurt()      <<  ";";
        outputFile  <<   features->get_gyro_norm_skew()      <<  ";";

            //Magnetometer Norm
        outputFile  <<   features->get_mag_norm_aad()      <<  ";";
        outputFile  <<   features->get_mag_norm_mean()      <<  ";";
        outputFile  <<   features->get_mag_norm_std()      <<  ";";
        outputFile  <<   features->get_mag_norm_kurt()      <<  ";";
        outputFile  <<   features->get_mag_norm_skew()  <<  ";" ;

        outputFile  <<   features->get_acc_norm_var()      <<  ";";
        outputFile  <<   features->get_gyro_norm_var()      <<  ";";
        outputFile  <<   features->get_mag_norm_var()      <<  ";";
        outputFile  <<   features->get_baro_norm_var()      <<  ";";


            //Time features
        outputFile  <<   features->get_time_diff() <<  "\n";

// Reinitiaize the features after they has been write
    delete features;

    }

} // No more line to read from, so no more compute


//Closing the output file that we have write in
outputFile.close();

}
    