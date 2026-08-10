# On Python Virtual Environments 

## The basic idea

A Python virtual environment (`venv`) gives a project its own **separate Python environment**.

Packages installed inside the virtual environment belong to that project and do not need to be installed in your system/base Python environment.

```text
Base Python
/usr/local/bin/python3
│
├── Python
├── pip
└── matplotlib ❌

Project virtual environment
Lab 6 Genetic Algorithm/.venv/
│
├── Python
├── pip
├── matplotlib ✅
├── numpy     ✅
└── pandas    ✅
```

The two environments are separate.

---

## Do I need to install packages every time?

**No.**

Once you install a package into your virtual environment:

```zsh
pip install matplotlib
```

it stays there.

The next time you work on the project, you only need to activate the environment:

```zsh
source .venv/bin/activate
```

You do **not** need to install `matplotlib` again.

The package remains installed until you remove or recreate the virtual environment.

---

## Why does matplotlib work in my venv but not in base Python?

This is normal and is one of the main purposes of a virtual environment.

```text
BASE PYTHON
/usr/local/bin/python3
│
└── matplotlib ❌

PROJECT VENV
your-project/.venv/
│
└── matplotlib ✅
```

When you activate:

```zsh
source .venv/bin/activate
```

your shell starts using the Python and `pip` inside `.venv`.

---

## Check which Python you're using

While the virtual environment is activated:

```zsh
which python
```

You should see something similar to:

```text
.../Lab 6 Genetic Algorithm/.venv/bin/python
```

Check `pip` too:

```zsh
which pip
```

It should point inside:

```text
.../.venv/bin/pip
```

You can verify matplotlib:

```zsh
python -c "import matplotlib; print(matplotlib.__version__)"
```

---

## Deactivating the environment

Run:

```zsh
deactivate
```

Your shell returns to the base Python environment.

If matplotlib was only installed inside `.venv`, it will no longer be available from the base environment. That's expected.

---

## Why use virtual environments?

They keep projects independent.

For example:

```text
Project A
└── .venv
    ├── numpy 1.x
    └── matplotlib

Project B
└── .venv
    ├── numpy 2.x
    └── pandas
```

Different projects can use different package versions without interfering with each other.

---

## Save your project's dependencies

Once you've installed the packages your project needs:

```zsh
pip freeze > requirements.txt
```

Your project might look like:

```text
Lab 6 Genetic Algorithm/
│
├── .venv/
├── setup_venv.zsh
├── requirements.txt
└── your_python_files.py
```

`requirements.txt` records the packages and versions installed in the environment.

---

## Recreate the environment

If `.venv` is deleted or you move the project to another machine:

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This recreates the environment with the project's dependencies.

---

## Important: Don't commit `.venv` to Git

Normally, you **do not put `.venv` into Git**.

Add this to `.gitignore`:

```text
.venv/
```

Instead of sharing the `.venv` folder, share:

```text
requirements.txt
```

Someone else can recreate the environment with:

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Typical workflow

### First time setting up a project

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install matplotlib numpy pandas
pip freeze > requirements.txt
```

### Every time you return to the project

```zsh
source .venv/bin/activate
```

That's it.

You **do not reinstall the packages every time**.

### When you're finished

```zsh
deactivate
```

---

## Quick mental model

Think of `.venv` as a **private Python environment for one project**:

```text
                 YOUR MAC
                    │
          ┌─────────┴─────────┐
          │                   │
      Base Python         Project .venv
          │                   │
     system packages     project packages
                              │
                       matplotlib ✅
                       numpy ✅
                       pandas ✅
```

**Activate → work → deactivate.**

The packages stay inside `.venv` between sessions.
