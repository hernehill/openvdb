name = "openvdb"

# version 13.0.0 is used by Houdini 22
version = "13.0.0.hh.1.0.0"

authors = [
    "DreamWorks & AcademySoftwareFoundation",
]

description = """Storage and manipulation of sparse volumetric data"""

with scope("config") as c:
    import os

    c.release_packages_path = os.environ["HH_REZ_REPO_RELEASE_EXT"]

requires = [
    "blosc-1.17",
    "tbb-2022",
    "boost-1.88",
    "openexr-3.4.4",
    "nanobind",  # only required if building with Python
]

private_build_requires = []

variants = [
    ["python-3.13", "numpy-2"],
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
            if python_ver.minor == 13:
                env.PYTHONPATH.append("{root}/lib64/python3.13/site-packages")


uuid = "repository.openvdb"
