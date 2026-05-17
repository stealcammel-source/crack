from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_dynamic_libs

# Собираем все субмодули
hiddenimports = collect_submodules('Cryptodome')

# Собираем данные и динамические библиотеки (.pyd файлы)
datas = collect_data_files('Cryptodome')
binaries = collect_dynamic_libs('Cryptodome')