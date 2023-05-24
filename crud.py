import pickle

class KeyValueStore:
    def __init__(self, filename, verbose=True):
        self.verbose = verbose
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def _save_data(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)

    def _push_data(self, data:dict):
        with open(self.filename, 'wb') as file:
            for key, value in data.items():
                self.create(key, value)
            self._save_data()

    def create(self, key, value):
        """Adiciona `key` : `value` ao BD se `key` nao existe."""
        if key in self.data:
            print(f"Key {key} Já existe!") if self.verbose else 0
            return
        self.data[key] = value
        self._save_data()

    def read(self, key):
        """Retorna um dict com todos os pares `{key: value}`"""
        return self.data.get(key)

    def update(self, key, value):
        """Atualiza `key` com `value` no BD se `key` existe."""
        if key not in self.data:
            print(f"Chave {key} não exite.") if self.verbose else 0
            return 
        self.data[key] = value
        self._save_data()

    def delete(self, key):
        """Deleta o par `{key: value}` se `key` existe."""
        if key not in self.data:
            print(f"Chave {key} não existe.") if self.verbose else 0
            return
        del self.data[key]
        self._save_data()

    def get_all_keys(self):
        """Retorna uma lista com todas as chaves do BD."""

        return list(self.data.keys())

    def get_all_values(self):
        """Retorna uma lista com todos os valores do DB."""
        return list(self.data.values())
