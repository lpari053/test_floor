#include "Features.hpp"

// Constructors
Features::Features():


//Initialization of each features


//Acc norm Features
_acc_norm_aad(0.0),_acc_norm_kurt(0.0),
_acc_norm_mean(0.0),
_acc_norm_skew(0.0),_acc_norm_mad(0.0),_acc_norm_std(0.0),acc_norm_var(0.0),

//Gyro norm Features
_gyro_norm_aad(0.0),_gyro_norm_kurt(0.0),
_gyro_norm_mean(0.0),
_gyro_norm_skew(0.0),_gyro_norm_mad(0.0),_gyro_norm_std(0.0),gyro_norm_var(0.0),

//Mag norm Features
_mag_norm_aad(0.0),_mag_norm_kurt(0.0),
_mag_norm_mean(0.0),
_mag_norm_skew(0.0),_mag_norm_mad(0.0),_mag_norm_std(0.0),mag_norm_var(0.0),


//Acc X Features
_acc_x_aad(0.0),_acc_arc(0.0),_acc_x_kurt(0.0),
_acc_x_mean(0.0),
_acc_x_skew(0.0),_acc_x_std(0.0),

//Acc Y Features
_acc_y_aad(0.0),_acc_y_kurt(0.0),
_acc_y_mean(0.0),
_acc_y_skew(0.0),_acc_y_std(0.0),

//Acc Z Features
_acc_z_aad(0.0),_acc_z_kurt(0.0),
_acc_z_mean(0.0),
_acc_z_skew(0.0),_acc_z_std(0.0),

//Gyro X Features
_gyr_x_aad(0.0),_gyr_arc(0.0),_gyr_x_kurt(0.0),
_gyr_x_mean(0.0),
_gyr_x_skew(0.0),_gyr_x_std(0.0),

//Gyro Y Features
_gyr_y_aad(0.0),_gyr_y_kurt(0.0),
_gyr_y_mean(0.0),
_gyr_y_skew(0.0),_gyr_y_std(0.0),

//Gyro Z Features
_gyr_z_aad(0.0),_gyr_z_kurt(0.0),
_gyr_z_mean(0.0),
_gyr_z_skew(0.0),_gyr_z_std(0.0),

//Mag X Features
_mag_x_aad(0.0),_mag_arc(0.0),_mag_x_kurt(0.0),
_mag_x_mean(0.0),
_mag_x_skew(0.0),_mag_x_std(0.0),

//Mag Y Features
_mag_y_aad(0.0),_mag_y_kurt(0.0),
_mag_y_mean(0.0),
_mag_y_skew(0.0),_mag_y_std(0.0),

//Mag Z Features
_mag_z_aad(0.0),_mag_z_kurt(0.0),
_mag_z_mean(0.0),
_mag_z_skew(0.0),_mag_z_std(0.0),

//Baro Features
_baro_aad(0.0),_baro_kurt(0.0),_baro_mean(0.0),_baro_skew(0.0),
_baro_std(0.0) ,_baro_diffFirstLast(0.0),_baro_pente(0.0),baro_norm_var(0.0),


//Extra Features
time(0.0),_time_diff(0.0),nb_step(0)               


{}


//Destructor
Features::~Features() {}

void Features::set_acc_norm_var(double acc_norm_var) {
    this->acc_norm_var = acc_norm_var;
}
double Features::get_acc_norm_var() const {
    return this->acc_norm_var;
}
void Features::set_gyro_norm_var(double gyro_norm_var) {
    this->gyro_norm_var = gyro_norm_var;
}
double Features::get_gyro_norm_var() const {
    return this->gyro_norm_var;
}
void Features::set_mag_norm_var(double mag_norm_var) {
    this->mag_norm_var = mag_norm_var;
}
double Features::get_mag_norm_var() const {
    return this->mag_norm_var;
}
void Features::set_baro_norm_var(double baro_norm_var) {
    this->baro_norm_var = baro_norm_var;
}
double Features::get_baro_norm_var() const {
    return this->baro_norm_var;
}



// Getteur et Setteur for each features


void Features::set_acc_norm_mean(double acc_norm_mean) {
    this->_acc_norm_mean = acc_norm_mean;
}
double Features::get_acc_norm_mean() const {
    return this->_acc_norm_mean;
}

void Features::set_acc_norm_std(double acc_norm_std) {
    this->_acc_norm_std = acc_norm_std;
}
double Features::get_acc_norm_std() const {
    return this->_acc_norm_std;
}

void Features::set_acc_norm_kurt(double acc_norm_kurt) {
    this->_acc_norm_kurt = acc_norm_kurt;
}
double Features::get_acc_norm_kurt() const {
    return this->_acc_norm_kurt;
}

void Features::set_acc_norm_skew(double acc_norm_skew) {
    this->_acc_norm_skew = acc_norm_skew;
}
double Features::get_acc_norm_skew() const {
    return this->_acc_norm_skew;
}

void Features::set_acc_norm_aad(double acc_norm_aad) {
    this->_acc_norm_aad = acc_norm_aad;
}
double Features::get_acc_norm_aad() const {
    return this->_acc_norm_aad;
}


void Features::set_gyro_norm_mean(double gyro_norm_mean) {
    this->_gyro_norm_mean = gyro_norm_mean;
}
double Features::get_gyro_norm_mean() const {
    return this->_gyro_norm_mean;
}

void Features::set_gyro_norm_std(double gyro_norm_std) {
    this->_gyro_norm_std = gyro_norm_std;
}
double Features::get_gyro_norm_std() const {
    return this->_gyro_norm_std;
}


void Features::set_gyro_norm_kurt(double gyro_norm_kurt) {
    this->_gyro_norm_kurt = gyro_norm_kurt;
}
double Features::get_gyro_norm_kurt() const {
    return this->_gyro_norm_kurt;
}

void Features::set_gyro_norm_skew(double gyro_norm_skew) {
    this->_gyro_norm_skew = gyro_norm_skew;
}
double Features::get_gyro_norm_skew() const {
    return this->_gyro_norm_skew;
}

void Features::set_gyro_norm_aad(double gyro_norm_aad) {
    this->_gyro_norm_aad = gyro_norm_aad;
}
double Features::get_gyro_norm_aad() const {
    return this->_gyro_norm_aad;
}


void Features::set_mag_norm_mean(double mag_norm_mean) {
    this->_mag_norm_mean = mag_norm_mean;
}
double Features::get_mag_norm_mean() const {
    return this->_mag_norm_mean;
}

void Features::set_mag_norm_std(double mag_norm_std) {
    this->_mag_norm_std = mag_norm_std;
}
double Features::get_mag_norm_std() const {
    return this->_mag_norm_std;
}

void Features::set_mag_norm_kurt(double mag_norm_kurt) {
    this->_mag_norm_kurt = mag_norm_kurt;
}
double Features::get_mag_norm_kurt() const {
    return this->_mag_norm_kurt;
}

void Features::set_mag_norm_skew(double mag_norm_skew) {
    this->_mag_norm_skew = mag_norm_skew;
}
double Features::get_mag_norm_skew() const {
    return this->_mag_norm_skew;
}

void Features::set_mag_norm_aad(double mag_norm_aad) {
    this->_mag_norm_aad = mag_norm_aad;
}
double Features::get_mag_norm_aad() const {
    return this->_mag_norm_aad;
}




void Features::set_nb_step(int _nb_step) {
    this->nb_step = _nb_step;
}
int Features::get_nb_step() const {
    return this->nb_step;
}

void Features::set_acc_x_mean(double acc_x_mean) {
    this->_acc_x_mean = acc_x_mean;
}
double Features::get_acc_x_mean() const {
    return this->_acc_x_mean;
}

void Features::set_acc_y_mean(double acc_y_mean) {
    this->_acc_y_mean = acc_y_mean;
}
double Features::get_acc_y_mean() const {
    return this->_acc_y_mean;
}

void Features::set_acc_z_mean(double acc_z_mean) {
    this->_acc_z_mean = acc_z_mean;
}
double Features::get_acc_z_mean() const {
    return this->_acc_z_mean;
}

void Features::set_gyr_x_mean(double gyr_x_mean) {
    this->_gyr_x_mean = gyr_x_mean;
}
double Features::get_gyr_x_mean() const {
    return this->_gyr_x_mean;
}

void Features::set_gyr_y_mean(double gyr_y_mean) {
    this->_gyr_y_mean = gyr_y_mean;
}
double Features::get_gyr_y_mean() const {
    return this->_gyr_y_mean;
}

void Features::set_gyr_z_mean(double gyr_z_mean) {
    this->_gyr_z_mean = gyr_z_mean;
}
double Features::get_gyr_z_mean() const {
    return this->_gyr_z_mean;
}

void Features::set_mag_x_mean(double mag_x_mean) {
    this->_mag_x_mean = mag_x_mean;
}
double Features::get_mag_x_mean() const {
    return this->_mag_x_mean;
}

void Features::set_mag_y_mean(double mag_y_mean) {
    this->_mag_y_mean = mag_y_mean;
}
double Features::get_mag_y_mean() const {
    return this->_mag_y_mean;
}

void Features::set_mag_z_mean(double mag_z_mean) {
    this->_mag_z_mean = mag_z_mean;
}
double Features::get_mag_z_mean() const {
    return this->_mag_z_mean;
}

void Features::set_baro_mean(double baro_mean) {
    this->_baro_mean = baro_mean;
}
double Features::get_baro_mean() const {
    return this->_baro_mean;
}

void Features::set_acc_x_std(double acc_x_std) {
    this->_acc_x_std = acc_x_std;
}
double Features::get_acc_x_std() const {
    return this->_acc_x_std;
}

void Features::set_acc_y_std(double acc_y_std) {
    this->_acc_y_std = acc_y_std;
}
double Features::get_acc_y_std() const {
    return this->_acc_y_std;
}

void Features::set_acc_z_std(double acc_z_std) {
    this->_acc_z_std = acc_z_std;
}
double Features::get_acc_z_std() const {
    return this->_acc_z_std;
}

void Features::set_gyr_x_std(double gyr_x_std) {
    this->_gyr_x_std = gyr_x_std;
}
double Features::get_gyr_x_std() const {
    return this->_gyr_x_std;
}

void Features::set_gyr_y_std(double gyr_y_std) {
    this->_gyr_y_std = gyr_y_std;
}
double Features::get_gyr_y_std() const {
    return this->_gyr_y_std;
}

void Features::set_gyr_z_std(double gyr_z_std) {
    this->_gyr_z_std = gyr_z_std;
}
double Features::get_gyr_z_std() const {
    return this->_gyr_z_std;
}

void Features::set_mag_x_std(double mag_x_std) {
    this->_mag_x_std = mag_x_std;
}
double Features::get_mag_x_std() const {
    return this->_mag_x_std;
}

void Features::set_mag_y_std(double mag_y_std) {
    this->_mag_y_std = mag_y_std;
}
double Features::get_mag_y_std() const {
    return this->_mag_y_std;
}

void Features::set_mag_z_std(double mag_z_std) {
    this->_mag_z_std = mag_z_std;
}
double Features::get_mag_z_std() const {
    return this->_mag_z_std;
}

void Features::set_baro_std(double baro_std) {
    this->_baro_std = baro_std;
}
double Features::get_baro_std() const {
    return this->_baro_std;
}

void Features::set_acc_x_skew(double acc_x_skew) {
    this->_acc_x_skew = acc_x_skew;
}
double Features::get_acc_x_skew() const {
    return this->_acc_x_skew;
}

// Skewness (suite)
void Features::set_acc_y_skew(double acc_y_skew) {
    this->_acc_y_skew = acc_y_skew;
}
double Features::get_acc_y_skew() const {
    return this->_acc_y_skew;
}

void Features::set_acc_z_skew(double acc_z_skew) {
    this->_acc_z_skew = acc_z_skew;
}
double Features::get_acc_z_skew() const {
    return this->_acc_z_skew;
}

void Features::set_gyr_x_skew(double gyr_x_skew) {
    this->_gyr_x_skew = gyr_x_skew;
}
double Features::get_gyr_x_skew() const {
    return this->_gyr_x_skew;
}

void Features::set_gyr_y_skew(double gyr_y_skew) {
    this->_gyr_y_skew = gyr_y_skew;
}
double Features::get_gyr_y_skew() const {
    return this->_gyr_y_skew;
}

void Features::set_gyr_z_skew(double gyr_z_skew) {
    this->_gyr_z_skew = gyr_z_skew;
}
double Features::get_gyr_z_skew() const {
    return this->_gyr_z_skew;
}

void Features::set_mag_x_skew(double mag_x_skew) {
    this->_mag_x_skew = mag_x_skew;
}
double Features::get_mag_x_skew() const {
    return this->_mag_x_skew;
}

void Features::set_mag_y_skew(double mag_y_skew) {
    this->_mag_y_skew = mag_y_skew;
}
double Features::get_mag_y_skew() const {
    return this->_mag_y_skew;
}

void Features::set_mag_z_skew(double mag_z_skew) {
    this->_mag_z_skew = mag_z_skew;
}
double Features::get_mag_z_skew() const {
    return this->_mag_z_skew;
}

void Features::set_baro_skew(double baro_skew) {
    this->_baro_skew = baro_skew;
}
double Features::get_baro_skew() const {
    return this->_baro_skew;
}

void Features::set_acc_x_kurt(double acc_x_kurt) {
    this->_acc_x_kurt = acc_x_kurt;
}
double Features::get_acc_x_kurt() const {
    return this->_acc_x_kurt;
}


void Features::set_acc_y_kurt(double acc_y_kurt) {
    this->_acc_y_kurt = acc_y_kurt;
}
double Features::get_acc_y_kurt() const {
    return this->_acc_y_kurt;
}

void Features::set_acc_z_kurt(double acc_z_kurt) {
    this->_acc_z_kurt = acc_z_kurt;
}
double Features::get_acc_z_kurt() const {
    return this->_acc_z_kurt;
}

void Features::set_gyr_x_kurt(double gyr_x_kurt) {
    this->_gyr_x_kurt = gyr_x_kurt;
}
double Features::get_gyr_x_kurt() const {
    return this->_gyr_x_kurt;
}

void Features::set_gyr_y_kurt(double gyr_y_kurt) {
    this->_gyr_y_kurt = gyr_y_kurt;
}
double Features::get_gyr_y_kurt() const {
    return this->_gyr_y_kurt;
}

void Features::set_gyr_z_kurt(double gyr_z_kurt) {
    this->_gyr_z_kurt = gyr_z_kurt;
}
double Features::get_gyr_z_kurt() const {
    return this->_gyr_z_kurt;
}

void Features::set_mag_x_kurt(double mag_x_kurt) {
    this->_mag_x_kurt = mag_x_kurt;
}
double Features::get_mag_x_kurt() const {
    return this->_mag_x_kurt;
}

void Features::set_mag_y_kurt(double mag_y_kurt) {
    this->_mag_y_kurt = mag_y_kurt;
}
double Features::get_mag_y_kurt() const {
    return this->_mag_y_kurt;
}

void Features::set_mag_z_kurt(double mag_z_kurt) {
    this->_mag_z_kurt = mag_z_kurt;
}
double Features::get_mag_z_kurt() const {
    return this->_mag_z_kurt;
}

void Features::set_baro_kurt(double baro_kurt) {
    this->_baro_kurt = baro_kurt;
}
double Features::get_baro_kurt() const {
    return this->_baro_kurt;
}

void Features::set_acc_x_aad(double acc_x_aad) {
    this->_acc_x_aad = acc_x_aad;
}
double Features::get_acc_x_aad() const {
    return this->_acc_x_aad;
}


void Features::set_acc_y_aad(double acc_y_aad) {
    this->_acc_y_aad = acc_y_aad;
}
double Features::get_acc_y_aad() const {
    return this->_acc_y_aad;
}

void Features::set_acc_z_aad(double acc_z_aad) {
    this->_acc_z_aad = acc_z_aad;
}
double Features::get_acc_z_aad() const {
    return this->_acc_z_aad;
}

void Features::set_gyr_x_aad(double gyr_x_aad) {
    this->_gyr_x_aad = gyr_x_aad;
}
double Features::get_gyr_x_aad() const {
    return this->_gyr_x_aad;
}

void Features::set_gyr_y_aad(double gyr_y_aad) {
    this->_gyr_y_aad = gyr_y_aad;
}
double Features::get_gyr_y_aad() const {
    return this->_gyr_y_aad;
}

void Features::set_gyr_z_aad(double gyr_z_aad) {
    this->_gyr_z_aad = gyr_z_aad;
}
double Features::get_gyr_z_aad() const {
    return this->_gyr_z_aad;
}

void Features::set_mag_x_aad(double mag_x_aad) {
    this->_mag_x_aad = mag_x_aad;
}
double Features::get_mag_x_aad() const {
    return this->_mag_x_aad;
}

void Features::set_mag_y_aad(double mag_y_aad) {
    this->_mag_y_aad = mag_y_aad;
}
double Features::get_mag_y_aad() const {
    return this->_mag_y_aad;
}

void Features::set_mag_z_aad(double mag_z_aad) {
    this->_mag_z_aad = mag_z_aad;
}
double Features::get_mag_z_aad() const {
    return this->_mag_z_aad;
}

void Features::set_baro_aad(double baro_aad) {
    this->_baro_aad = baro_aad;
}
double Features::get_baro_aad() const {
    return this->_baro_aad;
}


//ARC Features Getter Setter
void Features::set_acc_arc(double acc_arc) {
    this->_acc_arc = acc_arc;
}
double Features::get_acc_arc() const {
    return this->_acc_arc;
}


void Features::set_gyr_arc(double gyr_arc) {
    this->_gyr_arc = gyr_arc;
}
double Features::get_gyr_arc() const {
    return this->_gyr_arc;
}

void Features::set_mag_arc(double mag_arc) {
    this->_mag_arc = mag_arc;
}
double Features::get_mag_arc() const {
    return this->_mag_arc;
}





// EXTRA FEATURES
void Features::set_time_diff(double time_diff) {
    this->_time_diff = time_diff;
}
double Features::get_time_diff() const {
    return this->_time_diff;
}


void Features::set_time(double time) {
    this->time = time;
}
double Features::get_time() const {
    return this->time;
}

void Features::set_baro_diffFirstLast(double baro_diffFirstLast) {
    this->_baro_diffFirstLast = baro_diffFirstLast;
}
double Features::get_baro_diffFirstLast() const {
    return this->_baro_diffFirstLast;
}

void Features::set_baro_pente(double baro_pente) {
    this->_baro_pente = baro_pente;
}
double Features::get_baro_pente() const {
    return this->_baro_pente ;
}

