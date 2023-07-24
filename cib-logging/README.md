# CIB Logging

This project establishes a logging library and build system that fully supports the low-latency logging implementation showcased in the video below. The core of the logging functionality is already integrated within the [CIB library](https://github.com/intel/compile-time-init-build), included as a git submodule. My contributions encompass setting up the build system, which includes writing a Python file for parsing the undefined symbols and generating the template specialisations. Additionally, I've set up this repository as a template with a custom logging library, readily applicable to new projects with room for further customisation.

[![Embedded Logging Case Study: From C to Shining C++ - Luke Valenty -CppNow 2022](https://i3.ytimg.com/vi/Dt0vx-7e_B0/maxresdefault.jpg)](https://www.youtube.com/watch?v=Dt0vx-7e_B0)

## To Do
[] Test multiple library catalog generation