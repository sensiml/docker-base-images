# Adding Platforms to SensiML

These instructions are for partners to add specific hardware platforms to SensiML's service, allowing customers to access the platforms in [Analytics Studio](https://sensiml.com/products/analytics-studio/).


## Creating a Docker Image

SensiML uses [Docker](https://www.docker.com/) to run a build environment per platform, ensuring that code is built in the same way every time. In order to create a docker image, we have provided a number of base images on [Docker Hub](https://hub.docker.com/u/sensiml). The code for these base images resides on [GitHub](https://github.com/sensiml/docker-base-images)

### Adding platform SDK to Docker Image

In order to use a Docker image, you must first use a base image of your choosing:

The base image will provide you with an image that has the latest tools required on SensiML to build and communicate with our services:

``` Docker
FROM sensiml/base_image:latest
```

If there is an ARM-GCC version required, we have base images for those as well:

``` Docker
ARG BASE_VERSION
FROM sensiml/arm_gcc_none_eabi_base:${BASE_VERSION}
```

Here, `BASE_VERSION` will be "9.3.1", "10.2.1", etc. to match the version of `arm-none-eabi-gcc` downloads provided on the [Arm Developer site](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm)

After pulling in the base image, your platform SDK can be added to the image. If no context is given, our build scripts assume that the SDK has been copied into `/build`. This can be done in a few ways. If your SDK resides in an open repository, you can clone it directly.

``` Docker
RUN git clone --depth 1 --recursive https://repo_address.git /build
```

If you need to have an archive copied over, it is suggested to use a tar file

``` Docker
ADD sdk_tar.tar /build
```

### Testing a Docker Image


If your SDK has a knowledgepack example, you can build the docker image:

``` bash
docker build . -t my_sdk_testing
```

And then run the image interactively to test:

``` bash
docker run -it my_sdk_testing
```

From here you will be in the Docker container. You can navigate to where your application is built and run the Makefile(s) required to build.

### Finalizing your Image

Now it's time to delete the knowledgepack folder from the Docker image. This ensures that any model built using the Docker image will be using the generate model/source code from SensiML servers. In the example below, we assume all Knowledge Pack source/libraries are stored in a `knowledgepack` folder:

``` Docker
RUN find /build -type d -name "knowledgepack" -print0 | xargs -0 rm -R
```

## Providing Platform Information

In order for information to be added to SensiML servers and seen in Analytics Studio, we will need some information. This is done using YAML format.

### Architectures

SensiML has knowledge of many different architectures. These can be amended to support anything not yet represented.

| Architecture Name | Architecture Id |
|-------------------|-----------------|
| ARM               | 1               |
| x86(x86_64)       | 2               |
| RISC-V            | 3               |
| Tensilica         | 4               |
| AVR               | 5               |
| ARC               | 6               |
| Android           | 7               |
| PIC16             | 8               |
| PIC8              | 9               |


### Processor

If a processor with a specific name/family name is desired over the generic `Arm Cortex M4`, etc, we will need the following information:

``` yaml
- fields:
    uuid: a77ea523-cd39-44f7-ba9f-13703e21ef5d
    architecture: 1
    display_name: "Cortex M4"
    manufacturer: "ARM"
    compiler_cpu_flag: "-mcpu=cortex-m4"
    float_options:
        {
        "None": "-mfloat-abi=soft",
        "Soft FP": "-mfloat-abi=softfp -mfpu=fpv4-sp-d16",
        "Hard FP": "-mfloat-abi=hard -mfpu=fpv4-sp-d16",
        }
  model: processor
```

`uuid` would be a randomly generated UUID.

### Compiler

If you have created a Docker image for a specific compiler, it can be added with the following information:

``` yaml
- fields:
    uuid: 357a3637-2410-4bdf-aa8d-234e7faa2637
    name: GNU Arm Embedded (none-eabi)
    compiler_version: 9.2.1
    supported_arch: 1
    docker_image_base: "sensiml/arm_gcc_none_eabi_base"
  model: compiler
```

`docker_image_base` in this example would be replaced with your image name, and `compiler_version` would be replaced with your tag.

`uuid` would be a randomly generated UUID.

### Platform

``` yaml
- fields:
    uuid: 33ff4935-fdbe-4f80-85f7-906f7c6ebd00
    name: My Platform Name For Display
    description: Build libraries for My Platform boards/addons.
    platform_versions: ["1.0"]
    processors: [a77ea523-cd39-44f7-ba9f-13703e21ef5d]
    can_build_binary: true

    codegen_parameters:
      {
        "uses_simple_streaming": True,
        "app_environment":
          {
            "EXTRA_LIBS_DIR": "/build",
            "SML_KP_DIR": "/build/libsensiml",
            "SML_KP_OUTPUT_DIR": "/build/libsensiml/_build",
            "SML_APP_BUILD_DIR": "/build/firmware/project",
            "SML_APP_DIR": "/build/firmware/src",
            "SML_APP_CONFIG_FILE": "/build/firmware/src/app_config.h",
            "SML_APP_LIB_DIR": "/build/firmware/knowledgepack/libsensiml",
            "SML_APP_OUTPUT_BIN_DIR": "/build/firmware/output/dist/",
          },
      }
    supported_compilers: [357a3637-2410-4bdf-aa8d-234e7faa2637]
    default_selections:
      {
        "processor": "a77ea523-cd39-44f7-ba9f-13703e21ef5d",
        "compiler": "357a3637-2410-4bdf-aa8d-234e7faa2637",
        "float": "Hard FP",
      }
  model: platform
```

| Field                   | Format       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|-------------------------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| __uuid__                | UUID4        | UUID for your platform                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| __name__                | string       | Name for your platform to be displayed in Analytics Studio                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| __description__         | string       | Description of your platform/it's capabilities                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| __platform_versions__   | list(string) | Versions(s) your platform has. The version tag is used in specifying downloads. It can also be used to pull from a version tag in a public git repository on the image.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| __processors__          | list(uuid4)  | Processor(s) your platform supports. If your platform supports Generic ARM cores, providing SensiML with the Core names will be sufficient in this list                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| __can_build_binary__    | boolean      | Indicate whether or not the platform you're adding can build a binary.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| __codegen_parameters__  | dictionary   | Here, parameters are set for code generation:<br>`uses_simple_streaming` - This will likely be True. <br>`app_environment` - this dictionary provides us with path information that enables us to generate build scripts and properly compile a binary, or modify sensor configuration files.`SML_APP_BUILD_DIR` - Where the file(s) located to run your build commands reside.<br><br>`SML_APP_DIR` - Where the application source code resides.<br>`SML_APP_CONFIG_FILE` - File used to configure sensors for recognition (Sample rate, sensor range, etc.). <br>`SML_APP_LIB_DIR` - Where your platform expects Knowledge Pack libraries to reside.<br>`SML_APP_OUTPUT_BIN_DIR` - Where the output of a build resides on successful compilation |
| __supported_compilers__ | list(uuid)   | Compiler(s) supported by your platform. If SensiML's already built-in compilers are supported, providing those names will be sufficient.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| __default_selections__  | dictionary   | Provides the default selections that will be used in the platform display on Analytics Studio                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |


### Build scripts

With the above information, SensiML has enough in order to build the library. However, there are a couple other files needed:

#### config_sensor_files.sh

SensiML will use a file named `config_sensor_files.sh` to set the proper sensor variables for a model to be run on the device.

The example below can set the sample rate of an IMU, as well as the accelerometer and gyroscope ranges.

``` bash
#!/bin/bash

check_return_code() {
        #Check the return code of most recent calls.
        rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
}

inputs=$1

sensor_plugin_name=`$1 | jq -r '.["sensor_plugin_name"]'`
sample_rate=`$1 | jq -r '.["sample_rate"]'`
accel_range=`$1 | jq -r '.["accelerometer_sensor_range"]'`
gyro_range=`$1 | jq -r '.["gyroscope_sensor_range"]'`

# switch to recognition mode (add to mqtt app as well for backwards compatibility. The app config is for SDK versions > 1.8)
if [[ ! -z $sample_rate ]]; then
  echo "Changing Sample rate"
  echo "$SML_APP_CONFIG_FILE"
  sed -i "s/#define SNSR_SAMPLE_RATE\b.*/#define SNSR_SAMPLE_RATE $sample_rate/" $SML_APP_CONFIG_FILE
fi

if [[ ! -z $accel_range ]]; then
  echo "Changing Accel Range"
  sed -i "s/#define SNSR_ACCEL_RANGE\b.*/#define SNSR_ACCEL_RANGE $accel_range/" $SML_APP_CONFIG_FILE
fi
if [[ ! -z $gyro_range ]]; then
  echo "Changing Gyro Range"
  sed -i "s/#define SNSR_GYRO_RANGE\b.*/#define SNSR_GYRO_RANGE $gyro_range/" $SML_APP_CONFIG_FILE
fi
```

#### build_binary.sh

`build_binary.sh` is used to actually compile a binary application within the docker image. This file remains largely untouched, aside from any build steps needed to compile a binary.

``` bash

check_return_code() {
        #Check the return code of most recent calls.
        rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
}

inputs=$1

mount_point=`$1 | jq -r '.["mount_directory"]'`
project=`$1 | jq -r '.["application"]'`
kp_id=`$1 | jq -r '.["uuid"]'`
user=`$1 | jq -r '.["user_id"]'`
debug=`$1 | jq -r '.["debug_flag"]'`
version=`$1 | jq -r '.["version"]'`
platform=`$1 | jq -r '.["platform"]'`
build_tensorflow=n

if [ "$BUCKET_NAME" = "NO S3" ]; then
        rename_output=$outfile
else
        rename_output="codegen-compiled-output"
fi

echo "Building Binary"

mkdir -p $SML_APP_LIB_DIR

cp $SML_KP_OUTPUT_DIR/kb.a $SML_APP_LIB_DIR/libsensiml.a
cp $SML_KP_OUTPUT_DIR/libsensiml.a $SML_APP_LIB_DIR/libsensiml.a
cp $SML_KP_DIR/libtensorflow-microlite.a $SML_APP_LIB_DIR/
cp $SML_KP_DIR/kb.h $SML_APP_LIB_DIR

cp $SML_KP_DIR/kb_defines.h  $SML_APP_LIB_DIR
cp $SML_KP_DIR/model_json.h  $SML_APP_LIB_DIR
cp $SML_KP_DIR/kb_debug.h  $SML_APP_LIB_DIR
cp $SML_KP_DIR/kb_typedefs.h  $SML_APP_LIB_DIR
cp $SML_KP_DIR/testdata.h $SML_APP_LIB_DIR
cp $SML_KP_DIR/model.json $mount_point/

pushd $SML_APP_BUILD_DIR
pwd
#
# HERE YOU WILL ADD YOUR BUILD STEPS.
#
#
# make all -j

check_return_code

mkdir return_files
cd return_files

#
# HERE YOU WILL ADD ALL FILES YOU WISH TO BE RETURNED WITH THE BINARY.
# SensiML typically returns bin/hex file, map, and other informational files.
#

echo $outfile

outfile=kp_"$kp_id"_"$platform"_"$lib_bin"_"$version"_"$debug".zip
cp -RT "$SML_APP_OUTPUT_BIN_DIR" .
cp $SML_KP_DIR/model.json .
zip -r $outfile ./
cp ./$outfile $mount_point/$outfile


exit $?

```
