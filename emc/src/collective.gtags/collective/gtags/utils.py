
CATEGORY_DELIMITER = u"-"

def get_categories(tags):
    """Return a set of all unique categories contained in the given list of tags
    """
    categories = set()
    for tag in tags:
        category, value = split(tag)
        if category:
            categories.add(category)
    return categories
        
def split(tag):
    """Split a tag into (category, tag) parts. category may be None.
    """
    parts = tag.split(CATEGORY_DELIMITER)
    
    if len(parts) == 1:
        return None, tag
    else:
        return parts[0], CATEGORY_DELIMITER.join(parts[1:])