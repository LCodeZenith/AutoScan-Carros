# 🚗 AutoScan Carros

Programa de desktop em Python (tkinter) que consulta um banco de **56 carros** e **14 cores** e mostra, para o carro e a cor que você digitar, **no que são bons e no que são ruins**.

Você informa marca, modelo e cor, e o programa entende até erros de digitação (por exemplo, `corola` vira **Toyota Corolla** e `vw` vira **Volkswagen**).

> Projeto de estudo. Os pontos "bom em" e "ruim em" são avaliações gerais e subjetivas, não dados técnicos oficiais.

---

## ✨ Funcionalidades

- Interface gráfica escura, com visual técnico e discreto
- Banco com **56 modelos** (hatches, sedãs, SUVs, picapes, elétricos, esportivos e clássicos) e **14 cores**
- Busca tolerante a acentos, maiúsculas e erros de digitação
- Sugestões quando o carro não é encontrado ("Você quis dizer: ...?")
- Validação entre marca e modelo (por exemplo, "Fiat Gol" não existe)
- Painéis separados para **Modelo**, **Cor** e **Resumo** (pontos fortes e fracos combinados)
- Código em um único arquivo, sem dependências externas

## 🖥️ Como usar

| Ação | Como |
|------|------|
| Consultar | Preencha Marca, Modelo e Cor e clique em **CONSULTAR** (ou pressione `Enter`) |
| Limpar | Clique em **LIMPAR** (ou pressione `Esc`) |

Exemplos de entrada: `toyota` / `corolla` / `prata`, `vw` / `gol` / `branca`, `honda` / `hr-v` / `vermelha`.

## ▶️ Rodando o código

**Requisitos:** Python 3 com tkinter. Nenhuma biblioteca externa é necessária; o projeto usa só a biblioteca padrão. Foi desenvolvido e empacotado com Python 3.14.

```bash
git clone https://github.com/SEU-USUARIO/autoscan-carros.git
cd autoscan-carros
python AutoScanCarros.py
```

> No Linux, o tkinter às vezes vem separado do Python. Se der erro de importação, instale com `sudo apt install python3-tk`. No Windows e no macOS ele já vem junto.

## 📦 Gerando o executável (.exe)

Com o [PyInstaller](https://pyinstaller.org):

```powershell
python -m pip install --upgrade pyinstaller
python -m PyInstaller --onefile --windowed AutoScanCarros.py
```

O executável é criado em `dist/AutoScanCarros.exe`. Também dá para usar a ferramenta gráfica [Auto Py To Exe](https://pypi.org/project/auto-py-to-exe/), que usa o PyInstaller por baixo.

Observações sobre o `.exe`:
- Ele já inclui o Python e o tkinter, então quem for usar não precisa instalar nada.
- Funciona em **Windows 10 ou 11 de 64 bits** (limitação do Python 3.14).
- Antivírus e SmartScreen costumam marcar executáveis do PyInstaller como suspeitos (falso positivo comum). Na tela azul do Windows, clique em "Mais informações" e depois em "Executar assim mesmo".
- Evite versionar o `.exe` no repositório (são ~12 MB). Publique-o na aba **Releases** do GitHub.

## 🧠 Como funciona

1. **Normalização:** o texto digitado é convertido para minúsculas, sem acentos e sem pontuação.
2. **Apelidos (aliases):** cada modelo e cor tem apelidos (`hb20`, `hb 20`, `grafite` para Cinza, etc.). Primeiro o programa procura o apelido mais longo como palavra inteira.
3. **Busca aproximada:** se não achar, usa `difflib` para tolerar erros de digitação (apelidos com menos de 4 letras ficam de fora, para evitar falsos positivos).
4. **Validação da marca:** a marca digitada precisa combinar com a marca do modelo encontrado (apelidos como `vw` e `gm` são aceitos).
5. **Integração com a classe `carro`:** a função `integrar(carro)` cria o atributo `.carro` na classe, e `resposta.carro == resposta` é `True` quando o carro digitado existe no banco.

## ➕ Adicionando carros e cores

Dentro do `AutoScanCarros.py`, basta acrescentar uma linha no mesmo formato das existentes.

```python
# _m(nome, marca, categoria, [bom em...], [ruim em...], [apelidos...])
_m("Toyota Etios", "Toyota", "hatch compacto",
   ["confiabilidade", "consumo baixo"],
   ["acabamento simples", "desempenho"], ["etios"])

# _c(nome, [bom em...], [ruim em...], [apelidos...])
_c("Grafite", ["esconde sujeira", "visual moderno"],
   ["pouco vibrante"], ["grafite escuro"])
```

## 📁 Estrutura do repositório

```
autoscan-carros/
├── AutoScanCarros.py    # programa completo: banco, busca, classe carro e interface
├── docs/
│   └── index.html       # página com o código-fonte formatado (para o GitHub Pages)
├── README.md
├── .gitignore
└── .gitattributes
```

A pasta `docs/` guarda uma página HTML que exibe o código com cores e números de linha. Para publicá-la, ative o **GitHub Pages**: *Settings → Pages → Branch: `main` / pasta `/docs`*. Essa página é uma cópia do script, então atualize-a quando mudar o código.

## 🗺️ Ideias para o futuro

- Mais modelos, versões e anos de cada carro
- Exportar o banco para JSON ou SQLite
- Campo único de texto livre (por exemplo, "meu carro é um corolla prata")
- Captura de tela do programa neste README
