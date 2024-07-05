// Sensors.cpp
#include "Sensors.hpp"

Sensors::Sensors() : step(0),baro(0.0),_baro_norm(0.0),time(0.0),
_acc_x(0.0), _acc_y(0.0), _acc_z(0.0), _gyro_x(0.0), _gyro_y(0.0), _gyro_z(0.0),  _mag_x(0.0), _mag_y(0.0), _mag_z(0.0),
_acc_norm_nf(0.0), _gyro_norm_nf(0.0), _acc_norm(0.0), _gyro_norm(0.0), _mag_norm(0.0), _mag_norm_nf(0.0) {}

Sensors::Sensors(double time,int step,double baro,double acc_x, double acc_y, double acc_z, double gyro_x, double gyro_y, double gyro_z,double mag_x, double mag_y, double mag_z) :
time(time),step(step),baro(baro),_acc_x(acc_x), _acc_y(acc_y), _acc_z(acc_z), _gyro_x(gyro_x), _gyro_y(gyro_y), _gyro_z(gyro_z), _mag_x(mag_x), _mag_y(mag_y), _mag_z(mag_z), 
_acc_norm_nf(0.0), _gyro_norm_nf(0.0), _acc_norm(0.0), _gyro_norm(0.0), _mag_norm(0.0), _mag_norm_nf(0.0) {}

Sensors::~Sensors() {}

void Sensors::set_time(double time) {
    time = time;
}

double Sensors::get_time() const {
    return time;
}


void Sensors::set_step(int _step) {
    step = _step;
}

int Sensors::get_step() const {
    return step;
}

void Sensors::set_baro(double _baro) {
    baro = _baro;
}

double Sensors::get_baro() const {
    return baro;
}

void Sensors::set_baro_norm(double baro_norm) {
    _baro_norm = baro_norm;
}

double Sensors::get_baro_norm() const {
    return _baro_norm;
}

void Sensors::set_acc_x(double acc_x) {
    _acc_x = acc_x;
}

void Sensors::set_acc_y(double acc_y) {
    _acc_y = acc_y;
}

void Sensors::set_acc_z(double acc_z) {
    _acc_z = acc_z;
}

double Sensors::get_acc_x() const {
    return _acc_x;
}

double Sensors::get_acc_y() const {
    return _acc_y;
}

double Sensors::get_acc_z() const {
    return _acc_z;
}

void Sensors::set_acc_norm(double acc_norm) {
    _acc_norm = acc_norm;
}

double Sensors::get_acc_norm() const {
    return _acc_norm;
}

void Sensors::set_gyro_x(double gyro_x) {
    _gyro_x = gyro_x;
}

void Sensors::set_gyro_y(double gyro_y) {
    _gyro_y = gyro_y;
}

void Sensors::set_gyro_z(double gyro_z) {
    _gyro_z = gyro_z;
}

double Sensors::get_gyro_x() const {
    return _gyro_x;
}

double Sensors::get_gyro_y() const {
    return _gyro_y;
}

double Sensors::get_gyro_z() const {
    return _gyro_z;
}

void Sensors::set_gyro_norm(double gyro_norm) {
    _gyro_norm = gyro_norm;
}

double Sensors::get_gyro_norm() const {
    return _gyro_norm;
}

std::vector<double> Sensors::get_sensors_acc_gyro_xyz() const {
    std::vector<double> acc_gyro_xyz;
    acc_gyro_xyz.push_back(_acc_x);
    acc_gyro_xyz.push_back(_acc_y);
    acc_gyro_xyz.push_back(_acc_z);
    acc_gyro_xyz.push_back(_gyro_x);
    acc_gyro_xyz.push_back(_gyro_y);
    acc_gyro_xyz.push_back(_gyro_z);
    return acc_gyro_xyz;
}

std::vector<double> Sensors::get_sensors_acc_xyz() const {
    std::vector<double> acc_xyz;
    acc_xyz.push_back(_acc_x);
    acc_xyz.push_back(_acc_y);
    acc_xyz.push_back(_acc_z);
    return acc_xyz;
}

std::vector<double> Sensors::get_sensors_gyro_xyz() const {
    std::vector<double> gyro_xyz;
    gyro_xyz.push_back(_gyro_x);
    gyro_xyz.push_back(_gyro_y);
    gyro_xyz.push_back(_gyro_z);
    return gyro_xyz;
}


std::vector<double> Sensors::get_sensors_mag_xyz() const {
    std::vector<double> mag_xyz;
    mag_xyz.push_back(_mag_x);
    mag_xyz.push_back(_mag_y);
    mag_xyz.push_back(_mag_z);
    return mag_xyz;
}


void Sensors::set_mag_x(double mag_x) {
    _mag_x = mag_x;
}

void Sensors::set_mag_y(double mag_y) {
    _mag_y = mag_y;
}

void Sensors::set_mag_z(double mag_z) {
    _mag_z = mag_z;
}

double Sensors::get_mag_x() const {
    return _mag_x;
}

double Sensors::get_mag_y() const {
    return _mag_y;
}

double Sensors::get_mag_z() const {
    return _mag_z;
}

void Sensors::set_mag_norm(double mag_norm) {
    _mag_norm = mag_norm;
}

double Sensors::get_mag_norm() const {
    return _mag_norm;
}