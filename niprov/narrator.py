

class Narrator(object):
    """Generates human-readable text that describes provenance objects.
    """

    def narrate(self, img):
        provenance = img.provenance
        story = ''
        if 'protocol' in provenance:
            story += 'This is a {0} image. '.format(provenance['protocol'])
        if 'acquired' in provenance:
            datestr = provenance['acquired'].strftime('%B %d, %Y').replace(' 0',' ')
            story += 'It was recorded {0}. '.format(datestr)
        if 'subject' in provenance:
            story += "The participant's name is {0}. ".format(
                provenance['subject'])
        if 'size' in provenance:
            sizeInBytes = provenance['size']
            if sizeInBytes > (1000 * 1000):
                unit = 'MB'
                factor = 1000 * 1000
            else:
                unit = 'KB'
                factor = 1000
            size = int(provenance['size']/factor)
            story += "It is {0}{1} in size. ".format(size, unit)
        return story
