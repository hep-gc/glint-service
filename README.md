glint-service (Currently for Openstack Havana)
=============

Pre-req 

1. ensure you have sudo/root on your installation machine

2. check that ports 8080 8483 9494 are open on your test machine 
(glint uses 9494, horizon-glint uses 8080, and to secure horizon glint (even for testing) we use stunnel on 9494)


3. Since glint is registered with openstack as a service, you will need openstack administrative access. 

   a. login to the openstack horizon interface as admin
   
   b. goto Access & Security pages
   
   c. select API Access tab
   
   d. click Download openstack rc file


Make sure the file is accessible from the filesystem used to install glint, the glint setup script will read in the 
file and set the environment variables ... you will be prompted for the admin password during the setup of glint at some point

once ports are opened and you have the rc file 
(or have the proper environment variable set with openstack credentials) 

... we can try an install

Install and Setup

1. Get a copy of the installation scripts (this is all you need)
git clone https://github.com/rd37/glint-service.git

2. Start Download, Install and Setup
cd glint-service
sudo python glint_setup.py install



(this takes about 10-15 minutes)

* you will be prompted for your sudo password

* you will be prompted for you openstack admin password ~5 mins into install:: (unless it was already setup in the environment, 

i.e. you executed user@glint$  source openstack-admin.rc   #before sudo python glint_setup.py install





