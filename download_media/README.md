This folder contains code and sample json files to convert json dumps from Apollo (http://apollo3.cs.illinois.edu/) to media datasets.

The main script is ./code/read_apollo_dump.py
Dependencies on non-builtin modules is documented in dependencies.txt. Modules can installed using

```shell
$ pip install -r dependencies.txt
```

Currently only instagram and youtube interfaces are implemented. Planning to add support for Vine, Imgur,
TinyPIC and twitter embedded pictures as the need arises.