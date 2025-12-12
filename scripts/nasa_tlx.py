from scripts.utils import *

class NASATLX:
    def __init__(self, raw):
        self.raw = raw
        self.df = self.processed(raw)
        self.mci = mci(self.df["Mean"])
        self.mci_mental_demand = mci(self.df["Q1"])
        self.mci_physical_demand = mci(self.df["Q2"])
        self.mci_temporal_demand = mci(self.df["Q3"])
        self.mci_performance = mci(self.df["Q4"])
        self.mci_effort = mci(self.df["Q5"])
        self.mci_frustration = mci(self.df["Q6"])

    def processed(self, df):
        to_remove = [col for col in df.columns if not col.startswith("Q")]
        df = df.drop(columns=to_remove)

        to_keep = [col for col in df.columns if col.startswith("Q")]
        model = [f"Q{i}" for i in range(1, 7)]
        if to_keep != model:
            raise ValueError(f"The uploaded file does not conform to the template. Please ensure that the question columns are named exactly as: Q1 to Q6.")

        n = len(df)
        if n < 2:
            raise ValueError("The uploaded file must contain responses from at least 2 users.")
        
        df = (df-1) * 5

        df["Mean"] = df.mean(axis=1)
        df["MeanInterpretation"] = df['Mean'].apply(nasa_tlx_interpret)

        return df
    
def nasa_tlx_interpret(x):
    if x <= 9:
        return "Low"
    elif x <= 29 :
        return "Medium"
    elif x <= 49:
        return "Somewhat-High"
    elif x <= 79:
        return "High"
    elif x <= 100:
        return "Very-High"

def slider_nasa_tlx(score, interpretation):
    with open("assets/slider-nasa_tlx.svg", "r") as f:
        svg = f.read()
    svg = svg.replace("*sc*", f"{str(score)}")
    svg = svg.replace('width="817"', 'width=100%')
    css1 = f"<style>[id^='bubble-'] {{opacity: 0;}} [id^='frame-'] {{opacity: 0.5;}}</style>"
    css2 = f"<style>#bubble-{interpretation}, #frame-{interpretation} {{opacity: 1 !important;}}</style>"
    html = css1 + css2 + svg
    # Streamlit doesn't render raw SVG directly, so wrap it in HTML
    st.markdown(f"<div style='max-width: 100% !important;'>{html}</div>", unsafe_allow_html=True)
