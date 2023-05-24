from crud import KeyValueStore as kvs

bd = kvs('database.pkl')

# teste = {'1': 2, 3: '4', '5': '6', 7: 8}
# bd._push_data(teste)

bd.create(1, 2)   # C
print(bd.read(7)) # R
bd.update(1, '2') # U
bd.delete(1)      # D
bd.create(1, 2)

bd.verbose = False
for i in range(10):
    bd.create(1, 2) # Key '1' Já existe!

print(bd.data)

#
# (KVS) command   -----> server  <-------> CRUD 
# > output        <-------/
#