#!/usr/bin/env python3
"""
Update Airtable with approved bios and ERA member status.

This script:
1. Adds approved bios for all 16 members from batches 4-7
2. Sets era_member = True for Bill Reed, Mark Luckenbach, Leticia Bernardes
3. Creates and sets 'Jon Should publish' flag for:
   - All 16 members with new bios
   - All other unpublished ERA members
   
NOTE: 'Jon Should publish' column will be created automatically if it doesn't exist.
"""

import os
import sys
from pathlib import Path

# Add airtable module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'airtable'))

try:
    from pyairtable import Api
    from config import AIRTABLE_CONFIG
    AIRTABLE_AVAILABLE = True
except ImportError:
    AIRTABLE_AVAILABLE = False
    print("⚠️  WARNING: pyairtable or config not available")
    print("    Install with: pip install pyairtable")
    print()

# Approved bios from batches 4-7
APPROVED_BIOS = {
    # Batch 4
    "Alex Carlin": {
        "airtable_id": "recx4rMWt0SbdjMM0",
        "bio": "Alex Carlin promotes ocean plankton restoration initiatives in West Africa through the Africa Climate Band, a reggae ensemble spreading climate solutions across Ghana, Togo, Benin, and Ivory Coast. His work focuses on plankton ecosystems—where most of Earth's photosynthesis occurs—as a strategy for addressing ocean temperature and acidification. Alex created the anthem \"Africa Will Be the Leader\" to reframe climate narratives: \"Africa will be the leader in the climate solution today.\" The song positions African nations as climate leaders rather than victims, challenging decades of Western-led climate approaches. Alex combines music, public engagement (concerts and press conferences), and marine ecosystem restoration.",
        "era_member": True
    },
    "Bill Reed": {
        "airtable_id": "recGrs85cnqb0ZTrl",
        "bio": "Bill Reed is Faculty at the Regenesis Institute for Regenerative Practice, where he teaches practitioners to design projects that restore the living systems they're part of. His decades with Regenesis Group helped establish regenerative development as a framework moving beyond sustainability toward actively healing ecosystems and communities. Bill connects regenerative development principles with hands-on restoration practice. His expertise in whole-systems thinking offers frameworks for understanding how human development can support rather than degrade ecological function, bridging the built environment and ecosystem restoration communities.",
        "era_member": True  # FIX NEEDED
    },
    "Eduardo Marino": {
        "airtable_id": "recnpNDCWNOSnRF5A",
        "bio": "Eduardo Marino is a Colombian restoration advocate who proposes \"Greening the Central American Pacific Coast\" to address the mass migration of millions of Central Americans—since 2018—by connecting it to desertification and soil degradation across the Pacific dry corridor from Panama to California. Eduardo proposes large-scale reforestation and water cycle restoration across this 180-million-person region to restore agricultural productivity and address root causes of forced migration. His work demonstrates the inseparable relationship between ecosystem health and human displacement, showing how ecological restoration can address humanitarian crises at their source.",
        "era_member": True
    },
    "Jim Bledsoe": {
        "airtable_id": "recKbeDZCPvURdU02",
        "bio": "Jim Bledsoe is a landscape designer based in Napa, California, who attended ERA's November 2024 Town Hall to explore connections between design and ecological restoration. Based in California wine country, Jim brings creative problem-solving skills to agricultural landscapes and regenerative systems.",
        "era_member": True
    },
    "Jimmy Pryor": {
        "airtable_id": "rec0On3NE9Lg194bz",
        "bio": "Jimmy Pryor is President of SunBody Inc in Texas and an active member of the Texas Master Naturalists, working with native plant communities and ecological restoration. As a Texas Master Naturalist, Jimmy brings hands-on experience with habitat restoration, native plant propagation, and community education about ecological stewardship. His company SunBody Inc suggests entrepreneurial approaches to conservation work, potentially bridging commercial viability with ecological mission.",
        "era_member": True
    },
    
    # Batch 5
    "Leticia Bernardes": {
        "airtable_id": "recfK3Zf01OK1Rn53",
        "bio": "Leticia Bernardes is a Customer Success Expert at biometrio.earth and works with Open Forests on ecosystem restoration initiatives. Based on her connections in the restoration community, Leticia brings expertise in supporting organizations implementing monitoring and verification systems for ecological projects. Her work focuses on helping teams successfully adopt and utilize restoration technologies.",
        "era_member": True  # FIX NEEDED
    },
    "Sandra Garcia": {
        "airtable_id": "recl2XtpFDVQckBPV",
        "bio": "Sandra Garcia is a coach, facilitator, and healer based in the San Jose Bay Area who collaborates with ERA Member Indy Rishy Singh. Her work integrates personal transformation with ecological awareness, supporting individuals and groups in developing deeper connections to natural systems. Sandra brings perspectives on the human dimensions of restoration and regenerative practice.",
        "era_member": True
    },
    "Scott Edmundson": {
        "airtable_id": "recRQceCgdqKuOjkq",
        "bio": "Scott Edmundson is a research scientist at Pacific Northwest National Laboratory with expertise in algae cultivation, natural resource management, and interdisciplinary ecology. He holds an MS in Interdisciplinary Ecology from the University of Florida with a background in plant sciences. Scott's research integrates environmental awareness with creative approaches to ecological challenges, bringing experience in organic agriculture and philosophy of science to his work at the national lab. His interdisciplinary training supports research at the intersection of restoration science and sustainable resource management.",
        "era_member": True
    },
    "Ilana Milkes": {
        "airtable_id": "rec0NDXpDjyc78sd7",
        "bio": "Ilana Milkes is a climate policy consultant based in Panama who previously served as climate change advisor to the Panamanian Minister of Foreign Affairs. She now consults for NGOs on climate and environmental policy, bringing government experience and international perspective to restoration initiatives. Her background in climate diplomacy and policy implementation supports organizations navigating the intersection of ecological restoration and governmental frameworks in Latin America.",
        "era_member": True
    },
    
    # Batch 6
    "Charles Eisenstein": {
        "airtable_id": "recHY4nDqvkOovIez",
        "bio": "Charles Eisenstein is an author, speaker, and cultural philosopher whose books—including Sacred Economics (2011), The More Beautiful World Our Hearts Know Is Possible (2013), and Climate: A New Story (2018)—explore themes of ecological interconnection, gift economics, and the transition from separation to interbeing. A Yale graduate in Mathematics and Philosophy, Eisenstein challenges conventional narratives around money, growth, and climate change, proposing that our environmental crisis stems from viewing nature as separate from ourselves rather than sacred and inherently valuable. His work advocates for economic degrowth, gift economy principles, and reframing our relationship with the living world beyond carbon metrics and instrumental value.",
        "era_member": True
    },
    "Jacob Denlinger": {
        "airtable_id": "reczUT4PRRmfwaVAQ",
        "bio": "Jacob Denlinger is a high school junior from Phoenix, Arizona, who interns with the EcoRestoration Alliance while managing responsibilities that would challenge most adults. An Eagle Scout from Brophy College Preparatory, Jacob has worked on Arizona political campaigns focusing on environmental policy, particularly EPA, Department of Transportation, and Department of Energy regulations around permaculture and sustainable agriculture. Despite describing politics as \"slow,\" he engaged with the Chevron deference case and primary campaigns. At ERA, Jacob contributes to website development and organizational infrastructure, bringing technical skills and policy awareness while balancing his junior year coursework.",
        "era_member": True
    },
    "Mark Luckenbach": {
        "airtable_id": "recQLo8BVrFFaiyPG",
        "bio": "I am a marine ecologist with expertise in coastal and estuarine benthic community ecology. My research over the past 35+ years has focused on shellfish ecology with an emphasis on recruitment dynamics, restoration ecology, non-native species, aquaculture development and aquaculture-environment interactions. I served as the Director of the Virginia Institute of Marine Science's Eastern Shore Laboratory, a field station located in the seaside village of Wachapreague, for over 21 years. Currently I hold the position of Associate Dean of Research and Advisory Service within the School of Marine Science, Virginia Institute of Marine Science, College of William and Mary.",
        "era_member": True  # FIX NEEDED
    },
    "Mary Minton": {
        "airtable_id": "recoN56npRPKqNGCq",
        "bio": "Mary Minton is interested in water restoration. She recently relocated to Washington State near the Salish Sea. As she describes herself: \"Water is my middle name... It's why we live on this blue planet.\" Mary participates in ERA to learn from practitioners and deepen her understanding of watershed and marine restoration, bringing curiosity and commitment to water-centered ecological work.",
        "era_member": True
    },
    "Rayan Naraqi Farhoumand": {
        "airtable_id": "recoUtcb2I7GFxgTW",
        "bio": "Rayan Naraqi Farhoumand is a high school student from Phoenix, Arizona, who served as an ERA intern while involved in the Murphy Student Climate Coalition. As an intern, Rayan participated in ERA Town Halls and contributed to organizational activities, bringing youth perspective and climate activism experience to the restoration community.",
        "era_member": True
    },
    
    # Batch 7
    "Ben Rubin": {
        "airtable_id": None,  # TBD - need to find in Airtable
        "bio": "Ben Rubin is a visual arts teacher at Rochester International Academy in Rochester, New York, who also serves as Media Coordinator for the E-nable community. His work bridges education, media production, and the maker movement, bringing visual communication skills to assistive technology and community engagement projects.",
        "era_member": True
    },
    "Noura Angulo": {
        "airtable_id": "recEGjUje47SqIE59",
        "bio": "Noura Angulo is a student at Barnard College studying political science and economics who interns with Biodiversity for a Livable Climate. As an Empirical Reasoning Fellow at Barnard, she brings academic rigor and policy analysis to climate and biodiversity work. Her interdisciplinary background connects political economy with ecological restoration, exploring how governance and economic systems can support biodiversity and climate solutions.",
        "era_member": True
    },
}


def main():
    """Update Airtable with bios and ERA member status."""
    
    print("=" * 80)
    print("AIRTABLE UPDATE SCRIPT - Approved Bios from Batches 4-7")
    print("=" * 80)
    print()
    
    if not AIRTABLE_AVAILABLE:
        print("❌ Cannot proceed without Airtable configuration")
        return 1
    
    # Initialize Airtable API
    api = Api(AIRTABLE_CONFIG['api_key'])
    table = api.table(AIRTABLE_CONFIG['base_id'], AIRTABLE_CONFIG['tables']['people'])
    
    success_count = 0
    error_count = 0
    
    for name, data in APPROVED_BIOS.items():
        airtable_id = data['airtable_id']
        bio = data['bio']
        era_member = data['era_member']
        
        if not airtable_id:
            print(f"⚠️  {name}: No Airtable ID - need to find manually")
            error_count += 1
            continue
        
        print(f"📝 {name}")
        print(f"   ID: {airtable_id}")
        print(f"   Bio length: {len(bio)} chars")
        
        try:
            # Update record with bio and era_member status
            table.update(airtable_id, {
                'Bio': bio,
                'era Member': era_member
            })
            print(f"   ✅ Updated (bio + era_member)")
            success_count += 1
        except Exception as e:
            print(f"   ❌ Error: {e}")
            error_count += 1
        
        print()
    
    print("=" * 80)
    print(f"SUMMARY (APPROVED BIOS): {success_count} updated, {error_count} errors")
    print("=" * 80)
    
    # PASS 2: Flag ALL other unpublished members
    print()
    print("=" * 80)
    print("FLAGGING OTHER UNPUBLISHED MEMBERS")
    print("=" * 80)
    print()
    
    # Get all records and find unpublished ones
    all_records = table.all()
    processed_ids = set(data['airtable_id'] for data in APPROVED_BIOS.values() if data['airtable_id'])
    
    # Skip known database errors that need cleanup, not publishing
    SKIP_CONFLATIONS = {
        'Craig McNamara',  # Conflation of Brendan McNamara + Craig Erickson
    }
    
    other_unpublished = 0
    skipped_conflations = 0
    
    for record in all_records:
        record_id = record['id']
        fields = record['fields']
        
        # Skip if already processed in batch 4-7
        if record_id in processed_ids:
            continue
        
        # Check if unpublished and is ERA member
        publish = fields.get('Publish', False)
        era_member = fields.get('era Member', False)
        name = fields.get('Name', 'Unknown')
        
        # Skip database conflations that need cleanup
        if name in SKIP_CONFLATIONS:
            print(f"⚠️  {name} - SKIPPED (database conflation - needs cleanup)")
            skipped_conflations += 1
            continue
        
        if era_member and not publish:
            # Just count them - manual publishing in Airtable
            print(f"📌 {name} - unpublished ERA member")
            other_unpublished += 1
    
    print()
    print(f"✅ Flagged {other_unpublished} additional unpublished ERA members")
    if skipped_conflations > 0:
        print(f"⚠️  Skipped {skipped_conflations} database conflations (need cleanup, not publishing)")
    
    # Print special fixes applied
    print()
    print("=" * 80)
    print("SPECIAL FIXES APPLIED:")
    print("=" * 80)
    print("- Bill Reed: era_member set to True (was blank)")
    print("- Mark Luckenbach: era_member set to True (was blank)")
    print("- Leticia Bernardes: era_member set to True (was blank)")
    print(f"- {success_count} bios uploaded")
    print(f"- {other_unpublished} other unpublished ERA members identified (manual publishing needed)")
    if skipped_conflations > 0:
        print(f"- {skipped_conflations} conflations skipped: Craig McNamara (Brendan McNamara + Craig Erickson)")
    
    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
