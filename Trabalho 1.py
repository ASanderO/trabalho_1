import time
import logging

# Configuração do logger
logging.basicConfig(filename='ordenacao_busca.log', level=logging.INFO, format='%(asctime)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger()


# Função para gerar vetores de inteiros pseudo-aleatórios
def gerar_vetor_aleatorio(tamanho):
    random_seed = int(time.time() * 1000) % 1000000
    vetor = []
    for _ in range(tamanho):
        random_seed = (random_seed * 9301 + 49297) % 233280
        random_number = (random_seed / 233280.0) * 100000
        vetor.append(int(random_number))
    return vetor


# Algoritmo de ordenação Selection Sort
def selection_sort(arr):
    n_trocas = 0
    n_iteracoes = 0
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            n_iteracoes += 1
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        if i != min_idx:
            n_trocas += 1
    return arr, n_trocas, n_iteracoes


# Algoritmo de ordenação Quick Sort
def quick_sort(arr):
    def _quick_sort(arr, low, high):
        if low < high:
            pi, n_trocas, n_iteracoes = partition(arr, low, high)
            left_trocas, left_iteracoes = _quick_sort(arr, low, pi - 1)
            right_trocas, right_iteracoes = _quick_sort(arr, pi + 1, high)
            return n_trocas + left_trocas + right_trocas, n_iteracoes + left_iteracoes + right_iteracoes
        return 0, 0

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        n_trocas = 0
        n_iteracoes = 0
        for j in range(low, high):
            n_iteracoes += 1
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                n_trocas += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        n_trocas += 1
        return i + 1, n_trocas, n_iteracoes

    n_trocas, n_iteracoes = _quick_sort(arr, 0, len(arr) - 1)
    return arr, n_trocas, n_iteracoes


# Algoritmos de busca
def busca_linear(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1


def busca_binaria(arr, x):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (high + low) // 2
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1


# Funções auxiliares
def calcular_media(data):
    return sum(data) / len(data)


def calcular_desvio_padrao(data, media):
    variancia = sum((x - media) ** 2 for x in data) / len(data)
    return variancia ** 0.5


# Função para avaliar os algoritmos de ordenação
def avaliar_algoritmo_ordenacao(algoritmo_ordenacao, tamanhos, num_execucoes=10):
    logger.info(f'Avaliando algoritmo de ordenação: {algoritmo_ordenacao.__name__}')
    resultados = {tamanho: {'tempo': [], 'trocas': [], 'iteracoes': []} for tamanho in tamanhos}
    for execucao in range(num_execucoes):
        logger.info(f'Execução {execucao + 1} de {num_execucoes}')
        for tamanho in tamanhos:
            arr = gerar_vetor_aleatorio(tamanho)
            logger.info(f'Vetor gerado de tamanho {tamanho}: {arr[:10]}...')
            t1 = time.perf_counter()
            sorted_arr, n_trocas, n_iteracoes = algoritmo_ordenacao(arr.copy())
            t2 = time.perf_counter()
            tt = t2 - t1
            logger.info(f'Tempo de execução: {tt:.10f}, Trocas: {n_trocas}, Iterações: {n_iteracoes}')
            resultados[tamanho]['tempo'].append(tt)
            resultados[tamanho]['trocas'].append(n_trocas)
            resultados[tamanho]['iteracoes'].append(n_iteracoes)
    for tamanho in tamanhos:
        media_tempo = calcular_media(resultados[tamanho]['tempo'])
        desvio_padrao_tempo = calcular_desvio_padrao(resultados[tamanho]['tempo'], media_tempo)
        media_trocas = calcular_media(resultados[tamanho]['trocas'])
        desvio_padrao_trocas = calcular_desvio_padrao(resultados[tamanho]['trocas'], media_trocas)
        media_iteracoes = calcular_media(resultados[tamanho]['iteracoes'])
        desvio_padrao_iteracoes = calcular_desvio_padrao(resultados[tamanho]['iteracoes'], media_iteracoes)
        logger.info(f'Algoritmo de Ordenação: {algoritmo_ordenacao.__name__}, Tamanho: {tamanho}, '
                    f'Média de Tempo: {media_tempo:.10f}, Desvio Padrão de Tempo: {desvio_padrao_tempo:.10f}, '
                    f'Média de Trocas: {media_trocas:.2f}, Desvio Padrão de Trocas: {desvio_padrao_trocas:.2f}, '
                    f'Média de Iterações: {media_iteracoes:.2f}, Desvio Padrão de Iterações: {desvio_padrao_iteracoes:.2f}')


# Função para avaliar os algoritmos de busca
def avaliar_algoritmo_busca(algoritmo_busca, tamanhos, num_execucoes=10):
    logger.info(f'Avaliando algoritmo de busca: {algoritmo_busca.__name__}')
    resultados = {
        tamanho: {'tempo_ordenado': [], 'tempo_desordenado': [], 'posicao_ordenado': [], 'posicao_desordenado': []} for
        tamanho in tamanhos}
    for execucao in range(num_execucoes):
        logger.info(f'Execução {execucao + 1} de {num_execucoes}')
        for tamanho in tamanhos:
            vetor_desordenado = gerar_vetor_aleatorio(tamanho)
            target = vetor_desordenado[tamanho // 2]  # Garantindo que o alvo esteja presente no vetor
            vetor_ordenado = sorted(vetor_desordenado)
            logger.info(f'Target para busca: {target}')

            t1 = time.perf_counter()
            pos = algoritmo_busca(vetor_desordenado, target)
            t2 = time.perf_counter()
            tt = t2 - t1
            resultados[tamanho]['tempo_desordenado'].append(tt)
            resultados[tamanho]['posicao_desordenado'].append(pos)
            logger.info(f'Busca no vetor desordenado de tamanho {tamanho}: Tempo: {tt:.10f}, Posição: {pos}')

            t1 = time.perf_counter()
            pos = algoritmo_busca(vetor_ordenado, target)
            t2 = time.perf_counter()
            tt = t2 - t1
            resultados[tamanho]['tempo_ordenado'].append(tt)
            resultados[tamanho]['posicao_ordenado'].append(pos)
            logger.info(f'Busca no vetor ordenado de tamanho {tamanho}: Tempo: {tt:.10f}, Posição: {pos}')

    for tamanho in tamanhos:
        media_tempo_desordenado = calcular_media(resultados[tamanho]['tempo_desordenado'])
        desvio_padrao_tempo_desordenado = calcular_desvio_padrao(resultados[tamanho]['tempo_desordenado'],
                                                                 media_tempo_desordenado)
        media_tempo_ordenado = calcular_media(resultados[tamanho]['tempo_ordenado'])
        desvio_padrao_tempo_ordenado = calcular_desvio_padrao(resultados[tamanho]['tempo_ordenado'],
                                                              media_tempo_ordenado)
        logger.info(f'Algoritmo de Busca: {algoritmo_busca.__name__}, Tamanho: {tamanho}, '
                    f'Média de Tempo Desordenado: {media_tempo_desordenado:.10f}, Desvio Padrão de Tempo Desordenado: {desvio_padrao_tempo_desordenado:.10f}, '
                    f'Média de Tempo Ordenado: {media_tempo_ordenado:.10f}, Desvio Padrão de Tempo Ordenado: {desvio_padrao_tempo_ordenado:.10f}, '
                    f'Posição no Vetor Desordenado: {resultados[tamanho]["posicao_desordenado"]}, '
                    f'Posição no Vetor Ordenado: {resultados[tamanho]["posicao_ordenado"]}')


if __name__ == "__main__":
    tamanhos = [50, 500, 5000, 10000, 11000, 12000]
    algoritmos_ordenacao = [selection_sort, quick_sort]
    algoritmos_busca = [busca_linear, busca_binaria]
    num_execucoes = 2

    for algoritmo in algoritmos_ordenacao:
        avaliar_algoritmo_ordenacao(algoritmo, tamanhos, num_execucoes)

    for algoritmo_busca in algoritmos_busca:
        avaliar_algoritmo_busca(algoritmo_busca, tamanhos, num_execucoes)
