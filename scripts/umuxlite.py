from scripts.utils import *

class umuxlite:
    def __init__(self, raw):
        self.raw = raw
        self.df = self.processed(raw)
        self.mci = mci(self.df['UserScore'])
        self.mci_usability = mci(self.df['Usability'])
        self.mci_easeofuse = mci(self.df['EaseOfUse'])
        self.mci_sus = mci(self.df["SUS_Predicted"])
        self.mci_sus_grade = [sus_as_grade(x) for x in self.mci_sus]
        self.mci_sus_acceptability = [sus_as_acceptability(x) for x in self.mci_sus]

    def processed(self, df):
        to_remove = [col for col in df.columns if not col.startswith("Q")]
        df = df.drop(columns=to_remove)

        to_keep = [col for col in df.columns if col.startswith("Q")]
        model = [f"Q{i}" for i in range(1, 3)]
        if to_keep != model:
            raise ValueError(f"The uploaded file does not conform to the template. Please ensure that the question columns are named exactly as: Q1 to Q2.")

        n = len(df)
        if n < 2:
            raise ValueError("The uploaded file must contain responses from at least 2 users.")

        # Apply scoring rules
        for col in df.columns:
            df[col] = df[col] - 1

        # Sum across the 10 items
        df["UserScore"] = (df.sum(axis=1) / 12) * 100

        df["Usability"] = (df["Q1"] / 6) * 100
        df["EaseOfUse"] = (df["Q2"] / 6) * 100

        # Predict SUS Score
        df["SUS_Predicted"] = 0.65 * (df["UserScore"]) + 22.9

        df['SUS_Grade'] = df['SUS_Predicted'].apply(sus_as_grade)

        df['SUS_Acceptability'] = df['SUS_Predicted'].apply(sus_as_acceptability)

        return df
