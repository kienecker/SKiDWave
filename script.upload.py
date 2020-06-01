from dwave.system.samplers import DWaveSampler
from dwave.embedding import embed_ising, unembed_sampleset
from minorminer import find_embedding
from dimod import as_bqm

edp = 'https://cloud.dwavesys.com/sapi'
tkn = 'ABC-ihrtoken'
slv = 'DW_2000Q_5'
# Verfügbare Solver lassen sich per "Client(edp, tkn).get_solvers()" abfragen.
# Vorher ist ein "from dwave.cloud import Client" nötig.


# Verbindung aufbauen
sampler = DWaveSampler(endpoint = edp, token = tkn, solver = slv)


# Problembeschreibung
h = [0, 0, 0, 0]
J = {
    (0,1): 1,
    (1,3): 1,
    (3,2): 1,
    (2,0): 1
}


# Embedding finden
emb = find_embedding(J.keys(), sampler.edgelist) # Alternativ lässt sich das
    # Embedding (bei diesem Mini-Problem) auch von Hand definieren:
    # "emb = {0: [0], 1: [4], 2: [7], 3: [3]}"

print("EMBEDDING:")
print(emb)


# Problem einbetten
adj = sampler.adjacency # sampler.adjacency enthält die gleichen Informationen
    # wie sampler.edgelist, lediglich anders strukturiert, vgl.
    # https://docs.ocean.dwavesys.com/projects/system/en/latest/reference/
    # samplers.html#properties und
    # https://github.com/dwavesystems/dimod/blob/master/dimod/core/
    # structured.py#L103
th, tJ = embed_ising(h, J, emb, adj)


# Problem lösen
raw = sampler.sample_ising(th, tJ, num_reads = 100)

print("\nRAW RESULTS:")
print(raw)


# Einbettung rückgängig machen
res = unembed_sampleset(raw, emb, as_bqm(h, J, raw.vartype))

print("\nRESULTS:")
print(res)
