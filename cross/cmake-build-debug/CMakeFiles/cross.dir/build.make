# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.9

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/karol/clion-2017.3/bin/cmake/bin/cmake

# The command to remove a file.
RM = /home/karol/clion-2017.3/bin/cmake/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/karol/workspace/playground/cross

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/karol/workspace/playground/cross/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/cross.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/cross.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/cross.dir/flags.make

CMakeFiles/cross.dir/csolv.cpp.o: CMakeFiles/cross.dir/flags.make
CMakeFiles/cross.dir/csolv.cpp.o: ../csolv.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/karol/workspace/playground/cross/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/cross.dir/csolv.cpp.o"
	/usr/bin/g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/cross.dir/csolv.cpp.o -c /home/karol/workspace/playground/cross/csolv.cpp

CMakeFiles/cross.dir/csolv.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/cross.dir/csolv.cpp.i"
	/usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/karol/workspace/playground/cross/csolv.cpp > CMakeFiles/cross.dir/csolv.cpp.i

CMakeFiles/cross.dir/csolv.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/cross.dir/csolv.cpp.s"
	/usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/karol/workspace/playground/cross/csolv.cpp -o CMakeFiles/cross.dir/csolv.cpp.s

CMakeFiles/cross.dir/csolv.cpp.o.requires:

.PHONY : CMakeFiles/cross.dir/csolv.cpp.o.requires

CMakeFiles/cross.dir/csolv.cpp.o.provides: CMakeFiles/cross.dir/csolv.cpp.o.requires
	$(MAKE) -f CMakeFiles/cross.dir/build.make CMakeFiles/cross.dir/csolv.cpp.o.provides.build
.PHONY : CMakeFiles/cross.dir/csolv.cpp.o.provides

CMakeFiles/cross.dir/csolv.cpp.o.provides.build: CMakeFiles/cross.dir/csolv.cpp.o


# Object files for target cross
cross_OBJECTS = \
"CMakeFiles/cross.dir/csolv.cpp.o"

# External object files for target cross
cross_EXTERNAL_OBJECTS =

cross: CMakeFiles/cross.dir/csolv.cpp.o
cross: CMakeFiles/cross.dir/build.make
cross: CMakeFiles/cross.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/karol/workspace/playground/cross/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable cross"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/cross.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/cross.dir/build: cross

.PHONY : CMakeFiles/cross.dir/build

CMakeFiles/cross.dir/requires: CMakeFiles/cross.dir/csolv.cpp.o.requires

.PHONY : CMakeFiles/cross.dir/requires

CMakeFiles/cross.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/cross.dir/cmake_clean.cmake
.PHONY : CMakeFiles/cross.dir/clean

CMakeFiles/cross.dir/depend:
	cd /home/karol/workspace/playground/cross/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/karol/workspace/playground/cross /home/karol/workspace/playground/cross /home/karol/workspace/playground/cross/cmake-build-debug /home/karol/workspace/playground/cross/cmake-build-debug /home/karol/workspace/playground/cross/cmake-build-debug/CMakeFiles/cross.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/cross.dir/depend
