from scripts.utils import *
import pandas as pd

class nps:
    def __init__(self, raw):
        self.raw = raw
        self.df = self.processed(raw)
        self.mci = mci(self.df['Q1'])
        self.mci_grade = [sus_as_grade(x) for x in self.mci]
        self.mci_acceptability = [sus_as_acceptability(x) for x in self.mci]
        self.mci_learnability = mci(self.df['Learnability'])
        self.mci_usability = mci(self.df['Usability'])

    def processed(self, df):
        to_remove = [col for col in df.columns if not col.startswith("Q")]
        df = df.drop(columns=to_remove)

        to_keep = [col for col in df.columns if col.startswith("Q")]
        model = ["Q1"]
        if to_keep != model:
            raise ValueError(f"The uploaded file does not conform to the template. Please ensure that the question columns are named exactly as: Q1.")

        n = len(df)
        if n < 2:
            raise ValueError("The uploaded file must contain responses from at least 2 users.")

        # Apply SUS scoring rules
        for col in df.columns:
            if col in ["Q1", "Q3", "Q5", "Q7", "Q9"]:
                # Odd-numbered items
                df[col] = df[col] - 1
            elif col in ["Q2", "Q4", "Q6", "Q8", "Q10"]:
                # Even-numbered items
                df[col] = 5 - df[col]

        # Sum across the 10 items
        df["UserScore"] = df.sum(axis=1) * 2.5

        df['Grade'] = df['UserScore'].apply(sus_as_grade)

        df['Acceptability'] = df['UserScore'].apply(sus_as_acceptability)

        df["Learnability"] = df.filter(["Q4", "Q10"]).sum(axis=1) * (100/(2*4))
        df["Usability"] = df.filter(["Q1", "Q2", "Q3", "Q5", "Q6", "Q7", "Q8", "Q9"]).sum(axis=1) * (100/(8*4))

        return df
