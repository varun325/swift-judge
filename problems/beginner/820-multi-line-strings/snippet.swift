let name = "Taylor"
let poem = """
    Roses are red,
      \(name) is too,
    this line continues \
    here.
    """
print(poem)
print(poem.split(separator: "\n").count)
