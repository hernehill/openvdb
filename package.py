name = "openvdb"

# version 12.0 is used by Maya 2026.3
version = "12.0.1.hh.1.0.0"

authors = [
    "DreamWorks & AcademySoftwareFoundation",
]

description = """Storage and manipulation of sparse volumetric data"""

with scope("config") as c:
    import os

    c.release_packages_path = os.environ["HH_REZ_REPO_RELEASE_EXT"]

requires = [
    "blosc-1.17",
    "tbb-2021.9",
    "boost-1.82.0",
    "openexr-3.1.12",
    "nanobind",  # only required if building with Python
]

private_build_requires = [
    "visual_studio",
]


# NOTE: openvdb 12+ requires Python 3.10+. 
variants = [
    # ["python-3.9", "numpy-1.26.4"],
    ["python-3.10", "numpy-1.26.4"],
    ["python-3.11", "numpy-1.26.4"],
]

def pre_build_commands():
    import os
    import subprocess

    # nanobind is a rez-pip package, so it has no CMake config of its own on
    # CMAKE_PREFIX_PATH. Ask nanobind (via the resolved python) where its
    # bundled nanobindConfig.cmake lives and add that to CMAKE_PREFIX_PATH so
    # find_package(nanobind ...) in CMakeLists.txt can locate it.
    if "nanobind" in resolve and "python" in resolve:
        try:
            nanobind_cmake_dir = subprocess.check_output(
                ["python", "-m", "nanobind", "--cmake_dir"],
                universal_newlines=True,
            ).strip()
        except (subprocess.CalledProcessError, OSError) as e:
            raise RuntimeError(
                "Failed to determine nanobind CMake directory: {}".format(e)
            )

        if not nanobind_cmake_dir or not os.path.isdir(nanobind_cmake_dir):
            raise RuntimeError(
                "nanobind CMake directory not found: '{}'".format(nanobind_cmake_dir)
            )

        env.CMAKE_PREFIX_PATH.append(nanobind_cmake_dir)


def commands():
    env.REZ_OPENVDB_ROOT = "{root}"
    env.OPENVDB_ROOT = "{root}"
    env.OPENVDB_LOCATION = "{root}"
    env.OPENVDB_INCLUDE_DIR = "{root}/include"
    env.OPENVDB_LIBRARY_DIR = "{root}/lib"

    env.PATH.append("{root}/bin")
    env.LD_LIBRARY_PATH.append("{root}/bin")
    env.LIB.append("{root}/lib")

    if "python" in resolve:
        python_ver = resolve["python"].version
        if python_ver.major == 3:
            if python_ver.minor == 9:
                env.PYTHONPATH.append("{root}/lib/python3.9/site-packages")
                env.UE_PYTHONPATH.append("{root}/lib/python3.9/site-packages")
            elif python_ver.minor == 10:
                env.PYTHONPATH.append("{root}/lib/python3.10/site-packages")
                env.UE_PYTHONPATH.append("{root}/lib/python3.10/site-packages")
            elif python_ver.minor == 11:
                env.PYTHONPATH.append("{root}/lib/python3.11/site-packages")
                env.UE_PYTHONPATH.append("{root}/lib/python3.11/site-packages")

uuid = "repository.openvdb"
