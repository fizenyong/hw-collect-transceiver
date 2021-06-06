from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_title, print_result
from nornir_utils.plugins.tasks.files import write_file
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.filter import F
import logging
from getpass import getpass
from tqdm import tqdm
from colorama import Fore, Style


def result_content(task: Task) -> str:
    content = []

    for r in task.results:
        if r.severity_level < 20:  # Skip if logging.DEBUG
            continue
        # content.append(f"<{r.name}>")
        content.append(r.result)
        # content.append("</end>\n")
    return "\n".join(content)


def get_config(task: Task, pbar: tqdm):
    task.run(
        name="disp transceiver",
        task=netmiko_send_command,
        command_string=f"display transceiver",
    )

    task.run(
        task=write_file,
        filename=f"logs/{task.host.hostname}-{task.host.name}.txt",
        content=result_content(task),
        severity_level=logging.DEBUG,
    )

    pbar.update()
    tqdm.write(f"{task.host}: done!")


def check_result(result: Result):
    if result.failed == True:
        print(f"{Style.BRIGHT}{Fore.RED}Failed hosts: check nornir.log for Traceback")
        for host in result:
            print(host)


if __name__ == "__main__":

    nr = InitNornir(config_file="config.yaml")
    nr.inventory.defaults.password = getpass()

    print_title("Running on Test host")
    test_env = nr.filter(F(hostname__contains="192.168.1.1"))
    with tqdm(total=len(test_env.inventory.hosts)) as pbar:
        result = test_env.run(task=get_config, pbar=pbar)
    print_result(result)

    input("Continue? <Ctrl-C to exit>")

    print_title("Running on All host")
    with tqdm(total=len(nr.inventory.hosts)) as pbar:
        result = nr.run(task=get_config, pbar=pbar)

    print_title("Completed!")
    check_result(result)
