import subprocess

from classes.logging import Logger

logger = Logger()

def ls(url, config):
    """

    :param url:
    :param config:
    :return:
    """
    return  __s3cmd("ls", None, config, url)


def ls_recursive(url, config):
    """

    :param url:
    :param config:
    :return:
    """
    return __s3cmd("ls", "recursive", config, url)


def __s3cmd(command, option, config, url):
    """

    :param command:
    :param option:
    :param config:
    :param url:
    :return:
    """
    if option:
        cmd = "s3cmd {} --{} -c {} {}".format(command, option, config, url)
    else:
        cmd = "s3cmd {} -c {} {}".format(command, config, url)

    logger.info("Executing: {}".format(cmd))

    try:
        ret = subprocess.check_output([cmd], shell=True)
    except subprocess.CalledProcessError as err:
            raise err
    else:
        return ret
