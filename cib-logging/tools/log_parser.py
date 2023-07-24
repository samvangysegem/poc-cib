import sys
import json
import pyparsing as pp
import re

## CONSTANTS AND INITIALISATION ##
LEVELS = ["MAX", "FATAL", "ERROR", "WARN", "INFO", "USER1", "USER2", "TRACE"]

# Output directories
INPUT_FILE = sys.argv[1]
CPP_FILE = sys.argv[2]
JSON_FILE = sys.argv[3]
XML_FILE = sys.argv[4]

out = open(CPP_FILE, "w")
out.write(
    """
    #include <log/log.hpp>
    #include <log/catalog/catalog.hpp>
    #include <sc/lazy_string_format.hpp>
    #include <sc/string_constant.hpp>
    
    """
)

## HELPERS ##
messages = []
cataloged_strings = set()

## PARSER FUNCTIONS ##
class ParseException(Exception):
    pass

def parseMessageType(input):
    pattern = r"unsigned int catalog<(.+?)>\(\)"
    match = re.search(pattern, input)

    if match:
        message_type = match.group(1).strip()
        return message_type
    else:
        raise ParseException("MessageType: no match found in the input string")

def parseMessageInfo(input):
    pattern = r"unsigned int catalog<([^<]+)<\(logging::level\)(\d+), sc::undefined<sc::args<([^>]*)>, char, ([^>]+)>>>\(\)"
    match = re.search(pattern, input)

    if match:
        message_subtype = match.group(1)
        message_level = int(match.group(2))
        message_args = match.group(3).replace(" ", "").split(",")
        if len(message_args) == 1 and message_args[0] == "":
            message_args = []
        message_value = "".join([chr(int(c)) for c in match.group(4).replace("(char)", "").split(",")])
        return message_subtype, message_level, message_args, message_value
    else:
        raise ParseException("MessageInfo: no match found in the input string")


## PROCESS INPUT ##
message_id = 0
if __name__ == "__main__":
    with open(INPUT_FILE, "r") as f:
        for line in f:
            # Parse relevant information
            try:
                message_type = parseMessageType(line)
                message_subtype, message_level, message_args, message_value = parseMessageInfo(line)
            except Exception as e:
                print(e)
                continue

            # message_args = [" ".join(c for c in arg) for arg in message_info[3]]

            # Generating catalog
            if message_type not in cataloged_strings:
                cataloged_strings.add(message_type)

                # Template specialisation for CPP file
                out.write("/*\n")
                out.write('    "' + message_value + '"\n')
                out.write(" */\n")
                out.write(
                    "template<> auto catalog<{}>() -> string_id {{\n\t return {};\n}}\n".format(
                        message_type, message_id
                    )
                )
                out.write("\n")

                messages.append(
                    dict(
                        level=LEVELS[message_level],
                        msg=message_value,
                        type=message_subtype,
                        id=message_id,
                        arg_types=message_args,
                        arg_count=len(message_args),
                    )
                )

                message_id += 1

                """
                if len(message_args) == 0:
                    syst_format = et.SubElement(syst_short_message, "syst:Format")
                    syst_format.set("ID", "0x%08X" % string_id)
                    syst_format.set("Mask", "0x0FFFFFFF")
                    printf_string = string_value
                else:
                    syst_format = et.SubElement(syst_catalog_message, "syst:Format")
                    syst_format.set("ID", "0x%08X" % string_id)
                    syst_format.set("Mask", "0xFFFFFFFF")
                    printf_string = re.sub(r"{}", r"%d", string_value)
                    printf_string = re.sub(r"{:(.*?)}", r"%\1", printf_string)
                syst_format.text = "<![CDATA[" + printf_string + "]]>"
                """

    str_catalog = dict(messages=messages)
    json.dump(str_catalog, open(JSON_FILE, "w"), indent=4)
