#!/usr/bin/env python3
"""Add the work-in-progress pages to the User Manual landing page 1326972929 (storage edit)."""
import sys, os, re, importlib.util, html
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
PID = "1326972929"; DRY = "--dry-run" in sys.argv
p = pub.api(base, auth, "GET", f"/api/v2/pages/{PID}?body-format=storage")
if str(p["id"]) != PID: sys.exit("crossed read")
s = p["body"]["storage"]["value"]

def row(title, text, desc):
    t = html.escape(title, quote=True)
    return (f'<tr><td><p><ac:link><ri:page ri:content-title="{t}" /><ac:link-body>{html.escape(text)}</ac:link-body></ac:link></p></td>'
            f'<td><p>{html.escape(desc)} In review.</p></td></tr>')

ADD = {
 "Orders and samples": [
  ("Register a New Patient", "Register a new patient", "Add a patient record so the patient can be linked to orders."),
  ("Patient Management", "Patient management", "Find an existing patient to view or edit their record."),
  ("Merge Patient Records", "Merge patient records", "Combine two duplicate patient records into one."),
  ("Enter a clinical order", "Enter a clinical order", "Register a clinical order: the patient, the requesting site and provider, and its sample types and tests."),
  ("Prepare samples for a clinical order", "Prepare samples for a clinical order", "Record each sample of an order: collection, arrival, labels and storage."),
  ("Complete the sample check for a clinical order", "Complete the sample check for a clinical order", "Confirm each sample is acceptable and release the order to the laboratory."),
  ("Label & store samples (shared stage)", "Label and store samples (shared stage)", "Print order and specimen labels and assign each sample a storage location."),
 ],
 "Results, validation and reports": [
  ("Custom Data Export and My Report Queue", "Custom Data Export and My Report Queue", "Build a CSV extract of samples, tests, results and turnaround times without SQL, and rerun it for a new period."),
 ],
 "Environmental surveillance": [
  ("Enter results & read the compliance evaluation", "Enter results and read the compliance evaluation", "Record results for an environmental order and read the automatic pass or fail verdict."),
  ("Validate & release results", "Validate and release environmental results", "Review and release environmental results so they are final."),
 ],
 "Users, organizations and providers": [
  ("Admin: Import and export locations", "Import and export locations", "Load or update organizations, wards, sampling sites and geographic areas in bulk from CSV files."),
  ("Admin: Manage geographic areas", "Manage geographic areas", "Keep the list of administrative areas that patient addresses, organizations and sampling sites point to."),
  ("Admin: Manage sampling sites", "Manage sampling sites", "Record the fixed places where environmental samples are collected."),
 ],
 "Test catalog": [
  ("Test Catalog Management: the unified editor", "The unified test editor", "How the Test Catalogue Management editor is laid out and how its sections save."),
  ("Duplicate a test", "Duplicate a test", "Start a new test from a copy of an existing one."),
  ("Read-only & cross-link sections", "Read-only and cross-link sections", "The editor sections that show information kept elsewhere, and where to change it."),
  ("Manage lab units", "Manage lab units", "Create and maintain lab units: their domain, whether they are active, their tests and their display order."),
  ("Import a test catalog from CSV", "Import a test catalog from CSV", "Load or update the test catalog from CSV files instead of editing tests one at a time."),
  ("Author the test catalog in CSV files", "Author the test catalog in CSV files", "Write the CSV files a site's test catalog is loaded from."),
 ],
 "Result reporting and analyzers": [
  ("Set up an analyzer", "Set up an analyzer", "Connect a laboratory analyser so its results arrive in OpenELIS against the right tests."),
  ("Map analyzer codes, resolve held results, and run QC", "Map analyzer codes, resolve held results and run QC", "Map an analyser's codes, clear held and undelivered results, and run Westgard QC."),
  ("Install the Analyzer Bridge", "Install the Analyzer Bridge", "Install and configure the Analyzer Bridge and pair it with OpenELIS."),
 ],
}
QA = [
  ("EQA provider: run a proficiency testing scheme", "EQA provider: run a proficiency testing scheme", "Run an EQA scheme for other laboratories: enrol them, ship panels, score results and follow up failures."),
  ("EQA participant: take part in a proficiency testing scheme", "EQA participant: take part in a proficiency testing scheme", "Enrol in an EQA scheme, test the panel, submit results and act on the scores."),
  ("Statistical QC: overview and daily review", "Statistical QC: overview and daily review", "Find statistical QC in OpenELIS and check each day whether any control has failed."),
  ("Receive and activate a control lot", "Receive and activate a control lot", "Register a new lot of control material so its results are judged against the lot's targets."),
  ("Review and act on alerts", "Review and act on alerts", "See the alerts OpenELIS has raised, such as overdue STAT orders and EQA deadlines, and record what was done."),
  ("Test accreditation and report logos", "Test accreditation and report logos", "Record the bodies that accredit your laboratory and their tests, so reports carry the right logo."),
]

def table_end(s, heading):
    i = s.find(f"<h3>{heading}</h3>")
    if i < 0: sys.exit("heading not found: " + heading)
    j = s.find("</tbody></table>", i)
    return j

changes = []
for h, rows in ADD.items():
    for (title, text, desc) in rows:
        if f'ri:content-title="{html.escape(title, quote=True)}"' in s: continue
        j = table_end(s, h); s = s[:j] + row(title, text, desc) + s[j:]; changes.append(f"{h}: + {title}")

# mark the merged organizations row as in review
k = s.find('ri:content-title="Admin: Manage organizations"')
if k > 0:
    e = s.find("</p></td></tr>", k)
    if "In review." not in s[k:e]:
        s = s[:e] + " In review." + s[e:]; changes.append("Manage organizations row marked In review")

if "<h3>Quality assurance</h3>" not in s:
    sec = ('<h3>Quality assurance</h3><p>External quality assessment, statistical QC, alerts and accreditation. '
           '<a href="https://uwdigi.atlassian.net/wiki/spaces/oeg/folder/1706098877">Open the folder</a>.</p>'
           '<table data-layout="default"><tbody><tr><th><p>Page</p></th><th><p>What it helps you do</p></th></tr>'
           + "".join(row(*r) for r in QA) + '</tbody></table>')
    i = s.find("<h3>Laboratory notebooks</h3>")
    s = s[:i] + sec + s[i:]; changes.append("Quality assurance section added")

old_intro = "Pages marked Older format come from the previous manual and are being rewritten; they are still the best guide for those workflows."
if old_intro in s and "In review are published" not in s:
    s = s.replace(old_intro, old_intro + " Pages marked In review are published before their review is finished, so you can use them now; details may still change.")
    changes.append("intro: In review explained")
old_rel = "new pages waiting for review before they join the manual."
if old_rel in s:
    s = s.replace(old_rel, "planning notes and drafts that are not ready to publish."); changes.append("Related: review area wording")

if "—" in "".join(changes): sys.exit("em dash")
print("\n".join(changes))
if DRY: sys.exit(0)
r = pub.api(base, auth, "PUT", f"/api/v2/pages/{PID}", {"id": PID, "status": "current", "title": p["title"], "parentId": p["parentId"],
    "body": {"representation": "storage", "value": s}, "version": {"number": p["version"]["number"] + 1, "message": "In-review pages added to the manual"}})
print("landing v%d" % r["version"]["number"])
