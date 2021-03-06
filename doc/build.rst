##################
Installation Guide
##################

This page gives instructions on how to build and install Secure XGBoost from scratch. Secure XGBoost has been tested only on Ubuntu 18.04, but it should also work with Ubuntu 16.04. It consists of three steps:

1. First install the Open Enclave SDK
2. Next install the Secure XGBoost dependencies
3. Then build Secure XGBoost from source. 

.. note:: Use of Git submodules

  XGBoost uses Git submodules to manage dependencies. So when you clone the repo, remember to specify ``--recursive`` option:

  .. code-block:: bash

   git clone --recursive https://github.com/mc2-project/mc2-xgboost.git

Please refer to the `Troubleshooting`_ section first if you have any problem
during installation. If the instructions do not work for you, please feel free
to open an issue on `GitHub <https://github.com/mc2-project/mc2-xgboost/issues>`_.

**Contents**

* `Installing the Open Enclave SDK`_

* `Installing Secure XGBoost Dependencies`_

* `Building Secure XGBoost`_

  - `Building the Targets`_
  - `Python Package Installation`_

* `Troubleshooting`_

*******************************
Installing the Open Enclave SDK
*******************************



1. The requirements are:

   - Open Enclave version 0.8.1
   - Intel SGX DCAP Driver version 1.21
   
   Follow the instructions `here <https://github.com/openenclave/openenclave/blob/master/docs/GettingStartedDocs/install_oe_sdk-Ubuntu_18.04.md>`_ to install the Intel SGX DCAP driver, and the Open Enclave packages and dependencies. 

   Alternatively, you may also acquire a VM with the required features pre-installed from `Azure Confidential Compute <https://azure.microsoft.com/en-us/solutions/confidential-compute/>`_; in this case, however, you may need to manually upgrade the SDK installed in the VM to version 0.8.1, and the DCAP driver to version 1.21:


   Confirm that Open Enclave is version 0.8.1:

   .. code-block:: bash
      
      sudo apt list open-enclave

   Confirm that the Intel SGX DCAP Driver is version 1.21:

   .. code-block:: bash

      modinfo intel_sgx

   If not, follow `these <https://github.com/openenclave/openenclave/blob/master/docs/GettingStartedDocs/install_oe_sdk-Ubuntu_18.04.md>`_ instructions to update.

2. Configure environment variables for Open Enclave SDK for Linux:

   .. code-block:: bash

      source /opt/openenclave/share/openenclave/openenclaverc

   Consider adding this line to your ``~/.bashrc`` to make the environment variables persist across sessions.

**************************************
Installing Secure XGBoost Dependencies 
**************************************

.. code-block:: bash

   sudo apt-get install -y libmbedtls-dev python3-pip
   pip3 install numpy pandas sklearn numproto grpcio grpcio-tools kubernetes   

Install cmake >= v3.11. E.g., the following commands install cmake v3.15.6.

.. code-block:: bash

   wget https://github.com/Kitware/CMake/releases/download/v3.15.6/cmake-3.15.6-Linux-x86_64.sh
   sudo bash cmake-3.15.6-Linux-x86_64.sh --skip-license --prefix=/usr/local

***********************
Building Secure XGBoost
***********************

Our goal is to build the shared library, along with the enclave:

- On Linux the target library is ``libxgboost.so``
- The target enclave is ``xgboost_enclave.signed``

The minimal building requirement is

- A recent C++ compiler supporting C++11 (g++-4.8 or higher)
- CMake 3.11 or higher

Building the Targets
==================

1. Clone the repository recursively:

   .. code-block:: bash

      git clone --recursive https://github.com/mc2-project/mc2-xgboost.git

2. Configure the enclave parameters in ``CMakeLists.txt``; these parameters are used by the Open Enclave SDK to configure the enclave build.

   * ``OE_DEBUG``: Set this parameter to 0 to build the enclave in release mode, or 1 to build in debug mode.
   * ``OE_NUM_HEAP_PAGES``: The amount of heap memory (in pages) committed to the enclave; this is the maximum amount of heap memory available to your enclave application.
   * ``OE_NUM_STACK_PAGES``: The amount of stack memory (in pages) committed to the enclave.
   * ``OE_NUM_TCS``: The number of enclave thread control structures; this is the maximum number of concurrent threads that can execute within the enclave.
   * ``OE_PRODUCT_ID``: Enclave product ID.
   * ``OE_SECURITY_VERSION``: Enclave security version number.

   More details on these parameters can be found `here <https://github.com/openenclave/openenclave/blob/master/docs/GettingStartedDocs/buildandsign.md>`_.

   We also provide some additional configuration options:

   * ``LOGGING``: Set this parameter to ``ON`` to enable logging within the enclave. This parameter requires ``OE_DEBUG`` to be set to 1.
   * ``SIMULATE``: Set this parameter to ``ON`` to build the enclave in simulation mode (for local development and testing, in case your machine does not support hardware enclaves). This parameter requires ``OE_DEBUG`` to be set to 1.
   * ``OBLIVIOUS``: Set this parameter to ``ON`` to perform model training and inference using data-oblivious algorithms (to mitigate access-pattern based side-channel attacks).


3. On Ubuntu, build the Secure XGBoost targets by running CMake:

   .. code-block:: bash

      cd mc2-xgboost
      mkdir -p build

      pushd build
      cmake ..
      make -j4
      popd


Python Package Installation
===========================

The Python package is located at ``python-package/``.

1. Install system-wide, which requires root permission:

.. code-block:: bash

  cd python-package; sudo python3 setup.py install

.. note:: Re-compiling Secure XGBoost

  If you recompiled Secure XGBoost, then you need to reinstall it again to make the new library take effect.

2. Set the environment variable ``PYTHONPATH`` to tell Python where to find
   the RPC library. For example, assume we cloned ``secure-xgboost`` on the home directory
   ``~``. then we can added the following line in ``~/.bashrc``.

.. code-block:: bash

   export PYTHONPATH=/path/to/mc2-xgboost/rpc


***************
Troubleshooting
***************

1. Compile failed after ``git pull``

   Please first update the submodules, clean all and recompile:

   .. code-block:: bash

     git submodule update && make clean_all && make -j4

2. ``Makefile: dmlc-core/make/dmlc.mk: No such file or directory``

   We need to recursively clone the submodule:

   .. code-block:: bash

     git submodule init
     git submodule update

   Alternatively, do another clone

   .. code-block:: bash

      git clone --recursive https://github.com/mc2-project/mc2-xgboost.git


