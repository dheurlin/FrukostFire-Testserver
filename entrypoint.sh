# Typecheck python files when they change, also watching for new files
mypy --ignore-missing-imports --package server
while true; do
    find /app/testserver -type f -name '*.py' | entr -d mypy --ignore-missing-imports --package server
    sleep 1
done &

# Launch the server
python server.py
