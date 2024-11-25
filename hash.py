class Jogo:
    def __init__(self, jogo_id, titulo, desenvolvedor, preco, generos):
        self.jogo_id = jogo_id
        self.titulo = titulo
        self.desenvolvedor = desenvolvedor
        self.preco = preco
        self.generos = generos


class NoJogo:
    def __init__(self, jogo):
        self.jogos = [jogo]  
        self.esquerda = None
        self.direita = None


class ArvoreJogos:
    def __init__(self):
        self.raiz = None

    def inserir(self, jogo):
        novo_no = NoJogo(jogo)
        if self.raiz is None:
            self.raiz = novo_no
        else:
            self._inserir_recursivo(self.raiz, novo_no)

    def _inserir_recursivo(self, atual, novo_no):
        if novo_no.jogos[0].preco < atual.jogos[0].preco:
            if atual.esquerda is None:
                atual.esquerda = novo_no
            else:
                self._inserir_recursivo(atual.esquerda, novo_no)
        elif novo_no.jogos[0].preco > atual.jogos[0].preco:
            if atual.direita is None:
                atual.direita = novo_no
            else:
                self._inserir_recursivo(atual.direita, novo_no)
        else:
            atual.jogos.append(novo_no.jogos[0])


    def buscar_por_preco(self, preco):
        return self._buscar_recursivo(self.raiz, preco)

    def _buscar_recursivo(self, atual, preco):
        if atual is None:
            return []
        if atual.jogos[0].preco == preco:
            return atual.jogos  
        elif preco < atual.jogos[0].preco:
            return self._buscar_recursivo(atual.esquerda, preco)
        else:
            return self._buscar_recursivo(atual.direita, preco)


    def busca_por_faixa_preco(self, preco_minimo, preco_maximo):
        resultados = []
        self._buscar_faixa_recursivo(self.raiz, preco_minimo, preco_maximo, resultados)
        return resultados

    def _buscar_faixa_recursivo(self, atual, minimo, maximo, resultados):
        if atual is not None:
            if minimo <= atual.jogos[0].preco <= maximo:
                resultados.extend(atual.jogos)
            if minimo < atual.jogos[0].preco:
                self._buscar_faixa_recursivo(atual.esquerda, minimo, maximo, resultados)
            if atual.jogos[0].preco < maximo:
                self._buscar_faixa_recursivo(atual.direita, minimo, maximo, resultados)

    def listar_em_ordem(self):
        jogos = []
        self._traversar_em_ordem(self.raiz, jogos)
        return jogos


    def _traversar_em_ordem(self, atual, jogos):
        if atual is not None:
            self._traversar_em_ordem(atual.esquerda, jogos)
            jogos.extend(atual.jogos)
            self._traversar_em_ordem(atual.direita, jogos)


class HashGeneros:
    def __init__(self):
        self.genero_para_jogos = {}

    def adicionar_jogo(self, jogo):
        for genero in jogo.generos:
            if genero not in self.genero_para_jogos:
                self.genero_para_jogos[genero] = []
            self.genero_para_jogos[genero].append(jogo.jogo_id)

    def obter_jogos(self, genero):
        return self.genero_para_jogos.get(genero, [])


class MotorBuscaJogos:
    def __init__(self):
        self.jogos = {}  
        self.catalogo_jogos = ArvoreJogos()  
        self.generos = HashGeneros() 

    def adicionar_jogo(self, jogo):
        if jogo.jogo_id in self.jogos:
            raise ValueError(f"\nJogo com ID {jogo.jogo_id} já existe.")
        if jogo.preco <= 0:
            raise ValueError("\nO preço do jogo deve ser um número positivo.")
        if not jogo.generos:
            raise ValueError("\nO jogo deve ter pelo menos um gênero.")

        self.jogos[jogo.jogo_id] = jogo
        self.catalogo_jogos.inserir(jogo)
        self.generos.adicionar_jogo(jogo)

    def buscar_por_preco(self, preco):
        return self.catalogo_jogos.buscar_por_preco(preco)

    def busca_por_faixa_preco(self, preco_minimo, preco_maximo):
        return self.catalogo_jogos.busca_por_faixa_preco(preco_minimo, preco_maximo)

    def buscar_por_genero(self, genero):
        ids_jogos = self.generos.obter_jogos(genero)
        return [self.jogos[jogo_id] for jogo_id in ids_jogos if jogo_id in self.jogos]


def menu():
    motor = MotorBuscaJogos()
    while True:
        
        try:
            print("\n1. Adicionar Jogo")
            print("2. Buscar por Preço")
            print("3. Buscar por Gênero")
            print("4. Listar Jogos por Preço")
            print("5. Buscar por Faixa de Preço")
            print("6. Sair")
            print("7. Exemplo de demonstração")
            opcao = input("Escolha uma opção: ")
            if opcao == "1":
                titulo = input("\nTítulo: ")
                desenvolvedor = input("Desenvolvedor: ")
                preco = int(input("Preço: "))
                generos = [g.strip() for g in input("Gêneros (separe por vírgula): ").split(",")]
                jogo_id = len(motor.jogos) + 1
                motor.adicionar_jogo(Jogo(jogo_id, titulo, desenvolvedor, preco, generos))
                print("\nJogo adicionado com sucesso!")
                
            elif opcao == "2":
                preco = int(input("Digite o preço: "))
                jogos = motor.catalogo_jogos.buscar_por_preco(preco)
                if jogos:
                    print(f"\nJogos encontrados com preço R${preco}:")
                    for jogo in jogos:
                        print(f"ID: {jogo.jogo_id} | Título: {jogo.titulo} | Desenvolvedor: {jogo.desenvolvedor} | Gêneros: {', '.join(jogo.generos)}")
                else:
                    print(f"\nNenhum jogo encontrado com o preço R${preco}.")

            elif opcao == "3":
                genero = input("\nDigite o gênero: ")
                jogos = motor.buscar_por_genero(genero)
                if jogos:
                    print(f"\nJogos encontrados no gênero '{genero}':")
                    for jogo in jogos:
                        print(f"ID: {jogo.jogo_id} | Título: {jogo.titulo} | Preço: R${jogo.preco}")
                else:
                    print(f"\nNenhum jogo encontrado no gênero '{genero}'.")

            elif opcao == "4":
                jogos = motor.catalogo_jogos.listar_em_ordem()
                if jogos:
                    print("\nJogos cadastrados ordenados por preço:")
                    for jogo in jogos:
                        print(f"ID: {jogo.jogo_id} | Título: {jogo.titulo} | Desenvolvedor: {jogo.desenvolvedor} | Preço: R${jogo.preco} | Gêneros: {', '.join(jogo.generos)}")
                else:
                    print("Nenhum jogo cadastrado.")
                    
            elif opcao == "6":
                break
            elif opcao == "7":
                exemplos = [
                    {"titulo": "Dark Soul 1", "desenvolvedor": "FromSoftware", "preco": 155, "generos": ["Soulslike", "Dificil", "RPG", "Ação"]},
                    {"titulo": "Dark Soul 2", "desenvolvedor": "FromSoftware", "preco": 115, "generos": ["Soulslike", "Dificil", "Ação", "Fantasia"]},
                    {"titulo": "Dark Soul 3", "desenvolvedor": "FromSoftware", "preco": 230, "generos": ["Soulslike", "Aventura", "Dificil", "Fantasia"]}
                ]
                for exemplo in exemplos:
                    jogo_id = len(motor.jogos) + 1
                    motor.adicionar_jogo(Jogo(jogo_id, exemplo["titulo"], exemplo["desenvolvedor"], exemplo["preco"], exemplo["generos"]))
                print("\nColeção Dark Souls™ adicionada!")
                
            elif opcao == "4":
                preco_min = int(input("\nDigite o preço mínimo: "))
                preco_max = int(input("Digite o preço máximo: "))
                jogos = motor.busca_por_faixa_preco(preco_min, preco_max)
                if jogos:
                    print(f"\nJogos encontrados entre R${preco_min} e R${preco_max}:")
                    for jogo in jogos:
                        print(f"ID: {jogo.jogo_id} | Título: {jogo.titulo} | Preço: R${jogo.preco}")
                else:
                    print(f"\nNenhum jogo encontrado na faixa de preço R${preco_min} - R${preco_max}.")

        except ValueError:
            print("\nEntrada inválida. Tente novamente.")


menu()
