* Social translucence server
[ TODO: complete readme]

** How to run
[TODO: create makefile]

*** Prepare python environment:
```zsh
$> virtualenv venv					  && echo created python virtual env
$> source ./venv/bin/activate 		  && echo activated virtual env
$> python -m pip install 			  && echo intalled requirements
$> python -m pip install ./fake_arlo  && echo install mock arlo client for arlo testing
```

*** Create config files

Create .env and test.env based on the template found in sample.env.


For .env, you should set ARLO_CLIENT to "arlo" (no quotes);
For test.env, you should set ARLO_CLIENT to "fake_arlo" (no quotes);

[TODO: document config file attrs]

*** Set-up database

```zsh
$> python init_db.py
```

*** Run server:

```zsh
$> python main.py
```


*** Test:
```zsh
$> python -m pytest
```

