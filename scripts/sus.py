import streamlit as st
import numpy as np
from scipy import stats

class sus:
    def __init__(self, raw):
        self.raw = raw
        self.df = self.processed(raw)
        self.scores = self.df['UserScore']
        self.mean = self.scores.mean()
        self.grade = self.as_grade(self.mean)
        self.acceptability = self.as_acceptability(self.mean)
        self.sd = self.scores.std(ddof=1)
        self.n = len(self.scores)
        self.se = self.sd / np.sqrt(self.n)
        self.dfree = self.n - 1
        self.t_crit = stats.t.ppf(1 - 0.05/2, self.dfree)
        self.errormargin = self.t_crit * self.se
        self.ci_low = self.mean - self.errormargin
        self.ci_high = self.mean + self.errormargin
        self.ci_low_grade = self.as_grade(self.ci_low)
        self.ci_low_acceptability = self.as_acceptability(self.ci_low)
        self.ci_high_grade = self.as_grade(self.ci_high)
        self.ci_high_acceptability = self.as_acceptability(self.ci_high)

    def processed(self, df):
        to_remove = [col for col in df.columns if not col.startswith("Q")]
        df = df.drop(columns=to_remove)

        to_keep = [col for col in df.columns if col.startswith("Q")]
        model = [f"Q{i}" for i in range(1, 11)]
        if to_keep != model:
            st.error(f"The uploaded file does not conform to the SUS template. Please ensure that the question columns are named exactly as: Q1 to Q10.")
            st.stop()

        n = len(df)
        if n < 2:
            st.error("The uploaded file must contain responses from at least 2 users.")
            st.stop()

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
        col = df.pop("UserScore")   # remove the column
        df.insert(0, "UserScore", col)  # reinsert at position 0

        df['Grades'] = df['UserScore'].apply(self.as_grade)
        col = df.pop("Grades")   # remove the column
        df.insert(0, "Grades", col)  # reinsert at position 0

        df['Acceptability'] = df['UserScore'].apply(self.as_acceptability)
        col = df.pop("Acceptability")   # remove the column
        df.insert(0, "Acceptability", col)  # reinsert at position 0

        return df

    def as_grade(self, s):
        if s <= 60:
            return "F"
        elif s <= 70:
            return "D"
        elif s <= 80:
            return "C"
        elif s <= 90:
            return "B"
        else:
            return "A"

    def as_acceptability(self, s):

        if s <= 50:
            return "NAC"   # Not Acceptable
        elif s <= 62:
            return "MAL"   # Marginal Low
        elif s <= 70:
            return "MAH"   # Marginal High
        else:
            return "ACP"   # Acceptable
