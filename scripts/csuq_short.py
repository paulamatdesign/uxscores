from scripts.utils import *

class csuq_short:
    def __init__(self, raw):
        self.raw = raw
        self.df = self.processed(raw)
        self.mci = mci(self.df["OverallMean"])
        self.mci_overall_satisfaction = mci(self.df['Q16'])
        self.mci_system_usefulness = mci(self.df["SystemUsefulness"])
        self.mci_information_quality = mci(self.df["InformationQuality"])
        self.mci_interface_quality = mci(self.df["InterfaceQuality"])

    def processed(self, df):
        to_remove = [col for col in df.columns if not col.startswith("Q")]
        df = df.drop(columns=to_remove)

        to_keep = [col for col in df.columns if col.startswith("Q")]
        model = [f"Q{i}" for i in range(1, 17)]
        if to_keep != model:
            raise ValueError(f"The uploaded file does not conform to the template. Please ensure that the question columns are named exactly as: Q1 to Q16.")

        n = len(df)
        if n < 2:
            raise ValueError("The uploaded file must contain responses from at least 2 users.")
          
        df["OverallMean"] = df.mean(axis=1)
        df["OverallInterpretation"] = df['OverallMean'].apply(csuq_interpret)
        df["SystemUsefulness"] = df.filter(["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]).mean(axis=1)
        df["InformationQuality"] = df.filter(["Q7", "Q8", "Q9", "Q10", "Q11", "Q12"]).mean(axis=1)
        df["InterfaceQuality"] = df.filter(["Q13", "Q14", "Q15"]).mean(axis=1)

        return df

def csuq_interpret(x):
    if x >= 5:
        return "High-Satisfaction"
    elif x >= 4 :
        return "Moderate-Satisfaction"
    elif x < 4:
        return "Low-Satisfaction"

def slider_csuq_short(score, interpretation):
    with open("assets/slider-csuq_short.svg", "r") as f:
        svg = f.read()
    svg = svg.replace("*sc*", f"{str(score)}")
    svg = svg.replace('width="822"', 'width=100%')
    css1 = f"<style>[id^='bubble-'] {{opacity: 0;}} [id^='frame-'] {{opacity: 0.5;}}</style>"
    css2 = f"<style>#bubble-{interpretation}, #frame-{interpretation} {{opacity: 1 !important;}}</style>"
    html = css1 + css2 + svg
    # Streamlit doesn't render raw SVG directly, so wrap it in HTML
    st.markdown(f"<div style='max-width: 100%;'>{html}</div>", unsafe_allow_html=True)
