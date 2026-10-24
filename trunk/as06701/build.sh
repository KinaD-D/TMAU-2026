#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# сборка
mkdir -p build
cd build
cmake -DCMAKE_BUILD_TYPE=Release .. >/dev/null
cmake --build . -j"$(nproc)"
cd ..

# запуск расчёта
echo ">>> Running simulation..."
./build/aaaaa "$@"

# какой CSV читать
CSV="output.csv"
prev=""
for arg in "$@"; do
    if [ "$prev" = "--out" ]; then
        CSV="$arg"
    fi
    prev="$arg"
done

# визуализация
echo ">>> Rendering plot from $CSV ..."
python src/plot.py --csv "$CSV"
