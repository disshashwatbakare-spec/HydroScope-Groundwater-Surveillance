from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT = "HydroScope_Project_Overview.docx"

NAVY = "17365D"
BLUE = "DCEAF7"
PALE = "F5F8FC"
GRID = "D9D9D9"

def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)

def set_cell_border(cell, color=GRID):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = "w:" + edge
        el = borders.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            borders.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:color"), color)

def set_cell_margin(cell, top=90, start=110, bottom=90, end=110):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    mar = tc_pr.first_child_found_in("w:tcMar")
    if mar is None:
        mar = OxmlElement("w:tcMar")
        tc_pr.append(mar)
    for side, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = mar.find(qn("w:" + side))
        if node is None:
            node = OxmlElement("w:" + side)
            mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")

def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.text = h
        shade(cell, NAVY)
        set_cell_border(cell)
        set_cell_margin(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True; r.font.color.rgb = RGBColor(255,255,255); r.font.size = Pt(9)
    for ri, row in enumerate(rows):
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cell = cells[i]
            cell.text = str(value)
            if ri % 2 == 1: shade(cell, PALE)
            set_cell_border(cell); set_cell_margin(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for p in cell.paragraphs:
                for r in p.runs: r.font.size = Pt(9)
    if widths:
        for row in table.rows:
            for i, width in enumerate(widths): row.cells[i].width = Inches(width)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)
    return table

def bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
    p.add_run(text)
    return p

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.65); sec.bottom_margin = Inches(0.65)
sec.left_margin = Inches(0.7); sec.right_margin = Inches(0.7)

styles = doc.styles
styles["Normal"].font.name = "Aptos"; styles["Normal"]._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
styles["Normal"].font.size = Pt(10)
styles["Normal"].paragraph_format.space_after = Pt(5)
for name, size in (("Title", 21), ("Heading 1", 14), ("Heading 2", 11)):
    s = styles[name]; s.font.name = "Aptos Display"; s._element.rPr.rFonts.set(qn("w:ascii"), "Aptos Display")
    s.font.size = Pt(size); s.font.color.rgb = RGBColor(0,0,0)
    s.font.bold = True
styles["Heading 1"].paragraph_format.space_before = Pt(13); styles["Heading 1"].paragraph_format.space_after = Pt(5)
styles["Heading 2"].paragraph_format.space_before = Pt(8); styles["Heading 2"].paragraph_format.space_after = Pt(3)

p = doc.add_paragraph(style="Title"); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("HydroScope Project Overview")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("AI Powered Groundwater Contamination Surveillance System")
r.bold = True; r.font.size = Pt(11); r.font.color.rgb = RGBColor(55,55,55)

p = doc.add_paragraph()
p.add_run("Purpose. ").bold = True
p.add_run("HydroScope converts historical groundwater observations into a practical testing-priority strategy. It helps field teams focus limited laboratory capacity on wells with the strongest evidence of high salinity risk or unusual local behaviour.")

doc.add_heading("1  Problem Being Solved", level=1)
doc.add_paragraph("Groundwater monitoring networks contain many more wells than can be tested each month. Random testing is slow and can miss high-risk locations. HydroScope uses historical patterns, local hydro-geological context and anomaly signals to rank wells for investigation.")
add_table(doc, ["Challenge", "HydroScope response"], [
    ["Rare high risk cases", "Uses SMOTE and suitable evaluation metrics so the model does not simply predict every well as clean."],
    ["Limited test budget", "Ranks wells by predicted risk and information value instead of selecting them randomly."],
    ["Regional differences", "Groups comparable wells first, then detects unusual wells within their local group."],
    ["Need for explanations", "Uses a Bayesian evidence layer to explain which factors drive a priority decision."],
], [2.0, 4.8])
doc.add_paragraph("In this prototype, contamination is an operational proxy: a record is labelled high risk when Electrical Conductivity (EC) is above 3,000 microSiemens/cm. EC indicates salinity or dissolved-ion loading; it is not a complete diagnosis of every contaminant.")

doc.add_heading("2  Data Used", level=1)
doc.add_paragraph("The project uses Central Ground Water Board style monitoring files for Maharashtra, Andhra Pradesh, West Bengal, Rajasthan and Gujarat. There are 15 raw CSV files: three data categories for each state.")
add_table(doc, ["Dataset", "Files", "Fields per file", "Current records", "Examples"], [
    ["Chemical water quality", "5", "46", "36,769", "EC, pH, TDS, fluoride, nitrate, chloride, metals"],
    ["Physical water quality", "5", "21", "50,232", "Temperature, turbidity, station and location fields"],
    ["Groundwater level", "5", "21", "47,668", "Quarterly groundwater level and elevation reference"],
], [1.45, 0.55, 0.8, 0.9, 3.1])
doc.add_paragraph("The chemical table supplies the EC value used to create the target label. It also contains richer chemistry such as fluoride, nitrate and trace metals, but these are not classifier inputs because they are normally known only after a water test.")
doc.add_heading("Electrical Conductivity as the Prediction Target", level=2)
doc.add_paragraph("Electrical Conductivity (EC) measures how easily water conducts electricity. Water with more dissolved charged particles - especially salts and minerals such as sodium, chloride, calcium and magnesium - conducts electricity more easily and therefore has a higher EC reading. EC is reported here in microSiemens per centimetre (microSiemens/cm).")
doc.add_paragraph("HydroScope uses EC as a practical salinity-risk proxy. For each historical record, EC above 3,000 microSiemens/cm becomes is_contaminated = 1; EC at or below that threshold becomes is_contaminated = 0. The classifier then learns which pre-test location and groundwater patterns are associated with this high-EC label, so it can rank a new or untested well for follow-up.")
doc.add_paragraph("A high EC result signals elevated dissolved-ion or salinity risk and makes the well a stronger candidate for laboratory testing. It does not by itself identify the exact pollutant or prove every aspect of water quality is unsafe; fluoride, nitrate, bacteria and metals require their own tests. In this project, EC is the consistent measurable indicator used to define and predict the high-risk class.")
doc.add_paragraph("Important coverage note: the current Rajasthan and Gujarat chemical files contain headers but no data rows. The architecture supports five states, but the present EC-labelled supervised training data is effectively drawn from the available Andhra Pradesh, Maharashtra and West Bengal chemistry records.")

doc.add_heading("3  Data Processing and Feature Set", level=1)
doc.add_paragraph("Records are normalized and merged primarily by station, district, state and month. The merged dataset has 102,109 observation rows and 86 columns. A row is a monitoring observation, not necessarily a unique physical well; stations can recur over time.")
add_table(doc, ["Pipeline dataset", "Rows", "Columns", "Purpose"], [
    ["Unified dataset", "102,109", "86", "Merged chemical, physical and groundwater-level observations"],
    ["Prepared dataset", "36,922", "11", "EC-labelled, model-ready records"],
    ["Clustered dataset", "36,922", "13", "Prepared records plus DBSCAN and agglomerative labels"],
    ["Anomaly dataset", "36,922", "15", "Clustered records plus anomaly score and flag"],
], [1.45, 0.75, 0.75, 3.85])
doc.add_heading("Model Inputs", level=2)
doc.add_paragraph("All main predictive and local-context stages use the same five leak-free features:")
for item in ["Latitude and longitude - where the monitoring point is located.", "Groundwater level in metres - a hydrological indicator.", "Encoded state and district - regional context."]:
    bullet(doc, item)
doc.add_paragraph("Target: is_contaminated = 1 when EC > 3,000 microSiemens/cm; otherwise 0. The final prepared file retains station, state, district, date and EC for reporting and validation, not as prediction features.")

doc.add_heading("4  Risk Classification", level=1)
doc.add_paragraph("The classifier answers: before a current laboratory test, how likely is this record to exceed the high-EC threshold from its geographic and groundwater context?")
add_table(doc, ["Model", "Role", "Key configuration"], [
    ["Random Forest plus SMOTE", "Primary model", "200 trees, maximum depth 12, class balancing"],
    ["AdaBoost plus SMOTE", "Secondary comparison", "150 estimators, learning rate 0.5"],
    ["K Nearest Neighbours", "Simple baseline", "7 neighbours, no SMOTE"],
], [1.8, 1.35, 3.65])
doc.add_paragraph("High-EC records are rare, so normal accuracy would be misleading. SMOTE generates minority-class examples only in training, allowing the models to learn rare high-risk patterns. Evaluation uses ROC-AUC, precision, recall, average precision and a cost-sensitive threshold.")
doc.add_paragraph("The cost rule gives a missed high-EC record ten times the penalty of an unnecessary test: Cost = 100 x false negatives + 10 x false positives. The documented Random Forest result is approximately ROC-AUC 0.922, making it the preferred risk-ranking model.")

doc.add_heading("5  Local Hydro Geological Context", level=1)
doc.add_paragraph("A national-level comparison can be misleading. For example, a shallow groundwater level may be normal in a coastal or alluvial zone yet unusual in a deep arid aquifer. HydroScope therefore evaluates a well against its local peers.")
doc.add_heading("Spatial grouping with DBSCAN", level=2)
doc.add_paragraph("DBSCAN clusters wells using the five context features after standardisation. It identifies dense, irregularly shaped regional groups and marks isolated wells as noise rather than forcing them into a group. EC is never used to form clusters, preventing target leakage. The documented implementation uses eps 0.35 and minimum samples 10, and reports about 39 clusters.")
doc.add_heading("Within cluster anomaly detection", level=2)
doc.add_paragraph("Isolation Forest runs separately inside each sufficiently large DBSCAN cluster. It uses the same five features and identifies records that can be isolated unusually quickly from their local peers. More negative anomaly scores mean more unusual behaviour; is_anomaly = 1 marks a local outlier. Tiny clusters and DBSCAN noise points are not scored in the same way.")

doc.add_heading("6  Explainable Risk and Testing Priority", level=1)
doc.add_paragraph("The Bayesian module is designed to combine five understandable evidence signals: state, groundwater-depth category, district risk, cluster risk and anomaly flag. It estimates P(high EC | evidence) and can express the reason for a recommendation in plain language.")
add_table(doc, ["Evidence", "Interpretation"], [
    ["Groundwater depth", "Shallow, medium or deep category"],
    ["District risk", "Whether historical district EC suggests elevated risk"],
    ["Cluster risk", "Whether the local cluster has at least 10 percent high-EC records"],
    ["Anomaly flag", "Whether the record differs from its local peers"],
    ["State", "Broad regional baseline"],
], [1.65, 5.15])
doc.add_paragraph("The intended operational output is a ranked laboratory testing queue. High predicted risk, high-risk cluster membership, local anomaly evidence and uncertainty can all increase priority. This supports a field team in making better use of a fixed testing budget.")

doc.add_heading("7  Current Implementation Status", level=1)
doc.add_paragraph("The executable full pipeline runs ingestion, merging, preparation, classification, clustering and anomaly detection. The Bayesian-network module exists separately but is not called by the full runner. The active-learning backend file is currently empty, and the Next.js dashboard uses seeded demonstration records rather than a live connection to the Python output. These are clear next steps for turning the prototype into a fully integrated deployment.")

doc.add_heading("8  One Minute Project Summary", level=1)
doc.add_paragraph("HydroScope is a groundwater-testing prioritization system. It learns high-EC risk from historical monitoring data without using the current water test as an input. It then groups wells by local hydro-geological similarity, flags locally unusual records and combines these signals into an explainable priority view. The result is a more systematic way to decide which wells should receive limited laboratory attention first.")

footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = footer.add_run("HydroScope Project Overview")
fr.font.size = Pt(8); fr.font.color.rgb = RGBColor(100,100,100)

doc.save(OUT)
print(OUT)
