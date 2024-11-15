#!/bin/csh

python IceAgeMapandDriver.py 201901 small
python IceAgeMapandDriver.py 201902 small
python IceAgeMapandDriver.py 201903 small
python IceAgeMapandDriver.py 201904 small


python IceAgeMapandDriver.py 201901 large
python IceAgeMapandDriver.py 201902 large
python IceAgeMapandDriver.py 201903 large
python IceAgeMapandDriver.py 201904 large


python IceAgeMapandDriver.py 201901 diy
python IceAgeMapandDriver.py 201902 diy
python IceAgeMapandDriver.py 201903 diy
python IceAgeMapandDriver.py 201904 diy


python IceAgeMapandDriver.py 201901 broadcast
python IceAgeMapandDriver.py 201902 broadcast
python IceAgeMapandDriver.py 201903 broadcast
python IceAgeMapandDriver.py 201904 broadcast


./UploadIceImages.csh