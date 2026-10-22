import argparse

MURZIK = '=^..^=______/'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Вежливый скрипт')
    parser.add_argument('name', help='Имя') 
    parser.add_argument('-s', '--surname', help='Фамилия') 
    parser.add_argument(
        '-c', 
        '--city', 
        help='Город',
        choices=['Chekhov', 'Dublin', 'Minsk', 'Simbirsk'],
    )    
    # Новый аргумент.
    parser.add_argument(
        '-m',
        '--murzik',
        action='store_true',
        help=f'Отправить кота Мурзика {MURZIK}'
    )
    args = parser.parse_args()
    parts = [] 
    parts.append(f'Здравствуйте, {args.name}')
    if args.surname is not None:
        parts.append(args.surname)
    if args.city is not None:
        parts.append(f'из {args.city}')
    # Новое условие для вывода изображения кота Мурзика.    
    if args.murzik:
        parts.append(MURZIK)
    print(*parts)
