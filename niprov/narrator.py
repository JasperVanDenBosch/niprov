

class Narrator(object):
    """Generates human-readable text that describes provenance objects.
    """

    def narrate(self, img):
        provenance = img.provenance
        story = ''
        if 'protocol' in provenance:
            story += 'This is a {0} image.'.format(provenance['protocol'])
        return story
