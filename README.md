# Citizen Assist AI

Assistente de terminal feito em Python para a Global Solution 2026.2 de Pensamento Computacional e Automação com Python.

## Integrantes

| Nome | RM |
| --- | --- |
| Raul Sampaio Mochnacs Arruda | 573523 |
| Pedro Sampaio Mochnacs Arruda | 573522 |

## Público e problema

Escolhemos jovens de 14 a 24 anos que estão procurando o primeiro emprego. Nessa fase a pessoa precisa resolver um monte de coisa de uma vez (CPF, identidade, título, carteira de trabalho, alistamento) e as informações ficam espalhadas em vários sites. Alguns parecem oficiais e não são.

O assistente responde com base em 12 orientações, divididas em Documentos, Trabalho, Estudos e benefícios e Consumidor. Toda resposta mostra a fonte e a data em que a informação foi conferida. Ele não pede nenhum dado pessoal.

## ODS relacionados

- ODS 8: trabalho decente e crescimento econômico, porque ajuda o jovem a se preparar para o primeiro emprego.
- ODS 10: redução das desigualdades, porque a orientação é gratuita e em linguagem simples.
- ODS 16: instituições eficazes, porque facilita o acesso a informação de serviços públicos.

## Como executar

Precisa de Python 3 e não usa biblioteca externa. Dentro da pasta do projeto:

```bash
python main.py
```

## Estrutura

- `orientacao.py`: classe `Orientacao`, um registro da base.
- `base_conhecimento.py`: classe `BaseConhecimento`, lê o JSON, lista as categorias e faz a busca.
- `assistente.py`: classe `Assistente`, faz o atendimento, guarda o histórico e calcula os indicadores.
- `main.py`: cria os objetos e mostra o menu.
- `data/`: base de conhecimento, histórico e CSV exportado.

## Regra de pontuação

Usamos a regra do enunciado, sem mudar os pesos. A pergunta, as palavras-chave e o título são normalizados (minúsculas, sem acento e sem pontuação) antes da comparação.

| Regra | Resultado |
| --- | --- |
| Palavra-chave da orientação que aparece na pergunta | +3 pontos |
| Palavra da pergunta com 4 letras ou mais que aparece no título | +1 ponto |
| Melhor orientação com 6 pontos ou mais | Confiança ALTA |
| Melhor orientação com 3 a 5 pontos | Confiança MÉDIA |
| Nenhuma orientação com 3 pontos | "Não encontrei" e sugestão das categorias |

Exemplo com "Como tirar o título de eleitor?": a orientação 3 ganha +3 pela palavra-chave "titulo de eleitor" e +1 por cada uma destas palavras que estão no título: "tirar", "titulo" e "eleitor". São 6 pontos, confiança ALTA.

A única mudança na função `normalizar()` do enunciado foi tratar o hífen como pontuação, senão "seguro-desemprego" não batia com "seguro desemprego".

## Como contamos um atendimento

Um atendimento vai da primeira pergunta até a pessoa resolver a dúvida ou desistir. Se ela reescreve a pergunta depois de um "não encontrei", isso conta como mais uma tentativa no mesmo atendimento. Quando ela desiste, a última pergunta vai para a lista de dúvidas sem solução.

Pergunta com 8 ou mais dígitos ou com @ é recusada antes de tudo, então não entra no histórico nem conta como tentativa.

A nota de facilidade é pedida ao sair e fica salva em todos os atendimentos daquela sessão, para o histórico continuar em um arquivo só.

## Integrações com outras disciplinas

Não fizemos integração com outras disciplinas.

## Fontes consultadas

Conferidas em 05/11/2026.

- CPF: https://www.gov.br/pt-br/servicos/inscrever-no-cpf
- Carteira de Identidade Nacional: https://www.gov.br/governodigital/pt-br/identidade/cin/perguntas-frequentes-sobre-a-cin
- Título de eleitor: https://www.tse.jus.br/comunicacao/noticias/2026/Marco/eleitor-em-dia-confira-quais-documentos-sao-necessarios-para-tirar-o-titulo-ate-6-de-maio
- Alistamento militar: https://www.gov.br/pt-br/servicos/alistar-se-no-servico-militar-obrigatorio
- Carteira de Trabalho Digital: https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho e https://www.gov.br/trabalho-e-emprego/pt-br/servicos/trabalhador/carteira-de-trabalho/perguntas-frequentes-carteira-de-trabalho-digital
- Jovem Aprendiz: https://www.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo/2026/julho/aprendizagem-profissional-regras-direitos-e-funcionamento-do-contrato-de-aprendizagem
- Vagas do Sine: https://www.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo/2025/janeiro/vagas-de-emprego-do-sine-podem-ser-visualizadas-na-carteira-de-trabalho-digital
- Seguro-Desemprego: https://www.gov.br/pt-br/servicos/solicitar-o-seguro-desemprego
- Isenção do Enem: https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/enem/enem-2026-saiba-quem-tem-direito-a-isencao-da-taxa-de-inscricao
- ID Jovem: https://www.gov.br/pt-br/servicos/obter-a-carteira-de-identidade-jovem
- Reclamação de consumidor: https://www.gov.br/mj/pt-br/assuntos/noticias/consumidor-gov-br-saiba-como-registrar-uma-reclamacao-pela-plataforma
- Direito de arrependimento (art. 49 do CDC): https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm

## Resultado do teste com usuários

Não fizemos o teste com pessoas de fora da equipe, então estes números não mostram como um usuário real se sairia. O histórico tem 23 atendimentos: 13 de um teste automatizado, em que um script passou as perguntas e as respostas s/n ao programa, e 10 feitos na mão pela equipe, nos testes e na gravação do vídeo.

- Total de atendimentos: 23
- Resposta encontrada: 78,3%
- Taxa de acerto: 69,6%
- Tentativas por atendimento: 1,0
- Tempo médio para encontrar: 16,4 s no total, mas esse número fica baixo porque o script responde na hora. Nos atendimentos feitos na mão, a média foi de 42,1 s.
- Facilidade de uso (1 a 5): 4,3, com notas dadas pela equipe. O script não deu nota.
- Dúvidas sem solução: "perdi meu rg, o que eu faço?", "como tirar a cnh", "com quantos anos eu posso tirar o titulo de eleitor" e "como eu tiro o passaporte" (essa foi usada de propósito no vídeo, porque não está na base). Também aparecem "como procurar trabalho" e "fui mandado embora o que eu faço?", que foram resolvidas com as melhorias abaixo.
- Melhoria feita a partir do teste: "como procurar trabalho" não foi encontrada, porque a base só tinha "procurar emprego". Incluímos a palavra-chave "procurar trabalho" na orientação 7 e a mesma pergunta passou a encontrar a orientação, com 4 pontos e confiança MÉDIA.
- Alteração feita ao vivo no vídeo: "fui mandado embora, o que eu faço?" não era encontrada. Incluímos "mandado embora" nas palavras-chave da orientação 8 e ela passou a encontrar o Seguro-Desemprego, com 3 pontos e confiança MÉDIA.

Os indicadores que aparecem no vídeo mostram 15 atendimentos porque foram gravados antes das partes 5 e 6. Os atendimentos dessas gravações entraram no histórico depois.

Tiramos do histórico um atendimento feito na mão ("Como tirar o titulo de eleitor?", marcado como não ajudou), porque ele registrou 52.556 s. O programa tinha ficado aberto de um dia para o outro na tela de pergunta e o contador continuou rodando.

## Limitações

- A busca compara texto. Se a pessoa usar uma palavra que não está na base, como um sinônimo, ela não encontra a resposta.
- Erro de digitação também não é reconhecido: "cartera de trabalho" não bate com "carteira de trabalho".
- A regra dos 8 dígitos pode recusar uma pergunta sem dado pessoal, como uma com a data 20/11/2026. Ela também não detecta um nome escrito na pergunta.
- Palavras comuns com 4 letras ou mais, como "como" ou "para", também podem somar ponto se estiverem no título. Por isso evitamos usar essas palavras nos títulos.
- A base é atualizada à mão. Se uma regra do governo mudar, a resposta só muda quando alguém editar o JSON.
- Alguns serviços mudam de estado para estado, como a Carteira de Identidade Nacional, então a resposta fica mais geral.
- O tempo medido inclui o tempo que a pessoa leva para digitar e ler, e continua contando se o programa ficar parado na tela de pergunta.
- O histórico é lido só quando o programa abre. Se ele for aberto duas vezes ao mesmo tempo, uma execução pode salvar por cima dos atendimentos da outra.
- A nota de facilidade é salva por atendimento, então quem fez mais atendimentos pesa mais na média.

## Vídeo

https://youtu.be/fEjlsDXn8zA (não listado)
