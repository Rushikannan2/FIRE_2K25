"""
Classification formatter for hierarchical sentiment analysis results.
Formats Level 1, Level 2, and Level 3 predictions into human-readable paths.
"""

def format_classification_path(level1, level2=None, level3=None):
    """
    Format hierarchical classification results into a full class path and description.
    
    Args:
        level1: Level 1 prediction (NOISE, OBJECTIVE, or SUBJECTIVE)
        level2: Level 2 prediction (NEUTRAL, NEGATIVE, or POSITIVE) - only if Level 1 = SUBJECTIVE
        level3: Level 3 prediction (NEUTRAL_SENTIMENTS, QUESTIONS, ADVERTISEMENTS, or MISCELLANEOUS) - only if Level 2 = NEUTRAL
    
    Returns:
        dict with 'path' and 'description' keys
    """
    
    # Level 1 mappings
    level1_map = {
        'NOISE': {
            'path': 'NOISE',
            'description': 'Unusable or irrelevant data',
            'stop': True
        },
        'OBJECTIVE': {
            'path': 'OBJECTIVE',
            'description': 'Factual, neutral statement',
            'stop': True
        },
        'SUBJECTIVE': {
            'path': 'SUBJECTIVE',
            'description': 'Opinionated or personal post',
            'stop': False
        }
    }
    
    # Level 2 mappings (only if Level 1 = SUBJECTIVE)
    level2_map = {
        'NEUTRAL': {
            'path': 'NEUTRAL',
            'description': 'Subjective but emotionally neutral',
            'stop': False
        },
        'NEGATIVE': {
            'path': 'NEGATIVE',
            'description': 'Subjective and emotionally negative',
            'stop': True
        },
        'POSITIVE': {
            'path': 'POSITIVE',
            'description': 'Subjective and emotionally positive',
            'stop': True
        }
    }
    
    # Level 3 mappings (only if Level 2 = NEUTRAL)
    level3_map = {
        'NEUTRAL_SENTIMENTS': {
            'path': 'NEUTRAL SENTIMENTS',
            'description': 'Subjective but neutral tone (e.g., "It\'s fine.")'
        },
        'QUESTION': {
            'path': 'QUESTIONS',
            'description': 'Subjective query or request for info'
        },
        'QUESTIONS': {
            'path': 'QUESTIONS',
            'description': 'Subjective query or request for info'
        },
        'ADVERTISEMENT': {
            'path': 'ADVERTISEMENTS',
            'description': 'Subjective promotional/ad-like content'
        },
        'ADVERTISEMENTS': {
            'path': 'ADVERTISEMENTS',
            'description': 'Subjective promotional/ad-like content'
        },
        'MISCELLANEOUS': {
            'path': 'MISCELLANEOUS',
            'description': 'Subjective neutral but unclassified post'
        }
    }
    
    # Normalize inputs
    level1 = str(level1).upper() if level1 else None
    level2 = str(level2).upper() if level2 else None
    level3 = str(level3).upper() if level3 else None
    
    # Start building the path
    if not level1 or level1 not in level1_map:
        return {
            'path': 'UNKNOWN',
            'description': 'Invalid or missing Level 1 classification',
            'full_path': 'UNKNOWN',
            'input_summary': f'Level 1 = {level1}, Level 2 = {level2}, Level 3 = {level3}'
        }
    
    l1_info = level1_map[level1]
    path_parts = [l1_info['path']]
    description = l1_info['description']
    
    # If Level 1 stops here, return
    if l1_info['stop']:
        return {
            'path': l1_info['path'],
            'description': l1_info['description'],
            'full_path': ' → '.join(path_parts),
            'input_summary': f'Level 1 = {level1}, Level 2 = None, Level 3 = None'
        }
    
    # Level 1 is SUBJECTIVE, check Level 2
    if not level2 or level2 not in level2_map:
        return {
            'path': 'SUBJECTIVE',
            'description': 'Subjective post (Level 2 classification missing)',
            'full_path': ' → '.join(path_parts),
            'input_summary': f'Level 1 = {level1}, Level 2 = None, Level 3 = None'
        }
    
    l2_info = level2_map[level2]
    path_parts.append(l2_info['path'])
    description = l2_info['description']
    
    # If Level 2 stops here, return
    if l2_info['stop']:
        return {
            'path': l2_info['path'],
            'description': l2_info['description'],
            'full_path': ' → '.join(path_parts),
            'input_summary': f'Level 1 = {level1}, Level 2 = {level2}, Level 3 = None'
        }
    
    # Level 2 is NEUTRAL, check Level 3
    if not level3 or level3 not in level3_map:
        return {
            'path': 'NEUTRAL',
            'description': 'Subjective but emotionally neutral (Level 3 classification missing)',
            'full_path': ' → '.join(path_parts),
            'input_summary': f'Level 1 = {level1}, Level 2 = {level2}, Level 3 = None'
        }
    
    l3_info = level3_map[level3]
    path_parts.append(l3_info['path'])
    description = l3_info['description']
    
    return {
        'path': l3_info['path'],
        'description': l3_info['description'],
        'full_path': ' → '.join(path_parts),
        'input_summary': f'Level 1 = {level1}, Level 2 = {level2}, Level 3 = {level3}'
    }


def format_classification_for_display(level1, level2=None, level3=None):
    """
    Format classification results in the requested format with emoji and structure.
    
    Returns formatted string ready for display.
    """
    result = format_classification_path(level1, level2, level3)
    
    formatted = f"""🧾 Input:
Level 1 = {level1 or 'None'}
Level 2 = {level2 or 'None'}
Level 3 = {level3 or 'None'}

✅ Result:
Full Class Path → {result['full_path']}
Description → {result['description']}"""
    
    return formatted

