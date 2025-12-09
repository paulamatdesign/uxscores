from scripts.utils import *
import pandas as pd

class NPS:
    def __init__(self, raw):
        self.raw = raw
        self.df = self.processed(raw)
        self.prop_detractors = self.prop_group("Detractors")
        self.prop_passives = self.prop_group("Passives")
        self.prop_promoters = self.prop_group("Promoters")
        self.score = 100 * (self.prop_promoters - self.prop_detractors)
        self.interpretation = self.interpret(self.score)

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
        
        def nps_as_group(x):
            x = int(x)
            if x <= 6:
                return "Detractors"
            elif x <= 8:
                return "Passives"
            else:
                return "Promoters"

        df['Group'] = df['Q1'].apply(nps_as_group)

        return df
    
    def prop_group(self, group):
        filtered = self.df[self.df["Group"] == group]
        return len(filtered) / len(self.df)

    def interpret(self, x):
        if x > 0:
            return "Good"
        elif x > 20:
            return "Favourable"
        elif x > 50:
            return "Excellent"
        elif x > 80:
            return "World-Class"
        else:
            return "Unacceptable"
        
def slider_nps(score, interpretation):
    with open("assets/slider-nps.svg", "r") as f:
        svg = f.read()
    svg = svg.replace("*sc*", f"{str(score)}%")
    svg = svg.replace('width="809"', 'width=100%')
    css1 = f"<style>[id^='bubble-'] {{opacity: 0;}} [id^='frame-'] {{opacity: 0.5;}}</style>"
    css2 = f"<style>#bubble-{interpretation}, #frame-{interpretation} {{opacity: 1 !important;}}</style>"
    html = css1 + css2 + svg
    # Streamlit doesn't render raw SVG directly, so wrap it in HTML
    st.markdown(f"<div style='max-width: 100%;'>{html}</div>", unsafe_allow_html=True)
