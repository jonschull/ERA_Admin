#!/usr/bin/env python3
"""
AI Recommendation System for Phase 4B-2

Uses heuristics to make intelligent recommendations for participant reconciliation.
High confidence → auto-recommend
Medium confidence → flag for batch AI analysis
Low confidence → recommend skip or manual review

Signals considered:
- Town Hall agenda context (local DB)
- Gmail presence
- Airtable fuzzy matching
- Name quality/completeness
- Learned mappings from previous rounds
"""

from fuzzywuzzy import fuzz

def calculate_confidence_score(
    name,
    town_hall_results,
    gmail_result,
    airtable_match,
    category,
    has_learned_mapping
):
    """
    Calculate confidence score 0-100 for making a recommendation.
    
    Returns: (score, signals_dict)
    """
    
    signals = {
        'town_hall_count': len(town_hall_results),
        'in_gmail': gmail_result['found'],
        'gmail_count': gmail_result['count'] if gmail_result['found'] else 0,
        'in_airtable': airtable_match[0],
        'airtable_score': airtable_match[2] if airtable_match[0] else 0,
        'has_learned': has_learned_mapping,
        'category': category,
        'name_quality': assess_name_quality(name, category)
    }
    
    score = 0
    
    # Learned mapping = highest confidence (already decided in previous round)
    if signals['has_learned']:
        score += 40
    
    # Town Hall context (strong signal - they participated in meetings)
    if signals['town_hall_count'] >= 3:
        score += 35  # Very strong
    elif signals['town_hall_count'] >= 2:
        score += 25  # Strong
    elif signals['town_hall_count'] >= 1:
        score += 15  # Moderate
    
    # Airtable match
    if signals['in_airtable']:
        if signals['airtable_score'] >= 90:
            score += 30  # Very high match
        elif signals['airtable_score'] >= 75:
            score += 20  # High match
        else:
            score += 10  # Moderate match
    
    # Gmail presence
    if signals['in_gmail']:
        if signals['gmail_count'] >= 5:
            score += 15
        elif signals['gmail_count'] >= 2:
            score += 10
        else:
            score += 5
    
    # Name quality
    if signals['name_quality'] == 'good':
        score += 5
    elif signals['name_quality'] == 'incomplete':
        score -= 10
    elif signals['name_quality'] == 'device_or_org':
        score -= 30
    
    return min(score, 100), signals


def assess_name_quality(name, category):
    """Assess if name is complete, partial, device, organization, etc."""
    
    # Device/phone indicators
    if category in ['phone', 'device']:
        return 'device_or_org'
    
    # Organization indicators
    if category == 'organization':
        return 'device_or_org'
    
    # Check for special chars that indicate org/device
    if any(char in name for char in ['www', '.com', '+1', '(', ')'] + list('0123456789')):
        return 'device_or_org'
    
    # Single name only
    if category == 'single_name':
        return 'incomplete'
    
    # Check word count
    words = [w for w in name.split() if len(w) > 1]
    if len(words) >= 2:
        return 'good'
    else:
        return 'incomplete'


def make_ai_recommendation(
    name,
    town_hall_results,
    gmail_result,
    airtable_match,
    category,
    has_learned_mapping,
    learned_decision=''
):
    """
    Make intelligent recommendation based on all available signals.
    
    Returns: (recommendation, confidence, reasoning)
    
    Confidence levels:
    - high (80-100): Auto-recommend, user just approves
    - medium (50-79): Flag for AI batch analysis
    - low (0-49): Recommend skip or needs manual review
    """
    
    in_airtable, matched_name, at_score, at_method = airtable_match
    
    # Get confidence score
    confidence_score, signals = calculate_confidence_score(
        name, town_hall_results, gmail_result, airtable_match, 
        category, has_learned_mapping
    )
    
    reasoning_parts = []
    
    # LEARNED MAPPINGS (highest priority)
    if has_learned_mapping and learned_decision:
        return learned_decision, 'high', '🔁 Resolved in previous round'
    
    # HIGH CONFIDENCE CASES
    
    # Case 1: Strong Town Hall + Airtable match
    if signals['town_hall_count'] >= 2 and in_airtable and at_score >= 85:
        reasoning_parts.append(f"In {signals['town_hall_count']} Town Hall meetings")
        reasoning_parts.append(f"Strong Airtable match ({at_score}%)")
        return f'merge with: {matched_name}', 'high', ' | '.join(reasoning_parts)
    
    # Case 2: Very strong Town Hall presence (participated multiple times)
    if signals['town_hall_count'] >= 3 and signals['name_quality'] == 'good':
        reasoning_parts.append(f"Participated in {signals['town_hall_count']} Town Hall meetings")
        if in_airtable:
            reasoning_parts.append(f"Match in Airtable: {matched_name}")
            return f'merge with: {matched_name}', 'high', ' | '.join(reasoning_parts)
        else:
            reasoning_parts.append("Not yet in Airtable")
            return 'add to airtable', 'high', ' | '.join(reasoning_parts)
    
    # Case 3: Perfect Airtable match
    if in_airtable and at_score >= 95:
        reasoning_parts.append(f"Perfect name match ({at_score}%)")
        if signals['town_hall_count'] > 0:
            reasoning_parts.append(f"Also in {signals['town_hall_count']} Town Hall")
        return f'merge with: {matched_name}', 'high', ' | '.join(reasoning_parts)
    
    # Case 4: Clear organization/device
    if category in ['organization', 'phone', 'device']:
        reasoning_parts.append(f"Identified as {category}")
        return 'drop', 'high', ' | '.join(reasoning_parts)
    
    # MEDIUM CONFIDENCE CASES (need AI batch analysis)
    
    # Case 5: Some Town Hall context but ambiguous
    if signals['town_hall_count'] >= 1:
        reasoning_parts.append(f"Found in {signals['town_hall_count']} Town Hall")
        if in_airtable and at_score >= 70:
            reasoning_parts.append(f"Possible match: {matched_name} ({at_score}%)")
            return f'AI_ANALYZE: likely merge with {matched_name}', 'medium', ' | '.join(reasoning_parts)
        elif signals['in_gmail']:
            reasoning_parts.append(f"Also in {signals['gmail_count']} emails")
            return 'AI_ANALYZE: likely add to airtable', 'medium', ' | '.join(reasoning_parts)
        else:
            reasoning_parts.append("Limited additional context")
            return 'AI_ANALYZE: unclear', 'medium', ' | '.join(reasoning_parts)
    
    # Case 6: Good Airtable match but not perfect
    if in_airtable and 75 <= at_score < 95:
        reasoning_parts.append(f"Good Airtable match ({at_score}%): {matched_name}")
        if signals['in_gmail']:
            reasoning_parts.append("Also in Gmail")
        return f'AI_ANALYZE: likely merge with {matched_name}', 'medium', ' | '.join(reasoning_parts)
    
    # Case 7: Found in Gmail but unclear
    if signals['in_gmail'] and signals['gmail_count'] >= 3:
        reasoning_parts.append(f"In {signals['gmail_count']} emails")
        if signals['name_quality'] == 'good':
            reasoning_parts.append("Good name quality")
            return 'AI_ANALYZE: likely add to airtable', 'medium', ' | '.join(reasoning_parts)
        else:
            reasoning_parts.append("Name incomplete or unclear")
            return 'AI_ANALYZE: needs research', 'medium', ' | '.join(reasoning_parts)
    
    # LOW CONFIDENCE CASES (auto-skip or needs manual review)
    
    # Case 8: No context anywhere
    if signals['town_hall_count'] == 0 and not signals['in_gmail'] and not in_airtable:
        reasoning_parts.append("No Town Hall, Gmail, or Airtable matches")
        return 'drop', 'low', ' | '.join(reasoning_parts)
    
    # Case 9: Single name only with minimal context
    if category == 'single_name' and signals['town_hall_count'] == 0:
        reasoning_parts.append("Incomplete name, no Town Hall context")
        return 'drop', 'low', ' | '.join(reasoning_parts)
    
    # Default: unclear case
    reasoning_parts.append("Insufficient context for auto-recommendation")
    return 'MANUAL_REVIEW', 'low', ' | '.join(reasoning_parts)


def format_recommendation_for_html(recommendation, confidence, reasoning):
    """Format recommendation for display in HTML table."""
    
    # Color coding
    if confidence == 'high':
        color = '#d4edda'  # Green
        icon = '✅'
        label = 'HIGH CONFIDENCE'
    elif confidence == 'medium':
        color = '#fff3cd'  # Yellow
        icon = '🤔'
        label = 'NEEDS AI REVIEW'
    else:  # low
        color = '#f8d7da'  # Red
        icon = '⚠️'
        label = 'LOW CONFIDENCE'
    
    # Extract action
    if recommendation.startswith('AI_ANALYZE:'):
        action = recommendation.replace('AI_ANALYZE:', '').strip()
        show_action = f"{icon} {action}"
    elif recommendation == 'MANUAL_REVIEW':
        show_action = f"{icon} Manual review needed"
    else:
        show_action = f"{icon} {recommendation}"
    
    return {
        'action': show_action,
        'confidence': label,
        'reasoning': reasoning,
        'bg_color': color,
        'raw_recommendation': recommendation
    }
