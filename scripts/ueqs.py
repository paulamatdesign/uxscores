from scripts.utils import *

class ueqs:
    def __init__(self, raw):
        self.raw = raw
        self.df = self.processed(raw)
        self.mci = mci(self.df['UserScore'])
        self.mci_pragmatic = mci(self.df["UserScore_Pragmatic"])
        self.mci_hedonic = mci(self.df["UserScore_Hedonic"])

    def processed(self, df):
        to_remove = [col for col in df.columns if not col.startswith("Q")]
        df = df.drop(columns=to_remove)

        to_keep = [col for col in df.columns if col.startswith("Q")]
        model = [f"Q{i}" for i in range(1, 9)]
        if to_keep != model:
            raise ValueError(f"The uploaded file does not conform to the template. Please ensure that the question columns are named exactly as: Q1 to Q8.")

        n = len(df)
        if n < 2:
            raise ValueError("The uploaded file must contain responses from at least 2 users.")
        
        df = df - 4
        
        df["UserScore"] = df.mean(axis=1)
        df["UserScore_Pragmatic"] = df.filter(["Q1", "Q2", "Q3", "Q4"]).mean(axis=1)
        df["UserScore_Hedonic"] = df.filter(["Q5", "Q6", "Q7", "Q8"]).mean(axis=1)

        return df
