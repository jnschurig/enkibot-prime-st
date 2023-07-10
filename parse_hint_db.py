import re, pandas as pd
import constants

def load_db_file(db_file_name:str=constants.HINT_DB_FILE_NAME):
    try:
        with open(db_file_name, 'r') as f:
            return f.read()
    except:
        return ''

def parse_raw(text_body:str):
    # print(text_body[:100])
    main_sections = text_body.split('## ')
    # print(main_sections[1])

    # First section is empty, so get rid of it.
    main_sections.pop(0)

    # output_dict = {}
    output_dict = []

    for idx, section in enumerate(main_sections):
        section_dict = {}
        # section_parts = section.split('\\n')
        section_parts = section.splitlines()
        # output_dict[idx] = {}
        # output_dict[idx]['section_name'] = section_parts.pop(0)
        # output_dict[idx]['section_parts'] = []

        section_dict['section_name'] = section_parts.pop(0)
        section_dict['section_parts'] = []
        
        for part in section_parts:
            # Remove any extraneous white space
            part = part.strip()

            # Remove leading *s
            part = re.sub('^\\* ', '', part)
            if part != '':
                # output_dict[idx]['section_parts'].append(part)
                section_dict['section_parts'].append(part)

        output_dict.append(section_dict)

    return output_dict

def easy_parse():
    raw_text = load_db_file()
    return parse_raw(raw_text)

def easy_df_parse():
    df = pd.DataFrame(easy_parse())

    # data_dict = easy_parse()
    
    return df


if __name__ == '__main__':
    import json 
    # db_text = load_db_file('hint_db.md')
    # result = parse_raw(db_text)
    result = easy_parse()
    # print(json.dumps(result[4], indent=4))

    data_df = easy_df_parse()

    print(data_df.head(5))