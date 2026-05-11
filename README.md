Projeto em desenvolvimento.
Objetivo: desenvolver noções de processamento de imagem, começando com a compressão de imagem seguindo padrão JPEG.
Código desenvolvido em Python no VSCode integrado ao Copilot (IA Agent: Claude Haiku 4.5).

A imagem comprimida será a de um mandril (MANDRILL.BMP), bem conhecida e amplamente utilizada em testes que envolvam processamento de imagem, dado suas características (cores, detalhes etc).

A etapa 1 do projeto é a de codificação, e envolve:
  * Carregamento e leitura da imagem; ---> FEITO.
  * Visualização da imagem como matriz; ---> FEITO.
  * Conversão da imagem original em componentes RGB; ---> FEITO.
  * Conversão da imagem RGB em YCbCr; ---> FEITO.
  * Separação dos canais de luminância (Y) e crominâncias (Cr e Cb); ---> FEITO.
  * Subamostragem das crominâncias Cb e Cr; ---> FEITO.
  * Conversão de canais para blocos 8x8. ---> FEITO.
  * Implementação de equação DCT ("Discrete Cosine Transform") no código ---> ESTA ETAPA NECESSITA DE CORREÇÃO;
  * Aplicação da DCT nos blocos Y, Cb e Cr; ---> À FAZER.
  * Quantização; ---> À FAZER.
  * Aplicar técnica de DPCM ("Differential Pulse Code Modulation"); ---> À FAZER.
  * Ordenação em zigue-zague; ---> À FAZER.
  * Codificação de corrida de zeros; ---> À FAZER.
  * Codificação de Huffman; ---> À FAZER.
  * Métricas de compressão. ---> À FAZER.
