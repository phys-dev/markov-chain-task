import random  
import sys     

#Функция для чтения текста из файла
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()  # Читаем
    return text

# Функция для построения цепочек Маркова
def build_chain(words, chain_length=2):
    chain = {}  # Создаем пустой словарь для наших цепочек
    
    # Проходим по списку слов (не доходя до конца на длину цепочки)
    for i in range(len(words) - chain_length):
        # Берем ключ (например, 2 или 3 слова подряд)
        key = tuple(words[i:i+chain_length])
        # Берем слово, которое идет сразу за ключом
        value = words[i+chain_length]
        
        # Если такой ключ уже есть в словаре - добавляем слово в список
        if key in chain:
            chain[key].append(value)
        # Если ключа нет - создаем для него новый список со словом
        else:
            chain[key] = [value]
    return chain

# Функция для генерации нового текста
def generate_text(chain, chain_length=2, text_length=100):
    # Ищем в словаре все ключи, которые начинаются с заглавной буквы
    start_keys = [k for k in chain.keys() if k[0][0].isupper()]
    # Если заглавных нет, берем любые
    if not start_keys:
        start_keys = list(chain.keys())
        
    # Выбираем случайное стартовое слово
    current_key = random.choice(start_keys)
    result_words = list(current_key)  # Кладем его в итоговый список
    
    # Начинаем генерировать остальные слова
    for _ in range(text_length - chain_length):
        # Если для текущего ключа нет продолжения - останавливаемся
        if current_key not in chain:
            break
            
        # Выбираем случайное следующее слово из возможных вариантов
        next_word = random.choice(chain[current_key])
        result_words.append(next_word)  # Добавляем слово в текст
        
        # Сдвигаем наше окно на одно слово вперед
        current_key = tuple(result_words[-chain_length:])
        
    # Склеиваем все слова через пробел и возвращаем результат
    return ' '.join(result_words)

if __name__ == '__main__':
    # Проверяем, ввели ли пользователь 3 параметра (файл, длина, длина цепочки)
    if len(sys.argv) != 4:
        print("Использование: python main.py <имя_файла> <длина_текста> <длина_цепочки>")
        sys.exit(1) 

    # Запоминаем то, что ввели в терминале
    filename = sys.argv[1]
    length = int(sys.argv[2])
    chain_len = int(sys.argv[3]) 

    # Выполняем шаги по порядку
    text = read_file(filename) # Читаем книгу
    words = text.split()  # Разбиваем текст на отдельные слова по пробелам
    
    chain = build_chain(words, chain_length=chain_len)  # Строим цепочку
    generated = generate_text(chain, chain_length=chain_len, text_length=length) # Генерируем текст
    
    print(generated) 
