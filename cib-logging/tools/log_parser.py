import sys
import json
import pyparsing as pp

## CONSTANTS ##
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

## PARSER DEFINITIONS ##
# Symbols
LPAR, RPAR, COMMA, LABR, RABR = map(pp.Suppress, "(),<>")
integer = pp.Word(pp.nums).setParseAction(lambda tokens: int(tokens[0]))

# Identifiers
symbol_id = pp.Literal("unsigned int catalog").suppress()
string_id = pp.Suppress("sc::lazy_string_format<sc::string_constant<char,")
format_id = pp.Suppress("cib::tuple")

# Message
char_field = pp.Suppress("(char)") + integer + pp.Optional(COMMA)
char_fields = pp.Group(pp.OneOrMore(char_field) + RABR)

# Formatting
format_arg = pp.Group(pp.OneOrMore(pp.Word(pp.alphas)) + pp.Optional(COMMA))
format_args = pp.Group(LABR + pp.Optional(pp.OneOrMore(format_arg, stopOn=RABR)) + RABR)

# Parser
type_parser = symbol_id + LABR + ... + pp.Literal(">()").suppress()
parser = symbol_id + LABR + pp.Word(pp.alphas) + LABR + pp.Suppress("(logging::level)") + integer + COMMA + string_id + char_fields + COMMA + format_id + format_args

## PROCESS INPUT ## 
message_id = 0
if __name__ == "__main__":
    with open(INPUT_FILE, "r") as f:
        for line in f:
            # Parse relevant information
            try:
                message_type = type_parser.parseString(line)
                message_info = parser.parseString(line)
            except:
                #print("Parse error for line: " + line)
                continue
            
            message_type = message_type[0]
            message_subtype = message_info[0]
            message_level = message_info[1]
            message_value = "".join([chr(int(c)) for c in message_info[2]])
            message_args = [" ".join(c for c in arg) for arg in message_info[3]]
            
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
                        level=LEVELS[message_info[1]],
                        msg=message_value,
                        type=message_subtype,
                        id=message_id,
                        arg_types=message_args,
                        arg_count=len(message_args),
                    )
                )

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

                message_id += 1

    str_catalog = dict(messages=messages)

    json.dump(str_catalog, open(JSON_FILE, "w"), indent=4)