# Social translucence server
[ TODO: complete readme]

## How to run

### Create config files

Create .env based on the template found in sample.env.

[TODO: document config file attrs]

### Install:

```zsh
$> make install
```

### Run:

```zsh
$> make run
```

### Testing:

Create test.env from sample.env and *change* FS_ROOT and DATABASE values to testing alternatives.
You should also set ARLO_CLIENT to "fake_arlo" (no quotes);

```zsh
$> python -m pytest
```

