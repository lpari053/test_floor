//
//  Features.cpp
//  labcom
//
//  Created by Yohann Tschudi on 15/02/2022.
//

#ifndef FEATURES_H_INCLUDED
#define FEATURES_H_INCLUDED

#include <vector>
#include <complex>
#include <iostream>
#include <numeric>
#include <valarray>

#include "Sensors.hpp"
#include "Features.hpp"

using namespace std;

class FeaturesCalculator {
    
public:
    // Constructor and destructor
    FeaturesCalculator();
    ~FeaturesCalculator();
    
    // Main functions
    bool computeSensor(Sensors*,int,int);
    Features* computeFeatureVertical();


private:
    vector<int> _nb_step;
    vector<double> _time;
    vector<double> _acc_norm;
    vector<double> _gyro_norm;
    vector<double> _acc_norm_nf;
    vector<double> _gyro_norm_nf;
    vector<double> _acc_x;
    vector<double> _acc_y;
    vector<double> _acc_z;
    vector<double> _gyro_x;
    vector<double> _gyro_y;
    vector<double> _gyro_z;

    vector<double> _mag_x;
    vector<double> _mag_y;
    vector<double> _mag_z;
    vector<double> _mag_norm;
    vector<double> _mag_norm_nf;

    vector<double> _baro;
    vector<double> _baro_norm;
    
    vector<double> denoiseTimeSeries(const vector<double>&);
    
    void rotateAndInsert(vector<int>&, double,int,int);
    void rotateAndInsert(vector<double>&, double);
    void rotateAndInsert(vector<int>&, int);
    vector<double> scalarProduct(const vector<double>&, double);
    vector<double> extractVector(const vector<double>&, int, int);
    vector<double> Insert(vector<double>&, double);
    double computeNorm(const vector<double>&);
    double computeNorm(const double& ,const double& ,const double& );

    double computeVariance(const vector<double>&);
    double computeVariance(const vector<double>&, const double&, int);

    vector<double> normalization(const vector<double>&);

    vector<double> cutVector(const vector<double>&,double);

    int fft_first_peak_index(const vector<double>&);

    double mean(const vector<double>&);

    double median(const vector<double>&);

    double median_absolute_deviation(const vector<double>&);

    double std(const vector<double>&);

    double mad(const vector<double>&);

    double arc(const vector<double>&,const vector<double>&,const vector<double>&);

    double aad(const vector<double>&);

    double kurtosis(const vector<double>&);

    double moyenneSecondHalf(const vector<double>&);

    double moyennePremierHalf(const vector<double>&);

    double differenceMeanHalf(const vector<double>&);

    double rms(const vector<double>&);

    double calculerPente(const vector<double>&);

    double skewness(const vector<double>&);

    double pc(const vector<double>&);

    double baroDifferenceFirstLast(const vector<double>&);


};

#endif // FEATURES_H_INCLUDED
