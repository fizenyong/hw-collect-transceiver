from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_title
from nornir.core.filter import F
from tqdm import tqdm
from ntc_templates.parse import parse_output
import re
import csv
from colorama import Fore, Style


def parse(task: Task, pbar: tqdm) -> Result:
    with open(f"logs/{task.host.hostname}-{task.host.name}.txt", "r") as f:
        data = re.sub(r"\s+$$", "", f.read(), flags=re.MULTILINE)  # rstrip

    parsed = parse_output(platform="huawei_vrp", command="disp transceiver", data=data)

    pbar.update()
    return Result(host=task.host, result=parsed)


def csvwrite(result: Result, fname: str):
    fieldnames = [
        "hostname",
        "interface",
        "sfp_type",
        "con_type",
        "wavelength",
        "vendor",
        "esn",
    ]

    for host in result.failed_hosts:  # Remove device with failed parsed result
        del result[host]

    with open(fname, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()

        for host in tqdm(result):
            for interf in result[host][0].result:
                interf["hostname"] = host  # Add hostname to every result row
                writer.writerow(interf)


def check_result(result: Result):
    if result.failed == True:
        print(f"{Style.BRIGHT}{Fore.RED}Failed hosts: check nornir.log for Traceback")
        for host in result.failed_hosts:
            print(f"{Style.BRIGHT}{Fore.RED} {host}")


if __name__ == "__main__":

    nr = InitNornir(config_file="config.yaml")

    print_title("Parsing transceiver info on All host")
    with tqdm(total=len(nr.inventory.hosts)) as pbar:
        result = nr.run(task=parse, pbar=pbar)

    check_result(result)

    print_title("Writing results to csv file")
    csvwrite(result, "csv_file.csv")

    print_title("Completed!")
