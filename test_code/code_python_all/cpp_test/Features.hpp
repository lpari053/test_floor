#ifndef FEATURES_HPP
#define FEATURES_HPP

class Features {
public:
    // Constructors
    Features();

    // Destructor
    ~Features();

    //Getter and setter for each Feature

        //Getter and Setter ACC norm

    void set_acc_norm_var(double acc_norm_var);
    double get_acc_norm_var() const;
    void set_gyro_norm_var(double gyro_norm_var);
    double get_gyro_norm_var() const;
    void set_mag_norm_var(double mag_norm_var);
    double get_mag_norm_var() const;
    void set_baro_norm_var(double baro_norm_var);
    double get_baro_norm_var() const;

    void set_acc_norm_mean(double acc_norm_mean);
    double get_acc_norm_mean() const;

    void set_acc_norm_aad(double acc_norm_aad);
    double get_acc_norm_aad() const;

    void set_acc_norm_std(double acc_norm_std);
    double get_acc_norm_std() const;

    void set_acc_norm_kurt(double acc_norm_kurt);
    double get_acc_norm_kurt() const;

    void set_acc_norm_skew(double acc_norm_skew);
    double get_acc_norm_skew() const;

        //Getter and Setter Gyro norm
    void set_gyro_norm_mean(double gyro_norm_mean);
    double get_gyro_norm_mean() const;

    void set_gyro_norm_aad(double gyro_norm_aad);
    double get_gyro_norm_aad() const;

    void set_gyro_norm_std(double gyro_norm_std);
    double get_gyro_norm_std() const;

    void set_gyro_norm_kurt(double gyro_norm_kurt);
    double get_gyro_norm_kurt() const;

    void set_gyro_norm_skew(double gyro_norm_skew);
    double get_gyro_norm_skew() const;

            //Getter and Setter Mag norm
void set_mag_norm_mean(double mag_norm_mean);
    double get_mag_norm_mean() const;

    void set_mag_norm_aad(double mag_norm_aad);
    double get_mag_norm_aad() const;

    void set_mag_norm_std(double mag_norm_std);
    double get_mag_norm_std() const;

    void set_mag_norm_kurt(double mag_norm_kurt);
    double get_mag_norm_kurt() const;

    void set_mag_norm_skew(double mag_norm_skew);
    double get_mag_norm_skew() const;

//Getter and Setter ACC 
    void set_acc_x_mean(double acc_x_mean);
    double get_acc_x_mean() const;

    void set_acc_y_mean(double acc_y_mean);
    double get_acc_y_mean() const;

    void set_acc_z_mean(double acc_z_mean);
    double get_acc_z_mean() const;



    void set_acc_x_std(double acc_x_std);
    double get_acc_x_std() const;

    void set_acc_y_std(double acc_y_std);
    double get_acc_y_std() const;

    void set_acc_z_std(double acc_z_std);
    double get_acc_z_std() const;



    void set_acc_x_skew(double acc_x_skew);
    double get_acc_x_skew() const;

    void set_acc_y_skew(double acc_y_skew);
    double get_acc_y_skew() const;

    void set_acc_z_skew(double acc_z_skew);
    double get_acc_z_skew() const ;



    void set_acc_x_kurt(double acc_x_kurt);
    double get_acc_x_kurt() const;

    void set_acc_y_kurt(double acc_y_kurt);
    double get_acc_y_kurt() const;

    void set_acc_z_kurt(double acc_z_kurt);
    double get_acc_z_kurt() const ;



    void set_acc_x_aad(double acc_x_aad);
    double get_acc_x_aad() const;

    void set_acc_y_aad(double acc_y_aad);
    double get_acc_y_aad() const;

    void set_acc_z_aad(double acc_z_aad);
    double get_acc_z_aad() const ;



    void set_acc_arc(double acc_x_arc) ;
    double get_acc_arc() const;


//Getter and Setter GYR 

 void set_gyr_x_mean(double gyr_x_mean);
    double get_gyr_x_mean() const;

    void set_gyr_y_mean(double gyr_y_mean);
    double get_gyr_y_mean() const;

    void set_gyr_z_mean(double gyr_z_mean);
    double get_gyr_z_mean() const;



    void set_gyr_x_std(double gyr_x_std);
    double get_gyr_x_std() const;

    void set_gyr_y_std(double gyr_y_std);
    double get_gyr_y_std() const;

    void set_gyr_z_std(double gyr_z_std);
    double get_gyr_z_std() const;



    void set_gyr_x_skew(double gyr_x_skew);
    double get_gyr_x_skew() const;

    void set_gyr_y_skew(double gyr_y_skew);
    double get_gyr_y_skew() const;

    void set_gyr_z_skew(double gyr_z_skew);
    double get_gyr_z_skew() const ;



    void set_gyr_x_kurt(double gyr_x_kurt);
    double get_gyr_x_kurt() const;

    void set_gyr_y_kurt(double gyr_y_kurt);
    double get_gyr_y_kurt() const;

    void set_gyr_z_kurt(double gyr_z_kurt);
    double get_gyr_z_kurt() const ;



    void set_gyr_x_aad(double gyr_x_aad);
    double get_gyr_x_aad() const;

    void set_gyr_y_aad(double gyr_y_aad);
    double get_gyr_y_aad() const;

    void set_gyr_z_aad(double gyr_z_aad);
    double get_gyr_z_aad() const ;



    void set_gyr_x_pc(double gyr_x_pc);
    double get_gyr_x_pc() const;

    void set_gyr_y_pc(double gyr_y_pc);
    double get_gyr_y_pc() const;

    void set_gyr_z_pc(double gyr_z_pc);
    double get_gyr_z_pc() const;



    void set_gyr_arc(double gyr_x_arc) ;
    double get_gyr_arc() const;


//Getter and Setter MAG

void set_mag_x_mean(double mag_x_mean);
    double get_mag_x_mean() const;

    void set_mag_y_mean(double mag_y_mean);
    double get_mag_y_mean() const;

    void set_mag_z_mean(double mag_z_mean);
    double get_mag_z_mean() const;



    void set_mag_x_std(double mag_x_std);
    double get_mag_x_std() const;

    void set_mag_y_std(double mag_y_std);
    double get_mag_y_std() const;

    void set_mag_z_std(double mag_z_std);
    double get_mag_z_std() const;



    void set_mag_x_skew(double mag_x_skew);
    double get_mag_x_skew() const;

    void set_mag_y_skew(double mag_y_skew);
    double get_mag_y_skew() const;

    void set_mag_z_skew(double mag_z_skew);
    double get_mag_z_skew() const ;



    void set_mag_x_kurt(double mag_x_kurt);
    double get_mag_x_kurt() const;

    void set_mag_y_kurt(double mag_y_kurt);
    double get_mag_y_kurt() const;

    void set_mag_z_kurt(double mag_z_kurt);
    double get_mag_z_kurt() const ;



    void set_mag_x_aad(double mag_x_aad);
    double get_mag_x_aad() const;

    void set_mag_y_aad(double mag_y_aad);
    double get_mag_y_aad() const;

    void set_mag_z_aad(double mag_z_aad);
    double get_mag_z_aad() const ;



    void set_mag_arc(double mag_x_arc) ;
    double get_mag_arc() const;


//Getter and Setter BARO 
void set_baro_mean(double baro_mean);
    double get_baro_mean() const ;


    void set_baro_std(double baro_std);
    double get_baro_std() const ;


    void set_baro_skew(double baro_skew);
    double get_baro_skew() const;


    void set_baro_kurt(double baro_kurt);
    double get_baro_kurt() const;


    void set_baro_aad(double baro_aad);
    double get_baro_aad() const;


    void set_baro_diffFirstLast(double baro_diffFirstLast);
    double get_baro_diffFirstLast() const;


    void set_baro_pente(double baro_pente);
    double get_baro_pente() const;

//Getter and Setter Extra Features
    void set_time_diff(double time_diff);
        double get_time_diff() const;

    void set_time(double time);
        double get_time() const;

    void set_nb_step(int nb_step);
        int get_nb_step() const;


// Attribut for each feature
private:
    double _acc_norm_mean;
    double _acc_norm_std;
    double _acc_norm_mad;
    double _acc_norm_kurt;
    double _acc_norm_skew;
    double _acc_norm_aad;

    double _gyro_norm_mean;
    double _gyro_norm_std;
    double _gyro_norm_mad;
    double _gyro_norm_kurt;
    double _gyro_norm_skew;
    double _gyro_norm_aad;

    double _mag_norm_mean;
    double _mag_norm_std;
    double _mag_norm_mad;
    double _mag_norm_kurt;
    double _mag_norm_skew;
    double _mag_norm_aad;



    double _acc_x_mean;
    double _acc_y_mean;
    double _acc_z_mean;

    double _gyr_x_mean;
    double _gyr_y_mean;
    double _gyr_z_mean;


    double _mag_x_mean;
    double _mag_y_mean;
    double _mag_z_mean;

    double _baro_mean;

    double _acc_x_std;
    double _acc_y_std;
    double _acc_z_std;

    double _gyr_x_std;
    double _gyr_y_std;
    double _gyr_z_std;


    double _mag_x_std;
    double _mag_y_std;
    double _mag_z_std;

    double _baro_std;

    double _acc_x_skew;
    double _acc_y_skew;
    double _acc_z_skew;

    double _gyr_x_skew;
    double _gyr_y_skew;
    double _gyr_z_skew;


    double _mag_x_skew;
    double _mag_y_skew;
    double _mag_z_skew;

    double _baro_skew;

    double _acc_x_kurt;
    double _acc_y_kurt;
    double _acc_z_kurt;

    double _gyr_x_kurt;
    double _gyr_y_kurt;
    double _gyr_z_kurt;


    double _mag_x_kurt;
    double _mag_y_kurt;
    double _mag_z_kurt;

    double _baro_kurt;

    double _acc_x_aad;
    double _acc_y_aad;
    double _acc_z_aad;

    double _gyr_x_aad;
    double _gyr_y_aad;
    double _gyr_z_aad;


    double _mag_x_aad;
    double _mag_y_aad;
    double _mag_z_aad;

    double _baro_aad;


    double _acc_arc;
    double _gyr_arc;
    double _mag_arc;

    double _baro_mad;
    double _baro_diffFirstLast;
    double _baro_pente;

    double _time_diff;
    int nb_step;
    double time;

    double acc_norm_var;
    double gyro_norm_var;
    double mag_norm_var;
    double baro_norm_var;


};

#endif // FEATURES_HPP
  
























