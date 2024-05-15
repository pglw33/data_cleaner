import streamlit as st
import re
import pandas as pd
from streamlit_tags import st_tags

st.title("Data cleaner")
ss=st.session_state
uploaded_file=st.file_uploader("Importez Votre fichier CSV ici:")
list_dep = st_tags(label="Départements à filtrer")

def supprimer_retour_ligne(chaine):
    return chaine.replace("\n", "")

def decouper_adresse(adresse):
    regex = r'^(.*?)\s+(\d{5})\s+(.*?)$'
    match = re.match(regex, adresse)
    if match:
        return match.group(1).strip(), match.group(2), match.group(3).strip()
    else:
        return None, None, None

def starts_with_dep(list_str,number):
    if len(list_str)==0:
        val = True
    else:
        number_str = str(number)
        val = any(number_str.startswith(element) for element in list_str)
    return(val)


def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

def pipeline(df,list_depa):
    df_final=df[["Dénomination de la société", "Lien-href", 'Activité', "SIREN", "APE", "Activité principale", "Adresses", "Nature juridique", "Salariés", "Date de création", "Description"]].copy()
    df_final["Adresses"]=df_final["Adresses"].astype(str).apply(supprimer_retour_ligne)
    df_final['Adresse'], df_final['Code postal'], df_final['Ville'] = zip(*df_final['Adresses'].apply(decouper_adresse))
    df_final=df_final.rename(columns={"Dénomination de la société": "Nom de l'entreprise", "Lien-href": "Lien Data.Gouv"})
    df_final["Code postal"]=df_final["Code postal"].fillna(0).astype(int)
    df_final["check"]=df_final["Code postal"].apply(lambda x: starts_with_dep(list_depa,x))
    df_final=df_final[df_final["check"]==True]
    df_final=df_final.drop(columns=["Adresses", "check"])
    return(df_final)

if (uploaded_file is not None):
    # Read the CSV file into a DataFrame
    dataframe_input = pd.read_csv(uploaded_file)
    try:
        dataframe_final = pipeline(dataframe_input,list_dep)
        st.dataframe(dataframe_final)
        csv = convert_df(dataframe_final)

        st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
        )
    except:
        st.write("Le dataframe uploadé n'est pas valide.")





