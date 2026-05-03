# Capa

**Projeto:** Sistema Solidario  
**ODS relacionado:** ODS 1 - Erradicacao da Pobreza  
**Autores:** [Preencher nomes da equipe]  
**Orientador:** [Preencher nome do orientador]  
**Instituicao:** [Preencher]  
**Data:** [Preencher]

# Sumario

1. Introducao
2. Justificativa e objetivos
3. ODS relacionado
4. Tecnologias utilizadas
5. Estrutura do sistema
6. Codigo-fonte e GitHub
7. Conclusao
8. Referencias
9. Evidencias

# Introducao

O Sistema Solidario foi desenvolvido para apoiar a distribuicao de doacoes entre doadores, beneficiarios e organizacoes sociais. A proposta utiliza tecnologia web para facilitar o cadastro de itens, o registro de necessidades e a visualizacao do impacto social das acoes realizadas.

# Justificativa e objetivos

Muitas comunidades enfrentam dificuldade para organizar doacoes de forma transparente e eficiente. O projeto busca reduzir esse problema por meio de uma plataforma simples, acessivel e orientada por dados.

## Objetivo geral

Criar um sistema web capaz de conectar doacoes e necessidades de maneira organizada, com autenticacao segura, relatorios de impacto e recursos de geolocalizacao simplificada.

## Objetivos especificos

- Cadastrar doadores, beneficiarios e organizacoes
- Registrar itens doados e solicitacoes de ajuda
- Atualizar o status das doacoes
- Filtrar registros por regiao com coordenadas
- Utilizar um algoritmo de casamento baseado em grafos
- Disponibilizar relatorios em PDF e Excel

# ODS relacionado

O projeto foi alinhado ao **ODS 1 - Erradicacao da Pobreza**. A plataforma contribui para a reducao da vulnerabilidade social ao melhorar a alocacao de recursos essenciais, como alimentos, roupas e kits de higiene, para pessoas e familias em situacao de necessidade.

# Tecnologias utilizadas

- Python para a API
- JWT para autenticacao
- HTML, CSS e JavaScript para a interface web
- JSON para persistencia leve dos dados
- OpenPyXL para exportacao em Excel
- ReportLab para exportacao em PDF
- Mermaid para representacao dos diagramas
- Git e GitHub para versionamento

# Estrutura do sistema

## Visao geral

O sistema foi dividido em duas camadas principais:

- Backend em Python responsavel pela API, autenticacao JWT, matching e relatorios
- Frontend estatico responsavel pela interface, consumo de JSON e dashboard

## MER

Consulte [mer.md](/D:/Laragon/laragon/www/Sistema-Solidario/docs/mer.md).

## SQL

Consulte [schema.sql](/D:/Laragon/laragon/www/Sistema-Solidario/docs/schema.sql).

## Diagramas UML

- Casos de uso: [uml-casos-de-uso.md](/D:/Laragon/laragon/www/Sistema-Solidario/docs/uml-casos-de-uso.md)
- Classes: [uml-classes.md](/D:/Laragon/laragon/www/Sistema-Solidario/docs/uml-classes.md)

## Print das telas

Inserir aqui os prints reais da tela inicial, dashboard, listagem de itens, solicitacoes e exportacao de relatorios.

# Codigo-fonte com comentarios e GitHub

Repositorio do projeto:

- [Sistema-Solidario](https://github.com/Gabriel-Dames-Peixoto/Sistema-Solidario)

O codigo-fonte foi organizado com comentarios objetivos nas partes mais importantes, especialmente no algoritmo de matching e na geracao de relatorios.

# Conclusao

O desenvolvimento do Sistema Solidario permitiu integrar conteudos de programacao web, estrutura de dados, autenticacao, modelagem de banco de dados e analise de coordenadas. Entre as principais dificuldades estiveram a definicao das regras de casamento entre itens e necessidades e a organizacao dos dados para gerar relatorios claros. Como aprendizado, destacou-se a importancia do versionamento com Git, da documentacao tecnica e do alinhamento entre tecnologia e impacto social.

# Referencias

- Documentacao oficial do Python
- Documentacao do OpenPyXL
- Documentacao do ReportLab
- Conteudos de sala sobre grafos, MER e UML

# Evidencias

Consulte o arquivo [evidencias.md](/D:/Laragon/laragon/www/Sistema-Solidario/docs/evidencias.md) e substitua este espaco por fotos, comprovacoes da pratica extensionista, pesquisa aplicada e link do video final.
