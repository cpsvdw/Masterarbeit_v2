from bs4 import BeautifulSoup
import pandas as pd
import glob


def extract_model_from_file(content):
    '''
    Extracts model, context values and if exists the error description from xmi file.   

            Parameters:
                    model_file (TextIOWrapper): xmi file containing the model

            Returns:
                    binary_sum (Dict): Model with context and error code
    '''
    model = {}

    # split file string into model and error code
    model_file = content[:content.index('</uml:Model>') + len('</uml:Model>')] + '\n' + '</xmi:XMI>'
    model_file = model_file.replace('\n', '')
    error_code = content[content.index('</uml:Model>') + len('</uml:Model>'):]

    # extract error description
    if 'Fehler' in error_code:
        model['is_error'] = 1
        error_code_lines = error_code.split("\n")
        for i, line in enumerate(error_code_lines):
            if 'Fehler' in line:
                error_description = line.partition('TAG_02_Fehlerbeschreibung = "')[2][0:-4]
                model['error_description'] = error_description
    else:
        model['is_error'] = 0
        model['error_description'] = ''

    # extract model name
    soup = BeautifulSoup(model_file, 'lxml')
    model_name = soup.packagedelement['name']
    model['model_name'] = model_name

    # extract model parameters and context variables
    for part in soup.packagedelement.packagedelement.find_all(True):
        part_id = part['type']
        part_name = soup.find('packagedelement', {'xmi:id': part_id})['name']
        part_category = soup.find('packagedelement', {'xmi:id': part_id}).parent['name']
        model[part_category] = part_name

    return model


def compare_new_model_to_known(new_model, known_models):
    '''
    Compare one model to all known models and calculate congruencies. 

            Parameters:
                    new_model (Dict): model that should be compared
                    known_models (DataFrame): models that are already known

            Returns:
                    congruency (Dict): Congruencies with all models the new model was compared with
    '''
    known_models = known_models.reset_index().drop(columns='index')  # make sure indexes pair with number of rows
    congruency = {}
    parameters = ['01_Rahmenlängsträger', '02_Rahmenquerträger', '03_1. Vorderachse', '04_1. Hinterachse',
                  '05_Federung VA', '06_Federung HA', '07_Motor', '07_SW_Motor', '08_Getriebe', '08_SW_Getriebe',
                  '09_Fahrerhaus']
    for index, row in known_models.iterrows():
        count = 0
        for col in known_models.columns.to_list():
            if col in parameters:
                if row[col] == new_model[col]:
                    count += 1
        congruency[index] = count / 11
    return congruency


# create table for models
column_names = ['model_name', '01_Rahmenlängsträger', '02_Rahmenquerträger', '03_1. Vorderachse', '04_1. Hinterachse',
                '05_Federung VA', '06_Federung HA', '07_Motor', '07_SW_Motor', '08_Getriebe', '08_SW_Getriebe',
                '09_Fahrerhaus', '01_Aussentemperatur', '02_Luftfeuchtigkeit', '03_Motordrehzahl']
df_models = pd.DataFrame(columns=column_names)

path_to_xmi_files = 'C:\\Users\\vanderweck\\PycharmProjects\\Masterarbeit\\Systemmodelle\\OldModels\\'  # DO: If the files are not in the same folder as the code file, add path to file.
file_names = [f for f in glob.glob(path_to_xmi_files + "*.xmi")]
#print(file_names)

for file_name in file_names:
    #print(file_name)
    with open(file_name, 'r') as file:
        content = file.read()
      # print(file)
    model = extract_model_from_file(content)
    df_models = df_models.append(model, ignore_index=True)
    #print(model)

# read new model

#working on it

#for newfile in golb.golb('C:\\Users\\vanderweck\\PycharmProjects\\Masterarbeit\\Systemmodelle\\NewModel\\*.xmi'):
 #   with open(newfile, 'r') as newfileopen:
 #       content = newfileopen.read()

path_to_new_xmi_file = 'C:\\Users\\vanderweck\\PycharmProjects\\Masterarbeit\\Systemmodelle\\NewModel\\'
new_files = [f for f in glob.glob(path_to_new_xmi_file + "*.xmi")]

for new_file in new_files:
    #print(file_name)
    with open(new_file, 'r') as file:
        content = file.read()

# working solution
#with open('C:\\Users\\vanderweck\\PycharmProjects\\Masterarbeit\\Systemmodelle\\NewModel\\ID7.xmi',
#          'r') as file:  # DO: specify new model path
#    content = file.read()

new_model = extract_model_from_file(content)
congruencies = compare_new_model_to_known(new_model, df_models)
# print(new_model)

# find congruencies
highest_congruency = 0
hc_model = 0  # Model with highest congruency
for model in congruencies:
    if highest_congruency < congruencies[model]:
        highest_congruency = congruencies[model]
        hc_model = model

# Output for model with highest congruency (can be forwarded to UI)

print('Modell mit höchster Übereinstimmung')
print('Modellname: ' + df_models.loc[hc_model].model_name)
print('Grad der Übereinstimmung: ' + str(highest_congruency))
print('Ist fehlerhaft: ' + str(df_models.loc[hc_model].is_error))
print('Fehlerbeschreibung: ' + df_models.loc[hc_model].error_description)
print('Kontext:')
print('Fehlerbeschreibung: ' + df_models.loc[hc_model]['01_Aussentemperatur'])
print('Fehlerbeschreibung: ' + df_models.loc[hc_model]['03_Motordrehzahl'])
print('Fehlerbeschreibung: ' + df_models.loc[hc_model]['02_Luftfeuchtigkeit'])
