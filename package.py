name = "openvdb"

# version 11.0.0 is used by Houdini 20.5.278
version = "11.0.0.hh.1.1.0"

authors = [
    "DreamWorks & AcademySoftwareFoundation",
]

description = """Storage and manipulation of sparse volumetric data"""

with scope("config") as c:
    import os

    c.release_packages_path = os.environ["HH_REZ_REPO_RELEASE_EXT"]

requires = [
    "blosc-1.17",
    "tbb-2020",
    "boost-1.82",
    "openexr-3.1.12",
    "pybind11",  # only required if building with Python
    "numpy",  # only required if building with Python
]

private_build_requires = []


# NOTE: openvdb 11+ requires Python 3.9+. Although we are building a REZ variant
# for Python 3.7, we will disable the 'OPENVDB_BUILD_PYTHON_MODULE' CMake option
# within CMakeLists.txt. This is so we can still have this openvdb version available
# for Python 3.7, but without 'pyopenvdb' support.
variants = [
    ["python-3.7"],
    ["python-3.9"],
    ["python-3.10"],
    ["python-3.11"],
    ["python-3.12"],
]


def commands():
    env.REZ_OPENVDB_ROOT = "{root}"
    env.OPENVDB_ROOT = "{root}"
    env.OPENVDB_LOCATION = "{root}"
    env.OPENVDB_INCLUDE_DIR = "{root}/include"
    env.OPENVDB_LIBRARY_DIR = "{root}/lib64"

    env.PATH.append("{root}/bin")
    env.LD_LIBRARY_PATH.append("{root}/lib64")

    if "python" in resolve:
        python_ver = resolve["python"].version
        if python_ver.major == 3:
            if python_ver.minor == 9:
                env.PYTHONPATH.append("{root}/lib64/python3.9/site-packages")
            elif python_ver.minor == 10:
                env.PYTHONPATH.append("{root}/lib64/python3.10/site-packages")
            elif python_ver.minor == 11:
                env.PYTHONPATH.append("{root}/lib64/python3.11/site-packages")
            elif python_ver.minor == 12:
                env.PYTHONPATH.append("{root}/lib64/python3.12/site-packages")


uuid = "repository.openvdb"
