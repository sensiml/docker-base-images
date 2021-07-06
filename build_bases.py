#!/usr/bin/env python
import docker
from docker.errors import BuildError
import json
import os
import argparse
from icecream import ic
from shutil import copyfile


def _copy_run_build(docker_path):
    run_build_path = os.path.join(docker_path, "run_build.sh")
    copyfile("run_build.sh", run_build_path)

    return run_build_path


def make_image(docker_client, image_path, repository, tag, **build_args):
    _copy_run_build(image_path)
    dc = docker_client

    ic(f"Building {repository}:{tag}")
    ic(build_args)

    try:
        img = dc.images.build(
            path=image_path,
            dockerfile=os.path.join(image_path, "Dockerfile"),
            tag=f"{repository}:{tag}",
            buildargs=build_args,
            rm=True,
            quiet=False,
        )
        return img
    except BuildError as e:
        ic(f"Failed build for {tag}")
        ic(e)
        return None
    finally:
        os.remove(os.path.join(image_path, "run_build.sh"))


def _get_input_args():
    parser = argparse.ArgumentParser(
        description="Make docker image(s) from a given folder."
    )

    parser.add_argument(
        "--in_dir",
        "-i",
        dest="in_dir",
        required=True,
        help="Choose directory to build from",
    )

    parser.add_argument(
        "--push_image",
        "-p",
        action="store_true",
        dest="push_image",
        required=False,
        help="Push Images Directly to repository",
    )


    return parser.parse_args()


def main():

    input_args = _get_input_args()

    abs_input_path = os.path.abspath(input_args.in_dir)
    docker_client = docker.from_env()
    if os.path.exists(f"{abs_input_path}/arguments.json"):
        with open(f"{abs_input_path}/arguments.json", "r") as inp:
            build_list = json.loads(inp.read())
        for image in build_list:
            built_image = make_image(docker_client,
                abs_input_path, image["repository"], image["tag"], **image["build_args"]
            )
            if built_image and input_args.push_image:
                docker_client.api.push(repository=image["repository"], tag=image["tag"])

    else:
        ic("Arguments.json required!")


if __name__ == "__main__":
    main()
