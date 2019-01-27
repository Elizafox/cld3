#!/usr/bin/env python

import subprocess
from os import path, makedirs

from setuptools import setup, Extension
from distutils.command.build import build

from Cython.Build import cythonize


PROTOS = ["src/sentence.proto", "src/feature_extractor.proto", "src/task_spec.proto"]

SOURCES = [
    "src/cld3.pyx",
    "src/base.cc",
    "src/cld_3/protos/src/feature_extractor.pb.cc",
    "src/cld_3/protos/src/sentence.pb.cc",
    "src/cld_3/protos/src/task_spec.pb.cc",
    "src/embedding_feature_extractor.cc",
    "src/embedding_network.cc",
    "src/feature_extractor.cc",
    "src/feature_types.cc",
    "src/fml_parser.cc",
    "src/lang_id_nn_params.cc",
    "src/language_identifier_features.cc",
    "src/nnet_language_identifier.cc",
    "src/registry.cc",
    "src/relevant_script_feature.cc",
    "src/script_span/fixunicodevalue.cc",
    "src/script_span/generated_entities.cc",
    "src/script_span/generated_ulscript.cc",
    "src/script_span/getonescriptspan.cc",
    "src/script_span/offsetmap.cc",
    "src/script_span/text_processing.cc",
    "src/script_span/utf8statetable.cc",
    "src/sentence_features.cc",
    "src/task_context.cc",
    "src/task_context_params.cc",
    "src/unicodetext.cc",
    "src/utils.cc",
    "src/workspace.cc",
]

INCLUDES = ["./src", "./src/cld_3/protos/"]

LIBRARIES = ["protobuf"]

CLASSIFIERS = [
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Programming Language :: C++",
    "Operating System :: OS Independent",
    "Development Status :: 4 - Beta",
    "Topic :: Text Processing :: Linguistic",
    "Intended Audience :: Developers",
]


class BuildProtobuf(build):
    def run(self):
        if not path.exists("src/cld_3/protos"):
            # Create protobufs dir
            makedirs("src/cld_3/protos")

        # Build protobuf stuff
        command = ["protoc"]
        command.extend(PROTOS)
        command.append("--cpp_out={}".format(path.join("src", "cld_3", "protos")))
        subprocess.run(command, check=True)

        build.run(self)


with open("README.md") as f:
    long_description = f.read()

ext = Extension(
    "cld3",
    sources=SOURCES,
    include_dirs=INCLUDES,
    libraries=LIBRARIES,
    language="c++",
    extra_compile_args=["-std=c++11"],
)

setup(
    name="cld3",
    version="0.2.2",
    cmdclass={"build": BuildProtobuf},
    author="Google, Johannes Baiter, Elizabeth Myers",
    author_email="elizabeth@interlinked.me",
    description="CLD3 Python bindings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache2",
    keywords=["cld3", "cffi"],
    url="https://github.com/Elizafox/cld3",
    ext_modules=cythonize([ext]),
)
