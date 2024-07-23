name = "openvdb"

version = "11.0.0.hh.1.0.0"

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
    # "pybind11",  # only required if building with Python
    # "numpy",  # only required if building with Python
]

private_build_requires = []


# NOTE: We could build against Python versions, to have 'pyopenvdb' available.
# Unfortunately, openvdb 11+ requires python 3.9.1+ and we still want python 3.7
# for Nuke 13. Once Python 3.7 is not a requirement anymore, we can build for all
# Python versions.
variants = []


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

    if building:
        env.CMAKE_MODULE_PATH.append("{root}/lib64/cmake/OpenVDB")


uuid = "repository.openvdb"
