#!/usr/bin/env python3
"""
Process all 13 members needing bio rewrites.
Following the documented workflow in Oct_29_Context_Recovery.md
"""

import json
import pandas as pd
from pathlib import Path

# LinkedIn profiles we fetched
linkedin_files = {
    "Terrance Long": "terrance-p-long-6b59829.json",
    "Douglas Sheil": "douglas-sheil-55330a9a.json",
    "Hollis Mclellan": "hollis-mclellan-a084b2b0.json",
    "Sarah Herzog": "sarah-herzog-78a07a243.json",
    "Nadait Gebremedhen": "nadaitgebremedhen.json",
    "Joe James": "joe-james-765b6415.json",
    "Scot Bryson": "scotbryson.json",
    "Coakee William Wildcat": "william-wildcat-93a21164.json",
    "Edib Korkut": "edib-korkut-21a00a29.json",
}

# Load LinkedIn data
linkedin_dir = Path("batches/linkedin_profiles")
linkedin_data = {}

for name, filename in linkedin_files.items():
    filepath = linkedin_dir / filename
    if filepath.exists():
        with open(filepath) as f:
            data = json.load(f)
            linkedin_data[name] = data['extracted']['full_text']

print(f"Loaded {len(linkedin_data)} LinkedIn profiles\n")
print("="*80)

# Bio rewrites based on research
# NOTE: Each bio was synthesized from LinkedIn + existing Airtable bio + Town Hall attendance
rewrites = {}

# 1. Terrance Long
print("\n1. Terrance Long")
print("   LinkedIn: Limited data (201 chars - possibly blocked)")
print("   Existing bio: 'Chair and CEO International Dialogues on Underwater Munitions (IDUM)'")
print("   Affiliation in DB: Retired military engineer, explosive ordnance disposal")
rewrites["Terrance Long"] = (
    "Terrance Long is Chair and CEO of International Dialogues on Underwater Munitions (IDUM), "
    "bringing decades of military engineering and explosive ordnance disposal expertise to addressing "
    "the environmental hazards of underwater munitions. His work connects military remediation with "
    "ocean ecosystem restoration and safety."
)

# 2. Fernando Cervignon  
print("\n2. Fernando Cervignon")
print("   No LinkedIn in DB")
print("   Airtable bio mentions: Trees4Humanity.org, Universidad Carlos III, Amazon/Borneo/Africa work")
rewrites["Fernando Cervignon"] = (
    "Fernando Cervignon founded Trees4Humanity.org and teaches at Universidad Carlos III de Madrid. "
    "His environmental protection work spans the Amazon, Borneo orangutan conservation, and anti-poaching "
    "efforts in Africa. He advocates for integrating technology, creative thinking, and Indigenous knowledge "
    "to address ecosystem threats."
)

# 3. Douglas Sheil
print("\n3. Douglas Sheil")
print("   LinkedIn: Prof at Wageningen University, ecologist/forester/conservationist")
if "Douglas Sheil" in linkedin_data:
    text = linkedin_data["Douglas Sheil"]
    print(f"   LinkedIn text: {len(text)} chars - has full profile")
rewrites["Douglas Sheil"] = (
    "Douglas Sheil is a Professor at Wageningen University and Research in the Netherlands and an affiliated "
    "researcher at the University of Oxford. An ecologist, forester, and conservationist, his research focuses "
    "on tropical forest ecosystems and their role in climate regulation. His work bridges ecological science "
    "with forest conservation practice, including recent investigations of the Biotic Pump theory."
)

# 4. Hollis Mclellan
print("\n4. Hollis Mclellan")
print("   LinkedIn: Limited data (201 chars)")
print("   DB affiliation: Founder of the Collaborative for Change, Public Health Consultant")
rewrites["Hollis Mclellan"] = (
    "Hollis Mclellan is a public health consultant specializing in environmental health and founder of the "
    "Collaborative for Change, which incubates and supports ecosystem restoration projects. Her work connects "
    "public health outcomes with ecological restoration, emphasizing the health benefits of restored ecosystems."
)

# 5. Sarah Herzog  
print("\n5. Sarah Herzog")
if "Sarah Herzog" in linkedin_data:
    text = linkedin_data["Sarah Herzog"]
    print(f"   LinkedIn: {len(text)} chars - full profile available")
    print("   DB affiliation: High School Biology/Life Science Teacher")
rewrites["Sarah Herzog"] = (
    "Sarah Herzog is a secondary science educator in Rochester, New York with a strong interest in transitioning "
    "to ecological restoration work. Her focus areas include permaculture, biodiversity conservation, sustainable "
    "infrastructure, phytoremediation, and biomimicry applications. She brings a systems-thinking approach from "
    "her science education background."
)

# 6. Nadait Gebremedhen
print("\n6. Nadait Gebremedhen")
if "Nadait Gebremedhen" in linkedin_data:
    text = linkedin_data["Nadait Gebremedhen"]
    print(f"   LinkedIn: {len(text)} chars - full profile")
    print("   Existing bio: Medical doctor turned social entrepreneur, founded Hagush/Taghuj")
rewrites["Nadait Gebremedhen"] = (
    "Nadait Gebremedhen, MD, is a medical doctor turned social entrepreneur who founded Hagush, a nonprofit "
    "social enterprise focused on creating a just and inclusive economy. Her work in global development addresses "
    "structural dimensions of inequality in the global economy, combining economic history with practical solutions "
    "for advancing sustainable development goals, with particular focus on Africa."
)

# 7. Joe James  
print("\n7. Joe James")
if "Joe James" in linkedin_data:
    text = linkedin_data["Joe James"]
    print(f"   LinkedIn: {len(text)} chars")
    print("   Existing bio: VERY long (500+ words) - needs condensing")
    print("   DB affiliation: Agri-Tech Producers LLC, patented CRBBP Process")
rewrites["Joe James"] = (
    "Joe James is President of Agri-Tech Producers LLC, where he developed the patented Combined Remediation "
    "Biomass and Bio-Product Production (CRBBP) Process. His approach uses fast-growing bio-crops for carbon "
    "capture via photosynthesis, then converts the biomass into biochar, bio-based filler powders, and other "
    "climate-smart products. Agri-Tech Producers partners with utilities and land-rich organizations to deploy "
    "the CRBBP process at scale, and was among the first 16 grantees of the US Government's BioMADE Program."
)

# 8. Scot Bryson
print("\n8. Scot Bryson")
if "Scot Bryson" in linkedin_data:
    text = linkedin_data["Scot Bryson"]
    print(f"   LinkedIn: {len(text)} chars - full profile")
    print("   Existing bio: Long life story - needs condensing")
    print("   DB affiliation: Orbital Farm")
rewrites["Scot Bryson"] = (
    "Scot Bryson founded Orbital Farm in 2018 to build closed-loop biotechnology systems that produce vaccines, "
    "medicines, hydrogen energy, and food using water, CO2, and electricity as primary inputs. His vision is to "
    "establish 200 circular mega-projects globally to address climate change and food security challenges."
)

# 9. Coakee William Wildcat
print("\n9. Coakee William Wildcat")
if "Coakee William Wildcat" in linkedin_data:
    text = linkedin_data["Coakee William Wildcat"]
    print(f"   LinkedIn: {len(text)} chars")
    print("   Airtable: Long bio with Indigenous background, ERA board member")
rewrites["Coakee William Wildcat "] = (  # Note: trailing space in Excel!
    "Coakee William Wildcat is Executive Director of Mother Tree Food & Forest and serves on the ERA board. "
    "Beginning life in the Oklahoma Seminole Nation, he integrates Indigenous agroecology, western soil ecology, "
    "syntropic agroforestry, and Miyawaki reforestation methods in his restoration work. He lives in the Mimbres "
    "watershed near the Gila wilderness, practicing and teaching approaches that help people meet their needs "
    "while restoring ecosystems and stabilizing climate."
)

# 10. Edib Korkut
print("\n10. Edib Korkut")
if "Edib Korkut" in linkedin_data:
    text = linkedin_data["Edib Korkut"]
    print(f"   LinkedIn: {len(text)} chars")
    print("   DB: Semi-retired MD in Washington DC")
rewrites["Edib Korkut"] = (
    "Edib Korkut is a semi-retired physician in Washington, DC with interests in ecosystem restoration "
    "and climate solutions."
)

# 11. Ryan Smith
print("\n11. Ryan Smith")
print("   No LinkedIn in DB")
print("   Airtable: Consulting forester in MA/CT, Yale School of Environment")
rewrites["Ryan Smith"] = (
    "Ryan Smith is a consulting forester working with private landowners in Massachusetts and Connecticut to "
    "promote forest restoration, agroforestry, and climate-smart management practices. A graduate of the Yale "
    "School of Environment, he brings experience working with smallholder farmers on three continents and a "
    "multidisciplinary approach to developing scalable, locally-adapted nature-based solutions."
)

# 12. Isabelle Claire Dela Paz
print("\n12. Isabelle Claire Dela Paz")
print("   No LinkedIn in DB")
print("   Airtable: CIFOR-ICRAF Philippines, urban agroforestry, IFSA President")
rewrites["Isabelle Claire Dela Paz"] = (
    "Isabelle Claire Dela Paz is Research and Communication Associate at CIFOR-ICRAF Philippines, engaged in "
    "projects advancing forest restoration. A forestry professional specializing in urban agroforestry, she "
    "graduated Magna Cum Laude from the University of the Philippines Los Baños and previously served as "
    "President of the International Forestry Students' Association (IFSA), advocating for meaningful youth "
    "engagement in the forestry sector."
)

# 13. Stephen Cook
print("\n13. Stephen Cook")
print("   No LinkedIn in DB")
print("   Airtable: Chief Strategy Officer, The Undaunted")
rewrites["Stephen Cook"] = (
    "Stephen Cook is Chief Strategy Officer at The Undaunted, a social impact organization. His work focuses "
    "on strategic planning and systems change for social and environmental challenges."
)

print("\n" + "="*80)
print(f"\n✅ Generated {len(rewrites)} bios")
print("\nNow updating Excel file...")

# Load Excel
df = pd.read_excel('member_reconciliation_report.xlsx', engine='openpyxl')

# Update each row
for name, bio in rewrites.items():
    mask = df['name_airtable'].str.strip() == name.strip()
    if mask.any():
        df.loc[mask, 'proposed_rewrites'] = bio
        df.loc[mask, 'comments'] = 'rewritten'
        print(f"✓ {name.strip()}: {len(bio)} chars")
    else:
        print(f"✗ NOT FOUND: {name}")

# Save
df.to_excel('member_reconciliation_report.xlsx', index=False, engine='openpyxl')
print("\n✅ Saved to member_reconciliation_report.xlsx")
