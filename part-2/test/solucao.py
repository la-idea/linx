import pandas as pd
import ast
import tarfile
import json
import time

ini = time.time()
# Extraindo o arquivo '.tar' para trabalhar o json como dataframe
tar = tarfile.open("/home/gabriel/Área de Trabalho/Desafio Linx/part2/src/input-dump")
files = tar.getmembers()
dump_file = tar.extractfile(files[0])
df_dump = pd.read_json(dump_file, lines=True, )

# Eliminar os duplicados
df_dump.drop_duplicates(subset="image", keep='first',inplace=True)
df_dump['image'].describe()


# Reorganizando em um novo Json com lista de no máximo 3 urls

## Reordenar

dump = df_dump.sort_values(by='productId')
dump = dump.reset_index(drop=True)


## Agregar em lista de 3
new_dump = pd.DataFrame(columns=['productId','image'])
new_dump.loc[0,'productId']= dump.iloc[0,0]
new_dump.loc[0,'image']= list()


aux =1
for i in dump.index:
        
    if dump.iloc[i,0] == new_dump.iloc[-1, 0] and (len(new_dump.iloc[-1,1]) < 3):
        new_dump.iloc[-1,1].append(dump.iloc[i,1])
        
             
    else:
        new_dump.loc[aux,'productId'] = dump.iloc[i,0]
        new_dump.loc[aux,'image'] = []
        new_dump.loc[aux,'image'].append(dump.iloc[i,1])
        aux = aux +1
        

# Salvar o resultado

new_dump.to_json('new_dumpgzip', orient='records', compression = 'gzip', lines=True)
fim = time.time()
print("O tempo foi de {}".format(fim-ini))

