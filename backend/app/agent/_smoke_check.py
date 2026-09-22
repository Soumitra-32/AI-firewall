"""Temporary smoke check (created for verification, safe to delete)."""
from tools import file_reader, calculator

print("file_reader(notes.txt) ->", file_reader.invoke({"filename": "notes.txt"}))
print("file_reader(missing)   ->", file_reader.invoke({"filename": "secret.txt"}))
print("calculator(2+2)        ->", calculator.invoke({"expression": "2 + 2"}))
print("calculator(bad)        ->", calculator.invoke({"expression": "import os"}))
