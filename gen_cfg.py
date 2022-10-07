import sys
import re


def read_input():
    seq_data = []
    file_name = f"{sys.argv[1]}"
    f = open(file_name, "r")
    file_data = f.readlines()

    for i, e in enumerate(file_data):
        file_data[i] = file_data[i].replace("\n", "")
        file_data[i].strip()

        temp_arr = file_data[i].split()
        for data in temp_arr:
            seq_data.append(data)

    return seq_data


def parse_input(seq_data):
    hostnames = []
    interfaces = []
    curr_ints = []
    curr_hostname = ""
    i = 0
    while i < len(seq_data):
        curr = seq_data[i]

        if is_hostname(curr):
            if curr_hostname == "":
                curr_hostname += curr
                curr_ints = []
                interfaces.append(curr_ints)
            else:
                curr_hostname += f" {curr}"
            i += 1

        elif is_interface_type(curr):
            if curr_hostname != "":
                hostnames.append(curr_hostname)
                curr_hostname = ""

            cleaned_int = clean([seq_data[i], seq_data[i+1], seq_data[i+2]])
            if i + 3 < len(seq_data):
                if is_ip_add(seq_data[i+3]):
                    cleaned_int.append(seq_data[i+3].lower())
                    i += 1
            curr_ints.append(cleaned_int)
            i += 3

    ret_arr = []

    for i in range(len(hostnames)):
        ret_arr.append({hostnames[i]: interfaces[i]})

    return ret_arr


def clean(inp_arr):
    ret_arr = []

    for i in range(len(inp_arr)):
        ret_arr.append(inp_arr[i].strip().lower())

    return ret_arr


def make_commands_hostname(parsed_data, file_name):
    f = open(file_name, "a")

    for name, interfaces in parsed_data.items():
        name = name.replace(" ", "_")
        f.write("==============================\n")
        f.write(name + "\n")
        f.write("------------------------------\n")
        f.write(f"en\n")
        f.write(f"conf t\n")
        f.write(f"hostname {name}\n\n")

    f.close()


def make_commands_ip(parsed_data, file_name):
    f = open(file_name, "a")

    for name, interfaces in parsed_data.items():
        f.write("==============================\n")
        f.write(name + "\n")
        for int_data in interfaces:
            if len(int_data) < 4:
                int_type, ip_add, subnet = int_data
                f.write("------------------------------\n")
                f.write(f"int {int_type}\n")
                f.write(f"ip add {ip_add} {subnet}\n")
                f.write(f"no shutdown\n")
                f.write(f"exit\n\n")
            else:
                int_type, ip_add, subnet, def_gateway = int_data
                f.write("------------------------------\n")
                f.write(f"int {int_type}\n")
                f.write(f"ip add {ip_add} {subnet}\n\n")
                f.write(f"no shutdown\n")
                f.write(f"exit\n\n")

    f.close()


def replace_var(parsed_data, var_arr, replace_arr):
    """ 
    @input : parsed_data
    @input : var_arr -> ["X", "Y", ... "Z"]
    @input : replace_arr -> ["7", "8", ..., "1"]
    """
    new_parsed_data = parsed_data.copy()

    for name, interfaces in new_parsed_data.items():
        for int_data in interfaces:
            for i, interface in enumerate(interfaces):
                for j, var in enumerate(var_arr):
                    new_parsed_data[name][i][1] = new_parsed_data[name][i][1].replace(
                        var.lower(), replace_arr[j])

                    new_parsed_data[name][i][2] = new_parsed_data[name][i][2].replace(
                        var.lower(), replace_arr[j])

                    if len(new_parsed_data[name][i]) > 3:
                        new_parsed_data[name][i][3] = new_parsed_data[name][i][3].replace(
                            var.lower(), replace_arr[j])

    return new_parsed_data


def is_hostname(inp_str):
    return not is_interface_type(inp_str) and not is_ip_add(inp_str)


def is_interface_type(inp_str):
    inp_str = inp_str.lower().strip()
    match = re.match("^[fgs]{1}.*[0-9]+$", inp_str)

    return "/" in inp_str or bool(match)


def is_ip_add(inp_str):
    inp_str = inp_str.lower().strip()
    match = re.match("^.+[.]{1}.+[.]{1}.+[.]{1}.+$", inp_str)
    return "." in inp_str and bool(match)


def main():
    # Configurable variables
    FILE_NAME_IP = f"{sys.argv[2]}" if len(sys.argv) >= 3 else "conf_ip.txt"
    FILE_NAME_HOSTNAME = f"{sys.argv[3]}" if len(
        sys.argv) >= 4 else "conf_hostname.txt"
    VARIABLES = ["X", "Y", "Z"]
    NPM = ["7", "8", "1"]

    # Process
    open(f"{FILE_NAME_IP}", 'w').close()
    open(FILE_NAME_HOSTNAME, 'w').close()

    inputs = read_input()
    parsed = parse_input(inputs)

    for e in parsed:
        e = replace_var(e, VARIABLES, NPM)
        make_commands_ip(e, FILE_NAME_IP)
        make_commands_hostname(e, FILE_NAME_HOSTNAME)


if __name__ == '__main__':
    main()
