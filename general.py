import constants
import re

def get_crystal_classes(crystal_name:str) -> list:
    # Return a list of classes based on an input crystal name.
    return_list = []
    crystal_list = []
    
    for opt in constants.UNKNOWN_OPTIONS:
        crystal_list.append(opt.replace('UNKNOWN ', ''))

    crystal_name = crystal_name.replace('UNKNOWN ', '')

    if crystal_name not in crystal_list:
        return return_list
    
    for key in constants.CLASS_CODE_LOOKUP.keys():
        if crystal_name == constants.CLASS_CODE_LOOKUP[key]['crystal']:
            return_list.append(constants.CLASS_CODE_LOOKUP[key]['code'])

    return return_list

def get_codes_from_selection(selection_list:list) -> list:
    # Get a list of class codes based on pretty name selection.
    return_list = []
    for item in selection_list:
        if 'UNKNOWN' in item:
            return_list += get_crystal_classes(item)
        elif constants.CLASS_CODE_LOOKUP[item]['code'] not in return_list:
            return_list.append(constants.CLASS_CODE_LOOKUP[item]['code'])

    return return_list

def format_class_list_as_str(class_list:list, seperator:str='|'):
    # A function for turning a list of classes back into a pretty string.
    return_val = ''

    for item in class_list:
        return_val += seperator + item 

    return_val = return_val[1:]

    return_val = '[' + return_val + ']'

    return return_val

def class_match_sections(section_parts:list, class_list:list=None, return_as_list:bool=False, debug:bool=False):
    # Takes a list of sections and searches for classes. If it is a class-based line, it will return if it matches.
    new_list = []
    if debug:
        new_list = section_parts
    else:
        for section in section_parts:
            class_matches = re.findall('^\\[\\S*?\\] ', section)
            if len(class_matches) > 0 and class_matches[0]:
                # This section has class-specific information in it...
                full_class_spec = class_matches[0]
                class_spec_list = re.sub('\\[|\\]|\\s*', '', full_class_spec)
                class_spec_list = re.sub('\\+', '|', class_spec_list).split('|')
                overlapping_classes = set(class_spec_list) & set(class_list)
                if '+' in full_class_spec:
                    if len(overlapping_classes) == len(class_spec_list):
                        # This is a full "and" situation
                        replacement_class_list = format_class_list_as_str(overlapping_classes, '+')
                        section = section.replace(full_class_spec, replacement_class_list + ' ')
                        new_list.append(section)
                elif len(overlapping_classes) > 0:
                    # This is the "or" situation
                    replacement_class_list = format_class_list_as_str(overlapping_classes)
                    section = section.replace(full_class_spec, replacement_class_list + ' ')
                    new_list.append(section)

            else:
                new_list.append(section)

    if return_as_list:
        return new_list
    
    return_string = ''
    for section in new_list:
        return_string += '* ' + section + '\n'

    return return_string

if __name__ == '__main__':
    print(get_crystal_classes('UNKNOWN WIND'))
