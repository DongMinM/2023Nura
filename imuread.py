from threading import Thread

from serial import Serial

from numpy import zeros
from numpy import int16, int32

from time import sleep



## raw imu data will be stored in this memory
raw_imu = zeros(65)

## header 
header_pass = 0
## index 
index = 0 
## bit shifting
shft8  = 2 ** 8
shft16 = 2 ** 16
shft24 = 2 ** 24

## weights
Ka = ( 1 / 32768.0 ) * 16
Kw = ( 1 / 32768.0 ) * 2000
Kt = ( 1 / 32768.0 ) * 180


class IMU(Serial, Thread):


    def __init__(self, port, baudrate=115200):

        super().__init__(port=port, baudrate=baudrate)

        self.reading = False

        self.daemon  = True


    def run(self):

        ## wait until flag goes on
        while not self.reading:
            sleep( 0.1 )

        ## the flag goes on start our reading sequence
        while self.reading:
            self.read()

    
    def read(self):

        data = super().read()[0]

        ## read header for the first time
        if ( header_pass == 0 ):

            if ( ( data == 85 ) and ( index == 0 ) ):
                raw_imu[index] = data
                index += 1

            if ( ( data == 81 ) and ( index == 1 ) ):
                raw_imu[index] = data
                index += 1

        ## after header, read data
        elif ( header_pass == 1 ):
            ## we have 8byte data => 64 bit
            if ( index < 65 ):
                raw_imu[index] = data
                index += 1
            ## after 65bit, it's the next data
            else:
                header_pass = 0
                index       = 0
                fin         = 1

                self.decode( )
        
        else:
            header_pass = 0
            index       = 0
            fin         = 0 


    def decode(self):
        ## decode acceleration
        ax = int16( raw_imu[3] * shft8 + raw_imu[2] ) / Ka
        ay = int16( raw_imu[5] * shft8 + raw_imu[4] ) / Ka
        az = int16( raw_imu[7] * shft8 + raw_imu[6] ) / Ka

        wx = int16( raw_imu[14] * shft8 + raw_imu[13] ) / Kw
        wy = int16( raw_imu[16] * shft8 + raw_imu[15] ) / Kw
        wz = int16( raw_imu[18] * shft8 + raw_imu[17] ) / Kw

        roll  = int16( raw_imu[25] * shft8 + raw_imu[24] ) / Kt
        pitch = int16( raw_imu[27] * shft8 + raw_imu[26] ) / Kt
        yaw   = int16( raw_imu[29] * shft8 + raw_imu[28] ) / Kt

        height = int32( raw_imu[42] * shft24 + raw_imu[41] * shft16 + raw_imu[40] * shft8 ) / 100

        raw_lon = int32( raw_imu[49] * shft24 + raw_imu[48] * shft16 + raw_imu[47] * shft8 + raw_imu[46] )
        raw_lat = int32( raw_imu[53] * shft24 + raw_imu[52] * shft16 + raw_imu[51] * shft8 + raw_imu[50] )

        speeds = int32( raw_imu[64] * shft24 + raw_imu[63] * shft16 + raw_imu[62] * shft8 + raw_imu[61] ) / 1000 * 3.6
        
        lon = ( raw_lon / 10000000 ) + ( raw_lon % 10000000) / 6000000.0
        lat = ( raw_lat / 10000000 ) + ( raw_lat % 10000000) / 6000000.0


if __name__ == "__main__":

    imuserial = IMU( port="/dev/ttyUSB0", baudrate=115200 )
    imuserial.start()