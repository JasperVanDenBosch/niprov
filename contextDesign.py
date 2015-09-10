# current
import niprov
options = niprov.options()
niprov.log(options)
options.x = y
niprov.log(options)

# context
import niprov
provenance = niprov.context()
provenance.log()
provenance.options.x = y
provenance.log()

## to support both;

context.reconfigure(options) # in existing functions?


