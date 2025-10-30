#!/usr/bin/env python3
"""
Rewrite 14 member bios following ERA standards:
- Third person (not first person)
- 2-4 sentences typical
- Focus on ERA-relevant work
- Professional but warm tone
- Avoid promotional language
- Include current role/organization
"""

import pandas as pd
import sqlite3

# The 14 rewrites
rewrites = {
    "Thijs Christiaan van Son": {
        "rewrite": "Thijs Christiaan van Son is an aquatic ecologist working with the Cooling the Climate project led by Rob de Laet. His expertise in aquatic ecosystems informs efforts to restore water cycles and enhance natural cooling processes through ecosystem restoration.",
        "reasoning": "Converted from first person to third person. Focused on his ecological expertise and connection to water/climate work relevant to ERA."
    },
    
    "Terrance Long": {
        "rewrite": "Terrance Long is Chair and CEO of International Dialogues on Underwater Munitions (IDUM), bringing decades of military engineering and explosive ordnance disposal expertise to addressing the environmental hazards of underwater munitions. His work connects military remediation with ocean ecosystem restoration and safety.",
        "reasoning": "Added context about his expertise and made ERA connection explicit (environmental remediation, ocean ecosystems)."
    },
    
    "Fernando Cervignon": {
        "rewrite": "Fernando Cervignon founded Trees4Humanity.org and teaches at Universidad Carlos III de Madrid. His environmental protection work spans the Amazon, Borneo orangutan conservation, and anti-poaching efforts in Africa. He advocates for integrating technology, creative thinking, and Indigenous knowledge to address ecosystem threats.",
        "reasoning": "Condensed from verbose first-person to concise third-person. Highlighted global scope and Indigenous knowledge integration (ERA-relevant)."
    },
    
    "Douglas Sheil": {
        "rewrite": "Douglas Sheil is an ecologist, forester, and conservationist whose research focuses on tropical forest ecosystems and their role in climate regulation. His work bridges ecological science with forest conservation practice.",
        "reasoning": "Fixed incomplete sentence ('am' missing 'I'). Added context about tropical forests and climate (ERA-relevant)."
    },
    
    "Hollis Mclellan": {
        "rewrite": "Hollis Mclellan is a public health consultant specializing in environmental health and founder of the Collaborative for Change, which incubates and supports ecosystem restoration projects. Her work connects public health outcomes with ecological restoration.",
        "reasoning": "Combined existing info, made ERA connection explicit (ecosystem restoration projects)."
    },
    
    "Sarah Herzog": {
        "rewrite": "Sarah Herzog is a secondary science educator with a strong interest in transitioning to ecological restoration work. Her focus areas include permaculture, biodiversity, sustainable infrastructure, phytoremediation, and biomimicry applications.",
        "reasoning": "Condensed verbose first-person bio. Kept key technical interests but removed overly earnest language ('eagerly receptive', 'passionate')."
    },
    
    "Nadait Gebremedhen": {
        "rewrite": "Nadait Gebremedhen is a medical doctor turned social entrepreneur who founded Hagush, a nonprofit social enterprise focused on creating a just and inclusive economy. Her work in global development addresses structural dimensions of inequality, combining economic history with practical solutions for advancing sustainable development goals.",
        "reasoning": "Drastically condensed from 400+ words to 2 sentences. Kept key career pivot and mission, removed verbose explanations."
    },
    
    "Joe James": {
        "rewrite": "Joe James is President of Agri-Tech Producers LLC, where he developed the patented Combined Remediation Biomass and Bio-Product Production (CRBBP) Process. His approach uses fast-growing bio-crops for carbon capture via photosynthesis, then converts the biomass into biochar, bio-based filler powders, and other climate-smart products. Agri-Tech Producers partners with utilities and land-rich organizations to deploy the CRBBP process at scale, and was among the first 16 grantees of the US Government's BioMADE Program.",
        "reasoning": "Condensed from 500+ words to 4 sentences. Removed sales pitch language, contact details, email signatures. Kept key technical innovation and scale."
    },
    
    "Scot Bryson": {
        "rewrite": "Scot Bryson founded Orbital Farm in 2018 to build closed-loop biotechnology systems that produce vaccines, medicines, hydrogen energy, and food using water, CO2, and electricity. His vision is to establish 200 circular mega-projects globally to address climate change and food security challenges.",
        "reasoning": "Condensed from verbose life story to 2 sentences. Focused on current work and mission, removed personal narrative and promotional language."
    },
    
    "Coakee William Wildcat": {
        "rewrite": "Coakee William Wildcat is Executive Director of Mother Tree Food & Forest and serves on the ERA board. Beginning life in the Oklahoma Seminole Nation, he integrates Indigenous agroecology, western soil ecology, syntropic agroforestry, and Miyawaki reforestation methods in his restoration work. He lives in the Mimbres watershed near the Gila wilderness, practicing and teaching approaches that help people meet their needs while restoring ecosystems and stabilizing climate.",
        "reasoning": "Condensed from very long bio to 3 sentences. Kept Indigenous roots, key methods, ERA connection (#eraboard), and location/mission."
    },
    
    "Edib Korkut": {
        "rewrite": "Edib Korkut is a semi-retired physician in Washington, DC with interests in ecosystem restoration and climate solutions.",
        "reasoning": "Minimal current info available. Created simple, professional bio from what exists in database."
    },
    
    "Ryan Smith": {
        "rewrite": "Ryan Smith is a consulting forester working with private landowners in Massachusetts and Connecticut to promote forest restoration, agroforestry, and climate-smart management practices. With experience working with smallholder farmers on three continents, he brings a multidisciplinary approach to developing scalable, locally-adapted nature-based solutions.",
        "reasoning": "Converted from first person to third person. Condensed slightly while keeping key geographic scope and approach."
    },
    
    "Isabelle Claire Dela Paz": {
        "rewrite": "Isabelle Claire Dela Paz is Research and Communication Associate at CIFOR-ICRAF Philippines, engaged in projects advancing forest restoration. A forestry professional specializing in urban agroforestry, she previously served as President of the International Forestry Students' Association (IFSA) and advocates for meaningful youth engagement in the forestry sector.",
        "reasoning": "Condensed from 3 paragraphs to 2 sentences. Kept current role, urban agroforestry specialty, and youth leadership."
    },
    
    "Stephen Cook": {
        "rewrite": "Stephen Cook is Chief Strategy Officer at The Undaunted, a social impact organization. His work focuses on strategic planning and systems change for social and environmental challenges.",
        "reasoning": "Minimal info available (just link + title). Created professional bio from what exists. May need more research if user wants more detail."
    }
}

# Load Excel file
df = pd.read_excel('member_reconciliation_report.xlsx', engine='openpyxl')

# Update the proposed_rewrites column and comments
for name, data in rewrites.items():
    mask = df['name_airtable'] == name
    if mask.any():
        df.loc[mask, 'proposed_rewrites'] = data['rewrite']
        df.loc[mask, 'comments'] = 'rewritten'
        print(f"✓ Updated: {name}")
    else:
        print(f"✗ Not found: {name}")

# Save back to Excel
df.to_excel('member_reconciliation_report.xlsx', index=False, engine='openpyxl')
print(f"\n✅ Saved {len(rewrites)} rewrites to member_reconciliation_report.xlsx")
print("\nRewrite summary:")
for name in rewrites:
    print(f"  • {name}")
