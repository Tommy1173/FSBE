# FSBE
Este é um projeto CLI básico desenvolvido em Python para monitorar eventos do sistema de arquivos em tempo real e interagir o máximo possível com o FS. Ele detecta alterações como criação, modificação, exclusão e movimentação de arquivos e pastas, exibindo os eventos com visual moderno e colorido usando a biblioteca Rich.

### Principais recursos

- Monitoramento singular de directório em tempo real com watchdog.

Interface rica no terminal com rich, incluindo tabelas e painéis estilizados.

Modo de filtragem opcional para extensão, tamanho, nome.

Modo log opcional para salvar eventos em um arquivo .log.

Suporte a listagem de propriedades de arquivos.

Extensível e modular — pronto para ser integrado a outros projetos Python (como gerenciadores de arquivos)
