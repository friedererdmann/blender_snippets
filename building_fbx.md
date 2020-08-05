# Building the FBX Python SDK for Blender 2.8.x
## Introduction

Autodesk provides the FBX SDK free of charge on their website, both for C++ and Python. However, for the longest time, the SDK was only available for Python 2.7 and 3.3. This made it automatically incompatible with Blender 2.8.x, which is based on Python 3.7.4.

Recently, Autodesk changed course and released the SIP bindings for its SDK. This is making it possible for anyone to build the Python SDK against any Python version they want with limited effort. Building a version compatible with Blender 2.8.x is now easy - just follow the steps below!

### Licensing

You are responsible to adhere to the Autodesk FBX SDK's terms and conditions if you use it in your project or try and distribute it! While you can access a lot of code from the SDK, it does NOT make the SDK an open source project like Blender.

## Getting started

### On Windows

To start building your own FBX Python SDK, please make sure you have the following things setup:

* VisualStudio 2015 (Community Edition works)
  * Make sure you have the packages for Visual C++ and the Windows 10 SDK and Tools installed
  * You can download the Community Edition for free here, if you sign up for Visual Studio Dev Essentials for free
    * https://my.visualstudio.com/Downloads?q=visual%20studio%202015&wt.mc_id=o~msft~vscom~older-downloads
* Python 3.7.4 __64-bit__
  * https://www.python.org/downloads/release/python-374/

### On Linux

Get Python 3.7.4 from your distribution package manager or build it yourself from sources.

Under Linux, all references to `python` should be `python3` or `python3.7` instead (if you're building with Python 3).

#### Ubuntu (apt-get)
Install all packages below with `sudo apt-get install` and then the package name:
* `build-essential`
* `libsqlite3-dev`
* `libbz2-dev`
* `libxml2-dev`

> If the installation of any package fails, try to run `sudo apt-get update` first.

#### CentOS (yum)
The quickest way to install the required development packages is using `sudo yum groupinstall 'Development Tools'`.

Next you will also need `sudo yum install libxml2-devel`

## Download

* https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-0
  * FBX SDK Windows - FBX SDK 2020.0.1 VS2015
  * FBX Python Bindings - FBX SDK 2020.0.1 Python Windows
  * If you're building on Linux, get the packages for Linux instead
* https://www.riverbankcomputing.com/software/sip/download
  * Sip 4.9.13

## Setting up

### Install

Install the FBX SDK and the Python Bindings.

#### On Linux

Change the permissions for the installers if necessary to allow them to be executed. Start a terminal in the directory where you unpacked the installers and write `chmod ugo+x fbx20201_fbxpythonbindings_linux` and `chmod ugo+x fbx20201_fbxsdk_linux`.

Next you need to run the installers from the same terminal and provide the folder where to install as an argument to the installer. E.g. `./fbx20201_fbxpythonbindings_linux /home/user/Documents/fbx_python_bindings` (make sure the folder you're installing to exists before hand).

#### Folder setup on Windows
For ease of operations, create a directory in your documents or on a drive that doesn't require admin rights when you work.

* Unpack the Sip package to this directory, e.g.
  * E:\fbxsdk\sip
* Copy the contents of the FBX Python bindings from the installation, e.g.
  * C:\Program Files\Autodesk\FBX\FBX Python Bindings\2020.0.1, to:
  * E:\fbxsdk\fbx

### Environment Variables

Create these two environment variables:
* __FBXSDK_ROOT__
  * Set to the place where you installed the FBX SDK to, e.g.
  * _C:\Program Files\Autodesk\FBX\FBX SDK\2020.0.1_
  * _/home/user/Documents/fbx_sdk_
* __SIP_ROOT__
  * To the location that you unpacked the SIP package to, e.g.
  * _E:\fbxsdk\sip_
  * _/home/user/Documents/sip-4.19.13_
* __PATH (on Windows - can also be done temporarily)__
  * Make sure that Python 3.7 is the Python version that is referenced in the PATH variable, e.g.
  * _C:\Users\username\AppData\Local\Programs\Python\Python37\_

## Preparing Sip

In the directory where you unpacked Sip (in the example above __E:\fbxsdk\sip__) run `python configure.py` in your commandline.

> If you're using a recent Ubuntu Linux version find the `siputils.py` and navigate the line `libs.extend(self.optional_list("LIBS))` and move it in front of the loop `for l in self.extra_libs:`.
> Otherwise you might encounter an ImportError later stating that `fbx.so` has an `undefined symbol: xmlFree`.

## Building the FBX Python SDK

In the directory that you copied the FBX bindings to (in the example above __E:\fbxsdk\fbx__), run `python PythonBindings.py Python3_x64 buildsip` from the commandline. (Under Linux use `python3` instead of `python`)

## Copying the FBX SDK into place

Once the build step is done, the FBX Python SDK files will be in __build\Distrib\site-packages\fbx__ (e.g. _E:\fbxsdk\fbx\build\Distrib\site-packages\fbx_).
* `fbx.pyd`
* `FbxCommon.py`
* `sip.pyd`

Copy the files from there to the `site-packages` directory (so that you have `site-packages/fbx.pyd`/`fbx.so`) and you can then `import fbx`.
