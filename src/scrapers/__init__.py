from .adressa import Adressa
from .bt import Bt
from .aftenposten import Aftenposten
from .aftenbladet import Aftenbladet
from .dagbladet import Dagbladet
from .morgenbladet import Morgenbladet

scrapers = {
	'aftenposten': Aftenposten,
	'bt': Bt,
	'aftenbladet': Aftenbladet,
	'dagbladet': Dagbladet,
	'morgenbladet': Morgenbladet,
	'adressa': Adressa,
}

scrapers['all'] = lambda: 'all'