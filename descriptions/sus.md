# System Usability Scale (SUS)

## Authors

Brooke, John. (1995). SUS: A quick and dirty usability scale. Usability Eval. Ind.. 189. [https://www.researchgate.net/publication/228593520_SUS_A_quick_and_dirty_usability_scale](https://www.researchgate.net/publication/228593520_SUS_A_quick_and_dirty_usability_scale)

## About

The System Usability Scale (SUS) is a simple, ten-item scale giving a global view of subjective assessments of usability. It was created by John Brooke in 1986 to be a "quick and dirty", reliable tool for measuring the usability. SUS has become an industry standard, with references in over 1300 articles and publications.

## Items

5-points Likert scales, Strongly disagree to Strongly agree:

- Q1: I think that I would like to use this system frequently.
- Q2: I found the system unnecessarily complex.
- Q3: I thought the system was easy to use.
- Q4: I think that I would need the support of a technical person to be able to use this system.
- Q5: I found the various functions in this system were well integrated.
- Q6: I thought there was too much inconsistency in this system.
- Q7: I would imagine that most people would learn to use this system very quickly.
- Q8: I found the system very cumbersome to use.
- Q9: I felt very confident using the system.
- Q10: I needed to learn a lot of things before I could get going with this system.

## Themes

- Learnability (items 4 and 10)
- Usability (other items: items 1, 2, 3, 5, 6, 7, 8, 9)

Source: [https://uxpajournal.org/revisit-factor-structure-system-usability-scale/](https://uxpajournal.org/revisit-factor-structure-system-usability-scale/)

## Transform

### Compute total SUS score

For odd items: subtract one from the user response.
For even-numbered items: subtract the user responses from 5. This scales all values from 0 to 4 (with four being the most positive response).
Add up the converted responses for each user and multiply that total by 2.5. This converts the range of possible values from 0 to 100 instead of from 0 to 40.

### Compute score by themes

Note: didn’t find official formula to compute learnability and usability. I applied the same protocol but multiplying buy 12.5 for learnability and 3.125 for usability to convert at same range as overall scoring.

## Interpretation

### SUS Grade

- 0–25.0: F  
- 25.1–51.6: F  
- 51.7–62.6: D  
- 62.7–64.9: C−  
- 65.0–71.0: C  
- 71.1–72.5: C+  
- 72.6–74.0: B−  
- 74.1–77.1: B  
- 77.2–78.8: B+  
- 78.9–80.7: A−  
- 80.8–84.0: A  
- 84.1–100: A+

### Acceptability

- 0–51.6: Not Acceptable  
- 51.7–71.0: Marginal  
- 71.1–100: Acceptable

Source: [https://measuringu.com/interpret-sus-score/](https://measuringu.com/interpret-sus-score/)

### Predicting NPS from SUS score

LTR = 1.33 + 0.08(SUS)

Source: [https://measuringu.com/nps-sus/](https://measuringu.com/nps-sus/)

### Market Average

The market average SUS score is 68.

Source: [https://measuringu.com/sus/](https://measuringu.com/sus/)
