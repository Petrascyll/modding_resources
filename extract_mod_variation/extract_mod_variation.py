import os
import re

ini = {
    'Constants': {},
    'Key': {},
    'Present': {},
    'TextureOverride': {},
    'ShaderOverride': {},
    'CommandList': {},
    'CustomShader': {},
    'Resource': {}
}

section_title_pattern = re.compile(r'\[(?P<Keyword>{})(?P<Target>.*)\]'.format('|'.join([k for k in ini.keys()])))


def get_ini_filepath():
    found = []
    for filename in os.listdir():
        if filename.endswith('.ini'):
            found.append(filename)
    
    if len(found) == 0:
        raise FileNotFoundError()
    elif len(found) == 1:
        return found[0]
    elif len(found) >= 2:
        raise FileExistsError(found)

def parse_ini(ini_filepath):
    with open(ini_filepath, 'r') as ini_file:
        ini_lines = ini_file.readlines()

    for i in range(len(ini_lines)):
        # print(i, line.__repr__())
        line = ini_lines[i]
        if line.startswith('['):
            
            parse_section(line.strip())

            while (
                i + 1 < len(ini_lines)
                and not ini_lines[i+1].startswith('[')
            ):
                # print(ini_lines[i].__repr__())
                i += 1
            # print()


def parse_section(section_title):
    match = re.match(section_title_pattern, section_title)
    if match:
        keyword, target = match.group('Keyword'), match.group('Target')
        ini[keyword] = {
            **ini[keyword],
            target: {}
        }
    else:
        print('Unexpected section title format!')
        print('\t', section_title)
        print('Quitting')
        exit(1)

def main():
    try:
        ini_filepath = get_ini_filepath()
        print('Found .ini file in current directory: "{}"'.format(ini_filepath))
    except FileNotFoundError:
        print("No .ini file found in current directory!")
        print("Quitting")
        exit(1)
    except FileExistsError as x:
        print("Multiple .ini files found in current directory!")
        print('\t', x.args[0])
        print("Quiting")
        exit(1)

    parse_ini(ini_filepath)
    
    for keyword in ini:
        print(keyword)
        for target in ini[keyword]:
            print('\t', target)
            for (k,v) in ini[keyword][target]:
                print('\t\t', k, v)
        print()
    

    # Need to figure out what body parts exist: BodyA, BodyA, BodyC, ...

    # parts = get_parts(config)
    # print(parts)
    # print(config.sections())

    # with open(ini_filepath, "r") as ini_file:
    #     ini_content = ini_file.read()
    #     # print(ini_content)


if __name__ == '__main__':
    main()