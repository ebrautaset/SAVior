import pandas as pd
import pyreadstat
import os


class savParser:

    def __init__(self, path):
        #Henter path for filen som parses
        self.path = path
        # Leser SAV filen. df inneholder alle data, metadata inneholder labels
        self.df, self.meta = pyreadstat.read_sav(path, apply_value_formats=True )
        #Henter ut en liste med alle kolonner som starter med 'Q' -> Navn på alle spørsmål i datasettet
        self.Qs = list(filter(lambda x: x.startswith('Q'), list(self.df)))
        #Henter ut to lister, en med record+spørsmål og en total med spørsmål ekskludert
        self.nqind, self.qind = self.parseIND()

    
    def readData(self):
        df, meta = pyreadstat.read_sav(self.path)


    #Produserer to arrays. 1: qind som inneholder alle spørsmålsIDer (Q_Id) + 'record, og 2: nqind som henter ut alle felter forutenom, men ekskluderer spørsmålsIDer (Q_Id)

    def parseIND(self):
        
        
        qind = []
        nqind = []

        for ind,col in enumerate(self.df.columns):
            if col in self.Qs:
                qind.append(ind)
            elif col == 'record':
                try:
                    qind.append(ind)
                except:
                    pass
                try:
                    nqind.append(ind)
                except:
                    pass
            else:
                nqind.append(ind)

        return nqind,qind


    #Lager en oversikt over alle respondentene. Her eklskuderer vi alle spørsmål basert på verdiene i self.nqind. Vi lagrer resultatet som respondents.csv i cwd

    def getRespondents(self):
        tempdf = self.df.iloc[:,self.nqind]
        tempdf.to_csv(os.getcwd()+"/respondents.csv",index=False)


    #Lager en avpivotert liste med svar på alle spørsmål for hver eneste respondent. Lagres som questions.csv

    def getQuestions(self):
        Qdf = self.df.iloc[:,self.qind].melt(id_vars="record", var_name="q_ID")
        Qdf.columns = ['record','q_ID','valueLabel']

        #Qdf["qId+value"] = Qdf["question"]+ Qdf["value"].astype(str).apply(lambda x: x.zfill(5))

        Qdf.to_csv(os.getcwd()+"/questions.csv", index=False)


    # Henter ut alle labels og tilhørende verdier, slik at vi får informasjon om spørsmålene som tilhører hvert q_ID (spørsmålsID). Brukes som støttetabell. Lagres som question_labels.csv

    def getQuestionLabels(self):


        # Hent question keys and labels

        ColLabels = self.meta.column_names_to_labels

        data = {
            "q_ID" : [*ColLabels],
            "q_label" : [*ColLabels.values()]

        }

        # Fjerner linebreak i spørsmål, slik at vi ikke hopper over linjer i csv eksporten

        for i,s in enumerate(data["q_label"]):
            try:
                data["q_label"][i] = data["q_label"][i].replace('\n','')
            except:
                pass


        tempdf = pd.DataFrame(data)
        tempdf = tempdf.loc[tempdf['q_ID'].isin(self.Qs)]

        tempdf.to_csv(os.getcwd()+"/question_labels.csv", index=False)

    
    # Henter ut alle labels og tilhørende verdier for alle svarverdiene i datasettet, slik at vi kan sortere svaralternativene. Brukes som støttetabell
    
    def getValueLabels(self):

        qValues = self.meta.variable_value_labels


        qCodes = [*qValues]
        qCodeValues = [*qValues.values()]

        spm_svar_value = []
        spm_svar_label = []
        q_ID = []
        qidValue = []

        for i,q in enumerate(qCodes):

            keys = [*qCodeValues[i].keys()]
            vals = [*qCodeValues[i].values()]

            for e in range(0,len(keys)):
                #qidValue.append(qCodes[i]+ '{0:0>5}'.format(keys[e]) )
                spm_svar_value.append(keys[e])
                q_ID.append(qCodes[i])
                spm_svar_label.append(vals[e])

        data = {
            #"QId+value" : qidValue,
            "q_ID" : q_ID,
            "valueLabel" : spm_svar_label,
            "Value" : spm_svar_value
        }

        
        tempdf = pd.DataFrame(data)
        tempdf = tempdf.loc[tempdf['q_ID'].isin(self.Qs)]
        tempdf = tempdf.drop(columns=['q_ID'])
        #Må gjøres til lowercase ettersom powerBI er case insenstivive
        tempdf['valueLabel'] = tempdf['valueLabel'].str.lower()
        #Fjerner alle duplikater
        tempdf = tempdf.drop_duplicates(subset='valueLabel',keep='first')
        tempdf['Value'] = tempdf['Value'].astype(int) 
        #lagre values.csv
        tempdf.to_csv(os.getcwd()+"/values.csv", index=False)





if __name__ == "__main__":

    ob = savParser("eks.sav")

    ob.getRespondents()
    ob.getQuestions()
    ob.getQuestionLabels()
    ob.getValueLabels()