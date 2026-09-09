# LogosThekne

Aplicativo desktop em Python para aprendizagem de tecnologia, com interface gráfica moderna, sistema de login, níveis, matérias, quizzes gerados por IA, progresso por usuário, missões e perfil personalizado.

## Visão geral

O LogosThekne é um projeto educacional que combina:

- autenticação de usuários com cadastro e login;
- navegação por telas com interface em `customtkinter`;
- seleção de nível e matérias;
- quizzes com perguntas e lições geradas por IA via Groq;
- progresso individual, moedas, missões e ranking interno;
- personalização de tema, idioma e avatar;
- banco SQLite para persistência local.

## Funcionalidades principais

- Cadastro de usuário com validação de nome, e-mail e senha
- Login por nome de usuário ou e-mail
- Escolha de nível: Iniciante, Intermediário e Avançado
- Seleção de matérias: Hardware, Redes e Programação
- Geração de perguntas de múltipla escolha por IA
- Geração de aulas curtas por IA
- Sistema de progresso por matéria e por nível
- Sistema de missões e moedas
- Perfil do usuário com biografia e foto
- Troca de tema claro/escuro
- Troca de idioma (português/inglês)
- Áudio interativo com sons gerados localmente

## Tecnologias utilizadas

- Python 3.x
- `customtkinter` para a interface gráfica
- `Pillow` para manipulação de imagens
- `sqlite3` para armazenamento local
- `Groq` para geração de conteúdo por IA
- `json`, `tkinter`, `pathlib` e módulos Python padrão

## Estrutura do projeto

```text
LogosThekne/
├── assets/
│   ├── azul/
│   ├── rosa/
│   └── sons/
├── screens/
│   ├── level_screen.py
│   ├── main_screen.py
│   └── start_screen.py
├── config.json
├── database.py
├── front_end.py
├── ia.py
├── idioma.py
├── main.py
├── registro.py
├── sons.py
├── utils.py
├── pyrightconfig.json
├── usuarios.db
└── README.md
```

## Arquivos principais

### `main.py`
Ponto de entrada da aplicação. Cria o banco de dados e inicia a interface principal.

### `front_end.py`
Controla a navegação entre telas e o ciclo de vida da aplicação.

### `database.py`
Responsável por todas as operações do banco SQLite, incluindo:

- criação e migração do banco;
- cadastro e login;
- matérias do usuário;
- progresso por nível;
- moedas e missões;
- perfil e foto.

### `ia.py`
Gera perguntas e aulas com a API da Groq. Aqui também fica a chave da API.

### `idioma.py`
Centraliza os textos em português e inglês usados pela interface.

### `registro.py`
Realiza validação de cadastro e exibe a tela de registro.

### `screens/`
Contém as telas principais do aplicativo:

- `start_screen.py`: tela inicial de login
- `level_screen.py`: seleção de nível
- `main_screen.py`: tela principal com estudo, missões, perfil e quizzes

### `utils.py`
Contém helpers globais, temas, logo, imagens, funções utilitárias e recursos visuais.

### `sons.py`
Gera sons locais para feedback de acerto/erro e outros eventos do app.

## Requisitos

Antes de executar, instale as dependências do projeto:

```bash
pip install customtkinter pillow groq
```

Se quiser validar e-mails no cadastro com maior precisão, também pode instalar:

```bash
pip install email-validator
```

## Como executar

1. Abra o terminal na pasta do projeto.
2. Instale as dependências.
3. Abra o arquivo `ia.py` e informe sua chave da Groq:

```python
client = Groq(
    api_key="Insira aqui sua Api Key da Groq"
)
```

4. Execute:

```bash
python main.py
```

## Banco de dados

Ao iniciar pela primeira vez, o projeto cria automaticamente o arquivo `usuarios.db` com as tabelas necessárias.

O banco armazena:

- usuários
- matérias
- relacionamento usuário-matéria
- progresso
- moedas
- missões concluídas
- perfil e foto

## Configuração

O arquivo `config.json` guarda a preferência de tema atual, por exemplo:

```json
{
  "tema": "dark"
}
```

## Observações importantes

- O projeto depende de uma chave válida da Groq para gerar perguntas e aulas.
- As imagens e sons da pasta `assets` são usados diretamente pela interface.
- A pasta `assets/sons` pode ser criada automaticamente em tempo de execução quando necessária.
- O projeto foi estruturado para execução local em ambiente desktop Windows, mas pode funcionar em outros sistemas com ajustes mínimos.

## Possíveis melhorias futuras

- exportação de progresso para arquivo JSON ou CSV
- sistema de ranking global
- loja de itens e skins
- suporte a mais idiomas
- melhor gerenciamento de cache e performance
- testes automatizados

## Licença

Este projeto não possui licença definida no repositório. Verifique com o responsável do código antes de reutilizar em produção.

## Autor

Projeto desenvolvido como aplicação educacional e de estudo em Python.
