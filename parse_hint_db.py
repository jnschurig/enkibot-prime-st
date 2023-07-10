import re, json
import pandas as pd
import constants

def load_db_file(db_file_name:str=constants.HINT_DB_FILE_NAME):
    # Simple function to load the db file as text
    try:
        with open(db_file_name, 'r') as f:
            return f.read()
    except:
        return ''

def parse_raw(text_body:str):
    # Parse the raw text into a list of sections, each with a section title.
    main_sections = text_body.split('## ')

    # First section is empty, so get rid of it.
    main_sections.pop(0)

    output_dict = []

    for idx, section in enumerate(main_sections):
        section_dict = {}
        section_parts = section.splitlines()

        section_dict['section_name'] = section_parts.pop(0)
        output_sections = []
        
        for part in section_parts:
            # Remove any extraneous white space
            part = part.strip()

            # Remove leading *s
            part = re.sub('^\\* ', '', part)
            if part != '':
                output_sections.append(part)

        section_dict['section_parts'] = json.dumps(output_sections)

        output_dict.append(section_dict)

    return output_dict

def easy_parse():
    # A quick combination of loading and parsing.
    raw_text = load_db_file()
    return parse_raw(raw_text)

def easy_df_parse():
    # Another quick combination to convert the resultant list into a dataframe.
    return pd.DataFrame(easy_parse())

if __name__ == '__main__':
    import json 
    # db_text = load_db_file('hint_db.md')
    # result = parse_raw(db_text)
    result = easy_parse()
    # print(json.dumps(result[4], indent=4))

    data_df = easy_df_parse()

    print(data_df.head(5))