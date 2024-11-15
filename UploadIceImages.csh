#!/bin/csh

set pk=(/home/ubuntu/.ssh/NewEarl.pem)

cd /work/NSIDC_Ice/Images/

#Upload all of the images
scp -i $pk -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./01-small/* ubuntu@3.231.241.65:/var/www/Images/NewDSImages/IceSnow--Weekly--Sea-Ice-Age--Arctic/01-small/
scp -i $pk -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./02-large/* ubuntu@3.231.241.65:/var/www/Images/NewDSImages/IceSnow--Weekly--Sea-Ice-Age--Arctic/02-large/
scp -i $pk -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./04-full_res_zips/* ubuntu@3.231.241.65:/var/www/Images/NewDSImages/IceSnow--Weekly--Sea-Ice-Age--Arctic/04-full_res_zips/
scp -i $pk -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./03-broadcast/* ubuntu@3.231.241.65:/var/www/Images/NewDSImages/IceSnow--Weekly--Sea-Ice-Age--Arctic/03-broadcast/

#Now for local cleanup
rm ./*/IceSnow*



