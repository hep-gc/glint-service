from distutils.core import setup

config_dir = "/etc/glint/"
config_files = []
config_files.append("glint-service/glint_services.yaml")
config_files.append("glint-service/glint_setup.yaml")

#etc_init_dir = "/etc/init.d/"
#etc_init_files = []
#etc_init_files.append("glint-service/openstack-glint")
#etc_init_files.append("glint-service/openstack-glint-horizon")
#etc_init_files.append("glint-service/openstack-glint-stunnel")

#df = [(config_dir,config_files),(etc_init_dir,etc_init_files)]
df = [(config_dir,config_files)]

setup(
    name = "glint-service",
    packages = ["glint-service"],
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        'glint-service': ['dev_https','glint','glint-horizon','openstack-glint','openstack-glint-horizon','openstack-glint-stunnel'],
        # And include any *.msg files found in the 'hello' package, too:
        #'hello': ['*.msg'],
    },
    data_files=df,
    version = "2013.2.4.12.dev",
    author = "Ron Desmarais",
    author_email = "rd@uvic.ca",
    url = "https://github.com/hep-gc/glint-service",
    download_url = "https://github.com/hep-gc/glint-service",
    keywords = ["encoding", "i18n", "xml"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Environment :: Other Environment",
        #"Framework :: Openstack",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        #"Topic :: Cloud Computing :: Image Distribution",
        ],
    #scripts = ['glint-service/glint','glint-service/glint-horizon'],
    long_description = """\
Universal character encoding detector
-------------------------------------

Manages
 - Openstack based cloud images
 - Multi-site User Credentials
 - Images Transfers between clouds

This version requires Python 2.
"""
)
