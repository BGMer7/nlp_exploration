from service.client import BertClient

bc = BertClient('ip = localhost')
vec = bc.encode(['hello world', 'good day'])
