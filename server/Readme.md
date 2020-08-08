* Social translucence server
[ TODO: complete readme]

** How to run
[TODO: create makefile]

*** Prepare everything up:
```zsh
$> virtualenv venv					  && echo created python virtual env
$> source ./venv/bin/activate 		  && echo activated virtual env
$> python -m pip install 			  && echo intalled requirements
$> python -m pip install ./fake_arlo  && echo install mock arlo client for arlo testing
```

*** Run server:
```zsh
$> python main.py
```


*** Test:
```zsh
$> python -m pytest
```

