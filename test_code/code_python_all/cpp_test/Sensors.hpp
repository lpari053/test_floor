// Sensors.hpp
#ifndef SENSORS_H
#define SENSORS_H

#include <vector>

class Sensors {
private:
double time;
    int step;
    double _acc_x;
    double _acc_y;
    double _acc_z;
    double _gyro_x;
    double _gyro_y;
    double _gyro_z;
    double _acc_norm_nf;
    double _gyro_norm_nf;
    double _acc_norm;
    double _gyro_norm;
     double _mag_x;
    double _mag_y;
    double _mag_z;
    double _mag_norm_nf;
    double _mag_norm;
    double baro;
    double _baro_norm;

public:
    Sensors();
    Sensors(double time,int step,double baro,double acc_x, double acc_y, double acc_z, double gyro_x, double gyro_y, double gyro_z,double mag_x, double mag_y, double mag_z);
    ~Sensors();


    void set_step(int _step);
    int get_step() const;
    
void set_time(double time);
    double get_time() const;

    void set_baro(double _baro);
    double get_baro() const;
    
    void set_baro_norm(double _baro_norm);
    double get_baro_norm() const;

    // Accelerometer
    void set_acc_x(double acc_x);
    void set_acc_y(double acc_y);
    void set_acc_z(double acc_z);
    double get_acc_x() const;
    double get_acc_y() const;
    double get_acc_z() const;

    void set_acc_norm(double acc_norm);
    double get_acc_norm() const;

    // Gyroscope
    void set_gyro_x(double gyro_x);
    void set_gyro_y(double gyro_y);
    void set_gyro_z(double gyro_z);
    double get_gyro_x() const;
    double get_gyro_y() const;
    double get_gyro_z() const;

    void set_gyro_norm(double gyro_norm);
    double get_gyro_norm() const;

    std::vector<double> get_sensors_acc_gyro_xyz() const;
    std::vector<double> get_sensors_acc_xyz() const;
    std::vector<double> get_sensors_gyro_xyz() const;


    void set_mag_x(double mag_x);
    void set_mag_y(double mag_y);
    void set_mag_z(double mag_z);
    double get_mag_x() const;
    double get_mag_y() const;
    double get_mag_z() const;

    void set_mag_norm(double mag_norm);
    double get_mag_norm() const;

    std::vector<double> get_sensors_mag_xyz() const;


};

#endif /* SENSORS_H */
