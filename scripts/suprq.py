from scripts.utils import *

class SUPRQ:
    def __init__(self, raw):
        self.raw = raw
        self.df = self.processed(raw)
        self.mci = mci(self.df['UserScore'])
        self.mci_usability = mci(self.df['Usability'])
        self.mci_credibility = mci(self.df['Credibility'])
        self.mci_appearance = mci(self.df['Appearance'])
        self.mci_loyalty = mci(self.df['Loyalty'])

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
        
        df["Q5_halved"] = df["Q5"] * 0.5
        
        def scoring(row):
            score = (row[["Q1", "Q2", "Q3", "Q4", "Q5_halved", "Q6", "Q7", "Q8"]].sum()) / 8
            return score

        df["UserScore"] = df.apply(scoring, axis=1)

        df["Usability"] = df[["Q1", "Q2"]].mean(axis=1)
        df["Credibility"] = df[["Q3", "Q4"]].mean(axis=1)
        df["Loyalty"] = df[["Q5_halved", "Q6"]].mean(axis=1)
        df["Appearance"] = df[["Q7", "Q8"]].mean(axis=1)
        
        return df

def slider_suprq(score, score_class):
    with open("assets/slider-suprq.svg", "r") as f:
        svg = f.read()
    svg = svg.replace("*sc*", str(score))
    svg = svg.replace('width="809"', 'width=100%')
    css1 = f"<style>[id^='bubble-'] {{opacity: 0;}} [id^='frame-'] {{opacity: 0.5;}}</style>"
    css2 = f"<style>#bubble-{score_class}, #frame-{score_class} {{opacity: 1 !important;}}</style>"
    html = css1 + css2 + svg
    # Streamlit doesn't render raw SVG directly, so wrap it in HTML
    st.markdown(f"<div style='max-width: 100%;'>{html}</div>", unsafe_allow_html=True)
