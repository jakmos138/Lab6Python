import json

def collect_configuration():
    config = {}
    config['web_server_log'] = input("Enter the name of the web server log: ")
    config['ip_address'] = input("Enter the IP address to be used as a filter: ")
    config['logging_level'] = input("Enter the logging level used by the application: ")
    config['lines_to_display'] = int(input("Enter the number of lines to be displayed at once: "))
    config['custom_parameter'] = input("Enter your own parameter: ")

    return config

def save_config(config, filename, encoding='utf-8'):
    with open(filename, 'w', encoding=encoding) as file:
        json.dump(config, file, ensure_ascii=False, indent=4)

def main():
    config = collect_configuration()
    save_config(config, 'config.json', encoding='utf-8')

if __name__ == "__main__":
    main()