# poez

Visão Geral

O poez (pronuncia-se como "pouse" em português) é uma aplicação para computador ou smartphone que permite a introdução de motion controls para executar funções de acessibilidade do sistema operativo.

Solução

Usamos um hand tracker pré-treinado em python para detectar a posição de vários pontos das mãos do utilizador, sendo que os diferentes gestos são posteriormente atribuídos às diversas funcionalidades. Com um simples movimento de mão será possível pausar media, aumentar o volume do computador, ou tirar uma foto sem recurso a um rato, teclado, ou toque no ecrã do smartphone.
Mais ainda, é possível imprimir um PDF que contem o desenho de um piano que, quando alinhado com a câmara, permite ao utilizador libertar a sua veia musical.

Tecnologias 

Todo o nosso código é desenvolvido em python com recurso às bibliotecas de OpenCV e MediaPipe. A versatilidade do OpenCV permite a exportação do código para outras plataformas como iOS e Android.
